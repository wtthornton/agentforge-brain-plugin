# agentforge-brain-plugin

TAP-763 — Wave B test rig for the tapps-brain save/recall round-trip.

Requires a live tapps-brain HTTP sidecar. Zero-brain unit tests live in
`tests/test_runner.py` and run anywhere. The full smoke tests live in
`backend/tests/test_brain_smoke.py` inside the AgentForge repo and are
skipped automatically unless `TAPPS_BRAIN_HTTP_URL` is set.

## Structure

```
agentforge_brain_test/
  __init__.py          # __version__ = "1.0.0"
  plugin.json          # AgentForge plugin manifest
  plugin.py            # register(app) entry point
  routes.py            # GET /api/brain-test/status, POST /api/brain-test/roundtrip
  agents/
    brain_test_agent/
      AGENT.md         # memory_profile: full
      runner.py        # BrainTestRunner.run() -> "brain:ok"
tests/
  test_runner.py       # unit tests (no live brain needed)
```

## Running the unit tests

```bash
cd /home/wtthornton/code/agentforge-brain-plugin
uv run pytest tests/
```

## Running the smoke tests (live sidecar)

```bash
cd /home/wtthornton/code/AgentForge
export TAPPS_BRAIN_HTTP_URL=http://localhost:8080
export TAPPS_BRAIN_AUTH_TOKEN=<token>
uv run pytest backend/tests/test_brain_smoke.py -v
```

## Installing into AgentForge

```bash
cd /home/wtthornton/code/AgentForge
uv pip install -e /home/wtthornton/code/agentforge-brain-plugin
```

## Key design notes

- `BrainBridge.save_fact(category, fact, *, tier)` — `category` is the first
  positional arg, `fact` is the second. The tagged value written to the brain
  is `"[{category}] {fact}"`.
- `recall_for_prompt(query, threshold=0.1)` returns `str | None`. A `None`
  result means no matching memories were found above the threshold.
- The plugin routes use `request.app.state.brain` (a `BrainBridge`) directly.
  No `BrainPool` dependency — the smoke app fixture wires one in.
