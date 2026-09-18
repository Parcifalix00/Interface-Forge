# Installation and maintenance on Windows

## Requirements and boundaries

Python 3.10+ is required for checks and managed installation. PowerShell is only one possible terminal. The `.ps1` wrappers are optional. Codex must already be available in order to use the skills. You do not need pip/npm, a Higgsfield account, API keys, graphics tools, or administrator privileges.

The package does not change PowerShell execution policy. If a wrapper is blocked, run the Python command directly. There is no need to weaken a system protection. Windows wrapper checks are separate from validation of the Python engine on Linux.

Install the suite in the environment where Codex runs. Windows and WSL use different home directories and filesystems. A copy in the Windows home directory is not evidence that the Linux home can see it. Do not duplicate installation until you know which host is active.

## Strategy: verified copies

The project directory contains the source. The runtime receives five verified copies. Do not edit those installed copies for development. Doing so creates runtime drift and causes the manager to block the next update.

This strategy avoids symlink/junction requirements on Windows and prevents unverified repository edits from becoming active immediately. The tradeoff is an explicit update after each release. It is not continuous synchronization and it does not create a second source of truth.

The manager rejects links, junctions, and other reparse points inside managed paths. If a path is an alias or reparse point, use an appropriate physical directory after inspecting your local setup. Do not remove a link blindly.

## Checks and installation

From the project root:

```powershell
python .\scripts\check_package.py --verify-integrity
python -m unittest discover -s tests -v
python .\scripts\manage_skills.py install
python .\scripts\manage_skills.py install --apply
python .\scripts\manage_skills.py status
```

Preview mode and `status` are read-only. Do not add `--apply` until the preview shows the intended destination. `--target` allows an explicit directory, for example a repository-specific `.agents/skills` directory when limited scope is genuinely desired. Use the same target for updates, uninstall, and restore operations.

The default is `$HOME/.agents/skills`, following [OpenAI Skills](https://developers.openai.com/codex/skills/). The installed directories are exactly the five entries in `suite.json`. Do not place the entire Interface-Forge repository under `skills`.

## Manual installation

You may copy the five directories under `skills/` into the destination without overwriting existing directories. Keep all files and licenses. Manual installation does not create manager state, so managed update/removal will not recognize those copies and will stop on collision. Choose one installation mode. Managed installation is the documented path for rollback support.

## Updating

Close sessions that are reading the suite. Extract the new complete release into a separate directory, validate it, and run from that directory:

```powershell
python .\scripts\check_package.py --verify-integrity
python .\scripts\manage_skills.py update
python .\scripts\manage_skills.py update --apply
```

An update requires a higher version when content changes. Reapplying the same release is idempotent. Downgrades use a verified backup, not `--force`. The manager blocks any local difference in the five installed directories, including added, missing, or modified files. Reconcile intentional changes back into the source project before proceeding.

## Backups and rollback

State is stored under a sibling directory: `<target-parent>/.interface-forge/<target-id>/`. It is outside `skills`, so backups are not exposed as additional skills. Every mutating operation preserves the previous snapshot and prints its backup ID.

```powershell
python .\scripts\manage_skills.py backups
python .\scripts\manage_skills.py restore --backup-id REAL_BACKUP_ID
python .\scripts\manage_skills.py restore --backup-id REAL_BACKUP_ID --apply
```

Replace the placeholder with an ID returned by `backups`. The backup created before first installation represents the previous empty state, so restoring it removes the suite. A backup created before an update contains the previous version. A backup created before uninstall can reinstall that version.

Backups remain local and are not deleted automatically, including after uninstall. Archive or remove them manually only after confirming that they are no longer needed. Do not publish them as part of the repository.

## Uninstalling

```powershell
python .\scripts\manage_skills.py uninstall
python .\scripts\manage_skills.py uninstall --apply
```

The manager removes only the five recognized, unmodified skill directories while preserving a snapshot and all unrelated skills. If drift exists, it stops instead of discarding local changes. Restart Codex or open a new session after installation, update, or removal.

## Interrupted operations

Replacing five directories is not globally atomic. The manager uses staging, a journal, snapshots, and exception recovery. A process crash or system shutdown may leave a lock or journal that must be inspected. See [TROUBLESHOOTING](TROUBLESHOOTING.md). The package does not claim proven resilience against disk failure or power loss on Windows.

## Optional wrappers

`install-windows.ps1`, `update-windows.ps1`, `uninstall-windows.ps1`, and `status-windows.ps1` call the same Python engine. Preview is the default. `-Apply` enables the action. They support `-Target` and a `-Python` executable. Calling Python directly avoids any dependency on PowerShell execution policy.
