from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import numpy as np
import pandas as pd


@dataclass(frozen=True)
class CohortDefinition:
    adult_age: int = 18
    min_valid_bp_readings: int = 2
    systolic_min: float = 50.0
    systolic_max: float = 260.0
    diastolic_min: float = 30.0
    diastolic_max: float = 160.0
    high_bp_systolic: float = 130.0
    high_bp_diastolic: float = 80.0


def read_xpt(path: str | Path) -> pd.DataFrame:
    return pd.read_sas(path, format="xport", encoding="utf-8")


def derive_smoking_status(df: pd.DataFrame) -> pd.Series:
    def classify(row):
        q100 = row.get("SMQ020")
        now = row.get("SMQ040")
        if q100 == 2:
            return "never"
        if q100 == 1 and now in (1, 2):
            return "current"
        if q100 == 1 and now == 3:
            return "former"
        return np.nan

    return df.apply(classify, axis=1)


def build_adult_bp_cohort(
    demo: pd.DataFrame,
    bp: pd.DataFrame,
    body: pd.DataFrame,
    activity: pd.DataFrame,
    smoking: pd.DataFrame,
    definition: CohortDefinition = CohortDefinition(),
) -> pd.DataFrame:
    demo_cols = [
        "SEQN", "RIDSTATR", "RIDAGEYR", "RIAGENDR", "RIDRETH3",
        "INDFMPIR", "WTMEC2YR", "SDMVSTRA", "SDMVPSU",
    ]
    bp_cols = [
        "SEQN", "BPXOSY1", "BPXODI1", "BPXOSY2",
        "BPXODI2", "BPXOSY3", "BPXODI3",
    ]

    df = (
        demo[demo_cols]
        .merge(bp[bp_cols], on="SEQN", how="left")
        .merge(body[["SEQN", "BMXBMI", "BMXWAIST"]], on="SEQN", how="left")
        .merge(activity[["SEQN", "PAD680"]], on="SEQN", how="left")
        .merge(smoking[["SEQN", "SMQ020", "SMQ040"]], on="SEQN", how="left")
    )

    df = df[
        (df["RIDAGEYR"] >= definition.adult_age)
        & (df["RIDSTATR"] == 2)
        & (df["WTMEC2YR"] > 0)
    ].copy()

    systolic = ["BPXOSY1", "BPXOSY2", "BPXOSY3"]
    diastolic = ["BPXODI1", "BPXODI2", "BPXODI3"]

    for col in systolic:
        df.loc[
            ~df[col].between(definition.systolic_min, definition.systolic_max),
            col,
        ] = np.nan
    for col in diastolic:
        df.loc[
            ~df[col].between(definition.diastolic_min, definition.diastolic_max),
            col,
        ] = np.nan

    df["n_valid_sbp"] = df[systolic].notna().sum(axis=1)
    df["n_valid_dbp"] = df[diastolic].notna().sum(axis=1)

    df = df[
        (df["n_valid_sbp"] >= definition.min_valid_bp_readings)
        & (df["n_valid_dbp"] >= definition.min_valid_bp_readings)
    ].copy()

    df["mean_sbp"] = df[systolic].mean(axis=1)
    df["mean_dbp"] = df[diastolic].mean(axis=1)

    df["high_measured_bp"] = (
        (df["mean_sbp"] >= definition.high_bp_systolic)
        | (df["mean_dbp"] >= definition.high_bp_diastolic)
    ).astype("int8")

    df.loc[~df["RIAGENDR"].isin([1, 2]), "RIAGENDR"] = np.nan
    df.loc[~df["RIDRETH3"].isin([1, 2, 3, 4, 6, 7]), "RIDRETH3"] = np.nan
    df.loc[~df["INDFMPIR"].between(0, 5), "INDFMPIR"] = np.nan
    df.loc[~df["BMXBMI"].between(10, 80), "BMXBMI"] = np.nan

    df.loc[~df["PAD680"].between(0, 1440), "PAD680"] = np.nan
    df = df.rename(columns={"PAD680": "sedentary_minutes"})

    df["smoking_status"] = derive_smoking_status(df)

    return df


def weighted_prevalence(df: pd.DataFrame) -> float:
    w = df["WTMEC2YR"]
    y = df["high_measured_bp"]
    return float((w * y).sum() / w.sum())
