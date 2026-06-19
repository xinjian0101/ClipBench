import unittest
import main


class ClipBenchTest(unittest.TestCase):
    def test_perfect_match(self):
        truth = [{"start": 0, "end": 10}]
        predicted = [{"start": 0, "end": 10}]
        report = main.evaluate(truth, predicted)
        self.assertEqual(report["f1"], 1.0)
        self.assertEqual(report["mean_iou"], 1.0)


if __name__ == "__main__":
    unittest.main()
