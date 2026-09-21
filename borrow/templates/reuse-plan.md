# Reuse decisions template

Use only the sections justified by the task, inline or in the existing plan.
A dedicated REUSE_PLAN.md is optional. Replace illustrative fields; the template
is not evidence and does not prescribe a fixed number of capabilities/candidates.

## Requirement snapshot

- Goal and observable acceptance criteria: [facts]
- Delivery target and constraints: [MVP/production, time, stack, platform/deployment]
- User choices and differentiation: [facts]
- Reuse Budget, source, and scope: [level; current instruction/policy/design/default]
- Relevant existing capabilities: [code, dependencies, services, infrastructure, patterns]

## Capability Reuse Map

| Capability | Classification | Decision | Reuse type | Direction | Strength |
| --- | --- | --- | --- | --- | --- |
| [capability] | [Commodity / Supporting / Core] | [ADOPT / ADAPT / BUILD / unresolved] | [Dependency-service / Code-project / Knowledge-pattern / None] | [direction] | [DECISION / PREFERENCE / OPEN] |

## Important capability: [name]

**Why:** [compare reuse and build ownership costs; explicit reason if BUILD]

**Evidence:** [relevant internal findings; authoritative sources and observation
dates; checks performed, rejected options, material unknowns]

**Search stopping reason:** [sufficient candidate, reasonable coverage exhausted,
or research constraint; distinguish absence of evidence from evidence of absence]

**Ownership boundary:** [external responsibilities / project-controlled responsibilities]

**Architecture impact:** [interfaces, data flow, adaptation, deployment, replacement implications]

**Handoff:**

- Fixed: [requirements, constraints, policies, and settled decisions]
- Preferred: [replaceable recommendations]
- Revalidate: [current API/compatibility, maintenance, material filters, local code, focused integration]
- Open/change conditions: [missing evidence, responsible agent, when to resolve or revisit]

## Durable policy

[Policy written to the applicable AGENTS.md, or proposed section when editing is
outside scope. Distinguish lasting project rules from temporary budget overrides.]

## Risks, assumptions, and open questions

[Only decision-relevant items. Assign implementation verification to search-first
when available or to the implementing agent otherwise. Do not imply checks ran.]
