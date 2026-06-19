from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path
from statistics import mean

import main


def load_manifest(path: str) -> tuple[dict, Path]:
    manifest_path = Path(path)
    value = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("Benchmark manifest must be a JSON object")
    items = value.get("items")
    if not isinstance(items, list) or not items:
        raise ValueError("Benchmark manifest requires a non-empty items list")
    identifiers = [item.get("id") for item in items if isinstance(item, dict)]
    if len(identifiers) != len(items) or any(not isinstance(identifier, str) or not identifier.strip() for identifier in identifiers):
        raise ValueError("Every benchmark item requires a non-empty id")
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("Benchmark item ids must be unique")
    for item in items:
        if not isinstance(item.get("truth"), str) or not isinstance(item.get("prediction"), str):
            raise ValueError("Every benchmark item requires truth and prediction paths")
    return value, manifest_path.parent


def metric_summary(results: list[dict]) -> dict:
    true_positive = sum(item["true_positive"] for item in results)
    false_positive = sum(item["false_positive"] for item in results)
    false_negative = sum(item["false_negative"] for item in results)
    precision = true_positive / (true_positive + false_positive) if true_positive + false_positive else 0.0
    recall = true_positive / (true_positive + false_negative) if true_positive + false_negative else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    boundary_values = [item["mean_boundary_error"] for item in results if item["mean_boundary_error"] is not None]
    return {
        "items": len(results),
        "true_positive": true_positive,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "micro_precision": round(precision, 6),
        "micro_recall": round(recall, 6),
        "micro_f1": round(f1, 6),
        "macro_precision": round(mean(item["precision"] for item in results), 6) if results else 0.0,
        "macro_recall": round(mean(item["recall"] for item in results), 6) if results else 0.0,
        "macro_f1": round(mean(item["f1"] for item in results), 6) if results else 0.0,
        "macro_mean_iou": round(mean(item["mean_iou"] for item in results), 6) if results else 0.0,
        "macro_boundary_error": round(mean(boundary_values), 6) if boundary_values else None,
    }


def evaluate_manifest(path: str) -> dict:
    manifest, base_directory = load_manifest(path)
    evaluation = manifest.get("evaluation", {})
    thresholds = evaluation.get("iou_thresholds", [0.5]) if isinstance(evaluation, dict) else [0.5]
    thresholds = sorted(set(main.validate_threshold(value) for value in thresholds))
    per_item = []

    for item in manifest["items"]:
        truth_path = base_directory / item["truth"]
        prediction_path = base_directory / item["prediction"]
        truth = main.load_intervals(str(truth_path), f"truth:{item['id']}")
        predicted = main.load_intervals(str(prediction_path), f"prediction:{item['id']}")
        sweep = main.evaluate_sweep(truth, predicted, thresholds)
        per_item.append({
            "id": item["id"],
            "truth_file": item["truth"],
            "prediction_file": item["prediction"],
            "duration_seconds": item.get("duration_seconds"),
            "results": sweep["results"],
        })

    aggregates = []
    for index, threshold in enumerate(thresholds):
        results = [item["results"][index] for item in per_item]
        aggregates.append({"threshold": threshold, **metric_summary(results)})

    return {
        "aggregate_version": 1,
        "benchmark_name": manifest.get("name", Path(path).stem),
        "item_count": len(per_item),
        "thresholds": thresholds,
        "aggregates": aggregates,
        "per_item": per_item,
    }


def run_self_test() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "truth").mkdir()
        (root / "predictions").mkdir()
        (root / "truth" / "a.json").write_text(json.dumps([{"start": 0, "end": 10}]), encoding="utf-8")
        (root / "predictions" / "a.json").write_text(json.dumps([{"start": 0, "end": 10}]), encoding="utf-8")
        (root / "truth" / "b.json").write_text(json.dumps([{"start": 20, "end": 30}]), encoding="utf-8")
        (root / "predictions" / "b.json").write_text(json.dumps([{"start": 40, "end": 50}]), encoding="utf-8")
        manifest = {
            "name": "self-test",
            "evaluation": {"iou_thresholds": [0.3, 0.5]},
            "items": [
                {"id": "a", "truth": "truth/a.json", "prediction": "predictions/a.json"},
                {"id": "b", "truth": "truth/b.json", "prediction": "predictions/b.json"},
            ],
        }
        manifest_path = root / "manifest.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        report = evaluate_manifest(str(manifest_path))
        assert report["item_count"] == 2
        assert report["thresholds"] == [0.3, 0.5]
        assert report["aggregates"][0]["true_positive"] == 1
        assert report["aggregates"][0]["false_positive"] == 1
        assert report["aggregates"][0]["micro_f1"] == 0.5
    print("ClipBench aggregate self-test passed")


def main_cli() -> None:
    parser = argparse.ArgumentParser(description="Evaluate a ClipBench dataset manifest.")
    parser.add_argument("manifest", nargs="?")
    parser.add_argument("-o", "--output", default="clip-bench-aggregate.json")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        run_self_test()
        return
    if not args.manifest:
        parser.error("manifest is required unless --self-test is used")
    report = evaluate_manifest(args.manifest)
    Path(args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    best = max(report["aggregates"], key=lambda item: (item["micro_f1"], -item["threshold"]))
    print(f"Evaluated {report['item_count']} items; best micro F1={best['micro_f1']} at IoU={best['threshold']}")


if __name__ == "__main__":
    main_cli()
