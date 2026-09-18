# States and flows

For every changed component, define a matrix containing state, visible content, available actions, accessible semantics, transition, and expected evidence.

- Loading: communicate activity and keep layout stable. Distinguish initial data loading from refresh. Do not make stale data look freshly updated.
- Empty: distinguish no data from no filter results and from an error. Any proposed action should be relevant and authorized.
- Error: explain what the user can do, preserve entered data, and show field errors in context. Do not expose secrets or stack traces in a public UI.
- Pending/success: prevent duplicate submission, provide observable confirmation, and avoid unnecessary focus loss.
- Disabled: communicate the reason when it is not obvious. Do not leave functionality unreachable without an alternate path.
- Offline/partial/stale: use only for products that genuinely support those states. Do not imply synchronization that does not exist.

Where relevant, verify multi-selection, cancellation, authorized simulated server failures, long content, and missing permissions. The visibility of a button does not replace server-side authorization.
