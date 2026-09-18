# Instructions for working on the Interface Forge repository

These instructions apply to this repository only. They are not installed globally.

- Keep the five skills and their separation. Do not add mandatory providers, costs, network access, imposed stacks, fonts, or private material.
- Do not introduce U+2014 in authored text. Preserve license notices and sources. Do not copy entire third-party skills without an audit and a compatible license.
- Respect the workflow requested by the user: no implicit commit, push, or deploy. When contracts change, update every canonical copy and verify that they remain identical.
- Do not rewrite historical QA results to make them look recent. Re-run tests and record the environment, checks performed, and limitations. Do not claim triggering or device compatibility without evidence.
- The manager must keep preview as the default, ownership tracking, drift detection, backups outside the skill discovery path, no `--force`, and no deletion of unrelated directories.
- Use only the Python standard library for repository tools. Run `python scripts/check_package.py` and `python -m unittest discover -s tests -v`. Also verify on Windows before claiming Windows validation.
- For a new release, update VERSION, suite.json, metadata for all five skills, the changelog, documentation, and validation results. Then regenerate the manifest and ZIP with `scripts/build_release.py`. Do not regenerate hashes to hide unexpected changes.
