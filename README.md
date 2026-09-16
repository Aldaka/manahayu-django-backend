# 🌿 Manahayu Holistic Farm Website

### Pengembangan Sistem Backend Website Manahayu Berbasis Django untuk Mendukung Manajemen Konten Digital

---

## 📌 1. Pendahuluan

Repositori ini berisi sistem backend dan antarmuka web yang dikembangkan untuk **Manahayu Holistic Farm**, sebuah unit usaha pariwisata, penginapan (*homestay*), dan kafe bernuansa tradisional Jawa di bawah naungan Badan Usaha Milik Desa (BUMDes) Giripurno, Kecamatan Bumiaji, Kota Batu.

Proyek **Praktek Kerja Lapangan (PKL)** ini bertujuan untuk mendukung digitalisasi pengelolaan usaha melalui sistem manajemen konten berbasis web. Sistem mencakup pengelolaan informasi penginapan, menu kafe, paket wisata, fasilitas, serta integrasi ulasan pelanggan dari Google Maps.

---

## 👥 2. Tim Pengembang

Proyek kolaborasi PKL mahasiswa Program Studi Teknik Informatika, Fakultas Teknologi dan Desain, **Institut Teknologi dan Bisnis Asia Malang**.

| Nama                     | NIM      | Peran                                     |
| ------------------------ | -------- | ----------------------------------------- |
| **Ahmad Zulfi Kurniadi** | 22201274 | Backend & Integration Support             |
| **Pasadena Saka**        | 22201298 | Lead Backend Developer & System Architect |

---

## 🚀 3. Fitur Utama Sistem

### 🖥️ Dashboard Admin

* Kustomisasi Django Admin Panel.
* Pengelolaan data menggunakan operasi CRUD (*Create, Read, Update, Delete*).
* Pengelolaan konten secara mandiri oleh pengelola.

### 🏡 Manajemen Penginapan & Fasilitas

* Pengelolaan data kamar.
* Pengelolaan tipe kamar.
* Pengelolaan harga per malam.
* Pengelolaan fasilitas.
* Relasi data antara kamar dan fasilitas.

### ☕ Katalog Menu Kafe

* Pengelolaan menu makanan dan minuman.
* Pengelompokan menu berdasarkan kategori.
* Pengelolaan galeri foto menu.

### 📅 Sistem Reservasi & Booking

* Struktur data untuk pemesanan kamar.
* Struktur data untuk paket wisata.
* Mendukung alur komunikasi antara pelanggan dan pengelola.

### ⭐ Integrasi Google Maps Reviews

* Integrasi dengan **SerpApi** untuk memperoleh data ulasan dari Google Maps.
* Penyimpanan data ulasan ke dalam database lokal.
* Pengelolaan data ulasan melalui sistem backend.

### 📱 Desain Responsif

Antarmuka website dikembangkan menggunakan **Tailwind CSS** sehingga dapat digunakan pada berbagai ukuran layar, baik desktop maupun perangkat mobile.

---

## 🛠️ 4. Arsitektur & Teknologi

Proyek ini menggunakan pola arsitektur **Model-View-Template (MVT)** yang disediakan oleh Django.

| Teknologi        | Penggunaan                                    |
| ---------------- | --------------------------------------------- |
| **Python**       | Bahasa pemrograman utama                      |
| **Django**       | Framework pengembangan web                    |
| **Tailwind CSS** | Styling dan antarmuka frontend                |
| **SQLite**       | Database untuk pengembangan                   |
| **PostgreSQL**   | Database yang siap digunakan untuk production |
| **SerpApi**      | Integrasi data Google Maps Reviews            |

---

## 📦 5. Panduan Instalasi & Menjalankan Proyek

Ikuti langkah berikut untuk menjalankan proyek pada komputer lokal.

### 1. Clone Repository

```bash
git clone https://github.com/USERNAME/REPOSITORY.git
cd REPOSITORY
```

> Ganti `USERNAME/REPOSITORY` dengan alamat repository GitHub yang sebenarnya.

### 2. Buat Virtual Environment

#### Windows

```bash
python -m venv venv
```

Aktifkan virtual environment:

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
```

Aktifkan virtual environment:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

Pastikan virtual environment sudah aktif, kemudian jalankan:

```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Environment

Buat file `.env` pada direktori utama project.

Contoh:

```env
SECRET_KEY=your-secret-key
DEBUG=True
SERPAPI_KEY=your-serpapi-key
```

> Jangan mengunggah file `.env` ke repository publik karena dapat berisi informasi sensitif seperti `SECRET_KEY` dan API key.

### 5. Migrasi Database

Jalankan perintah berikut:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Buat Akun Administrator

Untuk mengakses Django Admin Panel, buat akun superuser:

```bash
python manage.py createsuperuser
```

Kemudian masukkan username, email, dan password sesuai kebutuhan.

### 7. Jalankan Development Server

```bash
python manage.py runserver
```

Setelah server berjalan, buka browser dan akses:

**Website utama:**

```text
http://127.0.0.1:8000/
```

**Admin Panel:**

```text
http://127.0.0.1:8000/admin/
```

---

## 🗂️ 6. Struktur Direktori Proyek

```text
manahayu/
│
├── manahayu/             # Konfigurasi utama project Django
│   ├── settings.py       # Konfigurasi project
│   ├── urls.py           # Routing utama
│   └── ...
│
├── webapp/               # Aplikasi utama
│   ├── migrations/       # File migrasi database
│   ├── static/           # Aset statis
│   ├── templates/        # Template HTML
│   ├── admin.py          # Kustomisasi Django Admin
│   ├── models.py         # Struktur database
│   ├── views.py          # Logika aplikasi
│   └── ...
│
├── theme/                # Konfigurasi dan source Tailwind CSS
│
├── manage.py             # CLI utilitas Django
│
├── requirements.txt      # Dependencies Python
│
│
└── README.md             # Dokumentasi project
```

---

## 🔐 7. Keamanan

Beberapa file dan informasi sensitif tidak boleh diunggah ke repository publik.

Contohnya:

```text
.env
venv/
.venv/
node_modules/
```

File `.env` dapat berisi:

* Django `SECRET_KEY`
* API Key
* Password database
* Credential layanan eksternal

Gunakan file `.env.example` apabila ingin memberikan contoh konfigurasi kepada pengguna lain tanpa membagikan credential asli.

---

## 📄 8. Lisensi & Kredit

Proyek ini merupakan proyek akademis **Praktek Kerja Lapangan (PKL)** yang dikembangkan sebagai bagian dari kegiatan mahasiswa **Program Studi Teknik Informatika, Fakultas Teknologi dan Desain, Institut Teknologi dan Bisnis Asia Malang**.

Proyek dilaksanakan bekerja sama dengan **Pemerintah Desa Giripurno melalui BUMDes Manahayu Holistic Farm** pada periode **3 Februari hingga 31 Juli 2025**.

---

## 🙏 9. Acknowledgement

Terima kasih kepada:

* **Institut Teknologi dan Bisnis Asia Malang**
* **Pemerintah Desa Giripurno**
* **BUMDes Manahayu Holistic Farm**
* Dosen pembimbing dan seluruh pihak yang mendukung pelaksanaan kegiatan PKL.

---

<p align="center">
  🌿 <strong>Manahayu Holistic Farm</strong><br>
  Built with Django & Tailwind CSS
</p>
