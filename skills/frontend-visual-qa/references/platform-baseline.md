# Cross-platform baseline

Contract version: 1.0. This is a project policy, not a promise of universal support.

## Identify the product type first

| Type | Initial scope | Do not infer |
|---|---|---|
| Web / PWA | Desktop, Android phone/tablet, iPhone/iPad unless explicitly restricted | A narrow viewport is not proof of phone compatibility |
| Native Android | Declared SDK versions, windows, and form factors | Do not add an iOS version |
| Native iOS/iPadOS | Declared deployment target, safe areas, and form factors | Do not use browser testing as native-app evidence |
| React Native / Flutter / hybrid | Targets actually supported by the repository | A test on one platform does not cover the other |
| Dedicated desktop | Declared operating systems, scaling, keyboard behavior, and minimum size | Do not promise mobile compatibility |

For web work, record the actual browser and minimum supported version, device or simulation method, operating system, CSS viewport, orientation, zoom, and browser/PWA/WebView mode. If minimum versions are undecided, record them as unresolved. Do not rigidly equate a browser brand with a single engine in every jurisdiction. Verify the real target environment.

## Planning matrix

| Family | Initial checks | Evidence required for the corresponding claim |
|---|---|---|
| Desktop | Narrow window, laptop, wide monitor; keyboard; zoom | Actual browser and verified screenshot/flow |
| Android phone | Portrait/landscape, keyboard, scroll, back, touch | Browser on an Android device or declared emulator |
| Android tablet | Portrait/landscape, reduced window, keyboard/pointer | Android tablet environment or declared emulator |
| iPhone | Safe area, browser chrome, input focus, keyboard, scroll | Safari/target environment on iPhone or declared Apple simulator |
| iPad | Landscape/portrait, resized window, keyboard/pointer | iPad or declared Apple simulator |

Useful CSS samples for initial coverage, not certified devices: widths 320, 390, 768, 1024, 1366, and 1920. Choose meaningful heights and test between breakpoints too. Use content constraints rather than rigid device labels. The matrix is risk-based. It does not require the full Cartesian product of every size, but every declared family and every critical flow needs a traceable decision.

## Mobile web checks that must not be skipped

1. Content and actions must not be hidden by notches, home indicators, or system bars. Handle `env(safe-area-inset-*)` when the page is edge-to-edge and do not apply the same inset twice. A virtual keyboard is not a safe area.
2. Headers, bottom bars, drawers, and dialogs must remain usable when the visual viewport changes. `100dvh` is not a universal keyboard fix. Test open, focus, submit, scroll, and close behavior. Use feature detection for optional APIs.
3. No action may require hover. Avoid sticky hover behavior, undocumented gestures, drag-only actions, or controls placed too close together. Verify visible focus and tab order with an external keyboard where relevant.
4. Forms need persistent labels, associated messages, suitable input modes, appropriate autocomplete, and zoom that remains enabled. Do not add `user-scalable=no` or restrictive zoom limits to hide a layout defect.
5. Tables, editors, and maps may use justified local scrolling. The rest of the page must not scroll horizontally by accident. Do not hide essential data or actions just to make the layout fit.
6. Dialogs need managed focus, focus return to the trigger, reachable actions, and usable long content. Verify nested scrolling and supported close interactions. A scroll workaround must not leave the page locked after the dialog closes.
7. Test accented characters, long text, large numbers, empty content, and loading states. Do not lock orientation unless it is essential and approved. Verify reduced-motion behavior and available contrast preferences.
8. If PWA or WebView behavior is in scope, test it separately from the standard browser, including permissions, file pickers, authentication, and return-to-app flows. Do not promise automatic parity.

## Native and hybrid applications

Android: use the window sizes and adaptive APIs/components already adopted by the project. Handle system insets, the virtual keyboard, back navigation, and font scaling correctly. iOS/iPadOS: use safe areas, Dynamic Type, window adaptation, and accessible framework components. On both platforms, do not impose migrations and do not duplicate automatic and manual inset handling.

Verify real build and deployment targets before giving version-dependent advice. Android 16 checks, or checks for any other specific release, are not rules to paste into every project.

## Limits of simulation

A Chromium/WebKit/Firefox run with device parameters is `browser-emulation`. It verifies useful parts of behavior but does not automatically reproduce the operating system, distributed browser build, native keyboard, GPU, assistive technology, or system gestures. Record `platform-simulator` and `physical-device` separately. A `PASS` in one category does not automatically populate the others.

Sources: [Android adaptive](https://developer.android.com/develop/adaptive-apps/guides/support-different-display-sizes), [Apple UI](https://developer.apple.com/design/tips/), [WebKit safe area](https://webkit.org/blog/7929/designing-websites-for-iphone-x/), [Playwright emulation](https://playwright.dev/docs/emulation), [Playwright browsers](https://playwright.dev/docs/browsers), [VisualViewport](https://developer.mozilla.org/en-US/docs/Web/API/VisualViewport), [WCAG 2.2](https://www.w3.org/TR/WCAG22/).
