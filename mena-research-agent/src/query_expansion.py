"""Turn one English sub-question into parallel Arabic + English search queries.

This is the heart of the MENA-gap fix: every sub-question is searched in
both languages, with Arabic queries written the way Arabic sources actually
phrase the topic (not literal translations).
"""
from __future__ import annotations

import json


def expand_queries(sub_question: str, client, config) -> list[tuple[str, str]]:
    """Returns a list of (query, lang) tuples, lang in {"ar", "en"}."""
    n = config["research"]["queries_per_round"]
    raw_resp = client.messages.create(
        model=config["models"]["worker"],
        max_tokens=800,
        system=(
            "You are a bilingual search strategist. Given a research "
            "sub-question, produce search queries in BOTH English and "
            "Modern Standard Arabic. Arabic queries must use the natural "
            "phrasing Arabic media, government portals, and NGOs would use "
            "— not word-for-word translation. Prefer terms that surface "
            "primary sources (تقرير, إحصائيات, وزارة, الأمم المتحدة).\n"
            'Respond ONLY with JSON: {"en": [..], "ar": [..]}'
        ),
        messages=[{
            "role": "user",
            "content": f"Sub-question: {sub_question}\n"
                       f"Give {n} queries per language, 2-6 words each.",
        }],
    )
    text = "".join(b.text for b in raw_resp.content if b.type == "text")
    try:
        data = json.loads(text.strip().removeprefix("```json").removesuffix("```"))
    except json.JSONDecodeError:
        return [(sub_question, "en")]  # graceful fallback

    pairs = [(q, "en") for q in data.get("en", [])]
    pairs += [(q, "ar") for q in data.get("ar", [])]
    return pairs
