from __future__ import annotations

from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "ID_Pesanan",
    "Waktu_Transaksi",
    "Kategori_Menu",
    "Harga_Pesanan",
    "Jarak_Kirim_KM",
    "Waktu_Tunggu_Menit",
    "Rating_Pelanggan",
    "Ulasan_Teks",
    "Status_Promo",
    "Tingkat_Keluhan",
    "Status_Pesanan",
}

WEEKDAYS_ID = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]


def load_raw_data(path: str | Path) -> pd.DataFrame:
    """Load the supplied CSV without modifying the source file."""
    return pd.read_csv(path, dtype={"ID_Pesanan": "string"})


def clean_data(raw: pd.DataFrame) -> pd.DataFrame:
    """Normalize types and fields while retaining suspicious rows for review."""
    data = raw.copy()
    data.columns = data.columns.str.strip()
    missing_columns = REQUIRED_COLUMNS.difference(data.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Kolom wajib tidak ditemukan: {missing}")

    text_columns = [
        "ID_Pesanan",
        "Kategori_Menu",
        "Ulasan_Teks",
        "Tingkat_Keluhan",
        "Status_Pesanan",
    ]
    for column in text_columns:
        data[column] = data[column].astype("string").str.strip()
        data[column] = data[column].replace("", pd.NA)

    data = data.drop_duplicates(subset="ID_Pesanan", keep="first").reset_index(drop=True)
    data["Waktu_Transaksi"] = pd.to_datetime(
        data["Waktu_Transaksi"].astype("string").str.strip(),
        format="mixed",
        dayfirst=True,
        errors="coerce",
    )

    numeric_columns = [
        "Harga_Pesanan",
        "Jarak_Kirim_KM",
        "Waktu_Tunggu_Menit",
        "Rating_Pelanggan",
    ]
    for column in numeric_columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    invalid_rating = ~data["Rating_Pelanggan"].between(1, 5)
    data.loc[invalid_rating, "Rating_Pelanggan"] = pd.NA
    data.loc[data["Jarak_Kirim_KM"] <= 0, "Jarak_Kirim_KM"] = pd.NA
    data.loc[data["Waktu_Tunggu_Menit"] < 0, "Waktu_Tunggu_Menit"] = pd.NA

    promo = data["Status_Promo"].astype("string").str.strip().str.lower()
    data["Status_Promo"] = promo.map(
        {"true": True, "1": True, "ya": True, "false": False, "0": False, "tidak": False}
    ).astype("boolean")

    valid_positive_prices = data.loc[data["Harga_Pesanan"] > 0, "Harga_Pesanan"]
    if valid_positive_prices.empty:
        upper_fence = float("inf")
    else:
        first_quartile = valid_positive_prices.quantile(0.25)
        third_quartile = valid_positive_prices.quantile(0.75)
        upper_fence = third_quartile + 1.5 * (third_quartile - first_quartile)

    data["Anomali_Sumber_Kaggle"] = (data["Harga_Pesanan"] <= 0) | (
        data["Harga_Pesanan"] > 500_000
    )
    data["Outlier_IQR"] = data["Harga_Pesanan"] > upper_fence
    data["Harga_Mencurigakan"] = data["Anomali_Sumber_Kaggle"] | data["Outlier_IQR"]
    data["Bulan"] = data["Waktu_Transaksi"].dt.to_period("M").astype("string")
    data["Hari"] = data["Waktu_Transaksi"].dt.dayofweek.map(dict(enumerate(WEEKDAYS_ID)))
    data["Jam"] = data["Waktu_Transaksi"].dt.hour.astype("Int64")

    return data


def cleaning_summary(raw: pd.DataFrame, clean: pd.DataFrame) -> dict[str, object]:
    """Create compact, reproducible quality metrics for the report and dashboard."""
    missing = clean.isna().sum().astype(int).to_dict()
    return {
        "baris_awal": int(len(raw)),
        "baris_setelah_dedup": int(len(clean)),
        "duplikat_dihapus": int(len(raw) - len(clean)),
        "timestamp_gagal": int(clean["Waktu_Transaksi"].isna().sum()),
        "harga_nol_atau_negatif": int((clean["Harga_Pesanan"] <= 0).sum()),
        "anomali_menurut_sumber": int(clean["Anomali_Sumber_Kaggle"].sum()),
        "outlier_iqr": int(clean["Outlier_IQR"].sum()),
        "harga_mencurigakan_iqr": int(clean["Harga_Mencurigakan"].sum()),
        "nilai_kosong_per_kolom": missing,
    }