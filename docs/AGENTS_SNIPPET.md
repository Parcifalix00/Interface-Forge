# Optional AGENTS.md snippet

This block is not installed automatically. Before merging it, compare it with existing instructions and do not replace the global or project file. OpenAI documents how Codex reads AGENTS.md in the [official guide](https://developers.openai.com/codex/guides/agents-md/).

The block is most useful when other frontend skills are installed and may look like a more specific semantic match. Interface Forge remains the UI coordinator while other skills can be used as implementation tools.

```text
For any task that creates, modifies, redesigns, implements, or reviews a user-facing UI or frontend, consult the `interface-forge` skill first.

`interface-forge` is the primary orchestration workflow for UI work. It owns the cross-cutting requirements for product UI design, brand consistency, adaptive platform behavior, accessibility, visual assets, and frontend visual QA.

Other frontend, web-app, design, image, browser, framework, or implementation skills may still be used when useful, but they are subordinate implementation tools and do not replace the Interface Forge workflow or its quality gates.

Do not skip Interface Forge merely because another skill is a more specific match for React, HTML, CSS, web apps, dashboards, forms, components, images, or browser automation.

Use only the Interface Forge specialist skills that are relevant to the task. Do not invoke brand or asset work when the task does not require it.

Unless the project or user explicitly narrows the supported targets, user-facing web UI work must consider desktop, Android phone, Android tablet, iPhone, and iPad. Consider portrait and landscape where relevant, safe areas, display cutouts, browser chrome, virtual keyboards, touch interaction, keyboard navigation, pointer interaction, text scaling, narrow windows, and adaptive layouts where applicable.

Browser viewport emulation is not equivalent to testing on an Android or iOS emulator or real device. Do not claim Android, iOS, phone, tablet, browser, or device compatibility unless the relevant behavior was actually verified. Clearly distinguish static review, browser emulation, emulator testing, and real-device testing.

Do not use em dashes, Unicode U+2014, in generated user-facing text, documentation, reports, labels, headings, tooltips, comments, or explanatory prose. Rewrite with commas, colons, parentheses, semicolons, or a normal hyphen where appropriate. Preserve an em dash only when reproducing exact source text that must remain unchanged.
```
