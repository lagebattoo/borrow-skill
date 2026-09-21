# Borrow behavioral evaluations

These are real, independent Codex CLI runs against synthetic local projects. They
test observable skill selection and planning behavior, not whether the source
contains expected phrases. `cases.json` stores raw inputs and reviewer rubrics;
the agent receives only its user prompt and project fixtures, never the rubric.

## Run

Prerequisites: Python 3.11+, Git, and an authenticated Codex CLI. Use the existing
subscription login; the runner does not copy credentials or configure an API key.
The run consumes normal model usage. Model and reasoning effort inherit the
current user configuration, rather than silently substituting another model.

```powershell
python tests/evals/run.py --case 01-css --case 04-project-plan
```

Use repeated `--case` arguments to select cases. An optional `--output` directory
must be outside this repository and must not already contain the selected case
directories. Without it, the runner creates a temporary directory. Each case gets
a fresh Git repository and a copy of `borrow/` at `.agents/skills/borrow/`.

The CLI is ephemeral and ignores user configuration except the explicitly
inherited model/effort and Windows sandbox mode. Hooks, plugins, apps, memories,
browser/computer use, and delegation are disabled for the invocation. External
research is disabled; normal host skill discovery and global instructions may
still apply. The prompt limits work to the synthetic temporary project.

Read-only cases use the read-only sandbox. The settled-code and policy-write cases
use workspace-write. The policy follow-up is a fresh session in the same temporary
project to check repeated application without sharing the prior conversation.
No normal user-level Skill installation is performed.

## Review evidence

Each run records process/thread IDs, JSONL events, final response, elapsed time,
exit status, token usage, exact Skill hashes, executed commands, changed-file
hashes, and selected output files. Evidence remains in the temporary directory;
do not commit unreviewed raw logs containing machine paths or host context.

Check the following separately:

- Did the agent actually read `borrow/SKILL.md` in a successful tool call? A
  directory listing or merely naming the skill is not proof of loading it.
- Does the response and any produced artifact satisfy the case's semantic rubric?
  ADOPT/ADAPT labels alone do not prove sensible ownership or cost decisions.
- Were writes limited to the requested paths, with unrelated instructions intact?
- Did execution succeed without environment/permission failures? Exit code zero
  is not enough when the response says it could not read required inputs.

There is deliberately no wording-based automatic behavioral pass score. Review
the command results, responses and filesystem artifacts, then record the findings
in `REPORT.md`. A finite sample does not guarantee all future activations. Offline
fixtures validate reasoning about provided evidence, not live source discovery,
current package safety/licensing, production integration, or other agent hosts.
