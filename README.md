# 借物 · Borrow

**Plan what to adopt, adapt, or build before coding.**

Borrow is a design-stage reuse planning skill for AI coding agents. It turns
requirements into capability-level reuse decisions and carries lasting policies
into the target project's `AGENTS.md`.

**v0.1.0 · Early release · MIT** — tested in isolated Codex CLI scenarios. Real
project usage and live external source selection have not been validated.

> 借物先理解需求，再判断哪些能力值得借、哪些逻辑应该自己掌控。
> 目标是降低长期工程负担，而不是安装更多依赖。当前为早期版本，已通过
> 8 个离线场景、9 次实际 Agent 调用验证，尚无真实项目使用验证。

## What it does

- Understands requirements, constraints, existing capabilities, and your reuse budget.
- Separates commodity/supporting capabilities from core product differentiation.
- Compares dependency/service, code/project, and knowledge/pattern reuse.
- Produces ADOPT / ADAPT / BUILD decisions with costs, ownership boundaries, and open questions.
- Persists durable policy and hands implementation checks to the coding agent.

At comparable ownership costs, Borrow prefers **ADOPT → ADAPT → BUILD**. A small
stable function can still be BUILD when a dependency would cost more to maintain.
Core product logic stays project-controlled while underlying infrastructure can
be reused.

Borrow handles planning. It does not install dependencies, implement the product,
automatically clone/fork candidates, or replace implementation-stage search-first.
When search-first is unavailable, the implementing agent receives the verification
requirements directly.

## Install in Codex

Ask Codex to use its built-in installer:

```text
Use $skill-installer to install the skill from
https://github.com/lagebattoo/borrow-skill/tree/v0.1.0/borrow
```

Alternatively, download the tagged repository and copy the complete `borrow/`
directory into your target project's `.agents/skills/borrow/`, retaining its
references, templates, metadata, and license. If that directory already exists,
review the existing installation before replacing it.

Only `borrow/` is the installable skill. The repository-root `AGENTS.md`, design
specifications, and `tests/` support development of this skill; they are not target
project instructions. Borrow itself has no executable scripts or runtime packages.
External discovery uses whatever research tools the host agent has available.

Local skill locations and discovery are described in the
[official Codex skill documentation](https://learn.chatgpt.com/docs/build-skills).
If the new skill is not visible in your session, restart Codex and try again.

## Use

```text
Use $borrow to plan a PDF analysis MVP for this repository.
Keep the current stack. Reuse budget: Balanced.
Identify reusable capabilities and the logic we should own.
Give me the plan first; do not edit files yet.
```

中文也可以直接调用：

```text
用 $borrow 规划这个功能，复用预算 Balanced。
先检查项目已有能力，说明哪些 ADOPT、ADAPT、BUILD，以及为什么。
这次先给方案，不修改文件。
```

Borrow can also be selected implicitly for meaningful project, feature,
architecture, migration, or major-refactor planning with plausible reuse
opportunities. Routine bug fixes, CSS edits, code explanations, and implementation
of settled plans should not start the full workflow automatically. Explicit small
requests receive a proportionate analysis.

## Reuse budget

| Level | Preference |
| --- | --- |
| Conservative | Existing capabilities and lightweight dependencies; new complexity needs a clear benefit. |
| Balanced | Default: balance delivery speed with long-term ownership. |
| Aggressive | Favor mature building blocks to shorten delivery. |
| Maximum Reuse | Assemble from existing capabilities wherever worthwhile; requires an active user choice. |

The budget changes tolerance for external complexity. It never relaxes requirement
fit, correctness, security, licensing, or platform constraints. Temporary feature
budgets do not silently replace a project's lasting policy.

## Outputs

Expect a capability reuse map, decision reasons, architecture/ownership boundaries,
and implementation handoff. POLICY, DECISION, PREFERENCE, and OPEN distinguish
durable rules, settled choices, recommendations, and unresolved questions.

Small decisions stay in the existing plan. Complex projects may use `REUSE_PLAN.md`.
Durable rules go into the target project's `AGENTS.md` when edits are authorized;
read-only requests receive proposed text. Missing evidence remains explicitly
unverified instead of becoming a passed check.

## Validation and limitations

The initial evaluation used Codex CLI `0.155.0-alpha.9.2` with `gpt-6-astra` / `high`:
**8 synthetic offline scenarios and 9 independent invocations passed**. The cases
covered positive/negative triggering, reuse decisions, budget handling, hard
filters, offline uncertainty, and repeated policy writing.

This is a finite behavioral sample, not a universal reliability score. Live
registry discovery, actual dependency integration, real project use, other agent
hosts/models, and activation with all desktop plugins enabled remain unverified.

See the [evaluation report](tests/evals/REPORT.md),
[reviewed evidence](tests/evals/results.json), and
[reproduction instructions](tests/evals/README.md).

## Project documents

- [Skill entry point](borrow/SKILL.md)
- [Unified design specification v1 — Chinese](借物Skill统一设计规格v1.md)
- [Original design guide and positioning — Chinese](借物Skill指导方案.md)
- [v0.1.0 release notes](releases/v0.1.0.md)

For feedback, open a [GitHub issue](https://github.com/lagebattoo/borrow-skill/issues)
with the request, expected behavior, actual behavior, and agent/model used. Use
redacted or synthetic examples instead of private project data.

## License

[MIT](LICENSE). The installable directory includes its own identical license copy
so the notice stays with the skill when it is copied separately.
