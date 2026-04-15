# PLASU Complaints & Resolution Management System

A full-featured, Django-based complaint management platform for **Plateau State University**, enabling students and staff to file, track, and resolve complaints transparently.

---

## Features

- **Complaint Filing** — Submit complaints with category, priority, location, description, and file attachments
- **Role-Based Access** — Separate dashboards for Students, Staff, and Administrators
- **Real-Time Tracking** — Visual progress timelines and status badges (Pending, Under Review, In Progress, Resolved)
- **Admin Overview** — Statistics, category breakdown, staff assignments, and feedback analytics
- **Resolution Updates** — Staff/admins can post public and internal updates on complaints
- **Feedback & Ratings** — Users rate resolved complaints with 1–5 stars
- **Notifications** — In-app notifications when complaint status changes
- **Search & Filter** — Filter by status, priority, category, or keyword
- **Anonymous Complaints** — Users can file complaints anonymously
- **PSU Branding** — Green, gold, and white colour scheme reflecting university identity
- **Mobile Responsive** — Works across all screen sizes

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11+, Django 4.2 |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Frontend | HTML5, CSS3 (custom), Vanilla JS |
| File Uploads | Django FileField + Pillow |
| Config | python-decouple (.env) |

---

## Getting Started

### 1. Clone and set up environment

```bash
git clone https://github.com/your-org/psu-complaints.git
cd psu-complaints
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment variables

```bash
cp .env.sample .env
# Open .env and update SECRET_KEY and any other settings
```

### 3. Run migrations

```bash
python manage.py migrate
```

### 4. Seed initial data (categories + demo accounts)

```bash
python manage.py seed_data
```

This creates:

| Role | Username | Password |
|---|---|---|
| Administrator | `admin` | `Admin@PSU2024` |
| Staff | `staff_demo` | `Staff@PSU2024` |
| Student | `student_demo` | `Student@PSU2024` |

### 5. Collect static files (production only)

```bash
python manage.py collectstatic
```

### 6. Start the development server

```bash
python manage.py runserver
```

Visit: [http://localhost:8000](http://localhost:8000)



## User Roles

### Student
- Register and log in
- File complaints with attachments
- Track complaint status with timeline
- Leave feedback after resolution
- Receive notifications on updates

### Staff
- View and manage assigned complaints
- Post resolution updates
- Mark complaints as in progress or resolved

### Administrator
- Full access to all complaints
- Assign complaints to staff members
- View analytics and feedback summaries
- Access Django admin panel

---

## Complaint Lifecycle

```
Filed → Pending → Under Review → In Progress → Resolved → (Feedback)
```

---

## Production Deployment

1. Set `DEBUG=False` in `.env`
2. Configure PostgreSQL database credentials in `.env`
3. Configure SMTP email settings in `.env`
4. Run `python manage.py collectstatic`
5. Use **Gunicorn** as the WSGI server
6. Use **Nginx** as a reverse proxy
7. Set `ALLOWED_HOSTS` to your domain


## License

This project was developed as a case study for Plateau State University. All rights reserved.
