# Phase-1 Validation Run Set

Five questions, run once each. Q5 doubles as the Study Companion's
(workstream 5) provenance legwork and stress-tests the Arabic floor on
classical-scholarship topics.

## Before the session

```bash
cd mena-research-agent
source .venv/bin/activate
pytest tests/test_query_expansion.py -x   # live smoke test, needs API keys
```

## The questions

1. Water access trends in Yemen 2020-2026
2. Food insecurity and IPC classification trends in Sudan since the 2023 conflict
3. Education access for displaced children in Gaza and the West Bank, 2023-2026
4. Cholera outbreak response capacity in Lebanon and Syria, 2022-2026
5. Provenance, manuscript and edition history, and copyright status of
   al-Hikam al-'Ata'iyya by Ibn 'Ata' Allah al-Iskandari, including major
   published editions and any public-domain translations

Run each with:

```bash
python -m src.agent "<question>"
```

## After each run — record in `validation/runs/<n>-log.md`

Copy this template (the report itself stays in `outputs/`; commit both):

```markdown
# Run <n>: <question>
- Date / runtime:
- Tokens: <orchestrator in/out>, <worker in/out>   (printed at end of run)
- Language coverage: <AR> Arabic / <EN> English    (from report footer)
- Citation spot-check: pick 5 claims at random, open each cited source —
  <n>/5 verified
- Arabic floor: did rounds trigger on low AR share? worked / didn't / n-a
- Reviewer notes (what's wrong, missing, or surprising):
- Verdict for this run: useful as-is / useful with edits / not useful
```

## Closing the phase

After all five runs plus one external review (program lead or grant writer
reads one report), record the go/no-go in `docs/ROADMAP.md` workstream 1
with a one-line rationale. A "go" opens workstream 5.
