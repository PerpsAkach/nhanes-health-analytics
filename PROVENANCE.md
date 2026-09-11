# Provenance

## Recovered

The original academic project was recovered from the user's own files and is attributable to **Paul Ndiege, CSIT-558: Data Mining**.

Recovered materials include:

- original Jupyter notebook;
- project report;
- course presentation;
- NHANES public-use XPT datasets;
- exploratory/statistical analysis;
- an original composite health-risk workflow.

## Corrected

The modern audit corrected several analytical issues:

- `WTDRD1` is a dietary sample weight, not caloric intake;
- `PAD680` represents sedentary minutes/day rather than exercise minutes;
- smoking status is derived from `SMQ020` + `SMQ040`;
- invalid/special codes are excluded where appropriate;
- blood-pressure variables used to define the target are excluded from predictors;
- the original high-R² risk-score model is not retained as a success claim because of target leakage.

## Reconstructed

The clean pipeline, cohort logic, outcome derivation, reproducible scripts, tests, validation workflow, and challenger governance are reconstructed from the recovered project and its source datasets.

## Enhanced

The following are modern portfolio enhancements:

- modular Python source code;
- automated tests;
- held-out benchmark evaluation;
- bootstrap coefficient stability;
- calibration analysis;
- threshold analysis;
- subgroup checks;
- random-forest and gradient-boosting challengers;
- predeclared challenger-retention rules;
- model card and audit documentation.

## Retired claim

The original composite Health Risk Score regression and its approximately 0.93 R² are retained only as historical audit context. They are not presented as evidence of a validated health-risk predictor.
