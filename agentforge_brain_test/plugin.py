"""Plugin registration entry point for agentforge-brain-plugin (TAP-763)."""

from fastapi import FastAPI

from agentforge_brain_test.routes import router


def register(app: FastAPI) -> None:
    """Register the brain-test routes on the host FastAPI app."""
    app.include_router(router)
