# Dependency maintenance

Update `@tauri-apps/api` and the Rust `tauri` crate together on the same minor
release. Keep the JavaScript and Rust clipboard plugins on the same exact version.
Commit both lockfiles and use immutable/locked installs in CI. Avoid prereleases
and dependency overrides that bypass upstream compatibility requirements.

Rust 1.98.1 is pinned in `rust-toolchain.toml` and the CI toolchain inputs. Update
both when changing the compiler so local builds, benchmarks and CodeQL agree.

## Audit after the September 2026 update

`yarn npm audit --all --recursive` reports no advisories. `cargo audit` reports no
entries in its vulnerability list, but retains these upstream warnings:

| Crates                                                                                       | Advisory                                                                   | Status                                                                                                                          |
| -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `glib` 0.18.5                                                                                | [RUSTSEC-2024-0429](https://rustsec.org/advisories/RUSTSEC-2024-0429.html) | Unsound iterator implementation in the GTK dependency line used by Tauri; the application does not directly call this iterator. |
| `proc-macro-error` 1.0.4                                                                     | [RUSTSEC-2024-0370](https://rustsec.org/advisories/RUSTSEC-2024-0370.html) | Unmaintained transitive dependency.                                                                                             |
| `unic-char-property`, `unic-char-range`, `unic-common`, `unic-ucd-ident`, `unic-ucd-version` | RUSTSEC-2025-0081, 0075, 0080, 0100, 0098                                  | Unmaintained transitive dependencies.                                                                                           |

These warnings are not suppressed. Recheck upstream Tauri/GTK compatibility on
future upgrades; forcing a different GTK/GLib major is not a compatible lockfile
update. A clean vulnerability count is not a claim that all dependencies are
maintained or free of soundness issues.

The update removes the previously reported `quick-xml` vulnerabilities, the
`anyhow` and `rand` soundness warnings, and yanked versions. Repeat both audits
before publishing because advisory data changes independently of the lockfiles.
