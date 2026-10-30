# Releasing

## Prepare

1. Confirm that the user requested publication to the existing public repository.
2. Set the same version in skill metadata, its Version section and the README.
3. Add a changelog entry and `.github/RELEASE_NOTES_<version>.md`, using
   [.github/RELEASE_TEMPLATE.md](../.github/RELEASE_TEMPLATE.md).
4. Review staged files for private paths, secrets and unrelated local evidence.
5. Run distribution validation, validator regression tests, Markdown lint and the temporary installation test
   documented in [CONTRIBUTING.md](../CONTRIBUTING.md). For behavior changes,
   exercise the relevant disposable scenarios in [validation.md](validation.md).

## Publish

Push the reviewed commit only within the user's authorization and confirm that
its exact revision passes hosted CI. Create an annotated `v<version>` tag pointing
to that commit and publish a GitHub Release with the committed release notes.
Do not move an existing published tag; correct the problem in a later version.

For the initial release, the commands are:

```sh
git tag -a v0.1.0 -m 'Release v0.1.0'
git push origin v0.1.0
gh release create v0.1.0 --verify-tag --title 'v0.1.0 - Safe post-merge task closure' --notes-file .github/RELEASE_NOTES_0.1.0.md
```

Confirm the tag target, public release URL and published notes after creation.
Verify remote-source discovery and complete installed payloads with:

```sh
python3 scripts/smoke_install.py --source rgmez/cleanup-worktree
```

Use `--source https://github.com/rgmez/cleanup-worktree/tree/v0.1.0` to check the
versioned source. Document tested source forms only after the CLI accepts them.
Installer checks do not prove skills.sh catalogue indexing. Tests disable
telemetry and do not modify global installations or pinned automations.
