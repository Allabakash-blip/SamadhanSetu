# Backend

FastAPI backend for the SIH Social Innovation Collaboration Portal.

## Run

```powershell
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger: http://localhost:8000/docs

## Environment

Create `.env` from `.env.example` and add your local Aiven MySQL, Cloudinary, Google and JWT credentials.

## Milestones included

- Milestone 1: authentication, profiles, locations and role-based dashboards
- Milestone 2: admin verification and management
- Milestone 3: citizen problem reporting, media uploads and problem tracking
