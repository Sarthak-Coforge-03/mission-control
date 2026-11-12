# CLAUDE.md
Mission Control: a Go/No-Go launch console. Engineers file anomaly reports, a pipeline sorts and checks them, and the Flight Director approves a drafted briefing.

## Plans: which file is which
- `PLAN.md` (committed): the intended tech stack (Django + SQLite ORM, Django Ninja + Pydantic, Next.js + TypeScript, Anthropic SDK, Docker Compose).
- `plan.local.md` (gitignored): the assignment brief and the grading rubric. Check work against it before calling a step done, and flag any deviation from the rubric.

## Commands
- Install: `uv sync`; config: copy `.env.example` to `.env` (all values optional for local dev)
- Test: `uv run pytest`; single test: `uv run pytest tests/test_x.py::test_name`
- Lint and format: `uv run ruff check --fix . && uv run ruff format .`
- Django: `uv run python backend/manage.py runserver` (also `makemigrations`, `migrate`)
- Start app: `docker compose up` (not set up yet; add it here and in the README once it exists)
- uv is in non-package mode: code isn't installed; imports work via `sys.path` (`manage.py` folder, pytest `pythonpath`)

## Layout
- `backend/config/`: Django settings and root URLs. `backend/reports/`: the app. `tests/`: pytest-django tests.
- SQLite file: `backend/data/db.sqlite3` (gitignored), overridable with `MC_DB_PATH`.

## Rules
- Launch limits, the verdict, brief-by time and cost come from plain code, never from a model.
- All model calls go through one `LLMClient` interface; tests use its fake and need no network or API key.
- Only a person can approve a briefing; the pipeline never sets it approved.

## Hooks (.claude/settings.json)
- Ruff runs on every edited `.py` file; the test suite runs on Stop and must pass.
- `.env` files are blocked (`.env.example` is allowed).

## Git
- `main` is the main branch; feature work happens on `feature/*` branches.
