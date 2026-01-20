Bulk Email Campaign Management System
=====================================

Overview
--------
This is a Django-based bulk email campaign management system that allows administrators to:
- Upload recipients via CSV
- Create and manage email campaigns
- Send campaign reports to the admin
- Download campaign reports as CSV for detailed delivery logs
- Track email delivery status (success/failure)
---

Prerequisites
-------------
- Python 3.10+
- pip
- Redis (for Celery background tasks)
---

Setup Instructions
------------------

1. Clone the repository  
`git clone <repo_url>`  
`cd <project_folder>`

2. Create and activate a virtual environment  
`python -m venv venv`  
`source venv/bin/activate`  # Linux / Mac  
`venv\Scripts\activate`     # Windows

3. Install dependencies  
`pip install -r requirements.txt`

4. Apply database migrations  
`python manage.py makemigrations`  
`python manage.py migrate`

5. Create a superuser  
`python manage.py createsuperuser`

6. Run the development server  
`python manage.py runserver`  
- Open your browser at `http://127.0.0.1:8000/` and log in with your superuser credentials.

---

Running Background Tasks (Celery)
-------------------------------------------

1. Start Redis (if using Redis as broker)  
`sudo service redis-server start`  # Linux  
# For Windows using WSL, run: `sudo service redis-server start`

2. Run Celery worker  
`celery -A email_campaign worker -l info`

3. Run Celery Beat scheduler  
`celery -A email_campaign beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler`

> Run each command in separate terminals.

---

Configuration Notes
-------------------
- Update `settings.py` with:
  - `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` 
  - `ADMIN_EMAIL` for receiving campaign reports
- Logging is configured to track:
  - File uploads
  - Campaign report generation
  - Email sending success/failure
---

Usage
-----
1. Prepare a CSV file for recipients with columns: `name,email,is_subscribed`  
2. Upload recipients via the “Upload Recipient” page  
3. Create a campaign and schedule it  
4. Emails are sent to all recipients  
5. Admin receives a campaign report email  
---

