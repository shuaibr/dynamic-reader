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
- [ ] Run on 3–5 real Humaniti-style research questions; save outputs + reviewer notes
- [ ] Capture stakeholder feedback (program lead / grant writer review of one report)
- [ ] Implement or remove unused config: `language_weights`, `max_sources`,
      `compressor` model (config must not promise what code doesn't do)
- [ ] Wire the happy-path test into CI
- [ ] **Go/no-go decision:** _pending_

### 2. Agent hardening & extension — Phase 2 (blocked on go decision)

- [ ] Eval harness: 10 fixed questions, score citation accuracy per run
- [ ] Deduplicate search hits across queries before summarizing (token capacity)
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

### 4. Legacy prototypes — kill or fold in

- `gpt.py` + `summary_prompt.txt`: book-summary experiment on a sunset OpenAI API.
  Decision due: rewrite as an agent skill, or delete.
- `wordpress_text.py`: WordPress fetch experiment. Decision due: fold into local
  document search (workstream 2) or delete.

## Repo-level engineering debt (from principles review)

- [ ] Enable branch protection on `main` and GitHub secret scanning + push protection
- [ ] Commit lockfiles (`package-lock.json` is currently gitignored — breaks
      reproducible builds and `npm audit`)
- [ ] Minimal CI: lint + the agent smoke test on every push
