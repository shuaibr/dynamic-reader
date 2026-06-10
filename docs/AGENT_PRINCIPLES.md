# Agent Principles — Core Doc

**Status:** Foundational / living document
**Applies to:** All agent-assisted and human development in this repository
**Current application:** the active workstream is the [MENA Research Agent](../mena-research-agent/)
(Phase 1 — validation); see [ROADMAP.md](ROADMAP.md) for planning and phase status.

This document defines how we build with (and for) AI agents in this project. It is
organized around one operating rule:

> **Ship fast to validate the product. Harden only what's validated. But baseline
> security is never deferred.**

---

## 1. Operating Model: Validation Before Optimization

Work moves through explicit phases. Each phase has entry/exit criteria so we never
over-invest in code that hasn't earned it — and never under-invest in code that has.

| Phase | Goal | Optimize for | Explicitly deferred |
|-------|------|--------------|---------------------|
| **0 — Prototype** | Prove the idea is possible | Speed of learning | Scale, polish, advanced security, test coverage |
| **1 — Product/feature validation** | Prove users want it | Speed of delivery + feedback loops | Horizontal scaling, performance tuning, deep security hardening |
| **2 — Scale** | Prove it survives real load | Capacity, reliability, cost | Premature abstraction |
| **3 — Harden** | Prove it survives adversaries and time | Security depth, observability, resilience | — |

**Phase rules**

- A feature may not consume scaling/hardening effort until it has passed Phase 1
  exit criteria (below).
- **Baseline security (§5) applies in every phase, including Phase 0.** Deferring
  *hardening* is a choice; leaking secrets is an incident.
- Throwaway code is allowed in Phase 0–1 but must be labeled as such (file header
  comment or `prototypes/` location) so agents and humans don't harden it by accident.

**Phase 1 exit criteria (a feature is "validated" when):**

1. It is deployed or demoable end-to-end to a real user or stakeholder.
2. There is at least one feedback signal captured (usage event, interview note,
   conversion metric — anything measurable).
3. The core happy path is exercised by at least one automated check.
4. A go/no-go decision is recorded (keep, iterate, kill). Killed features are deleted,
   not commented out.

---

## 2. Layered Foundation for Agent Work

Every agent workflow in this repo must be answerable against four layers:

### 2.1 Abstraction
*Agents work best against clean seams.*

**Criteria**
- Public interfaces (API routes, module exports, prompts) are documented where they live.
- One canonical way to do each common task (build, run, test) — defined in `package.json`
  scripts and the README, so agents don't invent their own.
- Prompts and model configuration live in versioned files (e.g. `summary_prompt.txt`),
  not inline string literals scattered through code.

### 2.2 Isolation
*Agent actions must be containable and reversible.*

**Criteria**
- Agents work on feature branches, never directly on `main`.
- Side-effectful operations (external API calls, DB writes, deployments) are gated
  behind explicit human review until the feature is Phase 2+.
- Secrets are injected via environment, never available to be committed (§5).
- Experiments run in isolated directories/branches and are cleaned up after a
  go/no-go decision.

### 2.3 Validation
*Clear, cheap, fast checks — sized to the phase.*

**Criteria by phase**
- **Phase 0:** "Does it run?" Manual smoke test is sufficient. Record what you saw.
- **Phase 1:** One automated happy-path check per feature (script, unit test, or
  supertest call). CI runs it on every push. Human reviews every agent-authored diff.
- **Phase 2:** Integration tests on critical flows; load check on the hot path;
  lint + typecheck enforced in CI.
- **Phase 3:** Security testing (dependency audit, secret scanning, authz tests),
  regression suite, E2E on core journeys.

The validation bar deliberately starts low: a failing-fast manual check today beats a
perfect test suite for a feature nobody wants. The bar ratchets up with phase — it
never ratchets down.

### 2.4 Infrastructure capacity
*Match infrastructure spend to phase.*

**Criteria**
- Phase 0–1: single environment, simplest deploy that produces a shareable URL.
  No Kubernetes, no multi-region, no premature queueing.
- Capacity decisions are made when a measured bottleneck appears (§4), not
  speculatively.
- Token/API budget for LLM calls is tracked from the first integration — model usage
  is a capacity dimension like CPU or storage.

---

## 3. Fundamentals (Key Areas and Criteria)

Agents accelerate everything, including mistakes. These fundamentals still matter and
each has a concrete bar:

| Area | Criteria |
|------|----------|
| **Decision making** | Decisions that shape architecture or product direction get a short written record (issue, PR description, or `docs/decisions/`). One sentence of context + the decision is enough in Phase 0–1. |
| **Technical strategy** | The README's stated stack matches what's actually in the repo. Aspirational plans live under a clearly-labeled "Roadmap" heading, never presented as current state. |
| **Developer productivity** | A new contributor (human or agent) can go from clone → running app with the documented commands, with no tribal knowledge. Automation is preferred over toil: anything done manually 3+ times gets a script. |
| **Organizational collaboration** | Transparency by default: work happens in branches and PRs, not local hoards. Code review is mentorship — review comments explain *why*. Blameless treatment of mistakes; postmortems focus on systems, not people. |
| **Security** | Baseline (§5) always; hardening per phase (§2.3). |
| **Code health** | Dead code is deleted, not commented out. Formatting/linting is automated once Phase 1 is reached so reviews discuss substance, not style. |
| **Release hygiene** | `main` is always runnable. Every merge to `main` passes CI. Releases are tagged or otherwise identifiable. |
| **Reliability** | Errors are handled and surfaced, not swallowed. Phase 2+ features have at least minimal logging for diagnosis. |

---

## 4. Ecosystem Mapping Principles

When deciding *where* agents and effort should be applied, map the system using these
lenses:

- **Scale** — How many users/calls/files does this touch? Optimize big-N paths only.
- **Time** — How long do feedback loops take? Shorten the slowest loop first
  (e.g., deploy time, review latency).
- **Causality** — Trace symptoms to root causes before fixing; agents are good at
  patching symptoms, which hides causes.
- **Fan-in/out** — Changes to high fan-in components (shared utils, schemas, prompts)
  need proportionally more review.
- **Emergence** — Watch for behaviors no single component intended (e.g., prompt +
  user input interacting badly). Test combinations, not just units, once validated.
- **Incentives** — Make the right thing the easy thing: scripts, templates, and CI
  defaults beat written policy.
- **Capacity** — Know the limiting resource per phase (developer attention in Phase 0–1;
  compute/tokens in Phase 2+).
- **Feedback loops** — Every validated feature must feed a measurable signal back into
  decision making (§1 exit criteria).
- **Bottlenecks** — Fix the current bottleneck, not the most interesting one. Re-map
  after each fix; the bottleneck moves.

---

## 5. Baseline Repository Security (Non-Negotiable, All Phases)

This is the floor. It applies even to throwaway prototypes, because secrets and git
history outlive prototypes.

**Secrets**
- No credentials, API keys, or tokens in source, config, prompts, or git history.
- Secrets are loaded from environment variables / `.env`; `.env` is gitignored.
- `.env.example` documents every required variable with placeholder values.
- Never print or log secret values — not even during debugging.
- If a secret is ever committed: rotate it immediately; treat history as compromised.

**Repository settings**
- `main` is protected: changes land via PR, no force pushes.
- GitHub secret scanning (and push protection) enabled.
- Tokens granted to agents and CI are least-privilege and scoped to this repo.

**Dependencies**
- Lockfiles are committed so builds are reproducible and auditable.
- `npm audit` (and Python equivalent) run at least when dependencies change;
  high/critical findings on used code paths are fixed or consciously accepted in writing.

**Agent-specific**
- Treat all external content fed to LLMs (user input, scraped pages, fetched documents)
  as untrusted: it may contain prompt injection. Agent output that triggers actions
  (API calls, writes) requires validation before execution.
- Agent-authored changes are reviewed by a human before merging to `main`.

**Beyond baseline** (auth flows, rate limiting, encryption-at-rest, pen testing,
OWASP scanning) is *hardening* and is scheduled per the phase model — after the
feature is validated.

---

## 6. Culture

Borrowed deliberately from mature engineering ecosystems:

- **Engineering led, transparency by default.** Plans, decisions, and failures are visible.
- **Be a helper; share what you know.** Document the thing you just figured out.
- **Code review as mentorship**, for humans and as steering for agents.
- **Standardization is valuable.** One blessed path per task.
- **Continuous improvement, together.** Small frequent upgrades over big rewrites.
- **Blameless postmortems.** Fix systems, not people.
- **Sustainability over heroics.** If it only works because someone burned a weekend, it doesn't work.
- **Automation over toil.** Agents exist to eliminate toil — point them at it.

---

*Changes to this document go through PR review like any other change.*
