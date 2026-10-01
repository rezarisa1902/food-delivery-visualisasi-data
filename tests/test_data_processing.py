import unittest

import pandas as pd

from data_processing import clean_data, cleaning_summary


def make_row(order_id: str, timestamp: str, price: int, **overrides: object) -> dict[str, object]:
    row: dict[str, object] = {
        "ID_Pesanan": order_id,
        "Waktu_Transaksi": timestamp,
        "Kategori_Menu": "Kopi",
        "Harga_Pesanan": price,
        "Jarak_Kirim_KM": 2.5,
        "Waktu_Tunggu_Menit": 20,
        "Rating_Pelanggan": 4,
        "Ulasan_Teks": "Bagus",
        "Status_Promo": "False",
        "Tingkat_Keluhan": "Tidak Ada",
        "Status_Pesanan": "Selesai",
    }
    row.update(overrides)
    return row


class CleanDataTests(unittest.TestCase):
    def test_parses_both_timestamp_formats(self) -> None:
        raw = pd.DataFrame(
            [
                make_row("A", "2024-03-22 13:15:14", 20000),
                make_row("B", "24/02/2024 20:24", 25000),
            ]
        )

        clean = clean_data(raw)

        self.assertEqual(clean["Waktu_Transaksi"].dt.strftime("%Y-%m-%d").tolist(), [
            "2024-03-22",
            "2024-02-24",
        ])
        self.assertTrue(clean["Waktu_Transaksi"].notna().all())

    def test_deduplicates_and_preserves_invalid_price_as_flag(self) -> None:
        rows = [
            make_row("A", "2024-01-01 10:00:00", 10000),
            make_row("A", "2024-01-01 10:00:00", 10000),
            make_row("B", "2024-01-02 10:00:00", 0),
            make_row("C", "2024-01-03 10:00:00", 10000000),
        ]
        rows.extend(
            make_row(f"BASE-{price}", "2024-01-04 10:00:00", price)
            for price in range(11000, 18000, 1000)
        )
        raw = pd.DataFrame(rows)

        clean = clean_data(raw)
        summary = cleaning_summary(raw, clean)

        self.assertEqual(len(clean), 10)
        self.assertEqual(summary["duplikat_dihapus"], 1)
        self.assertTrue(clean.loc[clean["ID_Pesanan"].eq("B"), "Harga_Mencurigakan"].iloc[0])
        self.assertTrue(clean.loc[clean["ID_Pesanan"].eq("C"), "Harga_Mencurigakan"].iloc[0])
        self.assertTrue(clean.loc[clean["ID_Pesanan"].eq("B"), "Anomali_Sumber_Kaggle"].iloc[0])
        self.assertFalse(clean.loc[clean["ID_Pesanan"].eq("B"), "Outlier_IQR"].iloc[0])
        self.assertTrue(clean.loc[clean["ID_Pesanan"].eq("C"), "Outlier_IQR"].iloc[0])

    def test_invalid_rating_and_nonpositive_distance_become_missing(self) -> None:
        raw = pd.DataFrame(
            [make_row("A", "2024-01-01 10:00:00", 20000, Rating_Pelanggan=6, Jarak_Kirim_KM=0)]
        )

        clean = clean_data(raw)

        self.assertTrue(pd.isna(clean.loc[0, "Rating_Pelanggan"]))
        self.assertTrue(pd.isna(clean.loc[0, "Jarak_Kirim_KM"]))


if __name__ == "__main__":
    unittest.main()