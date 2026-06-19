# Metric Reference

ClipBench evaluates temporal highlight intervals rather than frame-level labels.

## Interval intersection over union

For intervals `A` and `B`:

```text
IoU = intersection_duration / union_duration
```

A prediction matches a ground-truth interval when the IoU is greater than or equal to the configured threshold. The default threshold is `0.5`.

## Matching policy

- Predictions are evaluated in input order.
- Each ground-truth interval can be matched once.
- The unmatched truth interval with the highest IoU is selected.
- Predictions below the threshold remain false positives.

## Precision

```text
precision = matched_predictions / all_predictions
```

Precision answers: how many predicted highlights were accepted by the matching rule?

## Recall

```text
recall = matched_truth_intervals / all_truth_intervals
```

Recall answers: how many annotated highlights were found?

## F1 score

```text
F1 = 2 * precision * recall / (precision + recall)
```

## Boundary error

For a matched pair:

```text
boundary_error = (absolute_start_error + absolute_end_error) / 2
```

The value is measured in seconds.

## Interpretation limits

A high IoU does not measure narrative completeness, opening strength, visual quality, or platform performance. Benchmark reports should include the annotation policy and threshold.
