## Summary

Describe the interval validation, matching, metric, threshold, aggregation, test, or documentation change.

## Evaluation impact

- Previous behavior:
- New behavior:
- Metric-definition impact:
- Result-schema impact:
- Compatibility impact:

## Verification

- [ ] Added fixed truth and prediction fixtures
- [ ] Ran `python -m unittest -v`
- [ ] Checked empty truth and prediction behavior
- [ ] Checked invalid interval behavior
- [ ] Checked single-threshold evaluation when relevant
- [ ] Checked threshold sweeps when relevant
- [ ] Checked manifest aggregation when relevant
- [ ] Preserved per-item results alongside aggregate metrics

## Reproducibility

- [ ] Source timeline and time unit are documented
- [ ] Annotation policy is unchanged or its revision is documented
- [ ] Thresholds are recorded in the result
- [ ] Micro and macro metrics are not mixed without labels
- [ ] Temporal accuracy is not presented as content-quality performance

## Documentation

- [ ] Updated README or metric reference
- [ ] Updated benchmark format or aggregation guidance when needed
- [ ] Recorded user-visible behavior changes

## Reviewer notes

List benchmark assumptions, comparison risks, limitations, and follow-up work.
