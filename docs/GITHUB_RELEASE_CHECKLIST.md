# GitHub Release Checklist

Use this checklist before pushing the MVP repository to GitHub.

## Must not commit

- `.env`
- `.venv/`
- `__pycache__/`
- `.pytest_cache/`
- `.DS_Store`
- `_vendor/`

These are excluded by `.gitignore`.

## Local verification

```bash
python -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m pytest
```

## Runtime verification

```bash
~/Applications/Postgres.app/Contents/Versions/16/bin/pg_isready -h 127.0.0.1 -p 5432
.venv/bin/alembic upgrade head
.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

In another terminal:

```bash
.venv/bin/python -m demos.procurement_demo
```

## First push

```bash
git init
git add .
git commit -m "Initial TrustMesh MVP"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```
