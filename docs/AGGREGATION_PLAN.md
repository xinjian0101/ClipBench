# Aggregation Plan

The current MVP evaluates one ground-truth file against one prediction file. Dataset-level evaluation should preserve per-item results before calculating aggregates.

## Proposed inputs

A benchmark manifest contains item identifiers, truth paths, prediction paths, and optional source duration.

## Per-item metrics

For every item, store:

- truth interval count;
- prediction interval count;
- true positives;
- false positives;
- false negatives;
- precision;
- recall;
- F1;
- mean IoU;
- mean boundary error;
- matching threshold.

## Aggregate metrics

### Micro average

Sum true positives, false positives, and false negatives across all items before calculating precision, recall, and F1. This weights items by interval count.

### Macro average

Calculate each metric per item and then average across items. This gives each item equal weight.

### Duration-weighted average

Optionally weight per-item metrics by source duration. This should be reported separately because long recordings may dominate the result.

## Threshold sweep

Recommended IoU thresholds:

```text
0.30, 0.50, 0.70
```

Do not select only the threshold that presents the best result. Report the complete configured sweep.

## Empty cases

The implementation must define behavior for:

- no truth and no predictions;
- truth present and no predictions;
- predictions present and no truth;
- no successful matches.

## Output artifacts

A dataset evaluation should produce machine-readable JSON, a flat CSV summary, a Markdown report, per-item result files, and a configuration record containing tool version and input checksums.
