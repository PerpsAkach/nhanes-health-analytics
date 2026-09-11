from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from src.data_io import discover_xpt_files
from src.evaluation import binary_metrics, expected_calibration_error, challenger_decision
from src.preprocessing import build_adult_bp_cohort, read_xpt, weighted_prevalence


RAW_DIR = Path("data/raw")
RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

NUMERIC = ["RIDAGEYR", "BMXBMI", "INDFMPIR", "sedentary_minutes"]
CATEGORICAL = ["RIAGENDR", "RIDRETH3", "smoking_status"]


def preprocessor():
    return ColumnTransformer(
        [
            ("numeric", SimpleImputer(strategy="median"), NUMERIC),
            (
                "categorical",
                Pipeline(
                    [
                        ("impute", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
                    ]
                ),
                CATEGORICAL,
            ),
        ]
    )


def make_pipeline(model):
    return Pipeline([("preprocess", preprocessor()), ("model", model)])


def subgroup_violations(frame: pd.DataFrame, benchmark_name: str, challenger_name: str):
    violations = []
    for group_column in ["sex_group", "age_group"]:
        for group_name, group in frame.groupby(group_column, observed=True):
            if len(group) < 80 or group["y"].nunique() < 2:
                continue
            from sklearn.metrics import recall_score, roc_auc_score

            b_auc = roc_auc_score(group["y"], group[f"p_{benchmark_name}"])
            c_auc = roc_auc_score(group["y"], group[f"p_{challenger_name}"])
            b_rec = recall_score(
                group["y"], group[f"pred_{benchmark_name}"], zero_division=0
            )
            c_rec = recall_score(
                group["y"], group[f"pred_{challenger_name}"], zero_division=0
            )
            if c_auc < b_auc - 0.05:
                violations.append(
                    f"{group_column}:{group_name} ROC-AUC {c_auc:.3f} vs {b_auc:.3f}"
                )
            if c_rec < b_rec - 0.10:
                violations.append(
                    f"{group_column}:{group_name} recall {c_rec:.3f} vs {b_rec:.3f}"
                )
    return violations


def main():
    paths = discover_xpt_files(RAW_DIR)
    cohort = build_adult_bp_cohort(
        read_xpt(paths["demo"]),
        read_xpt(paths["bp"]),
        read_xpt(paths["body"]),
        read_xpt(paths["activity"]),
        read_xpt(paths["smoking"]),
    )

    X = cohort[NUMERIC + CATEGORICAL]
    y = cohort["high_measured_bp"].astype(int)
    w = cohort["WTMEC2YR"].astype(float)

    X_train, X_test, y_train, y_test, w_train, w_test, idx_train, idx_test = (
        train_test_split(
            X, y, w, cohort.index,
            test_size=0.25,
            random_state=42,
            stratify=y,
        )
    )

    models = {
        "logistic_benchmark": make_pipeline(LogisticRegression(max_iter=3000)),
        "random_forest": make_pipeline(
            RandomForestClassifier(
                n_estimators=160,
                max_depth=None,
                min_samples_leaf=35,
                max_features="sqrt",
                random_state=123,
                n_jobs=-1,
            )
        ),
        "gradient_boosting": make_pipeline(
            HistGradientBoostingClassifier(
                max_iter=120,
                learning_rate=0.05,
                max_leaf_nodes=7,
                min_samples_leaf=25,
                l2_regularization=1.0,
                random_state=123,
            )
        ),
    }

    probabilities = {}
    results = {}

    for name, model in models.items():
        model.fit(X_train, y_train, model__sample_weight=w_train)
        probability = model.predict_proba(X_test)[:, 1]
        probabilities[name] = probability
        results[name] = binary_metrics(y_test, probability)
        results[name]["ece10"] = expected_calibration_error(y_test, probability)

    metadata = cohort.loc[idx_test].copy()
    metadata["y"] = y_test.to_numpy()
    metadata["sex_group"] = metadata["RIAGENDR"].map({1.0: "Male", 2.0: "Female"})
    metadata["age_group"] = pd.cut(
        metadata["RIDAGEYR"],
        bins=[18, 30, 45, 60, 200],
        right=False,
        labels=["18–29", "30–44", "45–59", "60+"],
    )

    for name, probability in probabilities.items():
        metadata[f"p_{name}"] = probability
        metadata[f"pred_{name}"] = (probability >= 0.5).astype(int)

    decisions = {}
    for challenger in ["random_forest", "gradient_boosting"]:
        violations = subgroup_violations(metadata, "logistic_benchmark", challenger)
        decisions[challenger] = challenger_decision(
            results["logistic_benchmark"], results[challenger], violations
        )

    output = {
        "cohort_n": int(len(cohort)),
        "weighted_prevalence": weighted_prevalence(cohort),
        "heldout_results": results,
        "challenger_decisions": decisions,
    }

    (RESULTS_DIR / "reproduced_results.json").write_text(
        json.dumps(output, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
