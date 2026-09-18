# Interface Forge: getting started

## 1. Keep the complete project

Extract the ZIP. The project directory is the one containing `suite.json`, `README.md`, `scripts`, and `skills`. You may rename or move it, for example to `Documents/Interface-Forge`. Do not copy only the five `SKILL.md` files. Their references, templates, metadata, and license notices are part of the package.

GitHub is not required to begin. Nothing in the package publishes content automatically.

## 2. Check before installing

Open PowerShell in the project directory. These commands do not require administrator privileges:

```powershell
python --version
python .\scripts\check_package.py --verify-integrity
python -m unittest discover -s tests -v
python .\scripts\manage_skills.py install
```

Python 3.10 or newer is required. If `python` does not resolve to an interpreter but `py -3` does, use `py -3` instead of `python` in the commands. Do not install Python packages. The tools use only the standard library.

The last command shows the destination and five skill directories without writing anything. If it reports collisions, unconfirmed integrity, or local modifications, stop. Do not delete directories just to bypass the safeguard.

## 3. Install after reviewing the preview

```powershell
python .\scripts\manage_skills.py install --apply
python .\scripts\manage_skills.py status
```

The manager copies the suite into `$HOME/.agents/skills`. It does not modify `AGENTS.md`, `config.toml`, the PowerShell profile, system settings, or other skills. State and backups are stored in a sibling directory outside the path scanned for skills.

## 4. Add the recommended global routing rule

If you use other frontend skills, manually merge the block in [AGENTS_SNIPPET](docs/AGENTS_SNIPPET.md) into your global `AGENTS.md` or another instruction level that should apply. Do not replace existing rules. The block makes Interface Forge the first UI coordinator, leaves specialist implementation work to technical skills, and makes the no em dash rule persistent.

This integration is intentionally manual. The installer does not edit `AGENTS.md`.

## 5. Verify in Codex

Open a new session or restart Codex. Look for `interface-forge` in the skill selector. In supported CLI or extension surfaces, you can use `$interface-forge` or `/skills`. The format and locations are documented by [OpenAI](https://developers.openai.com/codex/skills/).

Recommended settings for the first verification: **Plan Mode: No. Pursue Goal: No. Commit: No.**

```text
$interface-forge Verify that the suite is available without modifying the project. Read the shared contract and locate the real paths of the four specialist skills. Tell me which files you actually read, how you would coordinate a UI change, and which testing tools are available. Do not install anything, make paid calls, or commit changes.
```

This checks discovery and file loading, not UI quality. For implicit triggering and Android/iOS cases, use [EVALUATION_PLAN](docs/EVALUATION_PLAN.md) in a disposable test directory.

## 6. Continue using the suite

For installation, updates, removal, and rollback, see [INSTALL_WINDOWS](docs/INSTALL_WINDOWS.md). For results actually observed on this package, see [VALIDATION](docs/VALIDATION.md).
