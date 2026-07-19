# Trail API 

> **Production-ready asynchronous REST API** for tracking running/cycling routes with Telegram bot notifications, built from scratch with **FastAPI**, **SQLAlchemy 2.0 (async)**, **PostgreSQL**, and **APScheduler**.

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg)](https://www.sqlalchemy.org/)
[![Pytest](https://img.shields.io/badge/Pytest-8.x-orange.svg)](https://pytest.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://docs.docker.com/compose/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()
[![No AI](https://img.shields.io/badge/Code-100%25%20Human%20Written-FF6B6B.svg)]()

---

## 📑 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Requirements](#-requirements)
- [Quick Start (Docker)](#-quick-start-docker)
- [Configuration](#-configuration)
- [Usage & API Docs](#-usage--api-docs)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 About

**Trail API** is a fully functional backend service for a fitness tracking application. It allows users to register, log their routes (runs, rides, hikes), and retrieve personal statistics. The system features **real-time Telegram notifications** for admin monitoring (new user registrations, periodic health reports) and runs on a **modern async Python stack** with PostgreSQL.

> **Why this project exists:** Every architectural decision, every line of SQLAlchemy model, every pytest fixture, every Docker healthcheck reflects my personal understanding of async Python, database design, testing strategies, and production-grade deployment : ].

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **User Management** | Registration with validation (unique email, username, level enum) |
| **Route Tracking** | Create routes with title, distance, time, type (run/bike/hike), linked to user |
| **Personal Stats** | Aggregate distance, time, and route count per user |
| **Telegram Bot** | Async notifications: new user alerts + periodic system health reports |
| **Scheduled Jobs** | APScheduler background task (every 10 min) reporting active user count |
| **Full Test Coverage** | Async pytest suite: happy paths, validation errors (422), 404s, DB cleanup |
| **Docker Ready** | Multi-container setup with PostgreSQL healthchecks & dependency ordering |
| **Fully Async** | End-to-end async: FastAPI + SQLAlchemy asyncpg + httpx + APScheduler |

---

## 🧰 Tech Stack

| Layer | Technology | Why |
|-------|------------|-----|
| **API Framework** | **FastAPI 0.110+** | Native async, auto OpenAPI docs, type-safe DI |
| **Database** | **PostgreSQL 15** | Production-grade, ACID, JSON support |
| **ORM** | **SQLAlchemy 2.0 (async)** | Modern `Mapped`/`mapped_column`, `AsyncSession`, 2.0 API |
| **Driver** | **asyncpg** | Fastest Postgres driver for Python async |
| **Validation** | **Pydantic v2** | Runtime validation, serialization, OpenAPI schema gen |
| **Testing** | **pytest + pytest-asyncio + httpx** | True async test client, fixtures, parametrization |
| **Scheduling** | **APScheduler (AsyncIOScheduler)** | Non-blocking background jobs inside ASGI lifespan |
| **HTTP Client** | **httpx (async)** | Telegram API calls with proxy/timeout config |
| **Config** | **python-dotenv** | 12-factor app, `.env` separation |
| **Containerization** | **Docker + Docker Compose** | Reproducible dev/prod environments |
| **Server** | **Uvicorn** | ASGI server with reload for dev |

---

## 🏗 Architecture Highlights

### 1. **Pure Async End-to-End**
- **No blocking I/O anywhere**: FastAPI handlers → SQLAlchemy `AsyncSession` → `asyncpg` → `httpx` for Telegram
- **Lifespan management**: DB initialization + scheduler startup/shutdown via FastAPI `lifespan` context manager
- **Dependency Injection**: `get_async_session()` yields `AsyncSession` per request (scoped, auto-commit/rollback)

### 2. **SQLAlchemy 2.0 Declarative Models**
```python
# Modern typed mapping — no legacy __table_args__ or Column()
class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(40))
    email: Mapped[str] = mapped_column(String(40), unique=True)
    level: Mapped[str] = mapped_column(String(20))
    routes: Mapped[list["Route"]] = relationship(back_populates="user")

class Route(Base):
    __tablename__ = "route"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    title: Mapped[str] = mapped_column(String(200))
    distance_km: Mapped[float]
    time_minutes: Mapped[float]
    route_type: Mapped[str] = mapped_column(Text())
    user: Mapped["User"] = relationship(back_populates="routes")
```

### 3. **Robust Testing Strategy**
- **Session-scoped fixtures**: DB created once, client reused — fast test runs
- **Mocked external deps**: `send_tg_notifications` patched with `AsyncMock` — zero network calls in CI
- **Parametrized negative cases**: 5 invalid payload combos test Pydantic 422 validation
- **DB cleanup per test**: Each test deletes its own fixtures — no test pollution

### 4. **Production-Grade Docker Compose**
```yaml
# Healthcheck ensures DB is *ready*, not just "started"
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U myuser -d traildb"]
  interval: 5s
  timeout: 5s
  retries: 5

# Web waits for DB healthy before starting
depends_on:
  db:
    condition: service_healthy
```

### 5. **Observability via Telegram**
- **Event-driven**: New user → instant TG message
- **Heartbeat**: Scheduler reports user count every 10 min (configurable)
- **Graceful degradation**: Missing TG credentials → logged warning, no crash

---

## 📋 Requirements

- **Docker & Docker Compose** (recommended) — *or*
- **Python 3.12+**, **PostgreSQL 15+** (local)
- **Telegram Bot Token & Chat ID** (for notifications — optional, gracefully skipped)

---

## 🚀 Quick Start (Docker)

```bash
# 1. Clone
git clone https://github.com/LukaHash/Trail-API_FastAPI.git
cd Trail_API

# 2. Configure environment
cp .env.example .env
# Edit .env with your values (see Configuration below)

# 3. Launch
docker compose up --build -d

# 4. Verify
curl http://localhost:8000/docs    # Swagger UI
curl http://localhost:8000/health  # Optional health endpoint (add if needed)
```

**Services:**
- **API**: `http://localhost:8000`
- **Swagger Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **PostgreSQL**: `localhost:5432` (user: `myuser`, db: `traildb`)

---

## 🛠 Local Development (without Docker)

```bash
# 1. Create venv
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install deps
pip install -r requirements.txt

# 3. Start PostgreSQL (locally or via `docker run -d -p 5432:5432 ...`)

# 4. Configure .env (DB_HOST=localhost)

# 5. Run with hot reload
python fast_api.py
# or: uvicorn app.app:app --reload --host 0.0.0.0 --port 8000
```

---

## ⚙️ Configuration

Create `.env` from `.env.example`:

```env
# Telegram Notifications (optional but recommended)
TG_TOKEN=123456789:AAHxxxxxxxxxxxxxxxxxxxxxxx
TG_CHAT_ID=987654321
TG_PROXY=http://213.163.115.194:8080  # Optional proxy for restricted networks

# Database (matches docker-compose.yml defaults)
DB_USER=myuser
DB_PASS=mypassword
DB_HOST=db          # Use 'localhost' for local dev without Docker
DB_PORT=5432
DB_NAME=traildb
```

> **Security**: Never commit `.env`. It's in `.gitignore`. Use GitHub Secrets / Docker secrets in production.

---

## ▶️ Usage & API Docs

Interactive docs auto-generated from type hints:

| Interface | URL |
|-----------|-----|
| **Swagger UI** | `http://localhost:8000/docs` |
| **ReDoc** | `http://localhost:8000/redoc` |
| **OpenAPI JSON** | `http://localhost:8000/openapi.json` |

### Example Requests

**Create User**
```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "email": "alice@example.com", "level": "beginner"}'
```

**Create Route**
```bash
curl -X POST http://localhost:8000/routes \
  -H "Content-Type: application/json" \
  -d '{"title": "Morning Run", "distance_km": 5.2, "time_minutes": 30, "route_type": "run", "user_id": 1}'
```

**Get User Stats**
```bash
curl http://localhost:8000/users/1/stats
# Response:
# {
#   "total_distance": 15.6,
#   "total_time": 90.0,
#   "routes completed": 3
# }
```

---

## 🧪 Testing

```bash
# With Docker (recommended — matches CI)
docker compose run --rm web pytest -v

# Or locally (ensure test DB running)
pytest -v --asyncio-mode=auto
```

**Test Suite Coverage:**
```
app/tests/test_trail_api.py
├── test_user              # Happy path: create user + DB cleanup
├── test_bad_data[5 cases] # Parametrized 422 validation errors
└── test_unreal_userid     # 404 for missing user stats

app/tests/conftest.py
├── mock_tg                # Session-scoped AsyncMock for Telegram
├── prepare_db             # Session-scoped create_all()
├── client                 # Session-scoped AsyncClient (ASGITransport)
└── user_payload           # Unique email per run (randint)
```

**Key Testing Principles Applied:**
- **Isolation**: Each test cleans its own data
- **Speed**: Session-scoped fixtures avoid repeated setup
- **Realism**: `ASGITransport` tests actual FastAPI app, not `TestClient` sync mock
- **Safety**: External HTTP (Telegram) fully mocked

---

## 📁 Project Structure

```
Trail_API/
├── app/
│   ├── __init__.py
│   ├── app.py              # FastAPI app, lifespan, route handlers
│   ├── db.py               # Engine, sessionmaker, Base, DATABASE_URL
│   ├── models.py           # SQLAlchemy 2.0 models (User, Route)
│   ├── schemas.py          # Pydantic v2 models (RouteCreate, UserCreate)
│   ├── tg.py               # Async Telegram sender (httpx + proxy)
│   └── tests/
│       ├── conftest.py     # Pytest fixtures (mock, client, DB, payload)
│       ├── pytest.ini      # Asyncio config, pythonpath
│       └── test_trail_api.py # Test cases
├── fast_api.py             # Uvicorn entrypoint (dev: reload=True)
├── docker-compose.yml      # Web + DB with healthchecks
├── Dockerfile              # Python 3.12-slim, deps, uvicorn CMD
├── requirements.txt        # Pinned dependencies
├── .env.example            # Template for environment variables
├── .gitignore              # Standard Python + .env + IDE ignores
└── README.md               # You are here
```

---

## 🔍 API Endpoints

| Method | Path | Description | Response |
|--------|------|-------------|----------|
| `POST` | `/users` | Register new user | `200 User` / `422` / `500` |
| `POST` | `/routes` | Create route for user | `200 Route` / `422` / `500` |
| `GET` | `/users/{user_id}/stats` | Aggregate user stats | `200 Stats` / `404` / `500` |

**Schemas:**

```python
# UserCreate
{
  "username": "str (max 40)",
  "email": "str (unique, max 40)",
  "level": "str (max 20)"  # e.g. beginner/intermediate/pro
}

# RouteCreate
{
  "title": "str (max 200)",
  "distance_km": "float (>0)",
  "time_minutes": "float (>0)",
  "route_type": "str",      # run/bike/hike/walk...
  "user_id": "int (FK)"
}

# Stats Response
{
  "total_distance": "float",
  "total_time": "float",
  "routes completed": "int"
}
```

---

## 🤖 Telegram Integration

**File**: `app/tg.py`

```python
async def send_tg_notifications(text: str) -> httpx.Response | None:
    # 1. Validates TG_TOKEN & TG_CHAT_ID exist
    # 2. Builds request with optional proxy
    # 3. Sends via httpx.AsyncClient (30s timeout, 10s connect)
    # 4. Logs success/failure — never raises
```

**Triggers:**
1. **User registration** (`app.py:user_create`) — instant
2. **Scheduler heartbeat** (`app.py:report_tg`) — every 10 min

**Design Notes:**
- **Fire-and-forget**: Non-blocking, errors logged not raised
- **Proxy support**: For corporate/restricted networks
- **Graceful degradation**: Missing config → `print()` warning, continues

---

## ⏰ Background Jobs

**File**: `app/app.py` → `lifespan()` + `report_tg()`

```python
scheduler = AsyncIOScheduler()
scheduler.add_job(
    func=report_tg,
    trigger="interval",
    minutes=10,
    replace_existing=True,
    max_instances=1  # Prevent overlap
)
scheduler.start()
yield
scheduler.shutdown()  # Cleanup on app stop
```

**Job Logic** (`report_tg`):
- Opens new `AsyncSession`
- Counts all `User` rows
- Sends TG: `"Бот работает, кол-во бегунов в бд: {count}"`

> **Why APScheduler?** Battle-tested, supports async, integrates cleanly with FastAPI lifespan, handles timezone/overlap/misfire gracefully.

---

## 📝 Design Decisions & Trade-offs

| Decision | Rationale |
|----------|-----------|
| **No auth/JWT** | Scope: demonstrate core async backend skills. Auth adds boilerplate without showing DB/async mastery. |
| **Pydantic v2 + SQLAlchemy 2.0** | Modern, type-safe, future-proof. Avoids legacy `BaseModel.Config` / `Column()` patterns. |
| **AsyncSession per request (DI)** | Correct scope: auto-commit/rollback, no leaked connections, testable via override. |
| **No Alembic** | `create_all()` in lifespan + tests is sufficient for demo. Mentioned in FAQ for production. |
| **Text() for route_type** | Flexible enum-like values without migration on new types. |
| **Unique email constraint** | DB-level integrity, not just app-level. |
| **Parametrized negative tests** | Covers 5 invalid type combos in 1 test function — DRY + comprehensive. |
| **Docker healthcheck on pg_isready** | Prevents "DB up but not accepting connections" race condition. |
| **No ORM lazy loading** | Explicit `select(Route).where(...)` — predictable queries, no N+1. |

---

## 🐛 Troubleshooting

| Issue | Fix |
|-------|-----|
| **`asyncpg` connection refused** | Ensure PostgreSQL is healthy: `docker compose logs db` → wait for "database system is ready to accept connections" |
| **Telegram notifications not sending** | Check `.env`: `TG_TOKEN`, `TG_CHAT_ID` set? Proxy reachable? Logs: `docker compose logs web` |
| **Tests fail with "table already exists"** | Run `docker compose down -v` to wipe volumes, then `up --build` |
| **Port 8000/5432 in use** | Change `ports:` in `docker-compose.yml` or stop local Postgres/Uvicorn |
| **Pydantic validation errors (422)** | Check payload types: `distance_km`/`time_minutes` must be numbers, not strings |
| **Scheduler not firing** | Verify `lifespan` runs (check logs for "Scheduler started") — only works in ASGI server (uvicorn), not bare `python app.py` |

---

## License

Distributed under the **MIT License**. See `LICENSE` for more information.

---


Built with ☕ and Love 💜
**Open to backend/Full-stack opportunities** — let's talk! 🚀

---

*Star ⭐ this repo if you love your family!*
