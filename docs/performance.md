# Performance regression checks

Every Test and Release workflow compares the candidate's actual Rust `calculate`
command and JSON serialization with commit
`c212178debf19310ac238e705cffe3a40e13a81c` (the repaired 2.0.0 implementation).
The reference is pinned in `benchmarks/config.json`: moving `dev` or `main` does
not silently reset the budget and allow a series of small slowdowns to accumulate.

Both revisions are compiled with `cargo test --release --locked`, their own
Cargo manifests and lockfiles, and the same installed Rust toolchain. A shared
measurement harness is injected into temporary copies; it never replaces the
production calculation. This also catches dependency and release-profile changes.
Tauri assets are placeholders in these test executables because no window is
opened. Normal desktop builds and the Linux GUI smoke test remain separate checks.

The suite measures calculation at 1,000, 100,000, 1,000,000 and 10,000,000, and
serialization at 100,000 and 1,000,000. Known prime counts, largest primes and
ordering are verified before timing. Runtime startup and a 100 ms warmup are
excluded; allocations, calculation and result destruction are included. JSON
serialization measures the Rust serializer, not a full WebView IPC round trip.

On Linux, both binaries use the same CPU. Nine pairs of at least 300 ms are
measured, alternating baseline/candidate order to reduce thermal/order bias.
A workload fails if at least eight of nine pairs are more than 20% slower.
This intentionally tolerates isolated scheduling pauses on shared GitHub runners;
it is a practical noise filter, not a statistical confidence interval. Smaller
regressions, memory usage, startup time and frontend rendering are not gated by
these CPU benchmarks. Inspect the raw samples if the runner is unusually noisy.

The reusable build workflow includes the performance job, so the release upload
cannot run when it fails. JSON samples, compiler output and a Markdown comparison
are uploaded as `performance-results`; the comparison also appears in the job
summary. Compilation or measurement errors fail the job rather than accepting
missing data.

## Run locally

With Python 3.10+, Git, Rust and the normal Tauri native build dependencies:

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/benchmark.py
```

The candidate includes local Rust edits. The baseline commit must be available
locally (`git fetch --unshallow` in shallow clones). Results go to the ignored
`test-results/performance/` directory. `CARGO_TARGET_DIR` can point to an existing
Cargo cache. Linux is the CI measurement platform; other desktop platforms still
receive normal builds and correctness tests.

For a deliberate investigation, use `--baseline <commit>`. Update the pinned
baseline only in a reviewed task explaining the accepted performance tradeoff,
and retain the before/after report. Do not refresh it automatically after a merge.

## Branch workflow

Start each task from an up-to-date `dev` and create a dedicated branch. Commit
using English Conventional Commits without a parenthesized scope. Merge completed
tasks into `dev`, push to both remotes, and wait for its CI build and benchmarks.
Promote `dev` to `main` after the day's work has been declared complete and all
checks pass. Keep release tags on the validated `main` commit. Avoid force pushes
for routine integration; they are only needed for an explicitly agreed history
rewrite. Do not commit `RELEASE_PLAN.md`.
