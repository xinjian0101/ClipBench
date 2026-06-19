# Reproducibility Checklist

Use this checklist before publishing or comparing benchmark results.

## Inputs

- Ground-truth file checksum recorded.
- Prediction file checksum recorded.
- Time unit confirmed as seconds.
- Annotation policy version recorded.
- Source duration recorded when available.
- Empty and malformed intervals reviewed.

## Tooling

- ClipBench commit SHA recorded.
- Python version recorded.
- Operating system recorded.
- Command arguments preserved.
- IoU threshold or threshold sweep preserved.
- Matching policy documented.

## Results

- Precision, recall, and F1 preserved.
- Mean IoU preserved.
- Mean boundary error preserved.
- Per-match details retained.
- Empty-input behavior stated.
- Micro and macro aggregation distinguished.

## Comparison rules

- Compare systems on the same benchmark revision.
- Use the same threshold set.
- Do not remove difficult items without documenting the change.
- Report both improvements and regressions.
- Keep per-item results so aggregate changes can be explained.

## Publication package

A complete package should include the benchmark manifest, annotation policy, truth files, prediction files, result JSON, flat summary, tool version, configuration, and checksums.

## Maintenance cycle 3

This checklist completes iteration 60 of the visible portfolio maintenance history. The third cycle added machine-readable schemas, review profiles, release records, batch formats, continuity fixtures, lifecycle fields, and benchmark result contracts across the active repositories.
