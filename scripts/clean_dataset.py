from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from data_processing import clean_data, cleaning_summary, load_raw_data


RAW_PATH = ROOT / "synthetic_fooddelivery_dataset.csv"
OUTPUT_DIR = ROOT / "data" / "processed"


def main() -> None:
    raw = load_raw_data(RAW_PATH)
    clean = clean_data(raw)
    summary = cleaning_summary(raw, clean)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    clean_path = OUTPUT_DIR / "food_delivery_cleaned.csv"
    summary_path = OUTPUT_DIR / "cleaning_summary.json"
    clean.to_csv(clean_path, index=False, encoding="utf-8-sig")
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Data bersih: {clean_path.relative_to(ROOT)} ({len(clean):,} baris)")
    print(f"Ringkasan cleaning: {summary_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()