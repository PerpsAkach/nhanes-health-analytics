import numpy as np
import pandas as pd

from src.preprocessing import CohortDefinition, build_adult_bp_cohort, derive_smoking_status


def test_smoking_status():
    df = pd.DataFrame(
        {
            "SMQ020": [2, 1, 1, 7],
            "SMQ040": [np.nan, 1, 3, np.nan],
        }
    )
    result = derive_smoking_status(df).tolist()
    assert result[0] == "never"
    assert result[1] == "current"
    assert result[2] == "former"
    assert pd.isna(result[3])


def test_bp_outcome_derivation_and_two_reading_rule():
    demo = pd.DataFrame(
        {
            "SEQN": [1, 2, 3],
            "RIDSTATR": [2, 2, 2],
            "RIDAGEYR": [40, 40, 40],
            "RIAGENDR": [1, 2, 1],
            "RIDRETH3": [3, 3, 3],
            "INDFMPIR": [2.0, 2.0, 2.0],
            "WTMEC2YR": [1.0, 1.0, 1.0],
            "SDMVSTRA": [1, 1, 1],
            "SDMVPSU": [1, 1, 1],
        }
    )
    bp = pd.DataFrame(
        {
            "SEQN": [1, 2, 3],
            "BPXOSY1": [132, 118, 135],
            "BPXODI1": [78, 72, 80],
            "BPXOSY2": [130, 120, np.nan],
            "BPXODI2": [76, 74, np.nan],
            "BPXOSY3": [128, 119, np.nan],
            "BPXODI3": [77, 73, np.nan],
        }
    )
    body = pd.DataFrame({"SEQN": [1, 2, 3], "BMXBMI": [25, 25, 25], "BMXWAIST": [90, 90, 90]})
    activity = pd.DataFrame({"SEQN": [1, 2, 3], "PAD680": [300, 300, 300]})
    smoking = pd.DataFrame({"SEQN": [1, 2, 3], "SMQ020": [2, 2, 2], "SMQ040": [np.nan, np.nan, np.nan]})

    cohort = build_adult_bp_cohort(demo, bp, body, activity, smoking)
    assert cohort["SEQN"].tolist() == [1, 2]
    assert cohort.set_index("SEQN").loc[1, "high_measured_bp"] == 1
    assert cohort.set_index("SEQN").loc[2, "high_measured_bp"] == 0
