"""Verify the release gate accepts noise and rejects sustained regressions."""
import importlib.util
import json
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location(
    "benchmark", Path(__file__).resolve().parents[1] / "scripts/benchmark.py"
)
benchmark = importlib.util.module_from_spec(spec)
spec.loader.exec_module(benchmark)


class RegressionGateTests(unittest.TestCase):
    def test_invalid_configuration_cannot_disable_the_gate(self):
        config = json.loads((benchmark.ROOT / "benchmarks/config.json").read_text())
        benchmark.validate_config(config)
        for key, value in [("rounds", 0), ("sample_ms", 0), ("max_slowdown", float("nan")),
                           ("max_slowdown", 1), ("cases", [])]:
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                benchmark.validate_config(dict(config, **{key: value}))

    def test_equal_performance_and_improvements_pass(self):
        for candidate in ([100] * 9, [70] * 9):
            self.assertFalse(benchmark.assess([100] * 9, candidate, 0.2)["regression"])

    def test_sustained_slowdown_fails(self):
        self.assertTrue(benchmark.assess([100] * 9, [130] * 9, 0.2)["regression"])

    def test_one_scheduling_pause_does_not_fail(self):
        self.assertFalse(benchmark.assess([100] * 9, [100] * 8 + [500], 0.2)["regression"])

    def test_one_fast_outlier_does_not_hide_a_regression(self):
        self.assertTrue(benchmark.assess([100] * 9, [130] * 8 + [80], 0.2)["regression"])

    def test_invalid_measurements_fail_closed(self):
        for samples in ([0] * 9, [float("nan")] * 9, [float("inf")] * 9, [100] * 4):
            with self.assertRaises(ValueError):
                benchmark.assess([100] * len(samples), samples, 0.2)

    def test_pairing_accounts_for_shared_machine_speed_changes(self):
        baseline = [100, 200, 100, 200, 100, 200, 100, 200, 100]
        self.assertFalse(benchmark.assess(baseline, [x * 1.05 for x in baseline], 0.2)["regression"])


if __name__ == "__main__":
    unittest.main()
