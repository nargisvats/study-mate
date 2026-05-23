# StudyMate

Global student–tutor live learning platform built with **Django 5**, **MySQL** (SQLite fallback for dev), and responsive HTML/CSS/JS templates.

## Features

- **Roles:** Student, Tutor, Admin
- **Tutor search** with filters (subject, country, price, rating, free demo)
- **Booking** with UTC scheduling, conflict detection, 1-on-1 and group sessions
- **Mock & Stripe payments** (pluggable `PaymentProvider`)
- **Live sessions** via Jitsi Meet embed or Daily.co API
- **Reviews**, notifications, session file sharing
- **Django Admin** for tutor verification and payment disputes
- **Admin analytics dashboard**

## Quick start (SQLite)

```bash
cd finalprojectstudymate
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py seed_subjects
python manage.py seed_demo
python manage.py runserver
```

Open http://127.0.0.1:8000

## Demo accounts

All demo accounts use password: **`StudyMate123!`**

| Role | Username | Notes |
|------|----------|--------|
| Student | `demostudent` | Has sample bookings (completed, confirmed, pending payment) |
| Tutor | `tutor_alex` | Math & Physics, USA, approved |
| Tutor | `tutor_maya` | English & Spanish, UK, approved |
| Tutor | `tutor_sam` | CS & Math, approved |
| Tutor (pending) | `tutor_pending` | For admin approval workflow |
| Platform admin | `demoadmin` | Analytics dashboard + tutor approval |

Re-seed demo data: `python manage.py seed_demo --reset`

## Demo walkthrough

1. **Find tutors** — http://127.0.0.1:8000/catalog/search/?subject=1&country=USA  
   Filter by subject, country, price, or free demo; open a tutor profile.

2. **Tutor profile & book** — http://127.0.0.1:8000/profiles/tutor/1/  
   Log in as `demostudent`, click **Book** on a subject, pick date/time within tutor availability.

3. **Pay (mock)** — Student dashboard → **Pay** on `PENDING_PAYMENT` booking, or complete checkout at `/payments/mock/<booking_id>/`.

4. **Live session** — After status is `CONFIRMED`, open **Join** on the dashboard or go to `/sessions/room/<booking_id>/` (Jitsi embed).

5. **Review** — Tutor marks session **complete** (or use seeded completed booking) → student **Leave review** on dashboard.

6. **Tutor dashboard** — Log in as `tutor_alex` → manage bookings, availability, earnings.

7. **Admin verification** — Log in as `demoadmin` → http://127.0.0.1:8000/admin-ops/dashboard/ → **Approve** `tutor_pending`, or use Django admin actions on Tutor profiles.

## MySQL setup

Set in `.env`:

```
USE_MYSQL=true
DB_NAME=studymate
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=127.0.0.1
DB_PORT=3306
```

Create the database, then run `migrate`.

## Environment variables

See `.env.example` for:

- `PAYMENT_PROVIDER` — `mock` or `stripe`
- `LIVE_PROVIDER` — `jitsi` or `daily`
- Stripe keys and Daily.co API key

## Management commands

```bash
python manage.py seed_subjects      # Seed subjects & languages
python manage.py seed_demo          # Demo users, tutors, bookings
python manage.py seed_demo --reset  # Replace demo users
python manage.py send_session_reminders   # Email/in-app reminders (cron)
```

## Production (Gunicorn)

```bash
pip install gunicorn
python manage.py collectstatic --noinput
gunicorn -c gunicorn.conf.py studymate.wsgi:application
```

## Project structure

```
accounts/          Custom User, auth
profiles/          Student/Tutor profiles, credentials, demos
catalog/           Subjects, tutor offerings, search
scheduling/        Availability, bookings
payments/          Mock + Stripe providers
sessions_live/     Jitsi/Daily rooms, file sharing
reviews/           Post-session ratings
notifications/     In-app + email reminders
admin_ops/         Analytics dashboard
templates/         HTML templates
static/            CSS & JS
```

## Tests

```bash
python manage.py test
```

## Default workflows

1. **Student:** Register → edit profile → search tutors → book session → pay (mock/Stripe) → join live room → leave review
2. **Tutor:** Register → complete profile → add subjects/availability → get verified in admin → accept bookings → conduct sessions
3. **Admin:** `/admin-ops/dashboard/` for KPIs and tutor approval; `/admin/` for full Django admin

## Phase notes

| Phase | Status |
|-------|--------|
| Phase 1 | Core MVP — auth, profiles, search, booking, reviews, mock pay, Jitsi |
| Phase 2 | Stripe webhooks, Daily.co rooms, session uploads |
| Phase 3 | Group join, reminder cron, admin analytics, Gunicorn config |
