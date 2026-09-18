# Platform matrix and evidence levels

For every target family in the baseline, create at least one requirement for the critical flow and additional requirements for specific risks. Each requirement includes `allowed_methods`, not a generic mobile label.

Available methods: `static`, `browser-emulation`, `desktop-browser`, `platform-simulator`, `physical-device`, `manual-assistive-tech`. These are categories, not one total ranking. A physical device without a screen reader does not replace an assistive-technology check.

A local WebKit run configured like an iPhone remains `browser-emulation`. An Apple simulator is `platform-simulator`. A real iPhone is `physical-device`. Always record environment, OS/browser, and version. Do not populate an iPad result with a reused desktop screenshot.

Example device requirement: `allowed_methods: ["physical-device", "platform-simulator"]`. Example screen-reader requirement: `allowed_methods: ["manual-assistive-tech"]`. If browser emulation is useful for part of the layout, create a separate requirement for it. Results must refer to the same platform as the requirement.

`NOT_APPLICABLE` requires a scope or technical reason. Do not use it merely because hardware is missing. `NOT_RUN` should explain what is unavailable. `PASS` and `FAIL` require evidence and an environment. A new build or UI change may invalidate old evidence, so record the revision and re-run affected flows.

The template starts intentionally incomplete. Adapt it to the brief before testing. Do not leave generic targets in place and later present the file as evidence for a real product.
