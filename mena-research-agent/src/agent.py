"""MENA Research Agent — orchestrator entry point.

Usage:
    python -m src.agent "Water access trends in Yemen 2020-2026"

Flow:
    1. Fable plans the research and produces sub-questions.
    2. query_expansion turns each sub-question into parallel AR + EN queries.
    3. Haiku workers search and summarize each source (with citations).
    4. Fable assesses coverage gaps; loops up to max_search_rounds.
    5. Fable writes the final cited report to outputs/.

NOTE: This file uses the raw Anthropic SDK for the worker calls and is
structured so you can lift the orchestrator into the Claude Agent SDK's
`query()` loop once you want hooks/tools/MCP. Verify current SDK usage at
https://docs.claude.com/en/api/agent-sdk/overview before extending.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from anthropic import Anthropic
from dotenv import load_dotenv

from src.query_expansion import expand_queries
from src.search.web import search_web
from src.synthesis.report import write_report

load_dotenv()
CONFIG = yaml.safe_load(Path("config.yaml").read_text())
client = Anthropic()

ORCHESTRATOR_PROMPT = Path("prompts/orchestrator.md").read_text()
SKILLS = "\n\n".join(
    p.read_text() for p in Path("skills").glob("*/SKILL.md")
)


def ask(model: str, system: str, user: str, max_tokens: int = 2000) -> str:
    resp = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return "".join(b.text for b in resp.content if b.type == "text")


def plan(topic: str) -> list[str]:
    """Fable decomposes the topic into 3-5 sub-questions."""
    raw = ask(
        CONFIG["models"]["orchestrator"],
        ORCHESTRATOR_PROMPT + "\n\n" + SKILLS,
        f"Topic: {topic}\n\nReturn ONLY a JSON array of 3-5 research "
        f"sub-questions in English. No prose.",
    )
    return json.loads(raw.strip().removeprefix("```json").removesuffix("```"))


def summarize_source(url: str, content: str, lang: str) -> dict:
    """Haiku worker: compress one source into cited claims."""
    raw = ask(
        CONFIG["models"]["worker"],
        "You extract factual claims from sources. Respond ONLY with JSON: "
        '{"claims": [{"claim": str, "confidence": "high|medium|low"}]}. '
        "If the source is Arabic, translate claims to English but keep "
        "key terms in Arabic in parentheses.",
        f"URL: {url}\nLanguage: {lang}\n\n{content[:8000]}",
        max_tokens=1000,
    )
    try:
        data = json.loads(raw.strip().removeprefix("```json").removesuffix("```"))
    except json.JSONDecodeError:
        data = {"claims": []}
    return {"url": url, "lang": lang, **data}


def assess_gaps(topic: str, findings: list[dict]) -> list[str]:
    """Fable reviews findings, returns follow-up sub-questions ([] = done)."""
    raw = ask(
        CONFIG["models"]["orchestrator"],
        ORCHESTRATOR_PROMPT,
        f"Topic: {topic}\nFindings so far:\n{json.dumps(findings)[:20000]}\n\n"
        "What important gaps remain? Return ONLY a JSON array of follow-up "
        "sub-questions (empty array if coverage is sufficient).",
    )
    try:
        return json.loads(raw.strip().removeprefix("```json").removesuffix("```"))
    except json.JSONDecodeError:
        return []


def run(topic: str) -> Path:
    findings: list[dict] = []
    questions = plan(topic)

    for round_n in range(CONFIG["research"]["max_search_rounds"]):
        print(f"\n— Round {round_n + 1}: {len(questions)} sub-questions")
        for q in questions:
            for query, lang in expand_queries(q, client, CONFIG):
                for hit in search_web(query, CONFIG):
                    findings.append(
                        summarize_source(hit["url"], hit["content"], lang)
                    )
        questions = assess_gaps(topic, findings)
        if not questions:
            break

    return write_report(topic, findings, client, CONFIG)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('Usage: python -m src.agent "<research topic>"')
    path = run(sys.argv[1])
    print(f"\nReport written to {path}")
