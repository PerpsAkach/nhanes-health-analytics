# Original Project Audit

The recovered CSIT-558 project contained meaningful multi-source NHANES work, including data merging, exploratory analysis, statistical comparisons, and predictive modeling.

The modernization audit identified four material issues that changed how the project should be presented:

1. **Dietary variable interpretation:** `WTDRD1` was treated as caloric intake, but it is a dietary sample weight. The reconstruction does not use that field as nutrition intake.
2. **Activity interpretation:** `PAD680` is sedentary time, so it is renamed and interpreted accordingly.
3. **Smoking coding:** `SMQ020` alone does not define current smoking; status is derived using `SMQ020` and `SMQ040`.
4. **Target leakage:** the original composite risk score was constructed from health measures and then predicted using overlapping measures. The approximately 0.93 R² is therefore retired from primary claims.

The audit does not erase the original project. It distinguishes historical coursework from the modern reconstructed implementation.
