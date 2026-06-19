# ClipBench

ClipBench is a temporal interval benchmark for highlight-detection systems. It matches reviewed ground-truth intervals against predicted intervals and reports IoU, precision, recall, F1, and mean boundary error.

> The current release evaluates temporal agreement only. It does not measure editing quality, narrative value, factual accuracy, audience response, or business performance.

## Use cases

- Compare highlight-detection algorithms
- Tune thresholds, window sizes, and merge policies
- Evaluate candidate intervals from long recordings
- Detect metric regressions after algorithm changes
- Build reproducible benchmarks for LiveHighlightEngine and similar systems

## Current capabilities

- Temporal intersection-over-union calculation
- One-to-one matching at a configurable IoU threshold
- Precision, recall, and F1 reporting
- Mean matched IoU
- Mean boundary error
- JSON input for truth and predictions
- JSON result output
- Local execution with no paid API

## Requirements

- Python 3.10 or newer

## Run

```bash
python main.py examples/truth.json examples/predicted.json --threshold 0.5 -o report.json
```

## Test

```bash
python -m unittest -v
```

## Input format

Truth and prediction files are JSON arrays. Every item requires `start` and `end` values in seconds.

### Ground truth

```json
[
  {"start": 10.0, "end": 24.0},
  {"start": 61.5, "end": 79.0}
]
```

### Predictions

```json
[
  {"start": 11.0, "end": 25.0},
  {"start": 58.0, "end": 76.0}
]
```

All files in one benchmark must use the same source version and time base.

## Metrics

### Intersection over Union

```text
IoU = intersection duration / union duration
```

A prediction is accepted when its IoU with an unmatched truth interval is greater than or equal to the configured threshold.

### Precision

The fraction of predicted intervals that were matched. Low precision indicates many unmatched predictions.

### Recall

The fraction of truth intervals that were matched. Low recall indicates many missed reviewed moments.

### F1

The harmonic mean of precision and recall.

### Mean boundary error

The average absolute difference between predicted and reviewed start and end boundaries for matched pairs.

## Recommended evaluation workflow

1. Freeze the source media version and checksum.
2. Define an annotation policy.
3. Create and review truth intervals.
4. Freeze the prediction-system version and configuration.
5. Evaluate at several IoU thresholds, such as `0.3`, `0.5`, and `0.7`.
6. Report results by content category as well as overall.
7. Preserve inputs, outputs, configuration, code commit, and checksums.

## Avoiding misleading comparisons

- Do not claim general performance from one recording.
- Do not revise truth intervals after viewing predictions without recording the change.
- Do not mix timelines from different media edits.
- Do not report only F1 while hiding precision, recall, and boundary error.
- Do not treat interval agreement as finished-video quality.

## Known limitations

- The evaluator does not understand interval content.
- Results depend on the annotation policy.
- Multi-annotator agreement is not calculated.
- Confidence intervals and significance tests are not included.
- Visual quality, titles, thumbnails, retention, and platform performance are outside scope.

## Documentation

- [Metric Reference](docs/METRICS.md)
- [Benchmark Format](docs/BENCHMARK_FORMAT.md)
- [Aggregation Plan](docs/AGGREGATION_PLAN.md)
- [Reproducibility Checklist](docs/REPRODUCIBILITY_CHECKLIST.md)
- [Maintenance Trace](MAINTENANCE_TRACE.md)

## Related projects

- **LiveHighlightEngine** produces candidate intervals for evaluation.
- **FlowFFmpeg** compiles approved interval workflows into inspectable media commands.

## License

MIT
