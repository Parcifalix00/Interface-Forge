# Using Interface Forge in Codex

## First explicit check

Use the prompt in [START_HERE](../START_HERE.md) in a new session. Confirm that the host can resolve all five skill names and that the agent actually reads the real file paths. Repeating names from the prompt is not sufficient evidence.

Skills can be selected explicitly and can also be selected implicitly through their descriptions. The locations and metadata follow [OpenAI Skills](https://developers.openai.com/codex/skills/) and the [Agent Skills specification](https://agentskills.io/specification). Implicit activation was verified with a small UI task during the operational validation of version 1.0.0, but it remains dependent on the host, model, context, and competing skills.

## Ordinary prompt

In a disposable project, for example: "Implement a dashboard with a table and filter, preserving the existing design system and project targets." The expected behavior is product design plus QA, not a new brand system or a paid image generator.

For a substantial UI task you can explicitly select `$interface-forge`. For a read-only audit, use `$frontend-visual-qa`. For isolated brand or asset work, use the corresponding specialist skill. You do not need to name every skill in one prompt. The orchestrator contains the routing rules and file-loading instructions.

## Persistent rules

The no em dash rule appears in every skill contract and in QA. When these skills are not active, that rule does not automatically become a global instruction. To apply it across Codex tasks and to give Interface Forge stable priority when competing frontend skills are installed, manually merge [AGENTS_SNIPPET](AGENTS_SNIPPET.md) into your global instruction file without replacing other rules. The package does not modify `AGENTS.md`.

Android/iOS targets are defined in the contract and platform baseline and do not need to be repeated in every prompt. A project can narrow them. Desktop-only does not become a mobile port, and native Android does not imply iOS. Precise support claims require declared minimum versions and real evidence.

## Cooperation with other skills

If a repository already uses a skill for React, HTML/CSS, shadcn, D3, browser automation, or another frontend technology, Interface Forge remains the coordinator for cross-cutting UI requirements. The specialist skill may implement the relevant technical portion. Avoid duplicate implementations and do not impose libraries, generated images, fonts, or themes without project justification.

## Sessions and updates

After installation or an update, restart Codex or open a new session if the skills do not appear. A session that already loaded instructions may retain old context. Avoid updating the suite during active work unless necessary. Do not keep global, repository-specific, and manually copied versions with the same skill names active at the same time without an explicit reason.

## Reporting

QA records where it looked, what it tested, and what remains unverified. `READY_FOR_REVIEW` means the declared checks are satisfied. It is not universal certification. `INCOMPLETE` preserves completed work without inventing device evidence.
