# Architecture, persistence, and handoff

## Integrate decisions into the design

For each important capability state what the reused solution owns, what the
project owns, and the resulting architecture changes: relevant interfaces, data
flow/storage, deployment dependencies, or adaptation work. Include only details
that affect the decision. A library shopping list is not an integrated design.

For auth, for example, a provider might own identity verification, sessions, and
password reset while the project owns role definitions and business authorization.
Name replacement or lock-in implications when meaningful.

## Decision strength

| Strength | Meaning and change handling |
| --- | --- |
| POLICY | Durable project rule. Preserve its scope and user authority; surface conflicts instead of silently overriding it. |
| DECISION | Settled current design. Follow it unless new evidence warrants an explicit revision and, when required, user approval. |
| PREFERENCE | Recommended direction, open to implementation-stage replacement with a reasoned alternative. |
| OPEN | Not resolved yet. State the missing information, decision owner, and when it must be resolved. |

Strength and ADOPT/ADAPT/BUILD are separate dimensions. The strategy to adopt a
mature auth solution can be a DECISION while the provider remains a PREFERENCE.
Mark unresolved choices OPEN rather than manufacturing a final decision.

## Output size and location

For a small task add concise reuse decisions to the current answer or plan. For a
standard project use its existing technical plan or architecture document. Use a
separate REUSE_PLAN.md only when the complexity makes it useful. Do not create
duplicate documents solely because templates are supplied.

Use a Capability Reuse Map with capability, classification, decision, reuse type,
and direction. For important capabilities add why, ownership boundaries,
architecture impact, evidence/uncertainty, strength, and implementation handoff.
Keep risks, assumptions, and open questions visible.

## Update the target project's AGENTS.md

Persist rules that should outlive this planning run: long-term budget, ownership
principles, reuse preferences, search routing/stop principles, and implementation
verification requirements. Keep candidate rankings, observed versions, stars,
commit IDs, and dated research evidence in the plan instead.

Read existing applicable instructions before editing. Merge a focused Reuse Policy
section, retaining unrelated instructions and explicit user choices. Reuse an
existing policy section rather than appending duplicates on repeated runs. Resolve
the applicable scope; do not promote a feature-specific rule to project-wide
policy. Do not write into a global user AGENTS.md to implement a project policy.

When a planning task authorizes project-file edits, persist the relevant policy
without introducing a new approval step. When the user asks for advice/read-only
analysis, supply a clearly labeled proposed section. Do not infer permission to
alter an explicit technology choice or perform external operations from a budget.

The [policy template](../templates/agents-reuse-policy.md) is a starting section,
not a replacement AGENTS.md. The [plan template](../templates/reuse-plan.md) is
optional; replace illustrative fields and remove irrelevant sections.

## Handoff to implementation

Tell the implementing agent:

- What is fixed: requirements, user constraints, policies, and settled decisions.
- What is preferred: candidates or directions that may change with new evidence.
- What must be checked: existing local implementation, current API/version and
  compatibility, maintenance, license/security concerns, and a focused integration
  check appropriate to the capability.
- What may change and why: permissible substitutions, open decisions, and evidence
  that should trigger reconsideration of the design.

Use search-first for local revalidation when it is available. Otherwise assign
these checks directly to the implementing agent; do not claim that search-first
ran or require its installation. Early discovery is not permanent fact. Keep
“documentation checked”, “integration tested”, and “still unverified” distinct.

Borrow's handoff does not authorize implementing the product, installing packages,
forking repositories, purchasing services, or deployment. Those actions follow
the user's actual task and the target project's authorization rules.
