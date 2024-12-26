# AZ Household Services (V1)

A Flask-based household services marketplace where:
- Customers can sign up, book services, and close requests with ratings/remarks.
- Service Professionals can sign up, accept/reject requests, and track request status.
- Admin can manage services, verify professionals, flag/unflag users, and view summaries.

## Tech Stack

- Python 3
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- SQLite
- Matplotlib + NumPy (for summary graphs)
- HTML templates + CSS

## Project Structure

```text
AZ-household-services-V1/
├── app.py
├── backend/
│   ├── controllers.py
│   └── models.py
├── static/
│   ├── graphs/
│   └── main.css
└── templates/
```

## Features

### Admin
- Add, edit, delete service categories and service items.
- Verify or reject professional accounts.
- Flag/unflag customers and professionals.
- Search across services, customers, and professionals.
- View summary charts and counts.

### Customer
- Register and log in.
- Browse services and book requests.
- Track request status.
- Close requests with rating and remarks.
- Edit profile.

### Professional
- Register and wait for admin verification.
- View eligible requests and accept/reject them.
- Track assigned requests.
- View summary charts and average ratings.
- Edit profile.

## Setup and Run

### 1. Clone and enter project

```bash
git clone https://github.com/premshuksaha/AZ-household-services-V1.git
cd AZ-household-services-V1
```

### 2. Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create instance folder

The app uses SQLite URI `sqlite:///household_app.sqlite3`. Create an `instance` folder before initializing the database.

```bash
mkdir -p instance
```

### 5. Create database tables (first run)

```bash
python3 -c "from app import app; from backend.models import db; app.app_context().push(); db.create_all(); print('Database initialized')"
```

This creates the SQLite database file (typically under `instance/household_app.sqlite3`).

### 6. Run the app

```bash
python3 app.py
```

Open in browser:
- http://127.0.0.1:5000/

## Optional: Create an Admin User

There is no built-in seed script. Admin login expects a record in `cs_info` with `role=0`.

Create one manually:

```bash
python3 -c "from app import app; from backend.models import db, cs_info; app.app_context().push(); u=cs_info(email='admin@example.com', password='admin123', fullname='Admin', address='HQ', pincode=000000, phone='0000000000', role=0); db.session.add(u); db.session.commit(); print('Admin created')"
```

Then log in at `/login` using those credentials.

## Important Notes

- This project stores passwords as plain text and is intended for learning/demo use only.
- Use a fresh virtual environment if dependency conflicts occur.
- If graph images do not update, make sure `static/graphs/` exists and is writable.

## Common Troubleshooting

### `ModuleNotFoundError`
- Activate your virtual environment and reinstall dependencies.

### Database-related errors
- Ensure `instance/` exists.
- Re-run the database initialization command.

### Port already in use
- Stop the process using port 5000 or run on a different port by updating `app.run()`.

