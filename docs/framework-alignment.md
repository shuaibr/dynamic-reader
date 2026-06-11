# Framework Alignment: mena

> Committed at `docs/framework-alignment.md` per the Phase 1 checklist below.
> The agent scaffold this builds on lives at `mena-research-agent/`.

**Status:** Planning V1 (PASSIVE until Active slot opens) | **Archetype:** Async Data Refinery
**Target Time-to-Validation:** 7d (brief #1 shipped to 10-person list, ≥3 replies)
**Coordination archetype:** single-agent — research synthesis is sequential (plan → gather → synthesize); bilingual query expansion is a function call, not an agent. Citation schema + operator review are the gates.

-----

## 1. The Loop

|Stage               |What it is for this project                                            |
|--------------------|-----------------------------------------------------------------------|
|**Sense** (input)   |Weekly topic → parallel AR+EN search queries → ~25 sources (existing mena-research-agent pipeline)|
|**Decide** (process)|Cited synthesis; language-coverage gate (≥40% AR or visible banner); AR-delta extraction|
|**Act** (output)    |Thursday draft to operator, forced-choice per section: `PUBLISH / EDIT / CUT`; Friday send|
|**Measure** (impact)|Replies, topic requests, link forwards; publish decision logged to metrics/loop_closure.csv|
|**Improve** (update)|Each brief commits/updates a country source-map skill; hrs/brief tracked (target −30% by brief 12)|

-----

## 2. Platform Split + Handoff Contract

**Google AI Plus — research & knowledge**
- Inputs it owns: long-form Arabic PDFs, ministry/UN reports, background dossiers.
- Tasks it owns: deep multilingual document analysis, topic landscape memos.

**Claude Code (Max 5x) — execution & production**
- Owns: GSD orchestration, pipeline runs, citation validation, source-map skills, newsletter formatting.
- Compute boundary: one pipeline run/week; tiered models per config.yaml; SQLite for source registry.

**Handoff contract:**
- Gemini output lands as: markdown dossiers per topic.
- Delivered to: `/research/inbox/<topic>/`.
- Claude Code consumes via: pipeline ingests inbox dossiers as additional cited sources (tagged `gemini-dossier`).
- Cadence: weekly, before the Mon research run.

-----

## 3. Architecture Gates

- **Abstraction:** search/LLM/newsletter providers in `src/adapters/`; one file each.
- **Isolation:** each brief a fresh run; corpus + source maps in git; merges only post-validation.
- **Validation:** zero uncited claims (schema-enforced); 20-claim golden set for citation accuracy before pipeline changes.
- **Capacity:** ≤45 min/run · ≤$5.00 CAD/brief · ≤3 hrs human review/brief · warn at 80%.

-----

## 4. Phase 1 Checklist

- [x] Repo initialized with this doc at `docs/framework-alignment.md`
- [x] `config.yaml` (model tiers, Arabic floor) from scaffold — note: $ and
      runtime budgets from §3 are not yet enforced in code (roadmap ws-2)
- [x] `/research/inbox/` created
- [ ] `npx get-shit-done-cc@latest`; feed this doc + SPEC.md + PRINCIPLES.md + OPERATIONS.md into `/gsd-plan-phase`
- [ ] Planner feedback noted → prune template

**Planner feedback:**
- Sections used:
- Sections ignored:
