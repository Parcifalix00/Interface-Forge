# Native, desktop, and hybrid UI

Identify the framework and deployment target before recommending APIs. Do not impose Jetpack Compose on Views, SwiftUI on UIKit, or Flutter on React Native. Adaptation belongs to the existing architecture unless a migration is explicitly requested.

Android: use real window sizes, system-bar and IME insets, target-specific edge-to-edge behavior, back navigation, and font scaling. Test reduced window sizes and orientation rather than display resolution alone. Use adaptive components available in the adopted version when they improve the task.

iOS/iPadOS: use safe areas, adaptive layout, Dynamic Type, VoiceOver, and keyboard support. On iPad, verify window behavior and pointer use. An iPad is not simply an enlarged phone. Safe areas and the virtual keyboard solve different problems.

Hybrid: distinguish native layout from WebView content. File pickers, authentication, permissions, keyboard behavior, and deep links cross platform boundaries and need target-specific verification. A web demo does not prove the compiled app.

Desktop: check scaling, keyboard use, focus, small windows, long content, and input devices. If the product is desktop-only, record mobile targets as excluded by scope rather than adding a port.

References: [Android adaptive](https://developer.android.com/develop/adaptive-apps/guides/support-different-display-sizes), [Android edge-to-edge](https://developer.android.com/develop/ui/views/layout/edge-to-edge), [Apple layout](https://developer.apple.com/design/human-interface-guidelines/layout), [Apple UI](https://developer.apple.com/design/tips/).
