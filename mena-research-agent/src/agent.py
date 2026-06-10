"""MENA Research Agent — orchestrator entry point.

Usage:
    python -m src.agent "Water access trends in Yemen 2020-2026"

Flow:
    1. Fable plans the research and produces sub-questions.
    2. query_expansion turns each sub-question into parallel AR + EN queries.
    3. Haiku workers search and summarize each source (with citations).
    4. Fable assesses coverage gaps — including whether the Arabic share is
       below the configured floor; loops up to max_search_rounds.
    5. Fable writes the final cited report to outputs/.

Findings are checkpointed to outputs/checkpoint.json after every round so a
crashed run loses at most one round of work.

NOTE: This file uses the raw Anthropic SDK for the worker calls and is
structured so you can lift the orchestrator into the Claude Agent SDK's
`query()` loop once you want hooks/tools/MCP. Verify current SDK usage at
https://docs.claude.com/en/api/agent-sdk/overview before extending.
"""
from __future__ import annotations

import json
import sys
import time
from collections import defaultdict
from pathlib import Path

import anthropic
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

USAGE: dict[str, dict[str, int]] = defaultdict(lambda: {"in": 0, "out": 0})


def parse_json(raw: str):
    return json.loads(raw.strip().removeprefix("```json").removesuffix("```"))


def ask(model: str, system: str, user: str, max_tokens: int = 2000) -> str:
    for attempt in range(4):
        try:
            resp = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system,
                messages=[{"role": "user", "content": user}],
            )
            break
        except anthropic.APIError as e:
            if attempt == 3:
                raise
            wait = 2 ** (attempt + 1)
            print(f"  ! {e.__class__.__name__}, retrying in {wait}s")
            time.sleep(wait)
    USAGE[model]["in"] += resp.usage.input_tokens
    USAGE[model]["out"] += resp.usage.output_tokens
    return "".join(b.text for b in resp.content if b.type == "text")


def plan(topic: str) -> list[str]:
    """Fable decomposes the topic into 3-5 sub-questions."""
    for _ in range(2):
        raw = ask(
            CONFIG["models"]["orchestrator"],
            ORCHESTRATOR_PROMPT + "\n\n" + SKILLS,
            f"Topic: {topic}\n\nReturn ONLY a JSON array of 3-5 research "
            f"sub-questions in English. No prose.",
        )
        try:
            return parse_json(raw)
        except json.JSONDecodeError:
            continue
    sys.exit("Planner did not return valid JSON after two attempts; "
             "try rephrasing the topic.")


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
        data = parse_json(raw)
    except json.JSONDecodeError:
        data = {"claims": []}
    return {"url": url, "lang": lang, **data}


def assess_gaps(topic: str, findings: list[dict]) -> list[str]:
    """Fable reviews findings, returns follow-up sub-questions ([] = done).

    Coverage below the configured Arabic floor is surfaced as a gap so the
    agent cannot quietly degrade into an English-only tool.
    """
    ar = sum(1 for f in findings if f["lang"] == "ar" and f.get("claims"))
    en = sum(1 for f in findings if f["lang"] == "en" and f.get("claims"))
    min_ar = CONFIG["research"]["min_arabic_share"]

    # Trim by dropping whole findings, never by slicing JSON mid-string.
    trimmed, size = [], 0
    for f in findings:
        chunk = len(json.dumps(f, ensure_ascii=False))
        if size + chunk > 20000:
            break
        trimmed.append(f)
        size += chunk

    raw = ask(
        CONFIG["models"]["orchestrator"],
        ORCHESTRATOR_PROMPT,
        f"Topic: {topic}\n"
        f"Source language coverage: {ar} Arabic, {en} English. "
        f"Minimum Arabic share target: {min_ar:.0%}. If Arabic coverage is "
        f"below target and Arabic sources plausibly exist, that is a gap.\n"
        f"Findings so far:\n{json.dumps(trimmed, ensure_ascii=False)}\n\n"
        "What important gaps remain? Return ONLY a JSON array of follow-up "
        "sub-questions (empty array if coverage is sufficient).",
    )
    try:
        return parse_json(raw)
    except json.JSONDecodeError:
        return []


def run(topic: str) -> Path:
    findings: list[dict] = []
    seen_urls: set[str] = set()
    max_sources = CONFIG["research"]["max_sources"]
    out_dir = Path(CONFIG["report"]["output_dir"])
    out_dir.mkdir(exist_ok=True)
    checkpoint = out_dir / "checkpoint.json"

    questions = plan(topic)

    for round_n in range(CONFIG["research"]["max_search_rounds"]):
        print(f"\n— Round {round_n + 1}: {len(questions)} sub-questions")
        for q in questions:
            for query, lang in expand_queries(q, client, CONFIG):
                for hit in search_web(query, CONFIG):
                    if hit["url"] in seen_urls or len(seen_urls) >= max_sources:
                        continue
                    seen_urls.add(hit["url"])
                    findings.append(
                        summarize_source(hit["url"], hit["content"], lang)
                    )
        checkpoint.write_text(
            json.dumps(findings, ensure_ascii=False, indent=1),
            encoding="utf-8",
        )
        if len(seen_urls) >= max_sources:
            print(f"— Source cap reached ({max_sources}); writing report")
            break
        questions = assess_gaps(topic, findings)
        if not questions:
            break

    for model, u in USAGE.items():
        print(f"— Tokens [{model}]: {u['in']:,} in / {u['out']:,} out")

    return write_report(topic, findings, client, CONFIG)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('Usage: python -m src.agent "<research topic>"')
    path = run(sys.argv[1])
    print(f"\nReport written to {path}")
