#!/usr/bin/env python3
"""Compare real Rust commands from two revisions, on one CPU, in release mode."""
import argparse
import io
import json
import math
import os
from pathlib import Path
import platform
import shutil
import statistics
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def command(args, **kwargs):
    return subprocess.check_output(args, text=True, **kwargs).strip()


def validate_config(config):
    if not isinstance(config["rounds"], int) or config["rounds"] < 5:
        raise ValueError("At least five rounds are required")
    if not 100 <= config["sample_ms"] <= 10000:
        raise ValueError("Sample duration must be between 100 and 10000 ms")
    if not 0 < config["max_slowdown"] < 1:
        raise ValueError("Slowdown budget must be between zero and one")
    if not config["cases"]:
        raise ValueError("At least one workload is required")
    keys = [(case["operation"], case["limit"]) for case in config["cases"]]
    if len(set(keys)) != len(keys):
        raise ValueError("Duplicate workloads are not allowed")


def assess(baseline, candidate, max_slowdown):
    if len(baseline) != len(candidate) or len(baseline) < 5:
        raise ValueError("At least five paired samples are required")
    if any(not math.isfinite(x) or x <= 0 for x in baseline + candidate):
        raise ValueError("Measurements must be finite and positive")
    ratios = [new / old for old, new in zip(baseline, candidate)]
    # Allow one noisy pair; a single scheduling pause must not fail a release.
    regression = sum(r > 1 + max_slowdown for r in ratios) >= len(ratios) - 1
    return {"baseline_ns": statistics.median(baseline),
            "candidate_ns": statistics.median(candidate),
            "slowdown": statistics.median(ratios) - 1,
            "regression": regression, "ratios": ratios}


def prepare(destination, revision=None):
    if revision:
        archive = subprocess.check_output(["git", "archive", revision], cwd=ROOT)
        with tarfile.open(fileobj=io.BytesIO(archive)) as source:
            # Git archives contain only repository paths. Python 3.10 CI support.
            source.extractall(destination)
    else:
        # Include working-tree edits for local runs, but never copy .git or targets.
        shutil.copytree(ROOT / "src-tauri", destination / "src-tauri",
                        ignore=shutil.ignore_patterns("target"))
    # Assets are not exercised by this CPU benchmark. Tauri's compile-time
    # context still needs an asset directory; no JS toolchain is necessary here.
    assets = destination / "public/build"
    assets.mkdir(parents=True, exist_ok=True)
    (assets / "index.html").write_text("<!doctype html><title>Benchmark</title>")
    main = destination / "src-tauri/src/main.rs"
    with main.open("a") as output:
        output.write('\n#[cfg(test)]\n#[path = "benchmark_harness.rs"]\nmod performance;\n')
    shutil.copyfile(ROOT / "benchmarks/harness.rs", main.with_name("benchmark_harness.rs"))


def build(source, target, binary, log):
    env = dict(os.environ, CARGO_TARGET_DIR=str(target))
    args = ["cargo", "test", "--release", "--locked", "--no-run", "--bin", "app",
            "--manifest-path", str(source / "src-tauri/Cargo.toml"),
            "--message-format=json-render-diagnostics"]
    with log.open("w") as output:
        subprocess.run(args, env=env, stdout=output, check=True)
    artifacts = [json.loads(line) for line in log.read_text().splitlines() if line.startswith("{")]
    executables = [a["executable"] for a in artifacts
                   if a.get("reason") == "compiler-artifact" and a.get("executable")
                   and a.get("profile", {}).get("test") and a["target"]["name"] == "app"]
    if len(executables) != 1:
        raise RuntimeError("Expected exactly one application test executable")
    shutil.copy2(executables[0], binary)


def measure(binary, case, sample_ms):
    env = dict(os.environ, GRAPHPRIME_BENCH_LIMIT=str(case["limit"]),
               GRAPHPRIME_BENCH_OPERATION=case["operation"], GRAPHPRIME_BENCH_MS=str(sample_ms))
    output = command([str(binary), "--exact", "performance::sample", "--ignored", "--nocapture"],
                     env=env, timeout=120)
    records = [json.loads(line.split("GRAPHPRIME_BENCH ", 1)[1])
               for line in output.splitlines() if "GRAPHPRIME_BENCH " in line]
    if len(records) != 1:
        raise RuntimeError(f"Missing benchmark measurement: {output}")
    return records[0]["ns_per_iteration"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", help="Override the pinned baseline for a deliberate comparison")
    parser.add_argument("--output", type=Path, default=ROOT / "test-results/performance")
    args = parser.parse_args()
    config = json.loads((ROOT / "benchmarks/config.json").read_text())
    validate_config(config)
    baseline = command(["git", "rev-parse", "--verify", (args.baseline or config["baseline"]) + "^{commit}"], cwd=ROOT)
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    report = {"baseline": baseline, "candidate": command(["git", "rev-parse", "HEAD"], cwd=ROOT),
              "dirty": bool(command(["git", "status", "--porcelain"], cwd=ROOT)),
              "platform": platform.platform(), "rustc": command(["rustc", "-Vv"]),
              "config": config, "results": []}
    # Compile with all available CPUs; pin only the subsequent measurements.
    target = Path(os.environ.get("CARGO_TARGET_DIR", ROOT / "src-tauri/target")).resolve()
    with tempfile.TemporaryDirectory(prefix="graphprime-benchmark-") as temporary:
        work = Path(temporary)
        binaries = {}
        for label, revision in [("baseline", baseline), ("candidate", None)]:
            print(f"Building {label} in release mode...", flush=True)
            source = work / label
            source.mkdir()
            prepare(source, revision)
            binaries[label] = work / f"{label}-benchmark"
            build(source, target, binaries[label], output / f"{label}-build.jsonl")
        if hasattr(os, "sched_getaffinity"):
            cpu = min(os.sched_getaffinity(0))
            os.sched_setaffinity(0, {cpu})
            report["cpu"] = cpu
        for case in config["cases"]:
            samples = {"baseline": [], "candidate": []}
            for iteration in range(config["rounds"]):
                order = ["baseline", "candidate"] if iteration % 2 == 0 else ["candidate", "baseline"]
                for label in order:
                    samples[label].append(measure(binaries[label], case, config["sample_ms"]))
            result = dict(case, **assess(samples["baseline"], samples["candidate"], config["max_slowdown"]), samples=samples)
            report["results"].append(result)
            print(f'{case["operation"]}/{case["limit"]}: {result["slowdown"]:+.1%}'
                  f' {"FAIL" if result["regression"] else "PASS"}', flush=True)
    (output / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    lines = ["## Performance comparison", "", f"Baseline: `{baseline}`", "",
             "| Workload | Baseline (ms) | Candidate (ms) | Change | Result |",
             "| --- | ---: | ---: | ---: | --- |"]
    for result in report["results"]:
        lines.append(f'| {result["operation"]}/{result["limit"]} | {result["baseline_ns"] / 1e6:.3f} '
                     f'| {result["candidate_ns"] / 1e6:.3f} | {result["slowdown"]:+.1%} '
                     f'| {"FAIL" if result["regression"] else "PASS"} |')
    summary = "\n".join(lines) + "\n"
    (output / "summary.md").write_text(summary)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as stream:
            stream.write(summary)
    return int(any(result["regression"] for result in report["results"]))


if __name__ == "__main__":
    raise SystemExit(main())
