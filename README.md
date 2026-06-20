<div align="center">

# ClipBench

**Reproducible temporal interval evaluation for highlight-detection systems.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Metrics](https://img.shields.io/badge/Metrics-IoU%20%7C%20Precision%20%7C%20Recall%20%7C%20F1-0969da)](docs/METRICS.md)
[![License](https://img.shields.io/badge/License-MIT-2ea44f)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active%20MVP-f59e0b)](MAINTENANCE_TRACE.md)

[Quick start](#quick-start) · [Metrics](#metric-reference) · [Threshold sweeps](#threshold-sweeps) · [Aggregation](#dataset-level-aggregation) · [About](ABOUT.md)

</div>

---

ClipBench evaluates predicted highlight intervals against reviewed ground truth. It provides strict interval validation, one-to-one matching, configurable IoU thresholds, threshold sweeps, per-item results, and dataset-level micro and macro aggregation.

> [!NOTE]
> Temporal agreement is not the same as editing quality, narrative value, factual accuracy, audience retention, or commercial performance.

## At a glance

| Area | Current support |
|---|---|
| Input | JSON arrays of intervals |
| Matching | One-to-one, best unmatched IoU |
| Metrics | Precision, recall, F1, mean IoU, boundary error |
| Thresholds | Single value or sorted multi-value sweep |
| Dataset evaluation | Manifest-based micro and macro aggregation |
| Reports | Versioned JSON |
| Runtime | Python standard library |

## Quick start

Evaluate one prediction file:

```bash
python main.py examples/truth.json examples/predicted.json \
  --threshold 0.5 \
  -o report.json
```

Evaluate several thresholds:

```bash
python main.py examples/truth.json examples/predicted.json \
  --thresholds 0.3,0.5,0.7 \
  -o sweep-report.json
```

Run tests:

```bash
python -m unittest -v
```

## Capability matrix

| Capability | Status | Notes |
|---|---:|---|
| Strict interval validation | ✅ | Finite, non-negative, positive duration |
| One-to-one matching | ✅ | Each truth interval used once |
| Threshold sweep | ✅ | Sorted and deduplicated |
| Per-match audit details | ✅ | Prediction index, truth index, IoU, error |
| Dataset aggregation | ✅ | Micro and macro summaries |
| Multi-annotator agreement | ⏳ | Not implemented |
| Content-quality scoring | ❌ | Intentionally outside scope |

## Input format

Truth and prediction files contain JSON arrays:

```json
[
  {"start": 10.0, "end": 24.0},
  {"start": 61.5, "end": 79.0}
]
```

All files in one benchmark must use the same source version, edit, timeline, and unit.

## Metric reference

| Metric | Meaning |
|---|---|
| IoU | Intersection duration divided by union duration |
| Precision | Matched predictions divided by all predictions |
| Recall | Matched truth intervals divided by all truth intervals |
| F1 | Harmonic mean of precision and recall |
| Mean IoU | Average IoU across matched pairs |
| Boundary error | Average start/end boundary difference for matches |

## Threshold sweeps

```bash
python main.py truth.json predictions.json --thresholds 0.3,0.5,0.7
```

Sweep reports include the normalized threshold list, a complete result for every threshold, and the best F1 result. Report all thresholds used when comparing systems.

## Dataset-level aggregation

```bash
python aggregate.py examples/benchmark-manifest.json \
  -o aggregate-report.json
```

Aggregation reports preserve:

- per-item results;
- micro precision, recall, and F1;
- macro precision, recall, and F1;
- macro mean IoU;
- macro boundary error;
- the threshold used for each summary.

Run the built-in aggregation self-test:

```bash
python aggregate.py --self-test
```

## Recommended evaluation workflow

```text
freeze source media and checksum
      ↓
define annotation policy
      ↓
review ground-truth intervals
      ↓
freeze prediction version and config
      ↓
evaluate multiple IoU thresholds
      ↓
inspect per-item failures
      ↓
publish reproducible aggregate report
```

## Repository map

| Path | Purpose |
|---|---|
| `main.py` | Interval validation, matching, metrics, and threshold sweeps |
| `aggregate.py` | Manifest-based dataset aggregation |
| `examples/` | Truth, predictions, and benchmark manifest |
| `schema/` | Result contract |
| `docs/` | Metrics, format, aggregation, and reproducibility |
| `test_*.py` | Core metric and sweep tests |
| `ABOUT.md` | Mission, maturity, boundaries, and governance |

## Avoid misleading comparisons

- Do not claim general performance from one recording.
- Do not change truth labels after viewing predictions without recording the revision.
- Do not mix timelines from different edits.
- Do not report only F1 while hiding precision, recall, and boundary error.
- Do not present interval accuracy as finished-video quality.

## Documentation

- [About the project](ABOUT.md)
- [Metric reference](docs/METRICS.md)
- [Benchmark format](docs/BENCHMARK_FORMAT.md)
- [Aggregation plan](docs/AGGREGATION_PLAN.md)
- [Reproducibility checklist](docs/REPRODUCIBILITY_CHECKLIST.md)
- [Maintenance trace](MAINTENANCE_TRACE.md)
- [Changelog](CHANGELOG.md)

## License

MIT
