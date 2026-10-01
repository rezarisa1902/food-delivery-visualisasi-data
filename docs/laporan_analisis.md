# Laporan Analisis Visualisasi Data

## Judul

**Data to Insight: Analisis Pesanan dan Pengalaman Pelanggan pada Layanan Food Delivery**

## Tujuan dan pertanyaan analisis

Project ini mengeksplorasi pola pesanan, waktu tunggu, jarak pengiriman, harga, dan rating pada dataset simulasi layanan food delivery. Pertanyaan yang dijawab dashboard:

1. Bagaimana jumlah pesanan berubah dari bulan ke bulan?
2. Kategori menu mana yang paling banyak dipesan?
3. Bagaimana distribusi waktu tunggu pada tiap kategori?
4. Apakah jarak pengiriman berhubungan dengan waktu tunggu?
5. Bagaimana distribusi rating pelanggan?
6. Pada kombinasi hari dan jam transaksi mana rata-rata waktu tunggu lebih tinggi?

## Data

Dataset berisi 8.500 baris dan 11 kolom, mencakup pesanan dari 1 Januari sampai 3 Desember 2024. Kolom utamanya meliputi waktu transaksi, kategori menu, harga, jarak kirim, waktu tunggu, rating, status promo, tingkat keluhan, dan status pesanan. Data ini sintetis; temuan hanya menggambarkan dataset untuk keperluan tugas. sumber URL: https://www.kaggle.com/datasets/zkyfauzi/food-delivery-dataset

Sumber: Kaggle, akun `zkyfauzi`, https://www.kaggle.com/datasets/zkyfauzi/food-delivery-dataset. Diakses 1 Oktober 2026. Lisensi yang tercantum pada Data Card: CC0 Public Domain.

## Cleaning dan preprocessing

- Tidak ditemukan ID pesanan duplikat pada file sumber. Pipeline tetap membuang duplikat berdasarkan ID jika ditemukan.
- Format timestamp bercampur antara ISO dan `DD/MM/YYYY HH:MM`; keduanya diparse ke datetime. Tidak ada timestamp yang gagal diparse.
- Nilai kosong dipertahankan sebagai missing dan tidak diisi dengan nilai buatan. Ada 595 jarak kirim kosong serta masing-masing 1.700 rating dan ulasan kosong.
- Rating dibatasi ke skala 1–5; nilai di luar skala dijadikan missing. Jarak nol/negatif dan waktu tunggu negatif juga dijadikan missing.
- Harga diberi dua flag: aturan sumber Kaggle (harga nol/negatif atau di atas Rp500.000, 270 baris) dan kandidat outlier Tukey IQR (harga positif di atas Rp85.250, 302 baris). Data tidak dihapus. KPI nilai pesanan menggunakan aturan sumber Kaggle, sedangkan flag IQR dipertahankan untuk analisis sensitivitas.
- Status promo dinormalisasi menjadi boolean. Kolom turunan bulan, hari, dan jam dibuat dari timestamp.

## Hasil utama

- Status pesanan terdiri dari 7.584 selesai (89,2%), 611 dibatalkan (7,2%), dan 305 refund (3,6%).
- Ayam adalah kategori dengan jumlah pesanan terbanyak: 3.030 (35,6%), diikuti Kopi 2.141, Mie 1.681, dan Martabak 1.648.
- Rata-rata rating yang tersedia adalah 4,18 dari 5. Rating hanya tercatat pada 6.800 pesanan, sehingga hasil ini tidak mencakup seperlima baris yang ratingnya kosong.
- Rata-rata waktu tunggu sekitar 22,7 menit. Mie memiliki rata-rata waktu tunggu tertinggi di antara kategori (23,19 menit), tetapi perbedaannya dengan kategori lain relatif kecil.
- Jarak kirim dan waktu tunggu menunjukkan korelasi Pearson sekitar 0,755 pada baris dengan kedua nilai tersedia. Ini adalah hubungan pada data sintetis, bukan bukti bahwa jarak menjadi satu-satunya penyebab waktu tunggu.
- Jumlah pesanan bulanan jauh lebih tinggi pada Januari–Maret (masing-masing 2.226, 2.101, dan 2.184) daripada April–Desember (207–245 per bulan). Format tanggal slash hanya muncul pada Januari–Maret, sedangkan bulan-bulan lain memakai ISO; pola waktu dan format sumber ini berimpit, sehingga penurunan tajam perlu diperlakukan sebagai karakteristik atau potensi ketidakseimbangan dataset, bukan langsung sebagai bukti penurunan permintaan nyata.
- Dengan mengecualikan anomali menurut aturan sumber Kaggle, metrik nilai pesanan memakai pesanan selesai yang tidak termasuk harga nol/negatif atau di atas Rp500.000. Angka ini bukan pendapatan aktual karena dataset sintetis dan tidak menyediakan informasi biaya, pajak, atau refund terperinci.
- Dengan kebijakan tersebut, terdapat 7.338 pesanan selesai valid dengan total nilai pesanan Rp243.363.500. Angka ini adalah metrik dataset, bukan pendapatan aktual.

## Visualisasi

Dashboard memuat line chart tren bulanan, bar chart jumlah pesanan per kategori, box plot waktu tunggu, scatter plot jarak terhadap waktu tunggu, histogram rating, dan heatmap hari-jam terhadap rata-rata waktu tunggu. Setiap grafik memiliki pertanyaan analisis, label, dan interaksi filter.

## Batasan dan rekomendasi

1. Dataset sintetis tidak dapat digunakan untuk menyimpulkan kinerja bisnis nyata atau menggeneralisasi perilaku pelanggan.
2. Volume Januari–Maret yang jauh berbeda dari bulan lain dan pencampuran format timestamp perlu dikonfirmasi terhadap proses pembentukan data sebelum tren musiman ditafsirkan.
3. Rating dan jarak kirim memiliki missing value; analisis yang memakai kolom tersebut hanya mencakup baris yang tersedia.
4. Nilai harga ekstrem memerlukan klarifikasi domain. Untuk sementara, nilai tersebut ditandai dan dikecualikan dari agregat nominal, tetapi tetap tersedia untuk audit.
5. Dataset tidak memiliki lokasi pelanggan/restoran, biaya, atau waktu antar-tahap pengiriman, sehingga belum cukup untuk mengevaluasi performa wilayah, profitabilitas, atau sumber keterlambatan secara kausal.

Untuk keputusan operasional nyata, kumpulkan data transaksi aktual yang representatif, validasi satuan dan format terhadap sumber, lalu bandingkan performa dengan konteks wilayah dan kapasitas kurir.