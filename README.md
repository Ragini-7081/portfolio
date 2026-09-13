# Ragini Yadav Portfolio

A responsive FastAPI portfolio with:
- Blue/purple navigation
- Light/dark theme toggle
- Responsive layout and mobile menu
- About, Skills, Projects, Education and Contact sections
- Project demo buttons
- Resume download
- Contact form stored in SQLite with SQLAlchemy
- FastAPI `/health`, `/api/contact`, and `/api/projects` endpoints

## Run locally

```powershell
python -m uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000

## Render

Build command:
```text
pip install -r requirements.txt
```

Start command:
```text
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Keep the Render Root Directory empty when the repository itself contains `app/` and `requirements.txt`.
