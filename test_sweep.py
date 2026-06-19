import json
import tempfile
import unittest
from pathlib import Path

import main


class ClipBenchSweepTest(unittest.TestCase):
    def test_invalid_interval_is_rejected(self):
        with self.assertRaises(ValueError):
            main.evaluate([{"start": 5, "end": 4}], [])

    def test_invalid_threshold_is_rejected(self):
        with self.assertRaises(ValueError):
            main.evaluate([], [], threshold=1.1)

    def test_threshold_sweep_is_sorted_and_unique(self):
        truth = [{"start": 0, "end": 10}]
        predicted = [{"start": 1, "end": 9}]
        report = main.evaluate_sweep(truth, predicted, [0.7, 0.3, 0.7, 0.5])
        self.assertEqual(report["thresholds"], [0.3, 0.5, 0.7])
        self.assertEqual(len(report["results"]), 3)
        self.assertEqual(report["best_f1"]["f1"], 1.0)

    def test_loader_requires_json_array(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "truth.json"
            path.write_text(json.dumps({"start": 0, "end": 10}), encoding="utf-8")
            with self.assertRaises(ValueError):
                main.load_intervals(str(path), "truth")

    def test_empty_inputs_have_defined_metrics(self):
        report = main.evaluate([], [])
        self.assertEqual(report["precision"], 0.0)
        self.assertEqual(report["recall"], 0.0)
        self.assertEqual(report["f1"], 0.0)
        self.assertIsNone(report["mean_boundary_error"])


if __name__ == "__main__":
    unittest.main()
