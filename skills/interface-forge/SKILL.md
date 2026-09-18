---
name: interface-forge
description: "Use for any task that creates, modifies, redesigns, implements, or reviews a user-facing UI or frontend, including websites, web apps, dashboards, screens, forms, components, and responsive layouts. This is the primary UI coordinator: it orchestrates product UI design, brand work when relevant, assets when needed, accessibility, desktop/Android/iOS compatibility across phone and tablet, and visual QA. Use it before specialist frontend implementation skills. Do not use it for backend, CLI, or documentation-only work with no UI."
license: MIT
compatibility: "Agents with workspace read access; browsers and native tools only when available. No API required."
metadata:
  version: "1.0.0"
  author: "Parcifalix00"
---

# Interface Forge

## Entry and preparation

Read the [shared contract](references/core-contract.md) and [routing rules](references/routing.md). Act as the task coordinator, not as a replacement for repository instructions. Before writing files, identify the user goal, surface, stack, design system, constraints, modification scope, and usable tools. Reuse existing documentation and assets. Do not create process directories for a simple CSS correction.

Classify the work as `new-ui`, `extend-ui`, `targeted-fix`, `redesign`, `audit-only`, `brand-only`, or `asset-only`. For web applications, read the [platform baseline](references/platform-baseline.md). For native/desktop applications, preserve the real targets. Unobserved requirements remain assumptions, not facts.

## Concrete coordination

Locate specialist skills in the available-skill inventory. In the installed suite, their files are sibling directories: `../product-ui-design/SKILL.md`, `../visual-brand-system/SKILL.md`, `../frontend-visual-qa/SKILL.md`, `../creative-assets/SKILL.md`.

Actually open the required `SKILL.md` using the host's file-reading tools, then load only relevant references. Do not print a fake skill call and do not assume that naming a skill executes it. If a path does not exist, use the path reported by the host. Do not search the entire disk and do not install anything. If a specialist skill is unavailable, report that limitation and use the gates included here for a limited review without presenting it as full-suite execution.

Not every task needs every skill. UI implementation normally uses design and QA. Brand work is included only when identity decisions must be resolved. Asset work is included only when assets are necessary. Specialist skills must not call the orchestrator again. If another applicable skill already handles React, shadcn, charts, browsers, or another implementation technology, assign one responsibility per phase and avoid duplicate implementation.

## Workflow

1. **Inspect context.** Read applicable instructions, relevant files, and screenshots. For an existing UI, observe current behavior when possible. Identify states and flows that must be preserved.
2. **Define acceptance.** Use the [UI brief](templates/ui-brief.md) only for substantial work. Record targets, primary tasks, constraints, expected evidence, and authorized costs, normally none. For a small fix, a note in the existing workflow is enough.
3. **Protect foundations.** Apply approved brand and components first. Use `visual-brand-system` for explicitly requested extensions or new identities, not to impose a rebrand.
4. **Design.** Apply `product-ui-design`, including hierarchy, layout, states, adaptive behavior, and interaction. A wireframe or coded prototype may be sufficient. Image generation is optional and does not authorize spending.
5. **Produce assets only when needed.** Apply `creative-assets` with a brief, provenance, and authorized tools. Higgsfield is not a dependency.
6. **Implement within scope.** Preserve relevant APIs, stack, naming, and patterns. Do not add authentication, backend work, or deployment unless requested. Interactive elements must be real controls, not screenshots of controls.
7. **Verify.** Apply `frontend-visual-qa` to the changed scope and compare against the prior state or approved specification. Browser-engine evidence and device evidence remain distinct. A successful build does not close the visual gate.
8. **Repair and hand off.** Fix material issues and re-run affected checks. Use the [quality gates](references/quality-gates.md) and [handoff rules](references/handoff.md). Do not claim what you did not verify.

## Minimum output

Report changed surfaces and files, skills actually read, checks performed with environment and evidence, missing/failed checks, and unresolved decisions. For substantial work, keep a [run log](templates/run-log.md) in the project's existing documentation system. Do not create a new tracking system when one already exists.

No implicit commit, push, deploy, or global update. Automatic activation depends on the model and must be tested. Explicit `$interface-forge` invocation selects the coordinator but does not guarantee task quality.

