# Maintenance Trace

This file records visible maintenance work applied to ClipBench.

## Maintenance cycle 1

- Expanded the repository entry point.
- Added interval examples, metric explanations, workflow guidance, limitations, and related-project links.
- Preserved the interval-only evaluation scope.

## Maintenance cycle 2

- Added metric documentation, benchmark format guidance, aggregation planning, result schemas, and reproducibility requirements.

## Maintenance cycle 3

- Added dataset-level manifest examples and formal result contracts.

## Maintenance cycle 4 — English-only repository content

### Consistency commit 1

- Replaced the Chinese README with a complete English benchmark guide.
- Converted all metric explanations, workflows, warnings, and limitations to English.

### Consistency commit 2

- Updated this maintenance trace.
- Confirmed that public documentation and examples are maintained in English.

## Verification

| Check | Result |
|---|---|
| Existing CLI retained | pass |
| Existing JSON interval format retained | pass |
| Existing metrics retained | pass |
| README is English | pass |
| Metric definitions remain unchanged | pass |
| Semantic-quality claims remain outside scope | pass |

## Maintenance rules

1. Metric changes require fixed truth and prediction fixtures.
2. Matching-policy changes require overlapping and duplicate-prediction examples.
3. Reports must record the IoU threshold.
4. Comparisons must identify code, configuration, annotation policy, and input versions.
5. Test data must use one documented time unit and one source timeline.
6. Aggregate metrics must not hide per-item failures.
7. Public repository content is maintained in English.

## Open work

- Multi-annotator agreement
- Confidence intervals and significance tests
- Ranking metrics for scored predictions
- Additional upstream format adapters

## Cycle summary

The fourth cross-repository cycle created 20 planned maintenance commits, followed by two consistency commits that completed the English conversion and repaired documentation paths.
