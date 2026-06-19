# Benchmark Format

The MVP uses two JSON arrays: one for ground truth and one for predictions.

## Interval record

```json
{
  "start": 10.0,
  "end": 20.0
}
```

Values are seconds from the beginning of the source media.

## Validation recommendations

- `start` and `end` must be finite numbers.
- `end` must be greater than `start`.
- Intervals should use one time base throughout a benchmark.
- Annotation overlaps should be documented.
- Prediction ordering should remain stable for reproducibility.

## Dataset-level manifest proposal

Future directory evaluation can use a manifest:

```json
{
  "benchmark_version": 1,
  "items": [
    {
      "id": "sample-001",
      "truth": "truth/sample-001.json",
      "prediction": "predictions/sample-001.json",
      "duration": 3600
    }
  ]
}
```

## Annotation policy

A benchmark should state what qualifies as a highlight, minimum and maximum duration, whether adjacent moments are merged, how ambiguous boundaries are handled, and whether annotators saw engagement data.

## Reproducibility record

Store the ClipBench version, IoU threshold, input checksums, prediction system version, and benchmark manifest with every published result.
