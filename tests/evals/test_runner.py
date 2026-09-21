"""Regression checks for evaluation isolation, not a semantic Skill grader."""

import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('eval_runner', Path(__file__).with_name('run.py'))
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


class RunnerIsolationTests(unittest.TestCase):
    def test_default_windows_directory_inherits_parent_access(self):
        # Exercise real mkdir rather than mocking the operation that caused the
        # sandbox failure. The actual Codex runs verify sandbox-account access.
        directory = runner.create_output_directory()
        try:
            self.assertTrue(directory.is_dir())
            if os.name == 'nt':
                # icacls uses a Windows console encoding even when Python runs
                # in UTF-8 mode. Its inheritance marker is ASCII in all locales.
                acl = subprocess.check_output(['icacls.exe', str(directory)])
                self.assertIn(b'(I)', acl, 'Expected inherited access entries')
        finally:
            directory.rmdir()

    def test_rejects_escaping_and_skill_overwriting_fixtures(self):
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp) / 'workspace'
            for name in ('../outside', '.git/config', '.agents/skills/borrow/SKILL.md'):
                with self.subTest(name=name), self.assertRaises(ValueError):
                    runner.fixture_path(workspace, name)
            self.assertEqual(runner.fixture_path(workspace, 'src/example.js'),
                             workspace / 'src/example.js')

    def test_missing_companion_fails_before_creating_case(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            with self.assertRaisesRegex(ValueError, 'Missing required Skills'):
                runner.run_case({'id': 'missing', 'files': {}, 'required_skills': ['unavailable']},
                                output, 'unused', {})
            self.assertFalse((output / 'missing').exists())

    def test_real_child_uses_case_cwd_and_preserves_skill_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            worker = output / 'fake_cli.py'
            worker.write_text(
                'import json, pathlib, sys\n'
                'args=sys.argv[1:]\n'
                'expected=pathlib.Path(args[args.index("-C")+1]).resolve()\n'
                'assert pathlib.Path.cwd().resolve()==expected\n'
                'assert pathlib.Path("fixture.txt").read_text()=="case fixture"\n'
                'prompt=sys.stdin.read()\n'
                'assert str(expected) in prompt\n'
                'assert "RUBRIC_MUST_STAY_OUT" not in prompt\n'
                'pathlib.Path(args[args.index("-o")+1]).write_text("done")\n'
                'print(json.dumps({"type":"turn.completed","usage":{}}))\n',
                encoding='utf-8')
            original_popen = subprocess.Popen

            def run_fake(command, **kwargs):
                return original_popen([sys.executable, str(worker), *command[1:]], **kwargs)

            case = {'id': 'cwd', 'files': {'fixture.txt': 'case fixture'},
                    'prompt': 'Inspect the fixture.', 'rubric': ['RUBRIC_MUST_STAY_OUT']}
            # git init still uses real subprocess.run; only replace model launch.
            def dispatch(command, **kwargs):
                if command[0] == 'fake-codex':
                    return run_fake(command, **kwargs)
                return original_popen(command, **kwargs)

            with patch.object(runner.subprocess, 'Popen', side_effect=dispatch):
                result = runner.run_case(case, output, 'fake-codex', {})[0]
            self.assertEqual(result['exit_code'], 0)
            self.assertTrue(result['turn_completed'])
            self.assertFalse(result['timed_out'])
            self.assertEqual(result['changed_files'], [])
            source = runner.ROOT / 'borrow/SKILL.md'
            copied = output / 'cwd/workspace/.agents/skills/borrow/SKILL.md'
            self.assertEqual(source.read_bytes(), copied.read_bytes())


if __name__ == '__main__':
    unittest.main()
