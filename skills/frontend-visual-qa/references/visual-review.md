# Visual review

Observe the rendered UI at real usage scale. Compare it with an approved specification, canonical assets, or the pre-change baseline. Name files and viewports rather than saying "I saw the design" without references.

Check hierarchy, alignment, rhythm, density, and consistency, then review typography for content and controls, contrast, icons, images, and crop. Inspect multiple sections/states when the surface does not fit in one screen. Do not reduce quality to a single aesthetic score.

For a substantial UI, record at least five concrete comparisons with expectation, observation, evidence, result, and correction. Examples: submit label, heading wrapping, column width, focus position, or bottom-bar safe area. For a small fix, real acceptance conditions are enough.

Test interactions, not only images. Equivalent screenshots do not prove tabs, filters, dialogs, and forms work. Anti-aliasing or font-rendering differences are not automatically regressions, while updating a baseline without review can hide defects.

Repair order: task blocker/data loss; unreachable content or actions; blocking accessibility issue; material inconsistency; polish. In audit-only mode, describe the fix but do not apply it without authorization.
