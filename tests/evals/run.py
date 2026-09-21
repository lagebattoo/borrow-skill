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


ROOT = Path(__file__).resolve().parents[2]


def snapshot(directory):
    return {
        p.relative_to(directory).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in directory.rglob('*')
        if p.is_file() and '.git' not in p.relative_to(directory).parts
    }


def run_case(case, output, executable, settings):
    case_root = output / case['id']
    workspace = case_root / 'workspace'
    workspace.mkdir(parents=True, exist_ok=False)
    subprocess.run(['git', 'init', '-q', str(workspace)], check=True)
    shutil.copytree(ROOT / 'borrow', workspace / '.agents/skills/borrow')
    for name, contents in case['files'].items():
        target = workspace / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(contents, encoding='utf-8')
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
        prompt += ('\n\n本次操作范围仅限当前临时项目。不访问外部网络、账号或其他项目，'
                   '不读取用户私人文件。当前项目 .agents/skills 中有可用技能，'
                   '按正常相关性自行决定是否使用，不要为了测试强制调用。')
        command.append('-')
        env = os.environ.copy()
        env['PYTHONUTF8'] = '1'
        env['GIT_TERMINAL_PROMPT'] = '0'
        started = time.monotonic()
        with prefix.with_suffix('.events.jsonl').open('w', encoding='utf-8') as log, \
                prefix.with_suffix('.stderr.txt').open('w', encoding='utf-8') as errors:
            process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=log, stderr=errors,
                                       text=True, encoding='utf-8', env=env)
            prefix.with_suffix('.pid').write_text(str(process.pid), encoding='ascii')
            try:
                process.communicate(prompt, timeout=420)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
                raise RuntimeError(f'{case["id"]}: model process exceeded 420 seconds')
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
            'turn_completed': any(e.get('type') == 'turn.completed' for e in events),
            'elapsed_seconds': round(time.monotonic() - started, 1),
            'thread_id': next((e.get('thread_id') for e in events if e.get('type') == 'thread.started'), None),
            'usage': next((e.get('usage') for e in events if e.get('type') == 'turn.completed'), None),
            'changed_files': changed, 'commands': commands,
            'file_changes': {k: {'before': before.get(k), 'after': after.get(k)} for k in changed},
            'response_file': str(prefix.with_suffix('.response.md')),
            'skill_hashes': {k: v for k, v in before.items() if k.startswith('.agents/skills/borrow/')},
        }
        prefix.with_suffix('.summary.json').write_text(json.dumps(summaries, ensure_ascii=False, indent=2), encoding='utf-8')
        for name in ('AGENTS.md', 'PLAN.md', 'src/normalize.js'):
            p = workspace / name
            if p.exists():
                shutil.copy2(p, case_root / f'run-{index}-{name.replace("/", "_")}')
        all_results.append(summaries)
        print(json.dumps({k: summaries[k] for k in ('id', 'run', 'exit_code', 'elapsed_seconds', 'changed_files')}, ensure_ascii=False), flush=True)
        if process.returncode:
            break
    return all_results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', action='append', required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    output = args.output.resolve() if args.output else Path(tempfile.mkdtemp(prefix='borrow-eval-'))
    if output.is_relative_to(ROOT):
        raise SystemExit('Evidence output must be outside the source repository.')
    output.mkdir(parents=True, exist_ok=True)
    codex = shutil.which('codex')
    if not codex:
        raise SystemExit('Codex CLI is required; log in with your existing subscription before running.')
    home = Path(os.environ.get('CODEX_HOME', Path.home() / '.codex'))
    config = home / 'config.toml'
    settings = tomllib.loads(config.read_text(encoding='utf-8')) if config.exists() else {}
    cases = json.loads((Path(__file__).parent / 'cases.json').read_text(encoding='utf-8'))
    chosen = [c for c in cases if c['id'] in args.case]
    if len(chosen) != len(set(args.case)):
        raise SystemExit('Unknown case ID')
    print(f'Evidence directory: {output}', flush=True)
    print(f'Configured model: {settings.get("model", "CLI default")}', flush=True)
    infrastructure_ok = True
    for case in chosen:
        for result in run_case(case, output, codex, settings):
            infrastructure_ok &= result['exit_code'] == 0 and result['turn_completed']
    if not infrastructure_ok:
        raise SystemExit('One or more runs did not complete; inspect the evidence.')


if __name__ == '__main__':
    main()
