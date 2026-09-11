# Model Card

## Model

Preferred model: **survey-weighted logistic regression**

Challengers evaluated: random forest and histogram gradient boosting.

## Intended use

Educational and portfolio demonstration of transparent model development, validation, calibration, and challenger governance using public NHANES data.

## Non-use

This model must not be used for diagnosis, treatment, triage, insurance, employment, or other health-related decisions.

## Outcome

`high_measured_bp = 1` when mean systolic BP >= 130 mm Hg or mean diastolic BP >= 80 mm Hg.

This is a project screening outcome from the NHANES examination and is not equivalent to a clinician-confirmed hypertension diagnosis.

## Predictor set

- age;
- sex;
- race/ethnicity category;
- BMI;
- family income-to-poverty ratio;
- sedentary minutes/day;
- smoking status.

Blood-pressure readings are excluded from predictors.

## Held-out performance

Preferred logistic benchmark:

- ROC-AUC: 0.668
- PR-AUC: 0.507
- accuracy: 0.616
- precision: 0.527
- recall: 0.443
- specificity: 0.732
- F1: 0.481
- Brier score: 0.223
- 10-bin ECE: 0.071

## Challenger decision

Random forest and gradient boosting both improved aggregate PR-AUC and calibration but failed subgroup guardrails, so neither replaced logistic regression.

## Key limitations

- modest discrimination;
- imperfect calibration;
- single-exam screening outcome;
- observational data;
- descriptive subgroup analysis;
- no causal interpretation;
- survey-weighted model fitting is not a substitute for all design-based inferential procedures.
