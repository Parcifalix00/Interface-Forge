# Accessibility: targeted checks

Web technical target: WCAG 2.2 AA unless the project specifies a different requirement. This checklist is partial and does not justify a complete conformance claim.

Check semantics, headings and landmarks, accessible control names, field labels, associated errors, focus order, and keyboard operation. Focus must remain visible and not be entirely obscured by author-created content. Check modals, sticky headers, and banners too.

Text: minimum contrast is 4.5:1, or 3:1 for large text as defined by the criterion. UI components and necessary graphical information have the separate non-text contrast criterion. Evaluate actual colors, states, and backgrounds rather than an abstract palette.

Reflow: where applicable, verify content at an equivalent width of 320 CSS px without unnecessary two-dimensional scrolling. Tables, maps, and other intrinsically two-dimensional content have defined exceptions. Do not extend those exceptions to the whole page. Verify 200% text resize and zoom without loss of content or functionality.

Targets: WCAG 2.2 AA 2.5.8 uses 24 x 24 CSS px or the stated exceptions, including the spacing rule. Do not describe it as a generic 24 px margin. As an ergonomic suite policy, prefer approximately 44 x 44 CSS px for primary web touch controls when practical. Apple recommends 44 x 44 points and Android recommends 48 x 48 dp. These units and criteria are not interchangeable.

Motion and gestures: respect reduced-motion preferences, avoid problematic flashing, and provide alternatives to dragging when required by the criterion. For sensitive forms, review accessible authentication and copy/paste/password-manager behavior as relevant.

Assistive technology: for iOS/iPadOS targets, plan VoiceOver checks; for Android, TalkBack; for desktop, the assistive tools required by the project. Automated checks do not execute these tests. Record `NOT_RUN` when the required environment is unavailable.

Sources: [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [target size](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html), [reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html), [focus](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html), [Apple](https://developer.apple.com/design/tips/), [Android accessibility](https://developer.android.com/guide/topics/ui/accessibility/apps).
