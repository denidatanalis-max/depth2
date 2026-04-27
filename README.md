# Jurnal POC — Sistem Manajemen Jurnal Ilmiah

Proof of Concept website untuk pengelolaan dan publikasi jurnal ilmiah internal.

## Fitur

- **Hierarki User**: Supervisor → Manager → Admin → Scoring (+ Super Admin)
- **Workflow Cycle**: Buat Draft → Ajukan ke Manager → Approve/Tolak → Upload PDF → Verifikasi Admin → Revisi (loop)
- **Data Isolation**: Supervisor tidak bisa melihat jurnal supervisor lain
- **Dashboard per Role**: Setiap role punya tampilan dashboard berbeda
- **Activity Log**: Riwayat lengkap setiap aksi pada jurnal
- **File Upload**: Upload file jurnal PDF

## Persyaratan

- Python 3.11
- pip

## Cara Install & Jalankan

### 1. Extract file dan masuk ke folder project

```bash
cd jurnal_poc
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

## Akun Demo

Password semua: `demo1234`

| Username | Role | Keterangan |
|----------|------|------------|
| `supervisor1` | Supervisor (Penulis) | Bawahan Manager 1 |
| `supervisor2` | Supervisor (Penulis) | Bawahan Manager 1 |
| `supervisor3` | Supervisor (Penulis) | Bawahan Manager 1 |
| `supervisor4` | Supervisor (Penulis) | Bawahan Manager 2 |
| `supervisor5` | Supervisor (Penulis) | Bawahan Manager 2 |
| `manager1` | Manager (Approver) | Budi Santoso |
| `manager2` | Manager (Approver) | Siti Rahma |
| `admin1` | Admin (Helpdesk) | Yuni Astuti |
| `scoring1` | Scoring (Penilai) | Prof. Reviewer |
| `superadmin` | Super Admin | Akses ke Django Admin Panel |

## Hierarki

```
Manager 1 (Budi Santoso) — manager1
├── Supervisor 1 (Andi Pratama) — supervisor1
├── Supervisor 2 (Dewi Lestari) — supervisor2
└── Supervisor 3 (Fajar Nugroho) — supervisor3

Manager 2 (Siti Rahma) — manager2
├── Supervisor 4 (Rina Wijaya) — supervisor4
└── Supervisor 5 (Hadi Kurniawan) — supervisor5

Admin (Yuni Astuti) — admin1
Scoring (Prof. Reviewer) — scoring1
Super Admin — superadmin
```

## Alur Workflow

```
Step 01: Supervisor buat jurnal (Draft / Sosialisasi)
    ↓
Step 02: Ajukan ke Manager → Manager Approve atau Tolak
    ↓ (jika disetujui)
Step 03: Supervisor upload file jurnal (PDF)
    ↓
Step 04: Admin mulai verifikasi kelengkapan
    ↓
Step 05: Admin monitoring → Lolos Verifikasi atau Minta Revisi
    ↓ (jika minta revisi)
    ↩ Kembali ke Step 02 (supervisor edit & ajukan ulang)
    ↓ (jika lolos)
    → Siap ke tahap Scoring (belum diimplementasi di POC ini)
```

## Struktur Project

```
jurnal_poc/
├── jurnal_poc/          # Settings & URL config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── journal/             # App utama
│   ├── models.py        # Model: UserProfile, Journal, JournalLog
│   ├── views.py         # Views per role
│   ├── forms.py         # Form jurnal & review
│   ├── urls.py          # URL routing
│   ├── admin.py         # Django admin config
│   └── management/
│       └── commands/
│           └── seed_demo.py  # Seed data demo
├── templates/           # HTML templates
│   ├── base.html        # Layout utama + sidebar
│   ├── login.html       # Halaman login
│   ├── dashboard/       # Dashboard per role
│   │   ├── supervisor.html
│   │   ├── manager.html
│   │   ├── admin.html
│   │   └── superadmin.html
│   └── journal/         # Halaman jurnal
│       ├── create.html
│       ├── detail.html
│       ├── edit.html
│       └── upload.html
├── static/              # Static files (CSS, JS)
├── media/               # Uploaded files
├── requirements.txt     # Dependencies
├── manage.py
└── README.md
```

## Deploy ke cPanel

1. Upload semua file ke cPanel
2. Setup Python App di cPanel → pilih Python 3.11
3. Set Application root ke folder project
4. Set Application URL
5. Set Application startup file: `passenger_wsgi.py` (buat file ini, lihat bawah)
6. Install requirements: `pip install -r requirements.txt`
7. Jalankan: `python manage.py migrate && python manage.py seed_demo && python manage.py collectstatic --noinput`

### File `passenger_wsgi.py` untuk cPanel:

```python
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jurnal_poc.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## Tech Stack

- Python 3.11
- Django 4.2 LTS
- Bootstrap 5
- SQLite (bisa upgrade ke MySQL/PostgreSQL)
- django-crispy-forms + crispy-bootstrap5
