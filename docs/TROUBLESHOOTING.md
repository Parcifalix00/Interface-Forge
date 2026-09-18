# Troubleshooting, stop conditions, and recovery

## Python is unavailable

Check `python --version` and, on Windows, `py -3 --version`. If neither resolves to Python 3.10+, do not run the scripts. Manual installation of the five directories is possible, but it gives up the documented managed-update and rollback behavior. No script downloads Python or other packages.

## Skill collision

One of the five target directories already exists without manager ownership state. It may be a manual copy or a different skill with the same name. Inspect and compare its contents. Do not delete it, create fake ownership state, or rename it blindly. Archive or move the previous installation only after identifying it.

## Local drift

Installed files or directories no longer match the recorded state. The manager stops to avoid losing changes. Compare the runtime copy with the source project, transfer intentional edits back into the project, and restore a known copy only after review. Even an added file may be significant. There is no `--force` mode.

## Release integrity is not confirmed

The ZIP may be incomplete or files may have changed after packaging. Do not regenerate the manifest only to silence the error. Compare against the original release. For intentional changes, update version, tests, documentation, and validation records, then use the normal development and packaging process.

## Links, junctions, or cloud-sync reparse points

The manager rejects reparse points in managed paths to avoid ambiguous destinations. Some filesystem or cloud setups may use them. Identify a physical destination that the active Codex host really reads. Do not disable protections or remove existing links automatically.

## Lock after an interruption

`status` reports the state directory and whether a lock exists. A lock may belong to an operation that is still running. Check the process and close sessions that may be modifying the suite. Only after confirming that no operation is active should you manually remove that exact `operation.lock`. The manager does not delete locks based on PID guesses.

If `pending.json` exists, do not delete it. First run `python .\scripts\manage_skills.py recover` for a preview, then run the same command with `--apply`. Recovery uses the previous snapshot and refuses unrelated content. If recovery fails, preserve the complete state directory, backups, and skill directories. Do not attempt recursive cleanup.

A simulated failure test does not prove recovery from every power, disk, or antivirus failure. If storage is damaged, inspect the environment rather than repeatedly forcing the manager.

## Codex cannot see the skills

Verify that each skill has `SKILL.md` directly inside its directory under the target, not two levels down. Open a new session or restart Codex. Check for disabled or duplicate skills in other scopes using the existing configuration. Do not edit `config.toml` blindly.

## iOS QA is incomplete

If no iPhone/iPad or Apple simulator is available, checks that require them are `NOT_RUN`. WebKit browser emulation is useful evidence but remains a different method. Do not change `allowed_methods` after testing only to produce a green report.

## Undeclared files in the installation payload

The installer does not copy caches or other manifest-excluded files into skills. If this error appears, compare the source directory with the release and start again from a clean extraction. Do not disable the check or rebuild the manifest just to include unknown files. The provided tests avoid creating bytecode inside skill directories.
