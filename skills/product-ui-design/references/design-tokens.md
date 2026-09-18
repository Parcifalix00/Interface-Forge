# Design system and tokens

Inventory existing CSS variables, theme, components, and conventions first. Define only what the task needs. Avoid color-specific names when the meaning is functional. Names such as `text-primary`, `surface-raised`, `border-default`, `focus-ring`, and `status-error` describe roles rather than prescribed values.

Document typography for content and application chrome: title, body, label, table, toolbar, and caption. Maintain a coherent hierarchy without shrinking operational controls into tiny text. Brand fonts and fallbacks must be verified at real usage sizes. Do not download fonts automatically.

Spacing and dimensions: a small scale can improve consistency, but do not force every value to a multiple when optical or accessibility needs justify otherwise. Radius, shadow, and border choices should represent real hierarchy. Do not wrap everything in nested cards.

Color: separate brand colors from semantic states and verify contrast between actually adjacent pairs. Add light/dark themes only when requested or already supported. There is no universal ban on serif fonts, palette families, or a fixed number of accents.

Interaction: document focus, hover, active, selected, disabled, and pending states. Variant differences should be intentional and implemented within the component rather than through divergent copies.

Motion: use movement for orientation and feedback, not to delay a task. Reduced-motion preferences, duration, and interruptibility are part of the contract. Do not add an animation library for marginal effects.
