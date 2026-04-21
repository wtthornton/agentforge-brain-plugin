"""BrainTestRunner — deterministic runner for the TAP-763 brain rig."""

from __future__ import annotations

from typing import Any


class BrainTestRunner:
    """Minimal runner that exercises save/recall via app.state.brain.

    Returns "brain:ok" when the round-trip succeeds, "brain:no-brain" when
    no BrainBridge is available on app state, and "brain:error:<msg>" on
    unexpected failure.
    """

    async def run(
        self,
        prompt: str,
        *,
        app_state: Any = None,
        **_kwargs: Any,
    ) -> str:
        brain = getattr(app_state, "brain", None) if app_state is not None else None
        if brain is None:
            return "brain:no-brain"

        try:
            await brain.save_fact(
                "test", "brain-runner round-trip probe", tier="context"
            )
            recalled = await brain.recall_for_prompt(
                "brain-runner round-trip probe", threshold=0.1
            )
            return "brain:ok" if recalled is not None else "brain:empty-recall"
        except Exception as exc:  # noqa: BLE001
            return f"brain:error:{exc}"
