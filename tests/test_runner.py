"""Unit tests for BrainTestRunner (no live brain required)."""

import asyncio

import pytest

from agentforge_brain_test.agents.brain_test_agent.runner import BrainTestRunner


def test_runner_returns_no_brain_when_app_state_missing() -> None:
    runner = BrainTestRunner()
    result = asyncio.run(runner.run("ping"))
    assert result == "brain:no-brain"


def test_runner_returns_no_brain_when_brain_attr_absent() -> None:
    class _State:
        pass

    runner = BrainTestRunner()
    result = asyncio.run(runner.run("ping", app_state=_State()))
    assert result == "brain:no-brain"


def test_runner_propagates_brain_error() -> None:
    class _BadBrain:
        async def save_fact(self, *args, **kwargs):
            raise RuntimeError("sidecar offline")

        async def recall_for_prompt(self, *args, **kwargs):
            return None

    class _State:
        brain = _BadBrain()

    runner = BrainTestRunner()
    result = asyncio.run(runner.run("ping", app_state=_State()))
    assert result.startswith("brain:error:")
    assert "sidecar offline" in result
