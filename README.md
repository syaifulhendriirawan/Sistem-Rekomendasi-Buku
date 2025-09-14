# Sistem Rekomendasi Buku

Proyek ini adalah sistem rekomendasi buku yang dibuat menggunakan _collaborative filtering_. Sistem ini akan merekomendasikan buku kepada pengguna berdasarkan kemiripan dengan buku yang telah dipilih. Aplikasi ini dibangun dengan `Streamlit` untuk antarmuka web yang interaktif.

## Cara Kerja

Sistem rekomendasi ini bekerja dengan cara berikut:

1.  **Pengumpulan Data**: Menggunakan dataset yang berisi informasi tentang buku, pengguna, dan peringkat yang diberikan oleh pengguna.
2.  **Pemrosesan Data**: Data dibersihkan dan diproses untuk memastikan kualitas rekomendasi. Hanya pengguna yang telah memberikan lebih dari 200 peringkat yang akan dipertimbangkan.
3.  **Pembuatan Model**: Sebuah _pivot table_ dibuat dengan buku sebagai baris, pengguna sebagai kolom, dan peringkat sebagai nilainya. Model `NearestNeighbors` dari `scikit-learn` kemudian dilatih pada _pivot table_ ini untuk menemukan buku-buku yang paling mirip berdasarkan peringkat pengguna.
4.  **Rekomendasi**: Ketika pengguna memilih sebuah buku, model akan mencari dan menampilkan 5 buku yang paling mirip.

## Instalasi

Untuk menjalankan proyek ini di lingkungan lokal Anda, ikuti langkah-langkah berikut:

1.  **Clone Repositori**

    ```bash
    git clone [https://github.com/syaifulhendriirawan/sistem-rekomendasi-buku.git](https://github.com/syaifulhendriirawan/sistem-rekomendasi-buku.git)
    cd sistem-rekomendasi-buku
    ```

2.  **Buat Lingkungan Virtual (Opsional, tapi direkomendasikan)**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Untuk Windows, gunakan `venv\Scripts\activate`
    ```

3.  **Instal Ketergantungan**
    Pastikan Anda memiliki file `requirements.txt` yang berisi semua pustaka yang diperlukan. Jalankan perintah berikut untuk menginstalnya:
    ```bash
    pip install -r requirements.txt
    ```

## Penggunaan

Anda dapat menggunakan aplikasi ini dengan dua cara: melatih model dari awal atau langsung menjalankan aplikasi web dengan model yang sudah ada.

### 1. Melatih Model (Opsional)

Jika Anda ingin melatih ulang model dengan data baru, Anda bisa menjalankan skrip `main.py`.

```bash
python main.py
```

Setelah proses pelatihan selesai, model dan artefak lainnya akan disimpan.

### 2. Menjalankan Aplikasi Web

Untuk menjalankan aplikasi web, gunakan perintah streamlit.

```bash
streamlit run app.py
```

Aplikasi akan terbuka di browser Anda. Berikut cara menggunakannya:

1. Pilih buku dari menu dropdown yang tersedia.
2. Klik tombol "Show Recommendation".
3. Sistem akan menampilkan 5 buku yang direkomendasikan beserta gambar sampulnya.

Selamat mencoba! 📚
