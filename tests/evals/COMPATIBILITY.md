# Borrow / search-first compatibility sample

This is the reviewed offline sample from 2026-09-21, before the local handoff
refinement. Borrow was based on repository commit `7bb5d61`; exact copied Skill
hashes and sanitized responses/artifacts are in [compatibility-results.json](compatibility-results.json).
It does not validate later edits or an entire ECC installation.

## Pinned upstream

Source: [ECC search-first at the tested commit](https://github.com/affaan-m/ECC/blob/2b6e839771e53096d8451a213d40dc64ec8acac0/skills/search-first/SKILL.md).

- Commit: `2b6e839771e53096d8451a213d40dc64ec8acac0`.
- Original file SHA-256: `d66d744228b9cf860acf35f8a90cbbe8195e61367860da9d3632f9fc65706733`.
- Historical copied fixture SHA-256: `2f649b0c28d34befdcafe6df61593473583ccecef897733a9d9ba74cd7f3f26c`.
- The historical fixture converted LF to CRLF; normalized text was identical.
  Borrow files were byte-identical. No Skill instructions were edited for that run.

The current runner preserves companion bytes. Thus rerunning the same inputs with
the original LF source will have the original upstream hash, not the historical
CRLF fixture hash. The upstream text is not vendored in this repository.

## Observed behavior

Codex CLI `0.155.0-alpha.9.2`, `gpt-6-astra`, high reasoning; three synthetic
projects and four independent calls, with external access disabled.

| Case | Successful Skill reads | Result |
| --- | --- | --- |
| Plan / policy, then explicit implementation handoff | Planning read Borrow and search-first; fresh implementation read search-first | Planning changed AGENTS.md / PLAN.md only; implementation changed src/export.js only; 2 existing CSV tests passed |
| Stale preferred provider | Borrow and search-first | Replaced an incompatible PREFERENCE using local evidence; kept budget, strategy and ownership; no writes or claimed integration test |
| Settled tiny implementation | Neither Skill | Performed local checks and implemented native arithmetic; 1 existing test passed; no Borrow overactivation; implicit search-first activation was **not observed** |

All four calls completed with exit code zero; reviewed command results showed no
failed commands. Conclusions concern supplied fictional evidence and these exact
runs. They do not establish automatic Skill chaining, live registry checks,
real-project reliability, full ECC compatibility or Claude Code compatibility.

## Reproduce deliberately

Review the pinned upstream source and its license, then obtain a local
`search-first/` directory at that revision. Do not substitute today's upstream
version and describe it as the same test. Run from this repository:

```powershell
python tests/evals/run.py --cases tests/evals/compatibility-cases.json --extra-skill <reviewed-local-search-first-directory> --case 01-planning-handoff --case 02-stale-preference --case 03-small-implementation
```

The fixtures and review rubrics are in [compatibility-cases.json](compatibility-cases.json).
The runner copies the supplied Skill only into the temporary projects. Current
Borrow edits and model changes can produce different results; review every rerun.

An earlier pilot failed because its Windows temporary directory was inaccessible
to the sandbox. It was terminated and excluded, not counted as a Skill failure or
a passing run. Its raw logs are not published. The valid rerun used an inherited
temporary-directory ACL, an explicit process working directory, and absolute
workspace paths; those fixes are now in the maintained runner. Archived evidence
contains only reviewed outputs with `${CASE_WORKSPACE}` replacing local paths;
raw event hashes identify the original locally retained logs, which may expire.
