# SPEC — Mena: Arabic Articles & Research Briefs

> **Governs workstreams 1–2** ([ROADMAP.md](../ROADMAP.md)) — the product and
> revenue layer on top of the `mena-research-agent/` scaffold in this repo.
> Read alongside [AGENT_PRINCIPLES.md](../AGENT_PRINCIPLES.md),
> [framework-alignment.md](../framework-alignment.md), and
> [OPERATIONS.md](../OPERATIONS.md).

## Vision

A weekly bilingual (Arabic + English) research brief on humanitarian and
development data in the MENA region — covering what English-only research
misses because the primary sources are Arabic. Free newsletter on top,
paid custom research underneath. Humaniti is client zero.

## Financial outcome

- **Primary:** custom research reports for NGOs/think tanks/grant writers,
  $500–2,000 CAD per report.
- **Secondary:** sponsorships once newsletter > 1,000 subscribers.
- **Loop closes when:** first paid external report delivered.
- **Kill criterion:** no paid inquiry after 12 published briefs.

## System architecture (four layers)

- **Abstraction:** search providers, LLM tiers, and newsletter platform
  (Buttondown/Substack) each behind an adapter; the report pipeline never
  imports a vendor SDK directly.
- **Isolation:** each brief is a fresh pipeline run; corpus of past briefs +
  source maps is versioned in git; a bad run can't pollute the corpus
  (merges happen only after validation).
- **Validation:** citation discipline from the scaffold (no uncited claims);
  language-coverage gate (≥40% Arabic sources or the brief carries a
  visible "AR coverage thin" banner); human review of every brief before
  send for the first 12 issues.
- **Infrastructure capacity:** per-brief budgets (max sources, max LLM spend,
  max runtime); weekly cadence sized to ~3 hrs human review max.

## Ecosystem map (initial)

- **Scale:** 1 brief/week, 1 topic/brief, ~25 sources/brief. 10x = topic
  verticals (water, displacement, food security) each with own source maps.
- **Time:** research Mon–Wed, review Thu, publish Fri. Custom reports: 2-week
  turnaround SLA.
- **Causality hypothesis:** organizations pay because Arabic-source coverage
  materially changes conclusions (test: each brief highlights ≥1 finding
  absent from English coverage — the "AR delta" box).
- **Fan-in:** all sources → synthesis (max validation). **Fan-out:** brief →
  subscribers → forwards into NGO Slacks (instrument link clicks).
- **Emergence:** readers will request topics — topic requests are the
  cheapest demand signal for paid work; capture them in a public board.
- **Incentives:** readers get unavailable-elsewhere findings; contributors
  (later) get bylines; Humaniti gets mission-aligned research; operator
  gets paid pipeline.
- **Capacity:** human review is the bottleneck early; source-map skills
  reduce per-brief research time — measure hrs/brief weekly, target ↓30%
  by brief 12.
- **Feedback loops:** (1) every brief adds/updates a country source-map
  skill (the compounding moat); (2) reader replies → topic backlog;
  (3) AR-delta tracking → proof library for sales.
- **Bottleneck #1:** trust. Mitigate with methodology page, full source
  lists, and corrections policy from issue 1.

## Communication loops

- Agent → operator: draft brief + confidence notes Thursday.
- Operator → audience: Friday newsletter with AR-delta box and
  language-coverage footer.
- Audience → pipeline: reply-to topic requests; public topic board.
- Open-source loop: framework repo public; country source packs accepted
  via PR (contributor guide + review checklist required in Phase 4).

## Engineering fundamentals (project-specific)

- Security: no scraping behind paywalls; respect robots.txt; subscriber
  list is PII.
- Code health: the brief pipeline and the scaffold share one codebase —
  no fork drift.
- Release hygiene: a brief is a release; tag it; corrections get a
  changelog entry in the next issue.

## Operations alignment (OPERATIONS.md governs)

- **Action output:** forced-choice only (Rule 1) — schema in framework-alignment.md.
- **Measure row = AOR** logged to `metrics/loop_closure.csv` (Rule 4).
- **Coordination:** single agent + citation schema + operator review. No multi-agent.
- Session hygiene: `reentry.md` on every stop (Rule 2); WIP cap (Rule 3) and
  meta-work quarantine (Rule 5) apply.

## Phases

- **Phase 1 — Smallest closed loop.** Pipeline produces brief #1 on a
  Humaniti-relevant topic; you review; publish to a 10-person list; collect
  ≥3 replies. Source-map skill for that country committed.
- **Phase 2 — Cadence + compounding.** 4 weekly briefs; source-map skills
  for 3 countries; hrs/brief tracked; AR-delta box standard.
- **Phase 3 — Monetization rail.** "Commission research" page, intake form,
  rate card, 2-week SLA; first proposal sent.
- **Phase 4 — Community.** Open-source the framework; contributor guide;
  first external source-pack PR merged.

## Out of scope (until first paid report)

Multi-language UI, Urdu track, automated publishing without human review,
podcasts/video.
