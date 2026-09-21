# Reuse Policy section template

Adapt the section below to the target project and merge it into the appropriate
AGENTS.md. Replace bracketed fields with project facts, remove inapplicable text,
and preserve existing instructions. Use it for durable policy, not candidate lists.

```markdown
## Reuse Policy

Reuse Budget: [Conservative / Balanced / Aggressive / Maximum Reuse]
Budget basis and scope: [explicit user choice / existing project policy / Balanced default; project scope]

Optimize total engineering ownership rather than code count or reuse percentage.
At comparable costs prefer ADOPT, then ADAPT, then BUILD. Explain BUILD decisions.
The budget changes acceptable external complexity, not correctness, security,
license, platform, or requirement-fit standards.

Before introducing a non-core capability, inspect existing project code,
dependencies, services, infrastructure, patterns, and available Skills/MCP.
If needed, route external discovery to the appropriate resource source. Stop
when evidence supports a good-enough decision; deepen research for high-impact,
hard-to-replace infrastructure.

Project-controlled differentiation: [specific rules, schemas, workflows, or algorithms]
Reuse appropriate infrastructure underneath this differentiation. Prefer the
needed dependency, component, or pattern over an entire project when sufficient.
Do not retain unsuitable existing systems solely because they already exist.

Respect explicit requirements and technology constraints. Do not install or
introduce dependencies merely because they might be useful later.

Before implementation, read this policy and the current project plan or decision
section. Use search-first when available or perform equivalent
local verification directly: check current project implementations, candidate
maintenance, API/compatibility, license/security evidence, and relevant integration
behavior. State new evidence before revising settled design decisions; surface
conflicts with user constraints rather than silently changing them.

Keep temporary candidates, versions, and dated evidence in the current plan.
```
