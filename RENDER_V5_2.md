# V5.2 FREE — Render

Root Directory: `backend`
Build: `pip install -r requirements.txt`
Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
Plan: Free
Health Check: `/api/health`

V5.2 defers XLSM loading until a data route needs it and pins Python/dependency versions to reduce startup crashes.
