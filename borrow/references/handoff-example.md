# Worked handoff: reuse a CSV encoder

This is a synthetic example of passing decisions to a fresh implementation
session. Names and compatibility claims below are fixture facts, not evidence
about real packages. Use the project's own paths and requirements.

## Planning request and available evidence

The user requests a CSV export with fixed `name,email` columns, at most 1000
records, and email redaction when `private === true`. The long-term budget is
Conservative. Existing `lib/csv.js` handles CSV quoting; the project supplies its
maintenance and license evidence. No new packages or services are authorized.

## Borrow's output

Merge lasting principles into the existing AGENTS.md: preserve Conservative,
reuse suitable internal capabilities, and keep field selection and redaction
under project control. Preserve unrelated rules and keep candidate details out
of that policy.

In the existing PLAN.md, record:

| Capability | Decision | Ownership and strength |
| --- | --- | --- |
| CSV serialization | ADOPT existing encoder | DECISION: reuse encoding infrastructure; verify its actual API and tests |
| Export composition | ADAPT through a thin adapter | DECISION: the project owns the adapter and fixed output contract |
| Field selection and redaction | BUILD small product logic | POLICY: the project controls which data may leave the system |

`lib/csv.js` is a PREFERENCE for the provider. Its exact integration is still
unverified. Behavior above 1000 records is OPEN until the user defines it; do not
silently truncate. These dimensions are separate from ADOPT/ADAPT/BUILD.

## Handoff to a fresh session

The user can give the implementing agent this scoped instruction:

> Read AGENTS.md and PLAN.md, then inspect lib/csv.js and the existing tests.
> Implement the planned export in src/export.js and run those tests. Preserve
> the policy, plan, encoder and tests. No network or package installation.
> Report what passed and what remains unverified.

The implementing agent can use search-first if available, or perform those
checks directly. No companion Skill is required. Merely naming a Skill in
PLAN.md does not run it.

## New evidence and completion

- If the preferred encoder is incompatible, compare a suitable local replacement
  and explain the changed PREFERENCE. Keep the CSV strategy and product rules.
- If the only available option requires a prohibited hosted service, expose that
  conflict and keep the provider OPEN. Do not treat reuse preference as permission
  to change the policy or install something.
- If the existing encoder fits, compose it with field selection and redaction;
  avoid copying its quoting implementation or reopening the whole architecture.

After actual execution, report the changed files and test results. Separate
runtime tests from fixture claims about maintenance, licensing and security.
If test scope is narrower than the acceptance criteria, list the remaining gap;
do not call the complete feature validated on the strength of a partial test.
