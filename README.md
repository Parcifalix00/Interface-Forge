# Interface Forge

A suite of five skills for designing, implementing, and verifying software interfaces without depending on Higgsfield, a specific image provider, or a mandatory application stack.

**Version 1.0.0.** Original material is MIT licensed. Validation results are documented in [VALIDATION](docs/VALIDATION.md). The v1.0 workflow was operationally verified on Windows before the final English localization. The English package passes the full deterministic test suite. Live Codex triggering with the English metadata has not been re-run yet. Real Android/iOS device tests are not included and are not reported as executed.

## Start here

Read [START_HERE.md](START_HERE.md). This package is both the project to keep under version control and the source used to install the five skills. You do not need a Higgsfield account, API keys, npm, pip, or new subscriptions to install these instructions and use the included local tools. The host model and any optional tools you choose remain subject to their own costs and limits.

| Skill | Responsibility |
|---|---|
| `interface-forge` | Coordinates complete UI work with explicit routing |
| `product-ui-design` | Information hierarchy, layout, components, states, and adaptive behavior |
| `visual-brand-system` | Existing brand systems, targeted extensions, and identity approvals |
| `frontend-visual-qa` | Visual review, regressions, accessibility, and cross-platform evidence |
| `creative-assets` | Relevant assets, provenance, and authorized tool selection |

Specialist skills can also be used directly. The orchestrator reads the files it needs and applies their procedures. It is not an autonomous service and does not magically create processes or subagents. It does not invoke every skill for every task.

## Core contracts

No em dash in authored text. No implicit redesign, new cost, private upload, dependency, commit, or deploy. Reuse the existing visual system and application stack. For unrestricted web UI work, include desktop, Android phone/tablet, iPhone, and iPad in planning. For native and desktop applications, respect the real declared targets without introducing out-of-scope ports.

Verification distinguishes `PASS`, `FAIL`, `NOT_RUN`, and `NOT_APPLICABLE`. Browser emulation, platform simulators, and physical devices are not treated as equivalent evidence. Structured reports do not by themselves certify accessibility or compatibility.

## Installation

From this directory, with Python 3.10 or newer:

```powershell
python .\scripts\check_package.py --verify-integrity
python .\scripts\manage_skills.py install
```

The second command is preview-only. To apply the installation, run `python .\scripts\manage_skills.py install --apply`. Close Codex sessions that use the skills before updating or removing the suite.

The default destination is `$HOME/.agents/skills`, as documented by [OpenAI Skills](https://developers.openai.com/codex/skills/). The installer uses verified copies rather than live links, so experimental repository changes do not become active across every session automatically. Updating requires a package check, a version change, and an explicit command.

## Structure

```text
Interface-Forge/
  skills/             five installable skills with references and templates
  contracts/          canonical rules replicated and checked inside the skills
  scripts/            installation, integrity, and packaging tools
  tests/              offline tests for repository tools
  evals/              Codex behavior and triggering cases
  docs/               installation, architecture, sources, validation, publishing
  licenses/           upstream MIT notice
  qa/                 recorded validation results for this package
```

## Documentation

[Windows installation](docs/INSTALL_WINDOWS.md) · [Codex usage](docs/CODEX_USAGE.md) · [Architecture](docs/ARCHITECTURE.md) · [Platform baseline](contracts/platform-baseline.md) · [Model evaluation](docs/EVALUATION_PLAN.md) · [GitHub publishing](docs/PUBLISH_GITHUB.md) · [Troubleshooting and recovery](docs/TROUBLESHOOTING.md) · [Provenance](docs/PROVENANCE.md) · [Sources](docs/SOURCES.md)

## Declared limitations

The suite guides agent behavior. It does not add an image generator, browser, emulator, or GPU. These rules are instructions, not a security sandbox. Implicit discovery depends on the host and model and must be tested. Brand templates are declarative, not a transactional database. The installation engine checks hashes and local drift, but the checksum is not a cryptographic publisher signature.

See [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES.md). No affiliation with the referenced organizations is implied.
