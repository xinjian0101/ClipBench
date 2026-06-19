# Maintenance Trace

Batch: `content-enrichment-2026-06-19`

## Iteration 19

- Expanded the README with use cases, input examples, metric explanations, recommended evaluation workflow, misuse warnings, limitations, and related-project links.
- Preserved the interval-only evaluation scope and avoided claims about semantic or commercial quality.

## Iteration 20

- Added this visible maintenance trace.
- Completed the 20-iteration cross-repository enrichment batch.
- Established reproducibility and benchmark-maintenance expectations.

## Validation record

| Check | Result |
|---|---|
| Existing CLI retained | pass |
| Existing JSON interval format retained | pass |
| Existing metrics retained | pass |
| Semantic-quality claims excluded | pass |
| README maintenance link reviewed | pass |

## Maintenance policy

1. Metric changes require fixed truth and prediction fixtures.
2. Matching-policy changes must include examples for overlapping and duplicate predictions.
3. Benchmark reports must record the IoU threshold.
4. Published comparisons must identify code, configuration, annotation-policy, and input versions.
5. Test data must use one documented time unit and one video timeline.
6. New aggregate metrics must not hide per-category failures.

## Open items

- No multi-annotator agreement calculation.
- No confidence interval or statistical significance module.
- No semantic or audience-retention evaluation.
- No automatic conversion from every upstream prediction schema.

## Batch summary

The batch updated seven repositories and intentionally excluded `continuity-director`, which was already the most complete project in the set. Twenty independent commits were created so GitHub history shows the maintenance sequence clearly.