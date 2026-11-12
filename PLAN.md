# Mission Control: Tech Stack

The intended tools for the Go/No-Go launch console. Change this file if a choice changes.

| Layer     | Choice                         | Why                                                                 |
|-----------|--------------------------------|---------------------------------------------------------------------|
| Back end  | Django                         | Mature, batteries included, built-in ORM, migrations and admin       |
| Database  | SQLite through the Django ORM  | Django's default, no server to run, reports survive a restart        |
| Front end | Next.js + TypeScript           | Typed components for the report form and the Flight Director console |
| Model     | Claude through the Anthropic Python SDK (`anthropic`) | Structured outputs for sorting, one SDK for every model call |
| API + validation | Django Ninja + Pydantic | One set of schemas validates form input (clear 422 messages), API responses and the model's structured replies |
| Containers | Docker + Docker Compose | Django and Next.js as two services, SQLite on a named volume so reports survive a restart, `docker compose up` to start |

## Ground rules that follow from the stack

- Every model call goes through one `LLMClient` interface. Tests use a fake, so they need no network and no API key.
- Launch limits, the verdict and the cost are plain Python, never a model.
- A model reply is parsed into a Pydantic schema; an invalid value falls back to a safe default in code.
- uv manages Python dependencies (`uv.lock`), in non-package mode; the Docker image installs them with `uv sync --frozen`.
