from __future__ import annotations
from pathlib import Path


REQUIRED_FILES = {
    "demo": "DEMO_L.XPT",
    "bp": "BPXO_L.XPT",
    "body": "BMX_L.XPT",
    "activity": "PAQ_L.XPT",
    "smoking": "SMQ_L.XPT",
}


def discover_xpt_files(raw_dir: str | Path) -> dict[str, Path]:
    raw_dir = Path(raw_dir)
    found = {}
    for key, filename in REQUIRED_FILES.items():
        matches = list(raw_dir.rglob(filename))
        if not matches:
            raise FileNotFoundError(
                f"Required NHANES file {filename!r} was not found under {raw_dir}."
            )
        if len(matches) > 1:
            raise RuntimeError(
                f"Multiple copies of {filename!r} were found under {raw_dir}; "
                "keep one canonical copy."
            )
        found[key] = matches[0]
    return found
