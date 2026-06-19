from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean


def interval_iou(first: tuple[float, float], second: tuple[float, float]) -> float:
    intersection = max(0.0, min(first[1], second[1]) - max(first[0], second[0]))
    union = max(first[1], second[1]) - min(first[0], second[0])
    return intersection / union if union > 0 else 0.0


def evaluate(truth: list[dict], predicted: list[dict], threshold: float = 0.5) -> dict:
    truth_intervals = [(float(item["start"]), float(item["end"])) for item in truth]
    predicted_intervals = [(float(item["start"]), float(item["end"])) for item in predicted]
    used_truth: set[int] = set()
    matches: list[dict] = []

    for prediction_index, prediction in enumerate(predicted_intervals):
        candidates = [
            (interval_iou(prediction, target), truth_index)
            for truth_index, target in enumerate(truth_intervals)
            if truth_index not in used_truth
        ]
        best_iou, best_index = max(candidates, default=(0.0, -1))
        if best_iou < threshold:
            continue
        used_truth.add(best_index)
        target = truth_intervals[best_index]
        matches.append({
            "prediction": prediction_index,
            "truth": best_index,
            "iou": round(best_iou, 6),
            "boundary_error": round((abs(prediction[0] - target[0]) + abs(prediction[1] - target[1])) / 2, 6),
        })

    true_positive = len(matches)
    precision = true_positive / len(predicted_intervals) if predicted_intervals else 0.0
    recall = true_positive / len(truth_intervals) if truth_intervals else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0

    return {
        "threshold": threshold,
        "truth": len(truth_intervals),
        "predicted": len(predicted_intervals),
        "true_positive": true_positive,
        "false_positive": len(predicted_intervals) - true_positive,
        "false_negative": len(truth_intervals) - true_positive,
        "precision": round(precision, 6),
        "recall": round(recall, 6),
        "f1": round(f1, 6),
        "mean_iou": round(mean(item["iou"] for item in matches), 6) if matches else 0.0,
        "mean_boundary_error": round(mean(item["boundary_error"] for item in matches), 6) if matches else None,
        "matches": matches,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate predicted highlight intervals.")
    parser.add_argument("truth")
    parser.add_argument("predicted")
    parser.add_argument("-o", "--output", default="clip-bench-report.json")
    parser.add_argument("--threshold", type=float, default=0.5)
    args = parser.parse_args()
    truth = json.loads(Path(args.truth).read_text(encoding="utf-8"))
    predicted = json.loads(Path(args.predicted).read_text(encoding="utf-8"))
    report = evaluate(truth, predicted, args.threshold)
    Path(args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"F1={report['f1']} precision={report['precision']} recall={report['recall']}")


if __name__ == "__main__":
    main()
