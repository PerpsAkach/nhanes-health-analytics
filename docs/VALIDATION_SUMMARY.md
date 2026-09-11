# Validation Summary

## Benchmark

Logistic regression was established as the transparent benchmark.

## Interpretation

The strongest stable associations in 300 bootstrap refits were age and BMI. Several lifestyle or categorical contrasts were less stable and are not overinterpreted.

## Calibration and thresholds

The benchmark has modest discrimination and imperfect probability calibration. Threshold 0.50 favors specificity over sensitivity. A lower threshold improves sensitivity at the cost of more false positives; no threshold is declared universally optimal.

## Subgroup validation

Sex- and age-group checks revealed materially different recall and within-group discrimination.

## Challenger governance

A challenger had to:

- improve ROC-AUC by at least 0.015 or PR-AUC by at least 0.020;
- worsen Brier score by no more than 0.010;
- worsen 10-bin ECE by no more than 0.020;
- avoid >0.05 subgroup ROC-AUC loss; and
- avoid >0.10 subgroup recall loss.

Neither random forest nor gradient boosting passed all guardrails.

## Final decision

Retain logistic regression as the preferred model.
