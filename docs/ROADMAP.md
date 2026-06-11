# Roadmap & Planning

**Status:** living document — updated when a go/no-go decision is made
**Phase model:** see [AGENT_PRINCIPLES.md §1](AGENT_PRINCIPLES.md#1-operating-model-validation-before-optimization)
**Portfolio governance:** [OPERATIONS.md](OPERATIONS.md) is binding (June 2026)

## Portfolio context

This repo hosts **two of the six portfolio projects**: **mena**
(workstreams 1–2 — agent scaffold + briefs/paid-research product, spec:
[specs/mena-briefs-SPEC.md](specs/mena-briefs-SPEC.md),
[framework-alignment.md](framework-alignment.md)) and **maruf**
(workstream 5 — spec: [specs/maruf-SPEC.md](specs/maruf-SPEC.md)).

Operating rules that bind work here (see OPERATIONS.md for the full set):

- **WIP cap = 1 across the portfolio; current Active: flow.** This repo is
  *Passive* until rotation: automated runs, critical isolated bugfixes, and
  completing the already-committed validation milestone only. New feature
  work waits for the Active slot.
- **Forced-choice outputs (Rule 1):** agent recommendations arrive as binary
  choices with a one-line reason (mena brief sections: `PUBLISH / EDIT / CUT`),
  never open-ended reports as the action interface. Vetoes append to `docs/codex.md`.
- **AOR (Rule 4):** % of recommendations acted on within 48h, logged to
  `metrics/loop_closure.csv`; < 50% over 2 weeks → demote to digest or mute.
- **R2R (Rule 2):** every session close writes `reentry.md` at repo root.
- **Single agent + schema + operator veto** — no multi-agent on this repo's
  sequential pipelines (adversarial two-agent review is scoped to scout only).
- **External validation only:** clean runs and friendly feedback don't count;
  validation = a stranger subscribes, pays, or describes the problem unprompted.

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

### 1. mena: Research Agent — Phase 1 (technical validation)

**Product layer (per [specs/mena-briefs-SPEC.md](specs/mena-briefs-SPEC.md)):**
weekly bilingual brief + paid custom research, Humaniti as client zero.
Loop closes on the **first paid external report** ($500–2,000 CAD); kill
criterion: **no paid inquiry after 12 published briefs**. The smallest closed
loop after technical validation: brief #1 to a 10-person list, ≥3 replies,
country source-map skill committed.

Technical-validation exit criteria (per principles §1): demoed end-to-end to a real
stakeholder, at least one captured feedback signal, happy path automated, go/no-go
recorded here. Note: per OPERATIONS.md these runs complete an already-committed
milestone and are allowed while the repo is Passive.

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
      reviewer notes + token cost per run. Question set + run-log protocol:
      [mena-research-agent/validation/QUESTIONS.md](../mena-research-agent/validation/QUESTIONS.md)
      (Q5 is the Study Companion provenance question)
- [ ] Capture stakeholder feedback (program lead / grant writer review of one report)
- [x] Wire a free offline test into CI (3 stub-client tests in
      `tests/test_offline.py`, run by `.github/workflows/ci.yml`; live smoke
      test stays manual, pre-session)
- [ ] **Go/no-go decision:** _pending_

### 2. mena: briefs product + hardening — Phase 2 (blocked on go decision + Active slot)

From [framework-alignment.md](framework-alignment.md) §3 and the mena spec:

- [ ] Enforce §3 budgets in code: ≤45 min/run, ≤$5 CAD/brief, warn at 80%
      (config keys exist for sources/rounds; $ and runtime are not yet enforced)
- [ ] 20-claim golden set gating citation accuracy before any pipeline change
- [ ] Brief pipeline on the scaffold (no fork drift): AR-delta box,
      language-coverage gate banner, `PUBLISH / EDIT / CUT` per section
- [ ] Adapters dir (`src/adapters/`): search, LLM, newsletter behind one file each
- [ ] Ingest `research/inbox/<topic>/` dossiers as cited sources (tagged `gemini-dossier`)
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

### 5. maruf: Classical Text Study Companion — GATED (opens on workstream 1 "go" + Active slot)

Spec: [specs/maruf-SPEC.md](specs/maruf-SPEC.md) (v2, supersedes the
sufi-text-companion spec; adds OPERATIONS alignment — forced-choice reviewer
schema `ACCEPT FIX / REJECT / ESCALATE TO SCHOLAR`, AOR logging).
A study companion for classical Islamic texts: public-domain Arabic texts with
vocabulary support, three-state annotations (machine-draft → community-reviewed →
scholar-verified), and study-circle tools. Community corrections improve the corpus
that teaches the next students. This is the truest descendant of the original
Dynamic Reader vision.

**Gate:** workstream 1's go/no-go must be recorded as "go" before any companion
code is written. One operator means one Phase-1 validation at a time — running two
halves the signal quality of both. The only pre-gate activity is the provenance
research question folded into workstream 1's validation runs (free, and serves both).

**On opening, in order:**

- [ ] Extract the shared Arabic core (MSA query phrasing, source-evaluation skill,
      Unicode/diacritics normalization) into one library consumed by both the
      research agent and the companion — extract at two consumers, not before
- [ ] Phase 1 per the spec's smallest closed loop: one short public-domain text,
      machine glosses, weekly portion email to the operator's own study circle,
      flag-a-gloss form, manual weekly corpus update; run for 4 circle sessions
- [ ] Non-deferrable floors from day one: provenance doc per text, machine-assisted
      labels with "not a fatwa / ask your teacher" notice, sensitive topics routed
      to human review
- [ ] **Kill criterion (record outcome here):** weekly active study sessions < 20
      after 3 months
- [ ] Loop-closes target: 25 paying subscribers or first institutional pilot

### Workstream interaction rule

Workstreams 1 and 5 share infrastructure (Arabic core, model tiering, principles)
but never share a validation loop, kill criterion, or go/no-go decision. The
research agent additionally serves workstream 5 as its corpus-building tool
(provenance research, discussion-prompt background briefs).

## Repo-level engineering debt (from principles review)

- [ ] Enable branch protection on `main` and GitHub secret scanning + push protection
- [ ] Commit lockfiles (`package-lock.json` is currently gitignored — breaks
      reproducible builds and `npm audit`)
- [x] Minimal CI: compile check + offline agent tests on every push/PR
      (`.github/workflows/ci.yml`); add a linter (ruff) when code churn warrants it
