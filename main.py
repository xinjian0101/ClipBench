from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from statistics import mean


def validate_interval(item: dict, index: int, source: str) -> tuple[float, float]:
    if not isinstance(item, dict):
        raise ValueError(f"{source} interval {index} must be an object")
    if "start" not in item or "end" not in item:
        raise ValueError(f"{source} interval {index} requires start and end")
    try:
        start = float(item["start"])
        end = float(item["end"])
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{source} interval {index} must use numeric boundaries") from exc
    if not math.isfinite(start) or not math.isfinite(end):
        raise ValueError(f"{source} interval {index} boundaries must be finite")
    if start < 0:
        raise ValueError(f"{source} interval {index} start must be non-negative")
    if end <= start:
        raise ValueError(f"{source} interval {index} end must be greater than start")
    return start, end


def validate_threshold(threshold: float) -> float:
    value = float(threshold)
    if not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError("IoU threshold must be between 0 and 1")
    return value


def interval_iou(first: tuple[float, float], second: tuple[float, float]) -> float:
    intersection = max(0.0, min(first[1], second[1]) - max(first[0], second[0]))
    union = max(first[1], second[1]) - min(first[0], second[0])
    return intersection / union if union > 0 else 0.0


def evaluate(truth: list[dict], predicted: list[dict], threshold: float = 0.5) -> dict:
    threshold = validate_threshold(threshold)
    truth_intervals = [validate_interval(item, index, "truth") for index, item in enumerate(truth)]
    predicted_intervals = [validate_interval(item, index, "prediction") for index, item in enumerate(predicted)]
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
        "result_version": 1,
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


def evaluate_sweep(truth: list[dict], predicted: list[dict], thresholds: list[float]) -> dict:
    if not thresholds:
        raise ValueError("At least one threshold is required")
    normalized = sorted(set(validate_threshold(value) for value in thresholds))
    results = [evaluate(truth, predicted, threshold) for threshold in normalized]
    return {
        "sweep_version": 1,
        "thresholds": normalized,
        "results": results,
        "best_f1": max(results, key=lambda item: (item["f1"], -item["threshold"])),
    }


def load_intervals(path: str, source: str) -> list[dict]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, list):
        raise ValueError(f"{source} file must contain a JSON array")
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate predicted highlight intervals.")
    parser.add_argument("truth")
    parser.add_argument("predicted")
    parser.add_argument("-o", "--output", default="clip-bench-report.json")
    parser.add_argument("--threshold", type=float, default=0.5)
    parser.add_argument("--thresholds", help="Comma-separated IoU thresholds for a sweep")
    args = parser.parse_args()
    truth = load_intervals(args.truth, "truth")
    predicted = load_intervals(args.predicted, "prediction")
    if args.thresholds:
        thresholds = [float(item.strip()) for item in args.thresholds.split(",") if item.strip()]
        report = evaluate_sweep(truth, predicted, thresholds)
        message = f"Evaluated {len(report['results'])} thresholds; best F1={report['best_f1']['f1']}"
    else:
        report = evaluate(truth, predicted, args.threshold)
        message = f"F1={report['f1']} precision={report['precision']} recall={report['recall']}"
    Path(args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(message)


if __name__ == "__main__":
    main()
