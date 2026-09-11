# Portfolio Summary

## NHANES Multi-Source Health Analytics

Modern reconstruction of a graduate Data Mining project using CDC/NHANES public-use data.

Built a reproducible multi-source health-data pipeline that merges demographic, body-measure, blood-pressure, physical-activity, and smoking datasets; derives a transparent high-measured-blood-pressure screening outcome; and compares an interpretable logistic-regression benchmark against random-forest and gradient-boosting challengers.

The final workflow emphasizes model governance rather than headline accuracy. Logistic regression remained the preferred model after nonlinear challengers produced only modest aggregate gains and failed predeclared subgroup guardrails.

### Technical highlights

- Multi-file XPT ingestion and joins on NHANES participant IDs
- Reproducible adult cohort and blood-pressure outcome construction
- Corrected variable semantics and categorical recoding
- Survey-weighted prevalence and model fitting
- Logistic regression with odds-ratio interpretation
- 300-bootstrap coefficient stability analysis
- ROC/PR discrimination, calibration, threshold analysis
- Age/sex subgroup validation
- Random-forest and gradient-boosting challenger testing
- Explicit model-retention governance
- Automated tests and provenance documentation

### Selected result

Preferred logistic benchmark: ROC-AUC 0.668, PR-AUC 0.507. Random forest and gradient boosting improved aggregate PR-AUC and calibration but were rejected because they materially worsened subgroup sensitivity/performance.

### Positioning

This project demonstrates data engineering, statistical reasoning, reproducible ML, model validation, fairness-aware evaluation, and model-risk/governance judgment—not clinical prediction.
