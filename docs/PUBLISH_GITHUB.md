# Publishing the repository from your PC

Publishing is manual and separate from installation. The package contains no GitHub tokens, does not call GitHub, and has no push-triggered publishing workflow.

## Preparation

Use the complete project directory, not runtime copies under `.agents/skills`. Run checks and tests, then review the files. Do not add project screenshots or logs, keys, `.env` files, local backups, or font files. `qa/local/` is excluded from Git. The distributed report under `qa/` concerns only the Interface Forge package.

For the CLI path, Git and GitHub CLI must already be available. Check `git --version`, `gh --version`, and `gh auth status`. If GitHub CLI is not authenticated, use `gh auth login` on your PC without pasting credentials into chat. For repository creation and push behavior, use the [official manual](https://cli.github.com/manual/gh_repo_create).

## Initialize the local repository

Only if the directory is not already a repository:

```powershell
if (Test-Path .git) { throw "Repository already exists. Inspect its state before reinitializing it." }
git init -b main
git config user.name "Parcifalix00"
git config --get user.email
```

The name is configured only for this repository. If the email is not configured or you do not want to publish it, stop and set the correct GitHub noreply address from your account settings. Do not invent an address. Git publishes author and committer metadata with commits.

## Controlled staging

```powershell
git add -- .gitattributes .gitignore AGENTS.md CHANGELOG.md LICENSE README.md START_HERE.md THIRD_PARTY_NOTICES.md VERSION suite.json release-manifest.json contracts docs evals licenses qa scripts skills tests
git diff --cached --check
git diff --cached --stat
git status --short
```

If any command reports a problem, stop. Inspect `git diff --cached` and review everything that will become public. Do not run `git add .` after copying personal logs or other local material into the project directory.

After review:

```powershell
git commit -m "Add Interface Forge v1.0.0"
git status --short
```

## Create the remote repository

Use `gh auth status` to confirm which account is active. Verify that there is no existing repository named `Interface-Forge` that should be preserved. The following command creates a public repository from the current local project and pushes the existing commit:

```powershell
gh repo create Interface-Forge --public --source . --remote origin --push
```

If the name already exists, do not create random duplicates and do not force-push. Inspect the existing repository first. Alternatively, create an empty public repository on GitHub without an initial README or license, then connect it using the commands GitHub shows for your real repository URL.

## After the push

Check the repository structure, README, licenses, and version on GitHub. You may keep the release ZIP and checksum as release artifacts, but they are not required for local operation. For future development, read `AGENTS.md` and [EVALUATION_PLAN](EVALUATION_PLAN.md).

