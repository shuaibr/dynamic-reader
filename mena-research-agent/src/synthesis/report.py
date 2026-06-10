"""Assemble the final cited report. Fable writes it; this module enforces
citation discipline and appends the language-coverage footer.
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path


def write_report(topic: str, findings: list[dict], client, config) -> Path:
    # Deduplicate sources and assign stable citation IDs
    sources, seen = [], set()
    for f in findings:
        if f["url"] not in seen and f.get("claims"):
            seen.add(f["url"])
            sources.append(f)

    numbered = [
        {"id": i + 1, "url": s["url"], "lang": s["lang"], "claims": s["claims"]}
        for i, s in enumerate(sources)
    ]

    resp = client.messages.create(
        model=config["models"]["orchestrator"],
        max_tokens=4000,
        system=(
            "You write rigorous humanitarian research reports in Markdown. "
            "RULES: Every factual claim must carry an inline citation [n] "
            "matching the provided source IDs. Never state a fact without "
            "a citation. Flag contradictions between sources explicitly. "
            "Structure: Executive Summary, Key Findings, Analysis, "
            "Limitations, Sources."
        ),
        messages=[{
            "role": "user",
            "content": f"Topic: {topic}\n\nSources and extracted claims:\n"
                       f"{json.dumps(numbered, ensure_ascii=False)[:60000]}",
        }],
    )
    body = "".join(b.text for b in resp.content if b.type == "text")

    if config["report"]["include_language_coverage_footer"]:
        ar = sum(1 for s in numbered if s["lang"] == "ar")
        en = sum(1 for s in numbered if s["lang"] == "en")
        body += (
            f"\n\n---\n*Language coverage: {ar} Arabic source(s), "
            f"{en} English source(s), {len(numbered)} total.*\n"
        )

    out_dir = Path(config["report"]["output_dir"])
    out_dir.mkdir(exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")[:60]
    path = out_dir / f"{date.today().isoformat()}-{slug}.md"
    path.write_text(body, encoding="utf-8")
    return path
