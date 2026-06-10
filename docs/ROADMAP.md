# Roadmap & Planning

**Status:** living document — updated when a go/no-go decision is made
**Phase model:** see [AGENT_PRINCIPLES.md §1](AGENT_PRINCIPLES.md#1-operating-model-validation-before-optimization)

## Direction (June 2026)

The project has pivoted from "build a reading platform first" to **agent-first**:
prove value with a working research agent, then grow product surface around what's
validated. The active bet is the **MENA Research Agent** — bilingual (AR/EN) deep
research for humanitarian topics, where English-only tooling demonstrably
under-serves the Arabic-language record.

Rationale, mapped to our ecosystem lenses:

- **Bottleneck:** knowledge access in MENA contexts is gated on Arabic sources that
  English-only research never surfaces. Fixing retrieval beats polishing UI.
- **Time:** an agent CLI delivers end-to-end value in days; the full reader platform
  is months. Shortest loop to real user feedback wins.
- **Feedback loops:** every generated report carries a language-coverage footer and
  citations — built-in, measurable validation signals.
- **Capacity:** tiered models (Fable orchestrates, Haiku does bulk work) keep token
  spend matched to task value.

## Workstreams

### 1. MENA Research Agent — Phase 1 (validation) — ACTIVE

Exit criteria (per principles §1): demoed end-to-end to a real stakeholder, at least
one captured feedback signal, happy path automated, go/no-go recorded here.

- [x] Working end-to-end pipeline: plan → bilingual query expansion → search →
      per-source claim extraction → gap assessment loop → cited report
- [x] Skills for Arabic source evaluation and Humaniti report format
- [x] Smoke test for query expansion (gated on API key)
- [x] Config honesty pass: Arabic floor (`min_arabic_share`) enforced in gap
      assessment, `max_sources` cap + URL dedup enforced in the run loop,
      unused `compressor` tier and `claude-agent-sdk` dependency removed
- [x] Run survivability: API retries with backoff, per-round findings
      checkpoint, robust planner JSON parsing, whole-finding truncation,
      token-usage printout per run
- [ ] Run on 3–5 real Humaniti-style research questions; save outputs +
      reviewer notes + token cost per run
- [ ] Capture stakeholder feedback (program lead / grant writer review of one report)
- [ ] Wire a free offline test into CI (live smoke test stays manual, pre-session)
- [ ] **Go/no-go decision:** _pending_

### 2. Agent hardening & extension — Phase 2 (blocked on go decision)

- [ ] Eval harness: 10 fixed questions, score citation accuracy per run
- [ ] Prompt-injection hardening before the agent becomes callable by other
      systems (MCP wrapper raises the blast radius)
- [ ] Local document hybrid search (Humaniti internal docs + web)
- [ ] MCP server wrapper so the agent is callable from Claude Code / other hosts
- [ ] Urdu query expansion as a third language track
- [ ] Migrate orchestrator loop to the Claude Agent SDK `query()` loop
      (hooks/tools/MCP) — agent.py is structured for this lift

### 3. Reader platform (client/ + server/) — Phase 0 — ON HOLD

The MERN scaffold stays as-is until an agent capability is validated and needs a UI.
Original feature ideas (preserved for when this resumes):

- Aggregating books, resources, and key pioneers across industries
- Dynamic reading system that simplifies complex ideas for the reader
- Intelligent testing / knowledge-discovery for frictionless learning
- Smart communities connecting learners with leaders across fields

When resumed, this workstream restarts at Phase 0 entry with its own validation plan.

### 4. Legacy prototypes — RESOLVED (June 2026: deleted)

- `gpt.py` + `summary_prompt.txt`: book-summary experiment on a sunset OpenAI
  API — deleted; the summary idea returns as an agent skill if/when the reader
  platform resumes.
- `wordpress_text.py`: WordPress fetch experiment — deleted; the internal-docs
  ingestion idea is tracked as local document hybrid search (workstream 2).
- All remain recoverable from git history.

## Repo-level engineering debt (from principles review)

- [ ] Enable branch protection on `main` and GitHub secret scanning + push protection
- [ ] Commit lockfiles (`package-lock.json` is currently gitignored — breaks
      reproducible builds and `npm audit`)
- [ ] Minimal CI: lint + the agent smoke test on every push
