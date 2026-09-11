# Data

This repository intentionally does not redistribute the original NHANES XPT files.

Place these CDC/NHANES public-use files anywhere below `data/raw/`:

- `DEMO_L.XPT`
- `BPXO_L.XPT`
- `BMX_L.XPT`
- `PAQ_L.XPT`
- `SMQ_L.XPT`

`run_pipeline.py` discovers them recursively by filename.
