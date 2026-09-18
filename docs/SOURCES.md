# Source register

Reviewed: 2026-09-18. Suite policies are project decisions. The references below support file formats, tool limitations, and technical criteria. They are not certifications or guarantees. Live documentation may change. Re-check relevant documentation before introducing version-dependent APIs.

| Primary source | Use and limitation |
|---|---|
| [OpenAI: Skills](https://developers.openai.com/codex/skills/) | Format, discovery, user/repository scope, metadata, and the need to test triggering; an official redirect to ChatGPT Learn documentation was observed during review |
| [OpenAI: AGENTS.md](https://developers.openai.com/codex/guides/agents-md/) | Global/project instructions; this package does not modify them automatically |
| [Agent Skills specification](https://agentskills.io/specification) | Name, description, layout, and progressive disclosure |
| [Higgsfield Skills, pinned commit](https://github.com/higgsfield-ai/skills/tree/d071406147a37b835bed09543d85ab3e9bd85c7d) | Methodologies adapted conceptually, not an execution dependency |
| [Higgsfield LICENSE](https://github.com/higgsfield-ai/skills/blob/d071406147a37b835bed09543d85ab3e9bd85c7d/LICENSE) | MIT text and upstream copyright |
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | Web reference criteria, not a visual-only checklist |
| [Contrast minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) | Thresholds, large text, and exceptions |
| [Non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html) | UI components and necessary graphical information |
| [Target size minimum](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) | 24 CSS px and level-AA rules/exceptions |
| [Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html) | Content reflow and two-dimensional exceptions |
| [Focus not obscured](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html) | Focus visibility under the AA criterion |
| [Android adaptive](https://developer.android.com/develop/adaptive-apps/guides/support-different-display-sizes) | Window sizes and form factors |
| [Android edge-to-edge](https://developer.android.com/develop/ui/views/layout/edge-to-edge) | Insets and target-dependent behavior |
| [Android accessibility](https://developer.android.com/guide/topics/ui/accessibility/apps) | Touch targets in dp and accessible controls |
| [Apple UI design](https://developer.apple.com/design/tips/) | Target size in points, layout, and readability |
| [Apple layout](https://developer.apple.com/design/human-interface-guidelines/layout) | Additional native-layout reference; page content requires JavaScript rendering and is not used as the sole source for numerical values |
| [WebKit safe area](https://webkit.org/blog/7929/designing-websites-for-iphone-x/) | Origin of viewport-fit and safe-area-inset; historical page, not a 2026 support matrix |
| [MDN VisualViewport](https://developer.mozilla.org/en-US/docs/Web/API/VisualViewport) | Distinction between visual/layout viewport, zoom, and virtual keyboard effects |
| [MDN CSS length](https://developer.mozilla.org/en-US/docs/Web/CSS/length) | Viewport units and their differences |
| [Playwright emulation](https://playwright.dev/docs/emulation) | What device profiles emulate |
| [Playwright browsers](https://playwright.dev/docs/browsers) | Supported engines and differences from distributed browsers |
| [OWASP IDOR prevention](https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html) | Object authorization, including when UUIDs are used |
| [OWASP authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) | Authentication versus authorization boundary |
| [GitHub CLI repo create](https://cli.github.com/manual/gh_repo_create) | Manual publication of a local repository |

No source is used to claim that Interface Forge is already validated on every Codex version, Windows setup, Safari version, or physical device. Package-specific evidence is reported separately in [VALIDATION](VALIDATION.md).
