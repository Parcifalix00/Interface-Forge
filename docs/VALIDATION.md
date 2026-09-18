# Version 1.0.0 validation

Date: 2026-09-18. This release combines deterministic package tests with operational validation performed on Windows. The two evidence categories remain separate.

## Package tests

Build environment: Linux x86_64, Python 3.13.5.

**81 tests executed, 81 passed, 0 failures, 0 errors, 0 skipped.**

| Area | Result and evidence |
|---|---|
| Automated tests | PASS. [Full log](../qa/unit-tests.txt), 81 cases. |
| Five-skill format | PASS. Frontmatter, names, descriptions, version, required files, and Codex metadata. |
| Independent YAML parsing | PASS. 5 frontmatters and 5 `agents/openai.yaml` files parsed with PyYAML 6.0.3. PyYAML is not a runtime dependency of the suite. |
| Contracts and licenses | PASS. Shared copies compared byte-for-byte; original licenses and upstream notices present in every skill. |
| Links and sources | PASS for local links, Python/JSON syntax, and UTF-8 readability. |
| Authored copy and distributable files | PASS. No em dash or en dash in authored text, and no fonts, `.env`, or key files included. |
| Installer | PASS in temporary directories: preview without writes, installation of five skills, idempotency, update, uninstall, status, and restore. |
| Data protection | PASS. Collisions, local drift, added files/directories, tampered backups, and invalid paths stop the operation. Other skills and configuration remain unchanged. |
| Recovery | PASS with an injected rename failure and an interrupted update journal reconstructed by the test. This does not simulate every physical or power failure. |
| UI report validator | PASS for structure, methods, states, rationale, evidence references, and file existence/confinement where required. It does not prove the content of the evidence. |
| Copy scanner | PASS for result handling, encoding, exclusions, duplicate inputs, non-followed links, and non-mutation of source files. |

## Windows operational validation of the pre-localization release candidate

Observed environment: Windows, PowerShell 7.6.6, Python 3.14.7, Codex desktop. This operational run was performed before the final repository-wide English localization. The localization changed authored instructions, metadata text, templates, test fixtures, and user-facing tool messages. Core installation and QA logic was not intentionally changed, but implicit skill triggering can depend on wording and therefore is not claimed as revalidated for the English metadata yet.

| Check | Result |
|---|---|
| Release integrity | PASS. 97 files checked, 5 skills, no errors. |
| Windows unit tests | PASS with limitation. 81 started, 78 `ok`, 3 `skipped`, 0 failures, 0 errors. The three skips concern symlink creation without the required Windows privilege. The `verified-copy` installation mode does not require symlinks. |
| Installer preview | PASS. Target `$HOME/.agents/skills`, five planned skills, no writes. |
| Managed installation | PASS. All five skills installed and `status` returned `installed-pristine` with no pending transaction. |
| Codex discovery | PASS. All five skills were visible and enabled as personal skills. |
| Explicit orchestration | PASS. `interface-forge` read the four specialist skills and applied routing, platform baseline, and QA gates without modifying files. |
| Implicit triggering | PASS in the executed micro smoke test. A UI request that did not mention Interface Forge activated `interface-forge`, `product-ui-design`, and `frontend-visual-qa`. Unneeded brand and asset skills were not activated. |
| Limitation reporting | PASS. The micro-task report distinguished static review from real Android/iOS testing and did not claim untested devices. |

Implicit selection remains dependent on host, model, context, and competing skills. The result above demonstrates the behavior observed in that test, not a universal guarantee. [AGENTS_SNIPPET](AGENTS_SNIPPET.md) makes UI coordination priority explicit while still allowing specialist frontend skills to act as implementation tools.

## Checks not executed

| Environment or behavior | Status | Consequence |
|---|---|---|
| PowerShell `.ps1` wrappers | NOT_RUN | The direct Python path was verified on Windows and is the primary documented route. |
| Complete run of every case in `evals/routing-cases.json` | NOT_RUN | Representative smoke tests were executed, not the full matrix. |
| Real Android devices | NOT_RUN | The Android baseline is formalized but not certified on hardware by this package. |
| Real iPhone/iPad or Apple simulators | NOT_RUN | Safe-area and platform requirements are formalized but do not constitute Safari/device evidence. |
| VoiceOver, TalkBack, and desktop screen readers | NOT_RUN | Assistive-technology checks must be performed against the actual application. |
| Post-localization Windows/Codex smoke check | NOT_RUN | The English package passes deterministic tests, but Windows discovery and implicit triggering have not been re-run after translation. |
| GitHub remote publication | NOT_RUN | No remote repository was created or modified by the release. |

## What version 1.0.0 means

The suite is ready as a first publishable release. Package format and deterministic behavior checks pass on the English package. Installation, discovery, explicit coordination, and one implicit-triggering path were also observed on the pre-localization v1.0 candidate. `1.0.0` does not mean certified compatibility with every UI, browser, or device. Testing against real applications remains proportional to each project and must report `PASS`, `FAIL`, `NOT_RUN`, or `NOT_APPLICABLE` with evidence.

File management uses preview, verified copy, hashes, backups, and a journal. It is not a single atomic transaction across all five directories and does not protect against every concurrent modification by other processes with the same permissions. Do not edit installed copies during installation or recovery.

## Repeat the checks

From the extracted project directory:

```powershell
python .\scripts\check_package.py --verify-integrity
python -m unittest discover -s tests -v
python .\scripts\manage_skills.py install
```

The last command is preview-only. If an older version of the suite is already installed, use the `update` path documented in [INSTALL_WINDOWS](INSTALL_WINDOWS.md).
