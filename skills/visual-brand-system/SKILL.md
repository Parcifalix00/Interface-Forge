---
name: visual-brand-system
description: "Apply, extend, or design visual identities for software and products: palette, typography, logo, brand design tokens, and asset consistency. Use when an existing brand must be respected or when identity work is explicitly requested. Do not start a rebrand during a normal UI fix and do not replace official assets without approval."
license: MIT
compatibility: "Agents with workspace read access; browsers and native tools only when available. No API required."
metadata:
  version: "1.0.0"
  author: "Parcifalix00"
---

# Visual Brand System

## First decision

Read the [shared contract](references/core-contract.md). Classify the task as `apply-existing`, `extend-partial`, or `create-identity`. A missing file is not authorization to create a new identity.

Inspect real assets and rules. Similar names do not prove that two logos are equivalent. Preserve the canonical path and, when useful, its hash and version. If the project already has a source of truth, extend it. Do not create a competing brand lock.

## Workflow

1. Collect the exact name, intended use, audience, official assets, available palette and fonts, prohibited treatments, and what may change. Do not invent brand values or market positioning.
2. Record a [brand lock](references/brand-lock.md) using the [JSON template](templates/brand-lock.json). Fill it with real references. `null` values remain unresolved, not approved.
3. For `apply-existing`, use official materials as-is, report technical conflicts, and do not redesign them. For `extend-partial`, propose only the missing slots. For `create-identity`, present a small number of meaningfully different directions and obtain approval on foundations before producing derivatives.
4. Apply [color and typography](references/typography-colour.md). Check contrast, semantic roles, readability at real sizes, and fallbacks. Do not include font files in the deliverable. Record name, source, and license requirements instead.
5. Maintain [dependencies and consistency](references/consistency.md). A foundation change marks affected derivatives for review. It does not delete or regenerate them automatically.
6. Export only formats the available tools can really produce. A raster image does not become vector or editable by changing its extension. Do not promise native Figma/PSD/AI files without verified capability.

## Assets and review

Use `creative-assets` for required graphic assets when available. Logo proposals remain proposals until the user chooses one. Generated images require inspection. A successful prompt or generation call is not evidence of visual fidelity.

Check minimum logo size, clear space, contrast on intended backgrounds, proportions, colors, typography, and consistency across outputs. Do not approve work based only on the skill's aesthetic preference.

## Output

Deliver the updated brand lock or existing source of truth, assets actually produced, approved decisions, pending proposals, and a list of derivatives that require review. Tie every approval to an explicit request or selection without storing unnecessary personal data. Do not call the orchestrator recursively.

