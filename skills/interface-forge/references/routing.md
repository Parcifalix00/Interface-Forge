# Routing and composition

| Request | Initial skill | Specialist skills to read |
|---|---|---|
| New dashboard / complete UI | interface-forge | product-ui-design, frontend-visual-qa; brand/assets only if needed |
| Extend a UI with a form or table | interface-forge or product-ui-design | Design and QA for the affected surface and flows |
| Focused visual fix | product-ui-design | Proportional QA; no new brand work |
| Audit without modifications | frontend-visual-qa | No implicit implementation |
| Explicit new identity request | visual-brand-system | creative-assets only for assets that must be produced |
| Asset-only task | creative-assets | Existing brand lock, no redesign |
| Backend, SQL, CLI, or text-only task with no UI | None of these | Use relevant technical skills, do not force this suite |

Descriptions may produce more than one plausible semantic match. For tasks that create, modify, redesign, implement, or review a UI, `interface-forge` is the primary coordinator when available. A more specific HTML, React, framework, browser, or asset skill can be used as an implementation tool, but it does not replace the coordinator's cross-platform and QA gates. For isolated audits, brand work, or asset work, it is still correct to enter through the relevant specialist skill directly.

Open every file that is actually needed. Reuse shared context already loaded rather than reading every reference in advance. If the host supports subagents, delegate a bounded review and inspect its report. Subagents are not a prerequisite and are not implied by the word "orchestrator".

Do not require installation of additional skills when the task can be completed with available tools. Resolve conflicts between skills using applicable project instructions, the brief, and one clear responsibility per phase. Interface Forge's primary role is UI coordination. It does not authorize ignoring a technical skill that is better suited to the concrete implementation.
