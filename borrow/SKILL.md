---
name: borrow
description: >-
  Plan software reuse before implementation: decompose capabilities, compare
  ADOPT, ADAPT, and BUILD, and carry lasting reuse policies into AGENTS.md.
  Use when users request Borrow/借物 or reuse planning, or when project, feature,
  architecture, migration, or major-refactor planning has meaningful capability
  scope and plausible reuse opportunities. Do not automatically trigger for
  routine bug fixes, CSS edits, code explanations, or implementing a settled plan.
---

# 借物 · Borrow

Create design-stage reuse decisions that reduce total engineering ownership.
Understand requirements before looking for reusable solutions. Let existing
solutions serve the product; do not reshape the product to fit a repository.

## When to run

Run when explicitly requested, including “用借物设计”, “先看看哪些能力能借”,
or a request to avoid reinventing capabilities. Otherwise require all three:

- **Stage:** the task is deciding how the system or feature should work.
- **Scope:** it contains capabilities worth independent build-versus-reuse decisions.
- **Opportunity:** useful existing code, dependencies, services, or patterns plausibly exist.

An architecture redesign during coding can re-enter this stage. A routine local
implementation problem normally belongs to implementation-stage search-first.
For an explicit request on a tiny task, scale the analysis down to that capability;
do not invent a full project or require extra documents.

## Workflow

### 1. Establish requirements and context

Read the conversation and relevant project instructions, plans, architecture,
dependency manifests, and implementations. Capture a brief requirement snapshot:
goal, observable acceptance criteria, delivery target (prototype/MVP/production),
time, technology, platform/deployment constraints, explicit user choices, and core
differentiation. Use supplied facts rather than asking users to fill a form.

Ask focused questions when a missing answer would change the goal, hard filters,
or an expensive architecture choice. Continue independent analysis where possible.
State low-impact assumptions; leave affected decisions OPEN when evidence is
insufficient. A delivery label such as “MVP” does not replace acceptance criteria.
Suggest alternatives to implementation ideas when useful, but treat explicit
technology choices as constraints until the user changes them.

### 2. Resolve the reuse budget and look inward

Read [reuse-budget.md](references/reuse-budget.md) when resolving the budget.
Use the current user choice, then applicable AGENTS.md, then the current design,
then Balanced. Recommend a different level only with reasons; do not silently
change it. Maximum Reuse requires an active user choice.

Before external discovery, inspect relevant existing code, dependencies, services,
infrastructure, patterns, Skills/MCP, and architecture. Existing capability is a
candidate, not an obligation to retain unsuitable or risky technical debt.

### 3. Decompose, discover, and decide

Read [decision-rules.md](references/decision-rules.md) for capability classification
and evaluation. Decompose at the level of independent reuse decisions, not just
“frontend/backend/AI” and not individual buttons. Classify Commodity, Supporting,
and Core Differentiation; split reusable infrastructure from project-owned logic.

Consider dependency/service, code/project, and knowledge/pattern reuse. Before
external discovery read [source-routing.md](references/source-routing.md). Choose
sources by resource type, gather only enough credible evidence, apply hard filters,
compare ownership costs, and stop when a defensible decision is possible.

Decide ADOPT, ADAPT, or BUILD for each important capability where evidence permits.
Record a reason for BUILD. If research is blocked, preserve an OPEN decision or a
clearly conditional PREFERENCE rather than treating unknowns as passed checks.

### 4. Integrate and persist

Read [handoff-policy.md](references/handoff-policy.md). Explain what the decision
changes in the architecture, what is externally supplied, and what stays under
project control. Distinguish POLICY, DECISION, PREFERENCE, and OPEN.

Produce a Capability Reuse Map with classification, decision, reuse type, and
direction. For each important capability include why, ownership boundaries,
architecture impact, decision strength, evidence/uncertainty, and handoff checks.
Scale detail to the task; the map can be a short section of the current plan.

Persist durable reuse policy and long-term budget in the target project's
AGENTS.md within the authorized scope. Preserve unrelated instructions. For
read-only/advice-only requests, provide a proposed section instead of editing.
Keep transient candidates and versions in the plan. Use the
[policy template](templates/agents-reuse-policy.md) or
[plan template](templates/reuse-plan.md) only when helpful; an independent
REUSE_PLAN.md is optional.

### 5. Hand off implementation verification

State what is fixed, preferred, open, and must be revalidated. Hand current
compatibility, API, maintenance, and local-code checks to search-first when
available, or explicitly to the implementing agent when it is not. Do not require
installing another Skill merely to complete the handoff.

## Rules that must survive compression

- Requirement first; inspect existing capabilities before external search.
- At comparable costs prefer ADOPT, then ADAPT, then BUILD. BUILD needs a reason.
- Reuse the needed capability, not automatically a whole project; keep core
  differentiation controlled by the project while reusing infrastructure.
- Route sources by resource type and stop at a good-enough, evidenced decision.
- Optimize total engineering ownership, including testing, debugging, integration,
  dependency, upgrade, maintenance, security, license, vendor, and replacement costs.
- Respect the user's reuse budget; it never relaxes hard filters or correctness.
- Persist durable policy in AGENTS.md and leave implementation verification to
  the implementing agent and search-first where available.

Borrow produces reuse strategy, not business implementation, dependency
installation, automatic cloning/forking, rankings, or exhaustive research.
An ADOPT/ADAPT recommendation does not itself authorize installing, purchasing,
deploying, or granting access. Match evidence depth to decision impact; distinguish
planning evidence from real integration tests and never claim unperformed checks.
