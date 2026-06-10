# ADR 0001 — One principles document

**Context:** An external GSD-style PRINCIPLES.md (spec pack) overlapped heavily with
docs/AGENT_PRINCIPLES.md; two principle files would compete as sources of truth.
**Decision:** AGENT_PRINCIPLES.md is the single principles doc. The stricter
enforcement rules worth keeping (closed-loop requirement, 5-line ADRs, budgets
enforced in config with 80% alerts, heartbeat alerts, model-tiering-in-config)
were folded into it; the external file is not committed.
