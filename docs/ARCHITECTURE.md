# Architecture and design choices

## Components

Interface Forge is a suite of Agent Skills instructions, not a resident agent application. Each skill contains `SKILL.md`, `agents/openai.yaml` metadata, relevant references and templates, and license notices. The five directories can be installed together. Specialist skills can also be used without explicit orchestration.

The orchestrator applies routing and phases. Product UI design defines structure and behavior. The brand skill governs identity. The asset skill produces materials when they are needed. QA evaluates the result. No phase automatically authorizes the next phase to spend money, publish, or expand the scope.

## Composition

There is no magic primitive that means "execute the other four skills." The agent locates and reads their files using host tools. Descriptions support implicit routing, while explicit invocation selects a skill directly. Selection quality must be tested on the real host/model, as noted in the [OpenAI documentation](https://developers.openai.com/codex/skills/).

The suite does not monopolize frontend implementation or QA. It can cooperate with framework, component, browser, or other specialist skills already present while preserving one responsibility per phase and respecting the project. It does not create subagents when the host does not support them. A review performed by the same agent is not an independent review.

## Progressive disclosure

Each `SKILL.md` remains focused. Detailed material is loaded only when relevant. `contracts/core-contract.md` is canonical and replicated into all five skills so each can be used independently. `platform-baseline.md` is replicated into the three skills that need it. Package checks verify that the copies are identical. Do not maintain divergent copies manually.

Brand and asset templates are declarative. They are not a database, do not save approvals automatically, and do not execute an invalidation graph. The agent must maintain decisions and preserve their provenance. Only installation management, hashes, copy checks, and structured report validation are implemented as deterministic code.

## State separation

Installation state is local to the machine, controlled by `manage_skills.py`, and stored outside the skill directory. UI task state belongs to the project being edited, either in existing documentation or in an agreed location. Brand state belongs to the project's canonical source of truth. Do not mix data from different projects into the global skill installation.

## Security and limitations

These instructions are not a sandbox. Access control, network restrictions, and spending controls come from the host and the project. The manager does not use the network, does not interpret input as shell commands, and does not modify unrelated skills. Overwrite prevention assumes a non-hostile local environment. It does not defend against another process with the same permissions modifying the same files at the same time.

The SHA-256 manifest detects changes relative to recorded values. It does not authenticate the publisher. An actor who can replace both the code and the manifest can replace both. Verify the provenance of the ZIP before running its scripts.
