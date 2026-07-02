# Helpdesk Ticketing System

A full-stack helpdesk / IT support ticketing app. Built with React (frontend), Django REST Framework (backend), and PostgreSQL (database).

## Features

- JWT authentication (register, login) with roles: Admin, Technician, User
- Ticket CRUD with status (Open, In Progress, Resolved, Closed) and priority (Low, Medium, High, Urgent)
- Assign tickets to technicians
- Dashboard with summary stats (status & priority charts)
- SLA tracking (automatic response & resolution targets based on priority, breach detection)
- Ticket comments, including internal notes (staff only)
- File attachments on tickets
- Knowledge base for troubleshooting articles
- Automated email notifications on ticket creation, status changes, and assignment

## Tech Stack

- **Frontend:** React (Vite), React Router, Axios, Recharts
- **Backend:** Django, Django REST Framework, Simple JWT
- **Database:** PostgreSQL (Supabase in production)

## Running Locally

### Backend

```bash
cd backend
python -m venv venv
./venv/Scripts/activate  # Windows
pip install -r requirements.txt
cp .env.example .env     # adjust as needed, or set USE_SQLITE=True for a quick start
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
