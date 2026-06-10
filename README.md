# Dynamic Reader

**Mission:** empower access to knowledge — books, research, scholars, and primary
sources — to help build understanding of science, nature, and the world, and to
support a more sustainable and equitable society.

**Current direction:** the project is now agent-first. The active workstream is the
**[MENA Research Agent](mena-research-agent/)** — a bilingual (Arabic + English) deep
research agent for humanitarian data, built on Claude. It plans in English, searches
in both languages, reads Arabic sources natively, and produces cited reports. This
directly attacks the biggest gap we found in knowledge access: English-only research
systematically misses the Arabic-language record (government data, regional NGOs,
local journalism).

See [docs/ROADMAP.md](docs/ROADMAP.md) for planning and
[docs/AGENT_PRINCIPLES.md](docs/AGENT_PRINCIPLES.md) for how we build and validate.

## What's in this repo

| Path | Status | What it is |
|------|--------|------------|
| `mena-research-agent/` | **Active (Phase 1 — validation)** | Bilingual deep research agent. Start here. |
| `docs/` | Active | Agent principles (spec) and roadmap (planning). |
| `client/`, `server/` | On hold (Phase 0 scaffold) | Vite + React + Express boilerplate for the eventual reader UI. Hello-world only. |
| `gpt.py`, `summary_prompt.txt` | Legacy prototype | Early book-summary experiment (uses a deprecated OpenAI API; non-functional). |
| `wordpress_text.py` | Legacy prototype | WordPress content-fetch experiment. |

## Quick start (MENA Research Agent)

```bash
cd mena-research-agent
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add ANTHROPIC_API_KEY and TAVILY_API_KEY
python -m src.agent "Water access trends in Yemen 2020-2026"
```

Reports are written to `mena-research-agent/outputs/`. Full architecture and design
notes: [mena-research-agent/README.md](mena-research-agent/README.md).

## Quick start (web scaffold — on hold)

```bash
npm install && (cd client && npm install)
npm run watch   # terminal 1: compile server TS
npm run dev     # terminal 2: run server + client
```

## Roadmap (summary)

1. **Now — validate the research agent:** run it on real Humaniti-style questions,
   capture feedback, score citation accuracy. Kill or iterate per the
   [phase model](docs/AGENT_PRINCIPLES.md#1-operating-model-validation-before-optimization).
2. **Next:** eval harness, local-document hybrid search, MCP wrapper so the agent is
   callable from other tools.
3. **Later:** resurrect the reader UI as a front end over validated agent
   capabilities (dynamic reading, summaries, knowledge discovery), then scale/harden.

Details in [docs/ROADMAP.md](docs/ROADMAP.md).

## Contributing

Closed for now. All changes land via PR per
[docs/AGENT_PRINCIPLES.md](docs/AGENT_PRINCIPLES.md); see also
[CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Authors

* **Shuaib Reeyaz** — *Initial work* — [shuaibr](https://github.com/shuaibr)

## License

See [LICENSE](LICENSE) for details.
