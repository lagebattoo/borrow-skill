# Capability decisions

## Decomposition and ownership

Make a capability small enough for an independent reuse decision and large
enough to matter architecturally. Classification depends on this product's value,
not only on the technology's name.

| Class | Default approach |
| --- | --- |
| Commodity | Reuse-first: common auth infrastructure, parsing, logging, drivers, charts, and payment SDKs. |
| Supporting | ADOPT/ADAPT first, including project-specific transformations and orchestration where suitable. |
| Core Differentiation | Retain control of distinctive rules, schemas, algorithms, and workflows; separately evaluate reusable underlying infrastructure. |

For example, a core evidence engine may ADOPT PDF extraction, embedding, storage,
and an LLM SDK while BUILDing its evidence schema and assessment logic. A workflow
can be Supporting in one product and Core in another.

Choose the reuse form separately from the decision:

- **Dependency/service:** package, SDK, component, framework, API, hosted service,
  or model accessed through an appropriate interface.
- **Code/project:** starter, template, example, component source, or a justified fork.
- **Knowledge/pattern:** architecture, algorithm, UX, prompt, workflow, data model,
  directory, or deployment design without importing the source itself.

BUILD can coexist with knowledge reuse. Use “None” when nothing is reused; do not
label original work as reuse simply to populate a table. Prefer a pattern or a
component over an entire repository when it meets the need. A wrapper, adapter,
extension, or composition often preserves upstream upgrades better than copied,
heavily modified code. Introduce an abstraction only when its benefit warrants it.

## Hard filters and evidence

Reject a candidate when evidence establishes a material requirement mismatch,
unacceptable license or security risk, platform incompatibility, infeasible
integration, or abandonment coupled with high dependency risk. A quiet project is
not automatically abandoned; inspect meaningful changes and the maturity of the
capability. Budget cannot relax these filters.

For important ADOPT/ADAPT candidates check authoritative information about license
and usage terms, maintenance and last meaningful update, known security concerns,
compatibility, dependency weight, and documentation. Include vendor and data
constraints where services or models are involved. Record sources and observation
dates for facts likely to change, plus what was and was not checked.

Unknown is not acceptable, unacceptable, or “no known vulnerabilities” by default.
When a material check is unavailable, mark it unverified and leave the choice OPEN
or a conditional PREFERENCE. Do not invent current versions, licenses, support,
or compatibility. Distinguish documented compatibility from tested integration.

## Compare total engineering ownership

Use qualitative comparisons with concrete reasons, not invented numerical scores.

| Reuse costs | Build costs |
| --- | --- |
| Integration, learning, testing, dependency weight, debugging, maintenance, upgrades, security surface, license obligations, vendor risk/lock-in, and replacement | Implementation, testing, debugging, learning, maintenance, future feature work, upgrades, and taking ownership of security and correctness |

Include fit, maturity, documentation, extensibility, and existing architecture in
the comparison. Stars and popularity are weak supporting signals. At otherwise
comparable costs, prefer the solution easier to replace and ADOPT over ADAPT over
BUILD. Consider current requirements and a reasonably visible future, not an
imagined billion-user system.

## Decision rules

| Decision | Evidence needed |
| --- | --- |
| ADOPT | Meets the need, passes material hard filters, and has reasonable integration and lifetime costs. |
| ADAPT | Removes the main difficulty but needs a bounded wrapper, extension, combination, partial reuse, or justified fork. State the adaptation and ongoing upgrade burden. |
| BUILD | Explain why reuse costs more, no acceptable candidate exists within a reasonable search scope, the function is tiny and stable, or the logic must remain project-controlled. |

“I can write it” is insufficient for BUILD. A tiny stable transformation may need
only a brief comparison with adding a dependency; it does not require an external
search to justify every line. “No candidate exists” requires actual scoped
discovery; unavailable search is not proof of absence.

For authentication, cryptography, payments, secret management, and permission
enforcement, favor mature trustworthy infrastructure. Keep business authorization
rules under project control without treating that as a reason to reinvent crypto
or authentication primitives.

## Common corrections

Avoid package accumulation by comparing tiny BUILD with the entire dependency
burden. Avoid reflexive BUILD by requiring reasons. Avoid endless repository
shopping by using stopping conditions. Avoid architecture hijacking by checking
against the requirement snapshot. Avoid premature forks by comparing dependency,
component, and pattern reuse first. Replace unsuitable existing infrastructure
when evidence supports the migration cost; internal availability is not a mandate.
