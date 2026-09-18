---
name: frontend-visual-qa
description: "Verify implemented UIs: visual comparison, regressions, responsive behavior, Android/iOS, phone/tablet layouts, accessibility, focus, forms, and states. Use for UI audits, visual QA, or final verification of frontend changes. Audit-only by default and does not modify files unless requested. This is not a penetration test or accessibility certification."
license: MIT
compatibility: "Agents with workspace read access; browsers and native tools only when available. No API required."
metadata:
  version: "1.0.0"
  author: "Parcifalix00"
---

# Frontend Visual QA

## Scope and tools

Read the [shared contract](references/core-contract.md) and [platform baseline](references/platform-baseline.md). During an audit, do not modify the product without authorization. During an implementation workflow, correct only defects within the requested scope. Inspect the diff, specification, design system, and canonical assets. If no baseline exists, state that explicitly. You can review usability and internal consistency but not fidelity to a nonexistent specification.

Identify available browsers, screenshots, emulators/simulators, and devices. Do not install them silently. A viewport change is simulation, not an iPhone test. Keep evidence levels separate.

## Execution

1. Define required checks before evaluating them. Use the [platform matrix](references/platform-matrix.md) and [QA report](templates/qa-report.json). Adapt targets and flows to the project without deleting rows only because you cannot execute them.
2. Run the functional checks required by the repository. Distinguish pre-existing failures from regressions without ignoring their effect on delivery readiness.
3. Launch the UI when possible. Exercise at least the primary flow of the changed surface: open, input, action, response, and error recovery when relevant. Do not stop at the first screenshot.
4. Apply [visual review](references/visual-review.md) and [accessibility review](references/accessibility.md). Compare images you actually inspected, not only the prompt that produced them. For complex surfaces, record at least five concrete comparisons. For small fixes, use proportional criteria.
5. Verify phone/tablet and required Android/iOS targets, including input and virtual keyboard behavior. If devices or simulators are unavailable, record `NOT_RUN` for checks that require them even when browser emulation passes.
6. Check authored copy. `scripts/check_copy.py` is read-only and reports U+2014 in explicitly selected files. It does not prove what is rendered and must not rewrite quotations or data.
7. Classify defects and repeat relevant checks after fixes following [evidence and regression](references/evidence-and-regression.md). Store screenshots or local logs without secrets, including environment and timestamp.

## Verifiable report

Use `scripts/validate_report.py <report.json>` to validate structure, completeness, and evidence-method consistency. The command returns 0 only when declared required checks are complete and not failed, 1 for incomplete/failed checks, and 2 for an invalid report. It does not prove that evidence is truthful, sufficient for the whole product, or actually observed. A reviewer still needs to inspect the evidence.

Every result distinguishes `PASS`, `FAIL`, `NOT_RUN`, and `NOT_APPLICABLE`. The report separates required tests from additional observations. Record OS/browser version, method, and limitations. Do not convert browser emulation into physical-device evidence. The validator rejects that upgrade when the declared method requires stronger evidence.

## Output

Report outcome, issues ordered by impact, evidence, missing tests, authorized changes made, and residual risks. Do not say "compatible everywhere" or "100% accessible." Do not call Interface Forge recursively. Do not perform offensive scanning or test third-party services. Security here means defensive review inside the authorized scope.

