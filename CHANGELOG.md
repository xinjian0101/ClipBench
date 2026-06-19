# Changelog

## Unreleased

### Added

- Temporal IoU calculation.
- One-to-one interval matching.
- Precision, recall, and F1 reporting.
- Mean IoU and mean boundary error.
- Metric reference documentation.
- Reproducible benchmark input-format guide.
- Runnable truth and prediction examples.
- Automated test workflow and aggregation roadmap.

### Known limitations

- Matching is greedy in prediction order rather than globally optimized.
- The MVP evaluates one pair of JSON files per command.
- Confidence scores and ranking metrics are not included.
- Narrative and visual quality are outside the metric scope.

## 0.1.0 — 2026-06-19

Initial executable interval benchmark MVP.

## Maintenance policy

- Metric formulas and matching behavior must remain documented.
- Changes to matching require regression fixtures.
- Published benchmark results should record threshold, version, and input checksums.
- New aggregate metrics must define empty-input behavior.

## Twenty-round portfolio maintenance cycle

This commit completes the twentieth visible maintenance iteration across the seven active MVP repositories. The cycle added architecture notes, versioned configurations, schemas, presets, rule references, benchmark definitions, and maintenance policies while leaving `continuity-director` unchanged.
