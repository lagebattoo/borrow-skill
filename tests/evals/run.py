"""Run independent Codex CLI cases; inspect evidence, not wording-based pass scores.

Uses the current ChatGPT login and configured model/effort, with external tools,
hooks, plugins, and memories disabled for this run. No auth files are copied.
Cases and evaluator rubrics remain outside each agent's temporary workspace.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
import tomllib
import uuid


ROOT = Path(__file__).resolve().parents[2]


def create_output_directory():
    # Python's mkdtemp uses an owner-only ACL on recent Windows versions. The
    # Codex sandbox account then cannot traverse the case directory. Inherit the
    # normal temp-parent ACL for these synthetic fixtures; never loosen an
    # existing directory or place credentials here.
    if os.name == 'nt':
        directory = Path(tempfile.gettempdir()) / ('borrow-eval-' + uuid.uuid4().hex)
        directory.mkdir(mode=0o777)
        return directory
    return Path(tempfile.mkdtemp(prefix='borrow-eval-'))


def fixture_path(workspace, name):
    target = (workspace / name).resolve()
    if not target.is_relative_to(workspace.resolve()) or target == workspace.resolve():
        raise ValueError(f'Fixture escapes workspace: {name}')
    if target.relative_to(workspace.resolve()).parts[0] in ('.git', '.agents'):
        raise ValueError(f'Fixture must not overwrite repository or Skill metadata: {name}')
    return target


def stop_process_tree(process):
    if os.name == 'nt':
        subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    if process.poll() is None:
        process.kill()
    process.wait()


def snapshot(directory):
    return {
        p.relative_to(directory).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in directory.rglob('*')
        if p.is_file() and '.git' not in p.relative_to(directory).parts
    }


def run_case(case, output, executable, settings, extra_skills=()):
    if not case['id'] or Path(case['id']).name != case['id'] or case['id'] in ('.', '..'):
        raise ValueError('Case id must be a directory name')
    sources = [ROOT / 'borrow', *map(Path, extra_skills)]
    names = [p.name for p in sources]
    if len(names) != len(set(names)) or any(not (p / 'SKILL.md').is_file() for p in sources):
        raise ValueError('Skills must have unique directory names and a SKILL.md')
    missing = set(case.get('required_skills', [])) - set(names)
    if missing:
        raise ValueError(f'Missing required Skills: {sorted(missing)}; use --extra-skill')
    case_root = output / case['id']
    workspace = case_root / 'workspace'
    fixtures = [(fixture_path(workspace, name), contents) for name, contents in case['files'].items()]
    workspace.mkdir(parents=True, exist_ok=False)
    subprocess.run(['git', 'init', '-q', str(workspace)], check=True)
    for source in sources:
        shutil.copytree(source, workspace / '.agents/skills' / source.name)
    for target, contents in fixtures:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(contents, encoding='utf-8', newline='\n')
    all_results = []
    for index, prompt in enumerate([case['prompt']] + ([case['followup']] if case.get('followup') else []), 1):
        prefix = case_root / f'run-{index}'
        before = snapshot(workspace)
        command = [executable, 'exec', '--ignore-user-config', '--ephemeral',
                   '--sandbox', 'workspace-write' if case.get('write') else 'read-only',
                   '-c', 'approval_policy="never"', '-c', 'web_search="disabled"',
                   '-C', str(workspace), '--json', '--color', 'never',
                   '-o', str(prefix.with_suffix('.response.md'))]
        for feature in ('hooks', 'plugins', 'apps', 'memories', 'browser_use',
                        'computer_use', 'multi_agent', 'multi_agent_v2'):
            command += ['--disable', feature]
        for key in ('model', 'model_reasoning_effort'):
            if settings.get(key):
                command += ['-c', key + '=' + json.dumps(settings[key])]
        if settings.get('windows', {}).get('sandbox'):
            command += ['-c', 'windows.sandbox=' + json.dumps(settings['windows']['sandbox'])]
        prompt += ('\n\n当前唯一工作目录：' + str(workspace.resolve()) + '。'
                   '文件操作使用此目录内的绝对路径；搜索前确认目录，不得从磁盘根目录搜索。'
                   '本次操作范围仅限当前临时项目。不访问外部网络、账号或其他项目，'
                   '不读取用户私人文件。当前项目 .agents/skills 中有可用技能，'
                   '按正常相关性自行决定是否使用，不要为了测试强制调用。')
        command.append('-')
        env = os.environ.copy()
        env['PYTHONUTF8'] = '1'
        env['GIT_TERMINAL_PROMPT'] = '0'
        started = time.monotonic()
        timed_out = False
        with prefix.with_suffix('.events.jsonl').open('w', encoding='utf-8') as log, \
                prefix.with_suffix('.stderr.txt').open('w', encoding='utf-8') as errors:
            process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=log, stderr=errors,
                                       text=True, encoding='utf-8', env=env, cwd=str(workspace))
            prefix.with_suffix('.pid').write_text(str(process.pid), encoding='ascii')
            try:
                process.communicate(prompt, timeout=420)
            except subprocess.TimeoutExpired:
                timed_out = True
                stop_process_tree(process)
        after = snapshot(workspace)
        changed = sorted(k for k in before.keys() | after.keys() if before.get(k) != after.get(k))
        events = []
        for line in prefix.with_suffix('.events.jsonl').read_text(encoding='utf-8').splitlines():
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        commands = [e.get('item', {}).get('command', '') for e in events
                    if e.get('type') == 'item.completed' and e.get('item', {}).get('type') == 'command_execution']
        summaries = {
            'id': case['id'], 'run': index, 'exit_code': process.returncode,
            'timed_out': timed_out,
            'turn_completed': any(e.get('type') == 'turn.completed' for e in events),
            'elapsed_seconds': round(time.monotonic() - started, 1),
            'thread_id': next((e.get('thread_id') for e in events if e.get('type') == 'thread.started'), None),
            'usage': next((e.get('usage') for e in events if e.get('type') == 'turn.completed'), None),
            'changed_files': changed, 'commands': commands,
            'file_changes': {k: {'before': before.get(k), 'after': after.get(k)} for k in changed},
            'response_file': str(prefix.with_suffix('.response.md')),
            'skill_hashes': {k: v for k, v in before.items() if k.startswith('.agents/skills/')},
            'command_failures': [
                {'command': e['item'].get('command'), 'exit_code': e['item'].get('exit_code')}
                for e in events if e.get('type') == 'item.completed'
                and e.get('item', {}).get('type') == 'command_execution'
                and e['item'].get('exit_code') not in (None, 0)
            ],
        }
        prefix.with_suffix('.summary.json').write_text(json.dumps(summaries, ensure_ascii=False, indent=2), encoding='utf-8')
        for name in set(('AGENTS.md', 'PLAN.md', 'src/normalize.js', *case.get('capture_files', []))):
            p = fixture_path(workspace, name)
            if p.exists():
                shutil.copy2(p, case_root / f'run-{index}-{name.replace("/", "_")}')
        all_results.append(summaries)
        print(json.dumps({k: summaries[k] for k in ('id', 'run', 'exit_code', 'elapsed_seconds', 'changed_files')}, ensure_ascii=False), flush=True)
        if process.returncode or timed_out or not summaries['turn_completed']:
            break
    return all_results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', action='append', required=True)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--cases', type=Path, default=Path(__file__).with_name('cases.json'))
    parser.add_argument('--extra-skill', action='append', type=Path, default=[],
                        help='Copy an already reviewed local Skill; does not download or install it globally')
    args = parser.parse_args()
    output = args.output.resolve() if args.output else create_output_directory()
    if output.is_relative_to(ROOT):
        raise SystemExit('Evidence output must be outside the source repository.')
    output.mkdir(parents=True, exist_ok=True)
    codex = shutil.which('codex')
    if not codex:
        raise SystemExit('Codex CLI is required; log in with your existing subscription before running.')
    home = Path(os.environ.get('CODEX_HOME', Path.home() / '.codex'))
    config = home / 'config.toml'
    settings = tomllib.loads(config.read_text(encoding='utf-8')) if config.exists() else {}
    cases = json.loads(args.cases.read_text(encoding='utf-8'))
    chosen = [c for c in cases if c['id'] in args.case]
    if len(chosen) != len(set(args.case)):
        raise SystemExit('Unknown case ID')
    print(f'Evidence directory: {output}', flush=True)
    print(f'Configured model: {settings.get("model", "CLI default")}', flush=True)
    infrastructure_ok = True
    for case in chosen:
        for result in run_case(case, output, codex, settings, args.extra_skill):
            infrastructure_ok &= result['exit_code'] == 0 and result['turn_completed'] and not result['timed_out']
        if not infrastructure_ok:
            break
    if not infrastructure_ok:
        raise SystemExit('One or more runs did not complete; inspect the evidence.')


if __name__ == '__main__':
    main()
