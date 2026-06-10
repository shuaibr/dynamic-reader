# MENA Research Agent

A bilingual (Arabic + English) deep research agent built on **Claude**.
Designed for humanitarian data research: it plans in English, searches in *both*
languages, reads Arabic sources natively, and synthesizes a cited report.
(It currently uses the raw Anthropic SDK; the orchestrator loop is structured
for a later lift into the Claude Agent SDK — see the roadmap.)

## Why this architecture

Most deep-research agents only query in English, which systematically misses
Arabic-language sources (govt portals, regional NGOs, Arabic press). This agent
fixes that with a **query-expansion layer** that generates parallel Arabic and
English search queries, and a **tiered model strategy**:

| Role | Model | Why |
|---|---|---|
| Orchestrator / planner / final synthesis | `claude-fable-5` | Best reasoning, long-horizon planning |
| Bulk retrieval, summarizing each source | `claude-haiku-4-5-20251001` | Cheap + fast for high-volume work |

The orchestrator's gap assessment enforces a configurable **minimum Arabic
share** (`min_arabic_share` in `config.yaml`): if Arabic coverage falls below
the floor, that is treated as a research gap and triggers another round
targeting Arabic sources — the agent cannot quietly degrade into an
English-only tool.

```
                 ┌──────────────────────────┐
                 │  Orchestrator (Fable)    │
                 │  plan → delegate → judge │
                 └─────┬──────────┬─────────┘
            ┌──────────┘          └───────────┐
   ┌────────▼────────┐              ┌─────────▼────────┐
   │ EN search worker │              │ AR search worker │
   │ (Haiku)          │              │ (Haiku)          │
   └────────┬────────┘              └─────────┬────────┘
            │   per-source claims + citations │
            └──────────┐          ┌───────────┘
                 ┌─────▼──────────▼─────┐
                 │ Gap assessment (Fable)│  loops until covered (incl. AR floor)
                 └──────────┬───────────┘
                 ┌──────────▼───────────┐
                 │ Report writer (Fable)│  → outputs/report.md
                 └──────────────────────┘
```

## Repo layout

```
mena-research-agent/
├── README.md
├── requirements.txt
├── .env.example
├── config.yaml              # models, search depth, Arabic coverage floor
├── src/
│   ├── agent.py             # entry point — orchestrator loop
│   ├── query_expansion.py   # EN topic → parallel AR + EN search queries
│   ├── search/
│   │   └── web.py           # search provider wrapper (Tavily/Brave/etc.)
│   └── synthesis/
│       └── report.py        # citation-tracked report assembly
├── skills/
│   ├── arabic-research/SKILL.md    # how to search & evaluate Arabic sources
│   └── humaniti-report/SKILL.md    # Humaniti report format & tone
├── prompts/
│   └── orchestrator.md      # system prompt for the planner
├── tests/
│   └── test_query_expansion.py
└── outputs/                 # generated reports land here
```

## Quick start

```bash
git clone <your-fork-url> && cd mena-research-agent
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add ANTHROPIC_API_KEY (+ TAVILY_API_KEY or similar)
python -m src.agent "Water access trends in Yemen 2020-2026"
```

## Design decisions worth keeping when you extend this

1. **Skills over prompts.** The `skills/` folder is loaded into the
   orchestrator's context. When you find yourself repeating an instruction,
   move it into a SKILL.md instead of editing code.
2. **Every claim carries a source ID.** Workers return
   `{claim, source_url, lang, confidence}` tuples; the report writer refuses
   uncited claims. This matters for grant-grade Humaniti output.
3. **Language coverage is enforced, then reported.** Gap assessment treats
   Arabic coverage below `min_arabic_share` as a gap, and the final report
   includes a footer showing how many AR vs EN sources informed it — your
   built-in check that the MENA data gap is actually being addressed, not
   reproduced.

## Roadmap ideas

- [ ] Local document hybrid search (Humaniti internal docs + web)
- [ ] MCP server wrapper so this agent is callable from Claude Code / Cowork
- [ ] Urdu query expansion as a third language track
- [ ] Eval harness: 10 fixed questions, score citation accuracy per run

## Docs

- Agent SDK: https://docs.claude.com/en/api/agent-sdk/overview
- Skills: https://docs.claude.com/en/docs/agents-and-tools/agent-skills
