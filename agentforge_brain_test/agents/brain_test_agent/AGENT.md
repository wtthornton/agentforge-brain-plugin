---
name: brain-test-agent
namespace: project.brain-test.brain-test-agent
description: Test agent for tapps-brain save/recall round-trip rig.
keywords: [brain, memory, save, recall, test]
memory_profile: full
runner: agentforge_brain_test.agents.brain_test_agent.runner:BrainTestRunner
---

# Brain Test Agent

Test fixture for the TAP-763 brain rig. Exercises the BrainBridge save/recall
round-trip without any LLM calls. Returns "brain:ok" on success.

Exists to verify `AgentLoader.load_external()` picks up agents from
installed plugins with `memory_profile: full`, and that the runner entry
point resolves correctly.
