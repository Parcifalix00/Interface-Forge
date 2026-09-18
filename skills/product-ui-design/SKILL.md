---
name: product-ui-design
description: "Design or implement product interfaces: dashboards, forms, tables, navigation, responsive/adaptive layouts, states, and design tokens. Use for concrete UI work inside the existing stack. Works independently or under Interface Forge. Do not use for audit-only work, image generation, or backend tasks with no UI."
license: MIT
compatibility: "Agents with workspace read access; browsers and native tools only when available. No API required."
metadata:
  version: "1.0.0"
  author: "Parcifalix00"
---

# Product UI Design

## Input

Read the [shared contract](references/core-contract.md) and [platform baseline](references/platform-baseline.md). Ask only for information that is missing and genuinely blocks the work, such as the surface, user task, constraints, or incompatible targets. Inspect the repository and design system before proposing frameworks or libraries.

For an extension, preserve structure and conventions. For a redesign, separate what is authorized to change from what must remain stable. For a new UI, distinguish requirements, proposals, and placeholder content. Do not turn operational dashboards into promotional landing pages.

## Design

1. Organize information around tasks and decisions: primary action, current state, secondary actions, and recoverable detail. Reduce noise without hiding operational information.
2. Select patterns from [layout patterns](references/layout-patterns.md). Define navigation, narrow-window behavior, and list/table behavior before visual polish.
3. Formalize semantic colors, typography, spacing, and variants using [design tokens](references/design-tokens.md). Reuse existing tokens. A brand palette alone does not define error, focus, and disabled states.
4. Define [interaction states](references/interaction-states.md) for changed components: loading, empty, error, success, disabled, pending, and offline only when relevant. Every control implies behavior that must be testable.
5. For web applications, use [mobile web](references/mobile-web.md). For native/hybrid applications, use [native adaptation](references/native-adaptive.md). Do not apply CSS APIs to native apps or native APIs to web apps.
6. Use a [design specification](templates/design-spec.md) when decisions need to persist. For a focused fix, before/after criteria are enough. Do not create moodboards, logos, or images for every task.

## Implementation

Use the project's semantic components and explicit variants. A table should remain a table when column comparison is essential. Preserve accessibility, DOM order, labels, and accessible names. Avoid rigid heights that clip content and responsive logic based only on user-agent detection.

Define breakpoints where content stops working. Keep essential actions visible or reachable. For dialogs and drawers, handle focus, return to trigger, scrolling, and virtual keyboards. Do not remove outlines without a visible replacement. Do not use color as the only signal.

Verify API availability in the versions already installed. Add a dependency only when necessary and authorized. Do not impose React, Tailwind, a specific icon set, dark mode, a fixed number of colors, or animation. Design should follow the product, not the aesthetic signature of the skill.

## Verification and handoff

Run the project's functional checks and visually verify the changed work. If `frontend-visual-qa` is available, read and apply it. Otherwise document the limited verification and missing checks. Do not call Interface Forge recursively.

Hand off changed components/files, important decisions, covered targets, evidence collected, and remaining limitations. Full WCAG conformance is not proven by these checks alone.

