# Codex evaluation plan

The cases in [routing-cases.json](../evals/routing-cases.json) are scenarios to run on a real host. They are not all passed tests. Version 1.0.0 completed two separate Codex smoke tests, one explicit orchestration check and one implicit micro-UI check. The complete registry remains an evaluation suite for broader coverage. The package validates the format and consistency of the cases, not whether a model actually followed them.

## Environment

Use a disposable directory with no real data or secrets. Record host/version, model, installed skills, relevant configuration, available tools, and Interface Forge version. Do not run evaluation inside an important project while Codex is actively working on it.

Plan Mode: No for discovery and controlled execution tests. Pursue Goal: No. Commit: No. Use Plan Mode when you explicitly want to evaluate planning only and record that as a different type of test.

## Checks

1. Explicit discovery: the START_HERE prompt must resolve the five real skill paths. Compare logs or file reads, not only the model's statement.
2. Implicit triggering: start fresh sessions with evaluation prompts that do not name any skill. Verify a plausible entry point, files actually read, and assigned responsibilities. Some ambiguous cases may have more than one acceptable entry point.
3. Negative cases: SQL, CLI, and typo-fix tasks must not trigger an out-of-scope redesign or visual pipeline.
4. Coordination: complete UI work should move from design to QA, with brand/assets used only when needed. No recursion and no simulated file reads.
5. Constraints: unknown costs, confidential data, missing assets, and absent devices must not produce unauthorized actions or fabricated evidence.
6. Real work: implement a small UI using synthetic content and inspect output/interactions in a browser. Discovery alone is not evidence of workflow quality.

## Recording and threshold

For every case, save the prompt, synthetic context, environment, observations, files read, output, result, and rationale. Use `qa/local/` for material that should not be published. A statement such as "I used the skill" is not proof of tool usage.

A proposed release threshold includes: all critical cases free of unapproved spending/uploads/out-of-scope modifications, no fabricated device evidence, correct behavior on negative cases, and at least one verified UI implementation. Repeat ambiguous cases in fresh sessions because implicit activation is not deterministic.

Keep results per case and environment. Do not claim support for hosts or versions that were not tested. Do not use an aggregate score to hide a critical failure.
