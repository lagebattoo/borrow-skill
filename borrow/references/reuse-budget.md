# Reuse budget

Budget describes acceptable external complexity, not money, a package quota, or
a required reuse percentage. Record the resolved level and where it came from.

| Level | Decision tendency |
| --- | --- |
| Conservative | Favor existing internal capabilities and light dependencies. New frameworks, services, and large projects need a clear ownership-cost advantage. Tiny stable functions may be BUILD. |
| Balanced | Default. Reuse mature commodity capabilities; justify large dependencies and keep simple BUILD options available. Balance delivery with maintenance. |
| Aggressive | Strongly favor mature packages, services, SDKs, templates, and OSS to shorten delivery. Reserve BUILD mainly for differentiation or when reuse is the larger burden. |
| Maximum Reuse | Assemble from suitable existing building blocks wherever practical. BUILD is a last option. Use only when the user actively selected this level, including a documented prior project choice. |

Within applicable instruction hierarchy, resolve the budget from the current
user instruction, then target-project AGENTS.md, then current design documents,
then Balanced. Do not infer Maximum Reuse from enthusiasm for speed. For a demo
or hackathon, suggest Aggressive if helpful, but keep the current level unless
the user changes it.

Budgets never waive requirement fit, correctness, acceptable licensing, basic
security, or platform feasibility. Production risk warrants stronger evidence at
any level; a hackathon does not need an enterprise-scale audit by default.

If the user chooses a temporary level for a single feature or experiment, apply it
to that scope and record it in the plan. Do not replace a project's lasting policy
with a one-off preference. Persist a long-term selection or the transparently
identified Balanced default when establishing a project's durable policy.

Use the same cost comparison at every level. Conservative can still ADOPT a large
system when it demonstrably lowers costs. Maximum can still BUILD a tiny function
when a dependency adds more burden than it removes.
