# Borrow behavioral evaluations

These are real, independent Codex CLI runs against synthetic local projects. They
test observable skill selection and planning behavior, not whether the source
contains expected phrases. `cases.json` stores raw inputs and reviewer rubrics;
the agent receives only its user prompt and project fixtures, never the rubric.

## Evidence sets

| Evidence | Scope |
| --- | --- |
| [Initial report](REPORT.md), [results](results.json) | Historical 8 cases / 9 calls; original baseline |
| [Compatibility report](COMPATIBILITY.md), [results](compatibility-results.json) | Historical 3 cases / 4 calls with a pinned ECC search-first; limited offline compatibility |
| [Refinement report](REFINEMENT.md), [results](refinement-results.json) | Current local handoff changes, three decision boundaries, and a fresh-session handoff without a companion Skill |

Keep historical results unchanged; a later source edit is not covered by an
earlier pass. Exact Skill hashes in each evidence set identify the tested inputs.

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

On Windows, the default directory inherits the normal temporary-parent access
entries so the sandbox account can traverse it. Recent Python `mkdtemp` owner-only
permissions can prevent this. The runner does not loosen an existing directory's
ACL. If using `--output`, choose a new directory with suitable inherited access.
Child processes start in the actual case workspace, and receive its absolute path
to prevent an unexpected shell working directory from causing a disk-root search.

Run the new boundary and standalone-handoff cases with:

```powershell
python tests/evals/run.py --case 09-missing-requirements --case 10-change-long-term-budget --case 11-policy-conflict --case 12-generic-handoff
python -m unittest discover -s tests/evals -p test_runner.py -v
```

The second command checks the runner without calling a model. For an optional
companion, `--cases` selects a separate fixture file and repeated `--extra-skill`
arguments copy reviewed local Skill directories with their original bytes. See
the compatibility report for the tested upstream revision. This neither downloads
third-party code nor installs a Skill into the user's normal environment.

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
Timeouts stop the recorded CLI process tree on Windows and retain the partial
evidence. Nonzero tool commands are recorded for review: for example, `rg` finding
no match is different from a permission error. Infrastructure success is not a
semantic pass.

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
in a dated report for the relevant evidence set. A finite sample does not guarantee all future activations. Offline
fixtures validate reasoning about provided evidence, not live source discovery,
current package safety/licensing, production integration, or other agent hosts.
