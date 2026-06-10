"""Offline tests — no API key or network required. These run in CI.

The live smoke test (test_query_expansion.py) stays manual: run it with a
real ANTHROPIC_API_KEY before each validation session.
"""
from src.query_expansion import expand_queries
from src.synthesis.report import write_report


class _Block:
    type = "text"

    def __init__(self, text):
        self.text = text


class _Resp:
    def __init__(self, text):
        self.content = [_Block(text)]


class StubClient:
    """Mimics the one Anthropic call shape the modules use."""

    def __init__(self, text):
        self._text = text

    @property
    def messages(self):
        return self

    def create(self, **kwargs):
        return _Resp(self._text)


CONFIG = {
    "models": {"orchestrator": "stub-model", "worker": "stub-model"},
    "research": {"queries_per_round": 2},
}


def test_expand_queries_returns_both_language_tracks():
    stub = StubClient(
        '```json\n{"en": ["yemen water access"], "ar": ["المياه في اليمن"]}\n```'
    )
    pairs = expand_queries("water access in Yemen", stub, CONFIG)
    assert ("yemen water access", "en") in pairs
    assert ("المياه في اليمن", "ar") in pairs


def test_expand_queries_falls_back_to_english_on_bad_json():
    pairs = expand_queries("water access in Yemen", StubClient("not json"), CONFIG)
    assert pairs == [("water access in Yemen", "en")]


def test_write_report_dedupes_sources_and_appends_coverage_footer(tmp_path):
    findings = [
        {"url": "https://a.example/ar", "lang": "ar",
         "claims": [{"claim": "x", "confidence": "high"}]},
        {"url": "https://a.example/ar", "lang": "ar",          # duplicate URL
         "claims": [{"claim": "y", "confidence": "low"}]},
        {"url": "https://b.example/en", "lang": "en",
         "claims": [{"claim": "z", "confidence": "medium"}]},
        {"url": "https://c.example/en", "lang": "en", "claims": []},  # no claims
    ]
    config = {
        "models": {"orchestrator": "stub-model"},
        "report": {"output_dir": str(tmp_path),
                   "include_language_coverage_footer": True},
    }
    path = write_report("Topic X", findings, StubClient("# Report body"), config)
    text = path.read_text(encoding="utf-8")
    assert "# Report body" in text
    assert "1 Arabic source(s), 1 English source(s), 2 total" in text
    assert path.parent == tmp_path
