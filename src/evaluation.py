from __future__ import annotations

import numpy as np
import pandas as pd
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


def binary_metrics(y_true, probability, threshold: float = 0.5) -> dict:
    y_true = np.asarray(y_true)
    probability = np.asarray(probability)
    prediction = (probability >= threshold).astype(int)
    return {
        "roc_auc": float(roc_auc_score(y_true, probability)),
        "pr_auc": float(average_precision_score(y_true, probability)),
        "accuracy": float(accuracy_score(y_true, prediction)),
        "precision": float(precision_score(y_true, prediction, zero_division=0)),
        "recall": float(recall_score(y_true, prediction, zero_division=0)),
        "specificity": float(recall_score(y_true, prediction, pos_label=0)),
        "f1": float(f1_score(y_true, prediction, zero_division=0)),
        "brier": float(brier_score_loss(y_true, probability)),
        "confusion_matrix": confusion_matrix(y_true, prediction).tolist(),
    }


def expected_calibration_error(y_true, probability, bins: int = 10) -> float:
    frame = pd.DataFrame({"y": np.asarray(y_true), "p": np.asarray(probability)})
    frame["bin"] = pd.qcut(frame["p"], q=bins, duplicates="drop")
    return float(
        sum(
            len(group) / len(frame) * abs(group["y"].mean() - group["p"].mean())
            for _, group in frame.groupby("bin", observed=True)
        )
    )


def challenger_decision(
    benchmark: dict,
    challenger: dict,
    subgroup_violations: list[str] | None = None,
) -> dict:
    subgroup_violations = subgroup_violations or []
    discrimination = (
        challenger["roc_auc"] - benchmark["roc_auc"] >= 0.015
        or challenger["pr_auc"] - benchmark["pr_auc"] >= 0.020
    )
    calibration = (
        challenger["brier"] - benchmark["brier"] <= 0.010
        and challenger["ece10"] - benchmark["ece10"] <= 0.020
    )
    keep = discrimination and calibration and not subgroup_violations
    return {
        "keep": bool(keep),
        "meaningful_discrimination_gain": bool(discrimination),
        "calibration_guardrail_pass": bool(calibration),
        "subgroup_guardrail_pass": not subgroup_violations,
        "delta_roc_auc": challenger["roc_auc"] - benchmark["roc_auc"],
        "delta_pr_auc": challenger["pr_auc"] - benchmark["pr_auc"],
        "delta_brier": challenger["brier"] - benchmark["brier"],
        "delta_ece10": challenger["ece10"] - benchmark["ece10"],
        "subgroup_violations": subgroup_violations,
    }
