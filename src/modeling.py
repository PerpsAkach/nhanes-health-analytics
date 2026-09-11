from __future__ import annotations

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def logistic_pipeline(numeric_features, categorical_features):
    preprocess = ColumnTransformer(
        [
            (
                "numeric",
                Pipeline(
                    [
                        ("impute", SimpleImputer(strategy="median")),
                        ("scale", StandardScaler()),
                    ]
                ),
                numeric_features,
            ),
            (
                "categorical",
                Pipeline(
                    [
                        ("impute", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                categorical_features,
            ),
        ]
    )

    return Pipeline(
        [
            ("preprocess", preprocess),
            ("model", LogisticRegression(max_iter=2000)),
        ]
    )


def evaluate_binary_model(model, X, y, weights=None, random_state=42):
    split = train_test_split(
        X,
        y,
        weights if weights is not None else np.ones(len(y)),
        test_size=0.25,
        random_state=random_state,
        stratify=y,
    )
    X_train, X_test, y_train, y_test, w_train, w_test = split

    fit_kwargs = {}
    if isinstance(model, Pipeline) and isinstance(
        model.named_steps.get("model"), LogisticRegression
    ):
        fit_kwargs["model__sample_weight"] = w_train

    model.fit(X_train, y_train, **fit_kwargs)
    prob = model.predict_proba(X_test)[:, 1]
    pred = (prob >= 0.5).astype(int)

    return {
        "n_train": len(X_train),
        "n_test": len(X_test),
        "test_prevalence": float(y_test.mean()),
        "roc_auc": float(roc_auc_score(y_test, prob)),
        "pr_auc": float(average_precision_score(y_test, prob)),
        "accuracy": float(accuracy_score(y_test, pred)),
        "precision": float(precision_score(y_test, pred, zero_division=0)),
        "recall": float(recall_score(y_test, pred, zero_division=0)),
        "f1": float(f1_score(y_test, pred, zero_division=0)),
        "brier": float(brier_score_loss(y_test, prob)),
        "confusion_matrix": confusion_matrix(y_test, pred).tolist(),
    }


def run_baseline_and_logistic_models(df: pd.DataFrame):
    y = df["high_measured_bp"]
    weights = df["WTMEC2YR"]

    baseline = DummyClassifier(strategy="prior")
    baseline_result = evaluate_binary_model(
        baseline,
        df[["RIDAGEYR"]],
        y,
        weights,
    )

    core_num = ["RIDAGEYR", "BMXBMI"]
    core_cat = ["RIAGENDR", "RIDRETH3"]
    core_model = logistic_pipeline(core_num, core_cat)
    core_result = evaluate_binary_model(
        core_model,
        df[core_num + core_cat],
        y,
        weights,
    )

    lifestyle_num = [
        "RIDAGEYR",
        "BMXBMI",
        "INDFMPIR",
        "sedentary_minutes",
    ]
    lifestyle_cat = [
        "RIAGENDR",
        "RIDRETH3",
        "smoking_status",
    ]
    lifestyle_model = logistic_pipeline(lifestyle_num, lifestyle_cat)
    lifestyle_result = evaluate_binary_model(
        lifestyle_model,
        df[lifestyle_num + lifestyle_cat],
        y,
        weights,
    )

    return {
        "baseline_prior": baseline_result,
        "logistic_core": core_result,
        "logistic_lifestyle_social": lifestyle_result,
    }
