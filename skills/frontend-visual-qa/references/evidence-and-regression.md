# Evidence, regressions, and defensive security

Every finding should have an identifier, surface, authorized manual steps, expected/observed behavior, impact, environment, and evidence. Store relevant screenshots and logs in the agreed location and redact sensitive data. Do not automatically delete evidence required for handoff.

Regression review should compare the same state and dimensions when possible. If dataset, fonts, time, or browser differ, record that. Do not update a baseline merely to make a test pass.

After a fix, re-run the failed check and affected shared flows. After two equivalent attempts, change the hypothesis or record the blocker. Do not chase an undefined "10/10" and do not keep consuming resources without new evidence.

Security work here is defensive review of authorized code and configuration: no secrets in frontend code, cautious handling of external HTML/SVG, synthetic test data, and server-side authorization. A UUID does not eliminate object-level access control. Do not provide or execute an attack workflow against third parties and do not call this work a penetration test.

Sources: [Playwright browsers and limitations](https://playwright.dev/docs/browsers), [OWASP authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html), [OWASP IDOR prevention](https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html).
