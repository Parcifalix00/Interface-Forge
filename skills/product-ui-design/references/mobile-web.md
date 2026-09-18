# Mobile web implementation

Use semantic HTML and adaptive CSS. Verify APIs against the actual target. Do not paste CSS fixes before reproducing the issue in the authorized context.

Safe area: for a genuinely edge-to-edge page, consider `viewport-fit=cover` and padding with `env(safe-area-inset-*)`. Preserve minimum content padding and check whether an outer container already applies insets. A bottom bar must avoid both the home indicator and overlaps introduced by the application.

Viewport: `svh`, `lvh`, and `dvh` describe different browser-UI conditions. Prefer flexible sizing and min-height where content needs to grow. Do not apply `height:100dvh` to every screen and do not treat it as a universal virtual-keyboard solution.

Keyboard: test focus on the first and last fields, error messages, selection controls, submit, and dismiss behavior. The visual viewport may differ from the layout viewport. Use `VisualViewport` with feature detection only where the base layout is insufficient. Remove listeners correctly and avoid unnecessary continuous measurement.

Touch: controls must be reachable without hover, gestures need alternatives, and scrolling should remain natural. Do not apply global `touch-action:none`, `preventDefault`, or body scroll locks without a bounded purpose and verified restoration.

Forms: preserve zoom and pinch gestures, visible labels, and appropriate `inputmode`/autocomplete. Verify browser behavior for input text sizing rather than treating one CSS threshold as iOS certification.

Fonts and media: verify fallbacks, line breaks, loading, intrinsic dimensions, and crop. Do not hide horizontal overflow globally before identifying the element that caused it.

Sources: [MDN viewport length](https://developer.mozilla.org/en-US/docs/Web/CSS/length), [VisualViewport](https://developer.mozilla.org/en-US/docs/Web/API/VisualViewport), [WebKit safe area](https://webkit.org/blog/7929/designing-websites-for-iphone-x/).
