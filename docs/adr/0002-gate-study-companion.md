# ADR 0002 — Study Companion is a gated workstream, not a product merge

**Context:** The sufi-text-companion spec shares mission and an Arabic-first core
with the MENA Research Agent, but has a different customer, revenue loop, cadence,
bottleneck (scholar review vs. search coverage), and kill criterion.
**Decision:** Same repo, separate workstream — gated on the agent's Phase-1 "go",
with its own validation loop and kill criterion. Shared Arabic core is extracted
only when both consumers exist. The agent serves the companion as its
corpus/provenance research tool starting now (one validation question).
