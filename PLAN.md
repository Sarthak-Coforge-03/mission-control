# Mission Control: Tech Stack

The intended tools for the Go/No-Go launch console. Change this file if a choice changes.

| Layer     | Choice                         | Why                                                                 |
|-----------|--------------------------------|---------------------------------------------------------------------|
| Back end  | Django                         | Mature, batteries included, built-in ORM, migrations and admin       |
| Database  | SQLite through the Django ORM  | Django's default, no server to run, reports survive a restart        |
| Front end | Next.js + TypeScript           | Typed components for the report form and the Flight Director console |
| Model     | Claude through the Anthropic Python SDK (`anthropic`) | Structured outputs for sorting, one SDK for every model call |

## Ground rules that follow from the stack

- Every model call goes through one `LLMClient` interface. Tests use a fake, so they need no network and no API key.
- Launch limits, the verdict and the cost are plain Python, never a model.
