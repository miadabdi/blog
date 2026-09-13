# blog

Personal blog — monorepo: FastAPI backend + React frontend.

| Path | What |
|------|------|
| `backend/` | FastAPI app (SQLAlchemy 2, Alembic, MinIO) — see [backend/README.md](backend/README.md) |
| `frontend/` | React SPA (Vite, TypeScript, pnpm) |

## Full stack (root compose)

```bash
cp backend/compose.env .env && printf '\nPORT=8081\n' >> .env
docker compose up --build
```

- API: http://localhost:8081/health
- UI: http://localhost:3000
- MinIO console: http://localhost:9001

Run from the repo root (the `env_file` path is relative). No bind-mounts or `--reload` here — this file is the deploy artifact.

## Backend-only dev loop

```bash
cd backend && docker compose up
```

Keeps the bind-mount + `uvicorn --reload` workflow from `backend/compose.env` / `backend/.env`.

## Env files (all untracked)

| File | Used by | Hosts |
|------|---------|-------|
| `backend/compose.env` | app container env (both composes) | `db`, `minio` |
| `backend/.env` | backend compose interpolation + host-run app/alembic | `127.0.0.1` |
| root `.env` | root compose interpolation (`PORT`, `POSTGRES_*`, `MINIO_*`) | — |

Fresh clone:

```bash
cp backend/compose.env.example backend/compose.env
cp backend/compose.env backend/.env && cp backend/compose.env .env && printf '\nPORT=8081\n' >> .env
# then set POSTGRES_HOST / MINIO_ENDPOINT to 127.0.0.1 in backend/.env
```

## Migrations

Run from `backend/` only — `alembic.ini` and app settings resolve paths relative to the working directory:

```bash
cd backend && alembic upgrade head
```

## CI

- `.github/workflows/ci.yml` — frontend lint / type-check / build (runs when `frontend/**` changes)
- `.github/workflows/docker.yml` — builds and pushes `miadabdi/blog-react` to Docker Hub after green CI on main

## Notes

- Frontend history lives in the archived [github.com/miadabdi/blog_react](https://github.com/miadabdi/blog_react); backend history is this repo's own.
- Husky hooks in `frontend/.husky` are inactive here. To re-enable: `git config core.hooksPath frontend/.husky` (they will then also gate backend commits).
