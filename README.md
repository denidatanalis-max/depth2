# Depth Culture — Sistem Manajemen Jurnal Perusahaan

Website lengkap untuk pengelolaan dan publikasi Jurnal Perusahaan internal.

## Fitur

- **Workflow Multi-Tahap**: Writer → Manager (2x review) → Admin → Scoring → Tim Rekomendasi → Publikasi
- **Hierarki User**: Writer → Manager → Admin → Scoring → Tim Rekomendasi (+ Super Admin)
- **Review Dua Kali oleh Manager**: Manager mereview judul/ringkasan, lalu mereview file PDF secara terpisah
- **Scoring & Penilaian**: 4 kriteria (Orisinalitas, Metodologi, Kualitas Penulisan, Relevansi), skor 1–100
- **Tim Rekomendasi**: Grup user multi-anggota yang memberi keputusan akhir sebelum publikasi
- **Admin Bisa Bypass**: Admin dapat mempublikasikan langsung tanpa menunggu Tim Rekomendasi
- **Edit Terkontrol**: Judul terkunci setelah disetujui Manager, ringkasan boleh diedit saat upload (dengan timestamp)
- **Halaman Publik**: Jurnal yang sudah dipublikasikan bisa dibaca tanpa login (`/publikasi/`)
- **Data Isolation**: Writer hanya bisa melihat jurnal miliknya sendiri
- **Dashboard per Role**: Setiap role punya tampilan dan aksi berbeda
- **Activity Log**: Riwayat lengkap setiap aksi pada jurnal
- **Revision Loop**: Jurnal bisa dikembalikan untuk revisi di berbagai tahap

## Persyaratan

- Python 3.11
- pip

## Cara Install & Jalankan

### 1. Masuk ke folder project

```bash
cd depth2
```

### 2. Buat virtual environment

```bash
python3.11 -m venv venv
source venv/bin/activate    # Linux/Mac
# atau
venv\Scripts\activate       # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Jalankan migrasi database

```bash
python manage.py migrate
```

### 5. Buat data demo (user & hierarchy)

```bash
python manage.py seed_demo
```

### 6. Jalankan server

```bash
python manage.py runserver
```

Buka browser: http://127.0.0.1:8000/

<<<<<<< HEAD
=======
<<<<<<< HEAD
## Hierarki
=======
>>>>>>> 76c0dd3
---

## Akun Demo

Password semua akun: `demo1234`

| Username | Role | Nama | Keterangan |
|----------|------|------|------------|
| `supervisor1` | Writer (Penulis) | Andi Pratama | Bawahan Manager 1 |
| `supervisor2` | Writer (Penulis) | Dewi Lestari | Bawahan Manager 1 |
| `supervisor3` | Writer (Penulis) | Fajar Nugroho | Bawahan Manager 1 |
| `supervisor4` | Writer (Penulis) | Rina Wijaya | Bawahan Manager 2 |
| `supervisor5` | Writer (Penulis) | Hadi Kurniawan | Bawahan Manager 2 |
| `manager1` | Leader (Approver) | Budi Santoso | — |
| `manager2` | Leader (Approver) | Siti Rahma | — |
| `admin1` | Admin | Yuni Astuti | Collect & Publikasi |
| `scoring1` | Scoring (Penilai) | Prof. Reviewer | — |
| `recom1` | Tim Rekomendasi | Dr. Hartono | — |
| `recom2` | Tim Rekomendasi | Dr. Melinda | — |
| `superadmin` | Super Admin | — | Akses ke Django Admin Panel |

---

## Hierarki User
<<<<<<< HEAD
=======
>>>>>>> 661d5a6 (30042026)
>>>>>>> 76c0dd3

```
Manager 1 (Budi Santoso) — manager1
├── Supervisor 1 (Andi Pratama)  — supervisor1
├── Supervisor 2 (Dewi Lestari)  — supervisor2
└── Supervisor 3 (Fajar Nugroho) — supervisor3

Manager 2 (Siti Rahma) — manager2
├── Supervisor 4 (Rina Wijaya)   — supervisor4
└── Supervisor 5 (Hadi Kurniawan)— supervisor5

Admin (Yuni Astuti)     — admin1
Scoring (Prof. Reviewer)— scoring1
Tim Rekomendasi         — recom1, recom2
Super Admin             — superadmin
```

---

## Alur Workflow

```
Step 01 — Writer membuat jurnal
          Isi: Judul + Ringkasan (belum ada PDF)
    ↓
Step 02 — Writer mengajukan ke Manager
          Manager mereview judul & ringkasan
          ├─ [Tolak] → kembali ke Writer untuk revisi judul/ringkasan
          └─ [Setuju] → kembali ke Writer untuk upload PDF
    ↓
Step 03 — Writer upload file PDF
          Judul terkunci (tidak bisa diedit)
          Ringkasan boleh diedit (dicatat timestamp perubahannya)
          Setelah upload → dikirim ke Manager untuk review file
    ↓
Step 04 — Manager mereview file PDF
          ├─ [Tolak file] → kembali ke Writer untuk upload ulang
          └─ [Setuju file] → dikirim ke Admin
    ↓
Step 05 — Admin mengumpulkan jurnal
          Admin melihat file PDF
          Tombol: "Kirim ke Scoring"
    ↓
Step 06 — Scoring memberikan penilaian
          4 kriteria × skor 1–100:
          • Orisinalitas
          • Metodologi
          • Kualitas Penulisan
          • Relevansi
          Hasil Scoring:
          ├─ [Perlu Revisi] → kembali ke Writer (revisi ulang dari Step 02)
          ├─ [Tidak Layak]  → NOT_RECOMMENDED (jurnal ditutup)
          └─ [Layak]        → dikirim ke Tim Rekomendasi
    ↓
Step 07 — Tim Rekomendasi memberikan keputusan akhir
          (Dapat diisi oleh lebih dari 1 anggota tim)
          ├─ [Tidak Direkomendasikan] → NOT_RECOMMENDED
          └─ [Setuju / Rekomendasikan] → RECOMMENDED → Admin dapat publikasi
    ↓
Step 08 — Admin mempublikasikan jurnal
          Pilihan Admin:
          • Publikasikan setelah Tim Rekomendasi setuju (RECOMMENDED)
          • Publikasikan langsung tanpa menunggu Tim Rekomendasi (bypass)
    ↓
Step 09 — Jurnal PUBLISHED
          Dapat diakses publik di /publikasi/<id>/
```

---

## Aturan per Role

| Role | Yang Bisa Dilakukan |
|------|---------------------|
| **Writer (Supervisor)** | Buat jurnal, edit judul+ringkasan (saat draft/revisi), upload PDF (saat approved), ajukan ke Manager |
| **Manager (Leader)** | Review & approve/tolak judul+ringkasan, review & approve/tolak file PDF |
| **Admin** | Kirim jurnal ke Scoring, publikasikan jurnal (bisa bypass Tim Rekomendasi) |
| **Scoring** | Beri nilai 4 kriteria, beri rekomendasi (layak/revisi/tidak layak) |
| **Tim Rekomendasi** | Review hasil Scoring, setujui atau tolak untuk publikasi |
| **Super Admin** | Publikasikan jurnal + akses Django Admin Panel (`/admin/`) |

---

## Status Jurnal

| Status | Keterangan |
|--------|------------|
| `draft` | Baru dibuat, belum diajukan |
| `submitted` | Diajukan ke Manager (menunggu review judul/ringkasan) |
| `approved` | Manager setuju → Writer siap upload PDF |
| `rejected` | Manager tolak → Writer revisi judul/ringkasan |
| `uploaded` | PDF diupload → menunggu review file oleh Manager |
| `under_review` | Manager setuju file → dikumpulkan Admin, siap ke Scoring |
| `scoring` | Sedang dinilai oleh Scoring |
| `score_revision` | Scoring minta revisi → Writer revisi ulang |
| `under_recommendation` | Menunggu keputusan Tim Rekomendasi |
| `recommended` | Tim Rekomendasi setuju → siap dipublikasikan |
| `not_recommended` | Ditolak (oleh Manager, Scoring, atau Tim Rekomendasi) |
| `published` | Dipublikasikan, bisa diakses publik |

---

## URL Penting

| URL | Keterangan |
|-----|------------|
| `/` atau `/dashboard/` | Dashboard (tampilan sesuai role) |
| `/login/` | Halaman login |
| `/publikasi/` | Halaman publik — daftar jurnal yang sudah terbit |
| `/publikasi/<id>/` | Detail jurnal publik beserta skor |
| `/journal/create/` | Buat jurnal baru (Writer) |
| `/journal/<id>/` | Detail jurnal (internal, aksi berbeda per role) |
| `/journal/<id>/upload/` | Upload PDF + edit ringkasan (Writer, setelah approved) |
| `/admin/` | Django Admin Panel (superadmin) |

---

## Struktur Project

```
depth2/
├── jurnal_poc/              # Settings & URL config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── journal/                 # App utama
│   ├── models.py            # UserProfile, Journal, JournalScore, JournalLog
│   ├── views.py             # Views per role + public views
│   ├── forms.py             # Form jurnal, upload, review, scoring
│   ├── urls.py              # URL routing
│   ├── admin.py             # Django admin config
│   └── management/
│       └── commands/
│           └── seed_demo.py # Seed data demo (semua role)
├── templates/
│   ├── base.html            # Layout utama + sidebar (tema merah marun)
│   ├── login.html           # Halaman login
│   ├── dashboard/
│   │   ├── supervisor.html  # Dashboard Writer
│   │   ├── manager.html     # Dashboard Manager
│   │   ├── admin.html       # Dashboard Admin
│   │   ├── scoring.html     # Dashboard Scoring
│   │   ├── recommendation.html  # Dashboard Tim Rekomendasi
│   │   └── superadmin.html  # Dashboard Super Admin
│   ├── journal/
│   │   ├── create.html      # Buat jurnal (judul + ringkasan)
│   │   ├── detail.html      # Detail jurnal + aksi per role
│   │   ├── edit.html        # Edit jurnal (saat draft/revisi)
│   │   └── upload.html      # Upload PDF + edit ringkasan
│   └── public/
│       ├── journal_list.html
│       └── journal_detail.html
├── static/
│   └── img/
│       └── background_login2.png  # Background tema
├── media/                   # File PDF yang diupload
├── requirements.txt
├── passenger_wsgi.py        # WSGI untuk cPanel
├── manage.py
└── README.md
```

---

## Deploy ke cPanel

1. Upload semua file ke cPanel
2. Setup Python App di cPanel → pilih Python 3.11
3. Set Application root ke folder project
4. Set Application URL
5. Set Application startup file: `passenger_wsgi.py`
6. Install requirements: `pip install -r requirements.txt`
7. Jalankan:
   ```bash
   python manage.py migrate
   python manage.py seed_demo
   python manage.py collectstatic --noinput
   ```

### File `passenger_wsgi.py` untuk cPanel

```python
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jurnal_poc.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

---

## Tech Stack

- Python 3.11
- Django 4.2 LTS
- Bootstrap 5 + Bootstrap Icons
- SQLite (bisa upgrade ke MySQL/PostgreSQL)
- django-crispy-forms + crispy-bootstrap5
