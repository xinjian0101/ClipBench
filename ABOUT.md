# About ClipBench

## Mission

ClipBench provides reproducible temporal evaluation for highlight-detection and candidate-selection systems.

## Intended users

- Researchers comparing interval prediction systems
- Developers tuning highlight detectors
- Teams tracking regressions across algorithm versions
- Maintainers building reviewed benchmark datasets

## Core capabilities

- Interval validation
- Temporal IoU calculation
- One-to-one prediction matching
- Precision, recall, F1, mean IoU, and boundary error
- Configurable single-threshold evaluation
- Multi-threshold sweeps
- Versioned JSON result output

## Boundaries

ClipBench evaluates time intervals only. It does not judge editing quality, narrative value, factual accuracy, audience retention, or commercial performance.

## Architecture

```text
Truth intervals + predictions -> validation -> matching
                              -> metrics -> threshold sweep -> report
```

## Design priorities

1. Reproducible evaluation
2. Explicit time units and source versions
3. Stable metric definitions
4. Per-match auditability
5. Clear empty-input behavior
6. Honest separation between temporal accuracy and content quality

## Maturity

The project is an executable MVP with interval validation, threshold sweeps, schemas, benchmark manifests, aggregation planning, tests, and reproducibility guidance.

## Related repositories

- `LiveHighlightEngine` produces candidate intervals
- `FlowFFmpeg` compiles approved intervals into media-processing arguments

## Governance

Metric and matching-policy changes require fixed fixtures, compatibility notes, and before-and-after comparisons. Public documentation and examples are maintained in English.
