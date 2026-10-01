# Data to Insight: Food Delivery

Project visualisasi data interaktif untuk menganalisis pesanan, waktu pengiriman, harga, dan rating pelanggan. Dataset yang digunakan adalah data sintetis yang telah dikonfirmasi boleh dipakai untuk tugas; hasilnya tidak mewakili transaksi bisnis nyata.
Sumber dataset: Kaggle, akun `zkyfauzi`.
URL: https://www.kaggle.com/datasets/zkyfauzi/food-delivery-dataset
Tanggal akses: 1 Oktober 2026.
Lisensi yang tercantum pada Data Card: CC0 Public Domain.

## Menjalankan aplikasi

Pastikan Python 3.10 atau lebih baru tersedia, lalu jalankan dari folder project:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Buka URL lokal yang ditampilkan Streamlit, biasanya `http://localhost:8501`.

## Hosting Online

Platform yang direkomendasikan adalah **GitHub + Streamlit Community Cloud**. Project ini adalah aplikasi Streamlit, sehingga tidak perlu diubah menjadi aplikasi Vercel.

1. Buat repository baru di GitHub, misalnya `food-delivery-visualisasi-data`.
2. Dari folder project, jalankan perintah berikut di PowerShell:

```powershell
git init
git add .
git commit -m "Initial food delivery visualization project"
git branch -M main
git remote add origin https://github.com/USERNAME/NAMA-REPOSITORY.git
git push -u origin main
```

Ganti `USERNAME/NAMA-REPOSITORY` dengan repository GitHub milikmu. Jangan mengunggah `.venv` atau file rahasia; `.gitignore` sudah menanganinya.

3. Buka https://share.streamlit.io/ dan masuk dengan GitHub.
4. Pilih **New app**.
5. Pilih repository, branch `main`, dan file utama `app.py`.
6. Klik **Deploy**.

Setelah deployment selesai, Streamlit Cloud memberikan URL publik yang dapat dibagikan kepada dosen atau dibuka dari laptop dan HP. Repository dapat dibuat **private** jika ingin membatasi akses kode; aplikasi tetap dapat dibagikan melalui URL deployment sesuai pengaturan akun.

## Isi project

- `synthetic_fooddelivery_dataset.csv`: data sumber, tidak dimodifikasi.
- `data_processing.py`: parsing, cleaning, fitur waktu, dan flag harga mencurigakan.
- `scripts/clean_dataset.py`: menghasilkan CSV bersih dan ringkasan cleaning.
- `app.py`: dashboard interaktif dengan filter dan enam visualisasi.
- `tests/test_data_processing.py`: tes unit aturan cleaning.
- `docs/laporan_analisis.md`: metode, temuan, batasan, dan rekomendasi.
- `data/processed/`: artefak hasil cleaning setelah skrip dijalankan.

Di dashboard, gunakan filter tanggal, kategori, status, dan promo. CSV hasil cleaning dapat diunduh melalui tombol di bagian bawah halaman.

Untuk membuat berkas hasil cleaning di project, jalankan:

```powershell
python scripts/clean_dataset.py
```

## Metode cleaning

Timestamp ISO dan `DD/MM/YYYY HH:MM` disatukan menjadi tipe datetime. Kolom numerik dikonversi ke angka, rating di luar skala 1–5 dan jarak tidak positif dijadikan missing, ID duplikat dibuang, dan status promo dinormalisasi menjadi boolean. Data kosong tidak diimputasi. Harga diberi dua flag: `Anomali_Sumber_Kaggle` untuk harga nol/negatif atau di atas Rp500.000, dan `Outlier_IQR` untuk kandidat di atas pagar statistik IQR. Semua baris tetap dipertahankan untuk audit. Nilai pesanan pada KPI menggunakan aturan sumber Kaggle.

Jalankan tes dengan:

```powershell
python -m unittest discover -s tests -v
```