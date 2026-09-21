# Discovery and stopping

Before external discovery inspect relevant existing implementations, dependencies,
services, infrastructure, design systems, Skills/MCP, and established patterns.
Use available tools and approved access. A source list is guidance, not a mandate
to query every platform or install a new connector.

## Route by resource type

| Resource | Useful starting routes after the internal check |
| --- | --- |
| JavaScript / TypeScript | Relevant package registry such as npm, official docs, upstream repository |
| Python | PyPI or the project's registry, official docs, upstream repository |
| UI | Existing design system, component ecosystem, package registry, upstream source |
| Model / dataset | Model hub such as Hugging Face, official provider and model/data cards, research implementation |
| Agent capability | Existing Skills/MCP first, then relevant registries and authoritative repositories |
| Architecture / pattern | Official documentation, mature OSS architecture, technical references and implementations |
| Complete application / starter | Relevant template ecosystem or hosting platform such as GitHub, GitLab, or Codeberg |

Choose the most effective source for the actual capability. Enterprise/internal
sources and new registries may replace these examples. A whole-product repository
is a starter or reference candidate, not an automatic fork recommendation.

Prefer official, maintained, well-documented, requirement-fitting candidates.
Follow discovery signals to authoritative evidence rather than treating a search
snippet, stars, or a README claim as sufficient for every check.

## Bound the search

For each significant capability, one clearly suitable candidate may be enough;
compare two or three when the tradeoff is not obvious. Stop expanding discovery
when evidence establishes requirement fit, no material hard blocker, acceptable
costs for the budget, and enough information to choose responsibly. Candidate
count is not a success metric and one candidate is not a reason to skip filtering.

If the primary source does not yield an acceptable option, try the relevant
secondary source, then broader OSS or knowledge/pattern reuse as warranted.
After reasonable coverage, BUILD with a documented reason is valid. State the
scope searched, rejected alternatives, and remaining uncertainty. Do not jump
from one failed query to “nothing exists”, or search indefinitely for proof that
no reusable solution exists anywhere.

When searches stop adding decision-relevant evidence after these relevant routes,
stop and record BUILD if justified, or OPEN if a material unknown remains. If a
research time limit was set, honor it; do not invent a numeric limit for all tasks.

Increase depth for hard-to-replace auth, payment, database, framework, security,
or vendor infrastructure, explicit deep-selection requests, and materially
different candidates. Keep low-impact renderer, icon, or simple chart choices
brief. Risk changes evidence depth, not the fundamental standard of correctness.

## Restricted or unavailable discovery

If tools, network, or authorization are unavailable, use accessible project
evidence and clearly distinguish it from unverified external possibilities.
Do not describe remembered package details as freshly checked. Mark affected
choices OPEN or conditional PREFERENCE and specify the evidence needed later.
Unavailable research does not itself justify BUILD or a passed security/license
check. Continue unaffected planning; do not install, authenticate, or widen access
merely because the Skill mentions a platform.
