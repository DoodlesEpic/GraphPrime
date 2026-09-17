# Continuous integration

`Test` runs on pushes to internal branches. Pull requests from forks also run it;
internal pull requests skip the build because their commits were tested on push.
The merge into `dev` is tested again to verify the integrated code. A skipped PR
workflow can still appear in GitHub, but does not allocate the desktop build or
performance runners. Dependency Review runs separately on all pull requests.

New pushes cancel obsolete Test runs for the same branch or pull request. Release
runs have a separate concurrency group and are never cancelled by Test.

The shared build workflow packages Linux, Windows and both macOS architectures.
Tauri's `beforeBuildCommand` builds the frontend once; Rust tests run afterwards
so the embedded assets exist. Linux additionally requires Rust formatting, Clippy,
and the packaged AppImage GUI smoke test. Performance comparisons run in a separate
job and must pass before a release can upload packages.

External actions are pinned to commit SHAs with version comments. Update the SHA
and comment together after checking the upstream release notes.

## CodeQL

`.github/workflows/codeql.yml` is the sole CodeQL configuration; GitHub's automatic
(default) setup is disabled. It analyzes Rust, JavaScript/TypeScript, Python and
GitHub Actions on pushes to `dev`/`main`, pull requests targeting either branch,
and weekly once the workflow reaches the default branch. Manual dispatch is also
available once the workflow is on the default branch.

Use the standard `default` query suite for precise security findings. CodeQL
complements ESLint, Clippy and dependency review. Its PR merge analysis is
intentional and independent of the Test workflow's push-based build checks.

Rust uses `build-mode: none` and requires Cargo and rustup. CodeQL still executes
build scripts and compiles macros through rust-analyzer; the Rust job installs
Tauri's native build-script dependencies without building desktop packages.

Check the code-scanning tool status page for extraction errors and actual files
analyzed, not just a green job or zero alerts. The supported-language documentation
does not list `.svelte`; JavaScript/TypeScript analysis is not complete coverage of
Svelte components or Tauri IPC. No custom extractors or generated bundles are added.

Sources: [setup types](https://docs.github.com/en/code-security/concepts/code-scanning/setup-types),
[query suites](https://docs.github.com/en/code-security/concepts/code-scanning/codeql/codeql-query-suites),
[Rust requirements](https://docs.github.com/en/code-security/reference/code-scanning/codeql/build-options-for-compiled-languages#building-rust),
[evaluating coverage](https://docs.github.com/en/code-security/tutorials/customize-code-scanning/evaluate-default-setup).
