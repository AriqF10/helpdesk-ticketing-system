# Helpdesk Ticketing System

Aplikasi helpdesk / IT support ticketing untuk portofolio. Dibangun dengan React (frontend), Django REST Framework (backend), dan PostgreSQL (database).

## Fitur

- Autentikasi JWT (register, login) dengan role: Admin, Technician, User
- CRUD tiket dengan status (Open, In Progress, Resolved, Closed) dan prioritas (Low, Medium, High, Urgent)
- Assign tiket ke teknisi
- Dashboard dengan ringkasan statistik (chart status & prioritas)
- SLA tracking (target respon & resolusi otomatis berdasarkan prioritas, deteksi breach)
- Komentar pada tiket, termasuk catatan internal (khusus staff)
- Upload lampiran file pada tiket
- Knowledge base artikel troubleshooting
- Notifikasi email otomatis saat tiket dibuat, status berubah, atau di-assign

## Tech Stack

- **Frontend:** React (Vite), React Router, Axios, Recharts
- **Backend:** Django, Django REST Framework, Simple JWT
- **Database:** PostgreSQL (Supabase di production)

## Menjalankan Secara Lokal

### Backend

```bash
cd backend
python -m venv venv
./venv/Scripts/activate  # Windows
pip install -r requirements.txt
cp .env.example .env     # sesuaikan isinya, atau set USE_SQLITE=True untuk quick start
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Deployment

- **Frontend:** Vercel
- **Backend:** Render
- **Database:** Supabase (PostgreSQL)
