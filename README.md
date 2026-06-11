# World Cup Pool 2026

A betting pool (bolão) web application for the 2026 FIFA World Cup. Built for a small group of friends, with a hypermedia-driven web UI and a REST API for future mobile clients.

## Stack

| Layer | Technology |
|-------|------------|
| Backend | [FastAPI](https://fastapi.tiangolo.com/) |
| Web UI | [HTMX](https://htmx.org/) + [Jinja2](https://jinja.palletsprojects.com/) + [Tailwind CSS](https://tailwindcss.com/) |
| API | REST (`/api/v1/...`) with Pydantic schemas |
| Database | PostgreSQL + SQLAlchemy + Alembic |
| Cache / sessions | Redis |
| Deployment | Docker Compose on a single AWS EC2 instance |

## Features (planned)

- Match score predictions with bets locking before kickoff
- Leaderboard and scoring rules
- Group-stage and knockout views
- Localization for **English** and **Portuguese (Brazil)**
- Timezone-aware match times (stored in UTC, displayed per user region)

## Project layout

```
world-cup-pool-2026/
├── app/                 # FastAPI application (routes, models, services)
├── alembic/             # Database migrations
├── templates/           # Jinja2 HTML templates (HTMX partials)
├── static/              # CSS, images, compiled assets
├── docker-compose.yml   # Local & production stack
├── Dockerfile
└── tests/
```

> Application code will be added in upcoming steps. This repository currently contains project scaffolding only.

## Getting started

### Prerequisites

- Docker & Docker Compose
- Python 3.12+ (for local development without Docker)

### Quick start (Docker — coming soon)

```bash
cp .env.example .env
# Edit .env with your values

docker compose up --build
```

The web app will be available at `http://localhost:8000`.

### Local development (without Docker — coming soon)

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

## Architecture notes

- **Hypermedia routes** return HTML fragments for HTMX (`text/html`).
- **REST routes** live under `/api/v1/` and return JSON for future mobile apps.
- Match kickoff times are stored in **UTC**; display uses the user's locale and timezone.
- Bets lock **N minutes** before kickoff (configurable via `BET_LOCK_MINUTES_BEFORE_KICKOFF`).

## Future work (out of scope for now)

The initial release targets a single EC2 instance with Docker Compose. The following are documented for later scaling and hardening—not part of the current build.

### Infrastructure & AWS services

- **Auto Scaling Groups (ASG) and load balancers** — horizontal scaling behind an Application Load Balancer instead of a single instance.
- **Amazon RDS** for PostgreSQL and **ElastiCache** for Redis — managed database and cache instead of containers on the app host.
- **Amazon S3** for file storage and **CloudFront** for static asset delivery.
- **AWS WAF** in front of the load balancer for common web exploits and rate limiting.
- **Amazon SES** and **SQS** for transactional email (notifications, digests) with queued, retryable delivery.

### Authentication & account management

- **Email-based registration** — for now, users sign up with a username and password only; no email verification flow.
- **Password reset** — forgot-password links, token expiry, and email delivery (depends on SES above).

### Testing

- **Load, stress, and soak tests** — performance benchmarking under concurrent users (e.g. locust, k6) before scaling to ASG or managed services. Unit and integration tests for domain logic (scoring, bet locking, auth) are in scope from the start.

## License

Private project — not licensed for public distribution.
