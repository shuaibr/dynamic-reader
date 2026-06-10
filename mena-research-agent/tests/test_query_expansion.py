"""Smoke test: query expansion returns both language tracks.
Run with a live API key: pytest tests/ -x
"""
import os
import pytest


@pytest.mark.skipif(not os.environ.get("ANTHROPIC_API_KEY"), reason="needs API key")
def test_expand_returns_both_languages():
    import yaml
    from anthropic import Anthropic
    from src.query_expansion import expand_queries

    config = yaml.safe_load(open("config.yaml"))
    pairs = expand_queries("water access in Yemen since 2020", Anthropic(), config)
    langs = {lang for _, lang in pairs}
    assert "en" in langs and "ar" in langs
