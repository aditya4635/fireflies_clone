# Fireflies.ai Clone — Full-Stack Assignment

A production-quality clone of [Fireflies.ai](https://fireflies.ai) — an AI-powered meeting assistant. Built as a Scaler SDE Full-Stack assignment.

![Tech Stack](https://img.shields.io/badge/Frontend-Next.js%2014-black?logo=next.js)
![Tech Stack](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)
![Tech Stack](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite)
![Tech Stack](https://img.shields.io/badge/Language-TypeScript-3178C6?logo=typescript)

---

## 🖥️ Live Demo

> Backend: `http://localhost:8000`  
> Frontend: `http://localhost:3000`  
> API Docs: `http://localhost:8000/docs`

---

## ✨ Features

| Feature | Status |
|---|---|
| Meeting Library / Dashboard | ✅ |
| Meeting CRUD (Create / Edit / Delete) | ✅ |
| Paste transcript text on creation | ✅ |
| Meeting Detail view with tabs | ✅ |
| Interactive Transcript viewer | ✅ |
| Click transcript → seek media player | ✅ |
| In-transcript search with highlighting | ✅ |
| AI-generated Summary (overview, topics) | ✅ |
| Collapsible Chapter navigation | ✅ |
| Action Items (add, complete, delete) | ✅ |
| Waveform Media Player (seek / speed) | ✅ |
| Export transcript as Markdown | ✅ |
| Global Search (meetings + transcripts) | ✅ |
| Participant avatars + management | ✅ |
| Fireflies brand design (dark theme) | ✅ |
| Loading skeletons + toast notifications | ✅ |
| Settings page scaffold | ✅ |
| FastAPI REST API with OpenAPI docs | ✅ |
| SQLite with async SQLAlchemy 2.0 | ✅ |
| Layered architecture (Router→Service→Repo) | ✅ |
| 6 seeded meetings with full data | ✅ |

---

## 🏗️ Architecture

```
assignment_scaler/
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── main.py             # App factory + lifespan
│   │   ├── config.py           # Pydantic Settings
│   │   ├── database.py         # SQLAlchemy async engine
│   │   ├── models/             # ORM models (Meeting, Participant, etc.)
│   │   ├── schemas/            # Pydantic request/response types
│   │   ├── repositories/       # Generic base + meeting repo
│   │   ├── services/           # Business logic layer
│   │   └── routers/            # FastAPI route handlers
│   ├── seed.py                 # Database seeder (6 meetings)
│   ├── requirements.txt
│   └── .env
│
└── frontend/                   # Next.js 14 App Router
    └── src/
        ├── app/                # Pages (meetings, search, settings)
        ├── components/
        │   ├── layout/         # Sidebar, Topbar
        │   ├── meetings/       # MeetingCard, CreateMeetingModal
        │   ├── transcript/     # TranscriptViewer
        │   ├── summary/        # SummaryPanel, ActionItemsPanel
        │   └── player/         # MediaPlayer
        ├── lib/
        │   ├── api.ts          # Typed API client
        │   └── utils.ts        # Formatters, helpers
        ├── hooks/
        │   └── useDebounce.ts
        └── types/
            └── index.ts        # All TypeScript types
```

### Design Patterns Used

- **Backend**: Repository pattern → Service layer → Router (strict separation of concerns)
- **Frontend**: React Query for server state, component composition, custom hooks
- **Database**: Normalized schema with FK constraints, cascade deletes, indexes

---

## 🗄️ Database Schema

```text
workspaces
    │
    ├──< meetings ──< meeting_participants >── participants
    │       │
    │       ├──< transcript_lines
    │       ├──  summaries (1:1)
    │       │      │
    │       │      ├──< chapters
    │       │      └──< summary_topics >── topics
    │       │
    │       └──< action_items
    │
    ├──< topics (also linked to workspaces directly)
    ├──< transcript_lines (linked to workspaces)
    ├──< summaries (linked to workspaces)
    ├──< chapters (linked to workspaces)
    └──< action_items (linked to workspaces)
```

---

## 🚀 Running Locally

### Prerequisites
- Python 3.10+
- Node.js 18+

### Backend

```bash
cd backend

# Install dependencies
pip install --only-binary :all: pydantic pydantic-settings pydantic-core
pip install fastapi uvicorn sqlalchemy alembic python-multipart aiofiles python-dotenv aiosqlite

# Seed the database (6 demo meetings with transcripts + summaries)
python seed.py

# Start the API server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Backend available at: http://localhost:8000  
Interactive API docs: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend available at: http://localhost:3000

---

## 📡 API Reference

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/meetings` | List meetings (search, pagination) |
| POST | `/api/v1/meetings` | Create a meeting |
| GET | `/api/v1/meetings/{id}` | Get meeting detail |
| PATCH | `/api/v1/meetings/{id}` | Update meeting |
| DELETE | `/api/v1/meetings/{id}` | Delete meeting |
| GET | `/api/v1/meetings/{id}/transcript` | Get transcript lines |
| POST | `/api/v1/meetings/{id}/transcript/paste` | Import pasted text |
| POST | `/api/v1/meetings/{id}/transcript/upload` | Upload .txt/.vtt file |
| GET | `/api/v1/meetings/{id}/transcript/search` | Search transcript |
| GET | `/api/v1/meetings/{id}/summary` | Get AI summary |
| PATCH | `/api/v1/meetings/{id}/summary` | Update summary |
| GET | `/api/v1/meetings/{id}/action-items` | List action items |
| POST | `/api/v1/meetings/{id}/action-items` | Create action item |
| PATCH | `/api/v1/action-items/{id}` | Update action item |
| DELETE | `/api/v1/action-items/{id}` | Delete action item |
| GET | `/api/v1/search?q=` | Global search |
| GET | `/api/v1/health` | Health check |

---

## 🎨 Design System

Exact Fireflies.ai branding:
- **Colors**: `#0C0C12` base, `#7C3AED` violet accent, `#A78BFA` light accent
- **Fonts**: DM Sans (headings) + Inter (body/transcript)
- **Components**: glassmorphism cards, skeleton loaders, animated waveform player

---

## 📋 Assignment Constraints Met

- ✅ Real audio transcription is out of scope — seeded transcript data provided
- ✅ Transcript upload (`.txt`) supported via `/transcript/upload`
- ✅ Transcript paste supported via `/transcript/paste` and the Create Meeting modal
- ✅ AI summary is pre-generated (seeded) — no live LLM call required
- ✅ No authentication required per assignment spec

---

## 🛠️ Tech Stack

**Backend**
- FastAPI (async)
- SQLAlchemy 2.0 (async, `aiosqlite`)
- Pydantic v2 + pydantic-settings
- Alembic (migrations)
- Python 3.13

**Frontend**
- Next.js 14 (App Router)
- TypeScript
- React Query (@tanstack/react-query)
- Lucide React (icons)
- react-hot-toast
- Vanilla CSS (design tokens / CSS variables)
