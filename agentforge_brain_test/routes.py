"""Routes for the brain-test plugin (TAP-763)."""

from fastapi import APIRouter, Request

from agentforge_brain_test import __version__

router = APIRouter(prefix="/api/brain-test", tags=["brain-test"])


@router.get("/status")
async def status() -> dict:
    return {"status": "ok", "plugin": "brain-test", "version": __version__}


@router.post("/roundtrip")
async def brain_roundtrip(request: Request) -> dict:
    """Save a fact then immediately recall it — tests save/recall round-trip."""
    brain = getattr(request.app.state, "brain", None)
    if brain is None:
        return {"success": False, "reason": "no brain on app.state"}

    # save_fact(category, fact, *, tier) — category is first positional arg.
    category = "test"
    fact = "AgentForge brain rig test fact"
    await brain.save_fact(category, fact, tier="context")

    recalled = await brain.recall_for_prompt("AgentForge brain rig test", threshold=0.1)
    return {
        "success": recalled is not None,
        "recalled": recalled is not None,
        "fact_saved": f"[{category}] {fact}",
    }
