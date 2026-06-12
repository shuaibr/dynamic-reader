# SPEC — Maruf: Sufi & Classical Text Research Companion

> **Workstream status: GATED** — does not open until mena's go/no-go is
> recorded as "go" AND this repo holds the portfolio's Active slot
> (see [OPERATIONS.md](../OPERATIONS.md) Rule 3 and [ROADMAP.md](../ROADMAP.md)
> workstream 5). Read alongside [AGENT_PRINCIPLES.md](../AGENT_PRINCIPLES.md).
> Scholarly integrity outranks growth in every tradeoff; treat scholar review
> as a non-deferrable floor, like baseline security.

## Vision

A study companion for classical Islamic texts (Sufi and adjacent
scholarship): public-domain Arabic texts presented with vocabulary support,
structured annotations, and discussion prompts for study circles. The
community's corrections and annotations ARE the product — a flywheel where
students improve the corpus that teaches the next students.

## Financial outcome

- **Primary:** subscription ($8–12 CAD/mo) for the study layer (saved
  progress, vocab decks, circle tools).
- **Secondary:** institutional licensing (weekend schools, study circles,
  university Arabic programs).
- **Loop closes when:** 25 paying subscribers or first institutional pilot.
- **Kill criterion:** weekly active study sessions < 20 after 3 months.

## Non-negotiable content principles

- Public-domain or properly licensed texts only; provenance documented
  per text in `corpus/<text>/PROVENANCE.md`.
- AI-generated glosses are clearly labeled as machine-assisted and carry a
  "not a fatwa / not a substitute for a teacher" notice; theological
  questions route to "ask your teacher," never to model opinion.
- Scholar review tier: contested annotations escalate to named human
  reviewers before publication. Sensitive-topic taxonomy maintained.

## System architecture (four layers)

- **Abstraction:** corpus store, annotation engine, vocab/SRS engine, and
  delivery surface (web first) are separate modules with typed interfaces.
- **Isolation:** corpus is append-only + versioned (git); user data separate
  from corpus; annotation proposals quarantined until review passes.
- **Validation:** three annotation states — machine-draft → community-reviewed
  → scholar-verified — each visually distinct in the UI; diacritics and
  citation checks automated; eval set of 50 known-correct glosses gates
  any model/prompt change.
- **Infrastructure capacity:** corpus growth budgeted (1 text/quarter to
  start); review bandwidth is the explicit capacity constraint — never
  publish faster than review capacity.

## Ecosystem map (initial)

- **Scale:** 1 text, 1 study circle (yours) at launch; 10x = 10 circles,
  3 texts — review pipeline must scale before corpus does.
- **Time:** weekly study-circle rhythm drives everything; SRS reviews daily;
  corpus releases quarterly.
- **Causality hypothesis:** retention comes from the circle (social), not
  the app (tooling). Build circle features before solo features.
- **Fan-in:** corrections from many students converge on the corpus —
  highest-validation node. **Fan-out:** one verified annotation serves
  every future reader.
- **Emergence:** students will propose new texts and form circles you
  don't run — design permissions for that from Phase 2.
- **Incentives:** students learn with lower friction; contributors earn
  named credit on verified annotations; scholars get a citable corpus;
  operator earns subscriptions.
- **Capacity:** scholar review hours — recruit 2 reviewers before Phase 3.
- **Feedback loops:** (1) correction → review → corpus improvement;
  (2) vocab-miss data → better glossing of hard constructions;
  (3) circle discussion questions → annotation backlog.
- **Bottleneck #1:** trust and scholarly legitimacy. Mitigate with named
  reviewers, provenance docs, and visible annotation states from day one.

## Communication loops

- Agent → student: weekly portion with glosses + 3 discussion prompts.
- Student → corpus: one-tap "flag this gloss" with optional note.
- Circle → operator: monthly survey (3 questions max).
- Reviewer ↔ pipeline: review queue with SLA dashboard.

## Engineering fundamentals (project-specific)

- Security: study activity is sensitive personal data — minimal collection,
  clear policy, easy export/delete.
- Code health: Arabic text handling standardized (Unicode normalization,
  diacritics) in ONE shared library used everywhere.
- Reliability: corpus integrity check in CI (no orphan annotations,
  no provenance-less texts).

## Operations alignment (OPERATIONS.md governs)

- **Action output:** forced-choice only (Rule 1) — schema in framework-alignment.md.
- **Measure row = AOR** logged to `metrics/loop_closure.csv` (Rule 4).
- **Coordination:** single agent + output schema + scholar review tier as the human gate.
- Session hygiene: `reentry.md` on every stop (Rule 2); WIP cap (Rule 3) and
  meta-work quarantine (Rule 5) apply.

## Phases

- **Phase 1 — Smallest closed loop.** One short public-domain text, machine
  glosses, weekly portion email to YOUR circle, flag-a-gloss form, manual
  weekly corpus update. Run for 4 circle sessions.
- **Phase 2 — Study layer.** Web reader with annotation states, vocab SRS,
  progress; circle permissions.
- **Phase 3 — Review pipeline.** Reviewer roles, queue, SLAs; second text
  onboarded through the full pipeline.
- **Phase 4 — Monetization + community.** Subscriptions; contributor
  credits; institutional pilot kit.

## Out of scope

Original translations of rights-encumbered works, theological Q&A,
audio recitation (until Phase 5+), mobile apps before web proves retention.
