# NHANES Multi-Source Health Analytics

A modern reconstruction of a recovered CSIT-558 Data Mining project using CDC/NHANES public-use data.

The project demonstrates multi-source XPT ingestion, cohort construction, careful variable recoding, survey-aware weighting, interpretable logistic regression, calibration analysis, subgroup validation, and governed challenger-model testing.

## Research question

Can demographic, body-composition, socioeconomic, sedentary-behavior, and smoking variables distinguish adults with **high measured blood pressure at the NHANES examination**?

The outcome is a screening construct used for this project:

- mean systolic blood pressure >= 130 mm Hg, or
- mean diastolic blood pressure >= 80 mm Hg.

It is **not** presented as a clinical hypertension diagnosis.

## Why this repository exists

The original academic project was recovered with its notebook, report, presentation, and source NHANES XPT files. A technical audit found several issues common in exploratory coursework:

- a dietary survey weight had been interpreted as caloric intake;
- sedentary minutes had been described as physical activity;
- smoking categories needed cleaner derivation;
- the original composite risk-score model had target leakage;
- NHANES survey-design variables were not incorporated consistently.

This reconstruction preserves the historical project while correcting those issues.

## Clean cohort

The reconstructed cohort contains **6,117 adults** with:

- age 18+;
- MEC examination status;
- positive MEC examination weight;
- at least two valid systolic readings; and
- at least two valid diastolic readings.

Observed high-measured-BP prevalence:

- unweighted: about **40.25%**
- MEC-weighted: about **37.46%**

## Benchmark and challenger results

| Model | ROC-AUC | PR-AUC | Accuracy | Precision | Recall | Specificity | F1 | Brier | ECE |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Logistic regression | 0.668 | 0.507 | 0.616 | 0.527 | 0.443 | 0.732 | 0.481 | 0.223 | 0.071 |
| Random forest | 0.675 | 0.529 | 0.620 | 0.558 | 0.274 | 0.853 | 0.368 | 0.216 | 0.049 |
| Gradient boosting | 0.676 | 0.538 | 0.630 | 0.558 | 0.393 | 0.790 | 0.461 | 0.217 | 0.027 |

### Governance decision

**Logistic regression remains the preferred model.**

Both nonlinear challengers improved aggregate PR-AUC and calibration, but both failed predeclared subgroup guardrails. Random forest materially reduced recall among men and adults age 60+. Gradient boosting also reduced recall in those groups and reduced ROC-AUC in the 18–29 subgroup.

The project therefore keeps the simpler model rather than promoting complexity solely because headline AUC increased.

## Interpretable associations

In the logistic model, selected 300-bootstrap odds-ratio estimates were:

- age, per 10 years: **OR 1.40** (bootstrap interval about 1.34–1.47);
- BMI, per 5 kg/m²: **OR 1.33** (about 1.27–1.42);
- female vs male: **OR 0.61** (about 0.52–0.72);
- non-Hispanic Black vs Mexican American: **OR 1.81** (about 1.24–2.68);
- sedentary time, per additional hour/day: approximately **OR 1.00**, with unstable direction.

These are model associations, not causal effects.

## Repository structure

```text
.
├── README.md
├── PROVENANCE.md
├── requirements.txt
├── run_pipeline.py
├── data/
│   └── README.md
├── src/
│   ├── data_io.py
│   ├── preprocessing.py
│   ├── modeling.py
│   └── evaluation.py
├── tests/
├── docs/
│   ├── MODEL_CARD.md
│   ├── ORIGINAL_PROJECT_AUDIT.md
│   └── VALIDATION_SUMMARY.md
├── figures/
└── results/
```

## Reproduce

Download the required CDC/NHANES public-use XPT files and place them anywhere below `data/raw/`:

- `DEMO_L.XPT`
- `BPXO_L.XPT`
- `BMX_L.XPT`
- `PAQ_L.XPT`
- `SMQ_L.XPT`

Then:

```bash
python -m pip install -r requirements.txt
python run_pipeline.py
pytest -q
```

The pipeline searches recursively under `data/raw/`, so the original academic folder structure is not required.

## Important limitations

- The outcome is based on measured BP at one NHANES examination, not longitudinal diagnosis.
- The machine-learning analysis is a portfolio/educational analysis, not a clinical decision tool.
- Survey weights are used in the model fitting and prevalence estimate, but this repository is not intended to replace a full design-based epidemiologic analysis.
- Subgroup checks are descriptive and some subgroups are smaller than others.
- No causal claims are made.

## Provenance

See `PROVENANCE.md` for the boundary between recovered academic work and the modern reconstruction.
