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

## CodeQL review (September 2026)

Keep GitHub's default setup as the only CodeQL configuration, with its weekly
schedule. It currently analyzes JavaScript/TypeScript, Python and GitHub Actions.
The recent analyses completed without errors or findings. The September 15 run
completed in approximately 81 seconds; this does not justify removing the check.
CodeQL complements ESLint, Clippy and dependency review rather than replacing them.

The current [supported languages documentation](https://codeql.github.com/docs/codeql-overview/supported-languages-and-frameworks/)
includes Rust editions 2021 and 2024. However, on September 17, 2026, this repository's
`PATCH /repos/DoodlesEpic/GraphPrime/code-scanning/default-setup` endpoint rejected
`rust` with HTTP 422, including with API version `2026-03-10`. The existing setup
was preserved. This is an API limitation observed here, not a lack of CodeQL
support: GitHub [announced general availability](https://github.blog/changelog/2025-10-14-codeql-scanning-rust-and-c-c-without-builds-is-now-generally-available/)
for Rust in both setup modes in October 2025. The REST documentation also omits
Rust from the language enum. The documented UI path is Settings → Advanced
Security → CodeQL analysis → View CodeQL configuration → Edit → Languages.
Select Rust there when available, then verify the resulting analysis. Do not
create a second CodeQL workflow alongside default setup. Rust currently has
mandatory Clippy, correctness tests and performance checks, not CodeQL coverage.

The same documentation does not list `.svelte` files. Do not interpret successful
JavaScript/TypeScript analysis as complete coverage of Svelte components or Tauri
IPC. No custom extractors or generated frontend bundles are added for this purpose.

Default setup is managed in GitHub's code-scanning settings, not in a repository
workflow. Its platform-managed triggers are independent of the Test deduplication
policy. Review its languages, coverage and duration there when changing the setup.

## CodeQL configuration practices

- Prefer default setup for this small repository; GitHub recommends advanced setup
  when the default configuration does not meet a concrete requirement.
- Keep the `default` query suite for high precision. `security-extended` adds
  lower-confidence queries and may produce more false positives; it is not a
  prerequisite for enabling Rust.
- Rust uses `build-mode: none`, requires Cargo and rustup, and uses rust-analyzer
  to execute build scripts and compile macros. It does not require a full desktop
  package build. Inspect extraction diagnostics for Tauri's build script/macros.
- Check the tool status page for files analyzed and errors, not just a green job
  or zero alerts. Record coverage limitations before claiming language coverage.
- Preserve CodeQL's PR integration analysis independently of Test's push checks.
  Default setup targets the default/protected branches and runs weekly; `dev` is
  currently unprotected, so its PRs are not automatically covered by this policy.
  Changing branch protection is a separate repository-policy decision.
- Keep analysis up to date through the managed setup. Never run default and
  advanced setup concurrently or suppress findings merely to obtain green CI.

Sources: [setup types](https://docs.github.com/en/code-security/concepts/code-scanning/setup-types),
[query suites](https://docs.github.com/en/code-security/concepts/code-scanning/codeql/codeql-query-suites),
[Rust requirements](https://docs.github.com/en/code-security/reference/code-scanning/codeql/build-options-for-compiled-languages#building-rust),
[evaluating coverage](https://docs.github.com/en/code-security/tutorials/customize-code-scanning/evaluate-default-setup).
