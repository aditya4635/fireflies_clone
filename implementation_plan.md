# Fireflies.ai Clone — Full-Stack Implementation Plan

> **Principal Engineer's perspective:** This document covers architecture, tech Scaler_SDE_Fullstack_Assignment_-_Fireflies_Clonestack decisions, DB schema, API contract, component hierarchy, seeding strategy, and the complete execution roadmap. Every decision here is justified by software engineering first principles.

---

## 1. Problem Statement & Scope

Build a **production-grade functional clone** of Fireflies.ai that:
- Mirrors the Fireflies visual identity (dark nav, purple/violet accents, DM Sans + Inter typography)
- Implements all core post-meeting workflows (library, transcript, AI summary, CRUD)
- Is backed by a clean REST API (FastAPI + SQLite)
- Has a clean, extensible, well-typed codebase ready for evaluation interview

**Out of scope (placeholder only):** Live bot, real STT, integrations, real auth.

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────┐
│                 CLIENT (Browser)                 │
│  Next.js 14 (App Router) + TypeScript           │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │ Dashboard│  │ Meeting  │  │ Create/Edit  │  │
│  │ /meetings│  │ /meetings│  │ Modals/Forms │  │
│  │          │  │ /[id]    │  │              │  │
│  └──────────┘  └──────────┘  └──────────────┘  │
└─────────────────────────────────────────────────┘
            │  HTTP / REST (JSON)
            ▼
┌─────────────────────────────────────────────────┐
│         BACKEND  (Python 3.11 + FastAPI)         │
│  ┌──────────────────────────────────────────┐   │
│  │            API Layer (Routers)           │   │
│  │  /meetings  /transcripts  /summaries     │   │
│  │  /action-items  /search  /stats          │   │
│  └──────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────┐   │
│  │         Service / Business Logic         │   │
│  └──────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────┐   │
│  │      Repository Layer (SQLAlchemy)       │   │
│  └──────────────────────────────────────────┘   │
│                    │                             │
│           SQLite (meetings.db)                   │
└─────────────────────────────────────────────────┘
```

**Key Architecture Decisions:**
| Decision | Choice | Rationale |
|---|---|---|
| Frontend framework | Next.js 14 App Router | SSR/SSG, file-based routing, TypeScript native |
| Backend framework | FastAPI | Async, Pydantic validation, OpenAPI auto-docs, Pythonic |
| ORM | SQLAlchemy 2.x (async) | Type-safe, relationship management, migration ready |
| Database | SQLite | Assignment requirement; file-based, zero infra |
| State management | React Query (TanStack) | Server-state caching, mutations, loading/error states |
| Styling | CSS Modules + CSS Variables | Scoped styles, no runtime overhead, full design token control |
| Migrations | Alembic | Production-grade even for SQLite |
| API contract | OpenAPI / Pydantic schemas | Self-documenting, strict validation |

---

## 3. Repository Structure

```
fireflies-clone/
├── frontend/                    # Next.js 14 App
│   ├── src/
│   │   ├── app/                 # App Router pages
│   │   │   ├── layout.tsx       # Root layout (sidebar + nav)
│   │   │   ├── page.tsx         # Redirect → /meetings
│   │   │   ├── meetings/
│   │   │   │   ├── page.tsx     # Dashboard / Library
│   │   │   │   ├── new/page.tsx # Create meeting
│   │   │   │   └── [id]/
│   │   │   │       ├── page.tsx         # Meeting detail
│   │   │   │       └── edit/page.tsx    # Edit meeting
│   │   │   └── settings/page.tsx        # Settings (placeholder)
│   │   ├── components/
│   │   │   ├── layout/          # Sidebar, Topbar, Layout
│   │   │   ├── meetings/        # MeetingCard, MeetingList, Filters
│   │   │   ├── transcript/      # TranscriptViewer, TranscriptLine
│   │   │   ├── summary/         # SummaryPanel, ActionItems, Topics
│   │   │   ├── player/          # MediaPlayer, SeekBar
│   │   │   ├── modals/          # CreateMeetingModal, DeleteConfirm
│   │   │   ├── search/          # SearchBar, GlobalSearch
│   │   │   └── ui/              # Button, Badge, Toast, Input (design system)
│   │   ├── hooks/               # useMediaPlayer, useMeetings, useSearch
│   │   ├── lib/
│   │   │   ├── api/             # API client (fetch wrapper + endpoints)
│   │   │   └── utils/           # formatDuration, formatDate, etc.
│   │   ├── types/               # TypeScript interfaces/types
│   │   └── styles/
│   │       ├── globals.css      # Design tokens, resets
│   │       └── *.module.css     # Component-scoped styles
│   ├── next.config.ts
│   ├── tsconfig.json
│   └── package.json
│
├── backend/                     # FastAPI Application
│   ├── app/
│   │   ├── main.py              # App factory, CORS, routers
│   │   ├── config.py            # Settings (pydantic-settings)
│   │   ├── database.py          # SQLAlchemy engine + session
│   │   ├── models/              # SQLAlchemy ORM models
│   │   │   ├── meeting.py
│   │   │   ├── participant.py
│   │   │   ├── transcript.py
│   │   │   ├── summary.py
│   │   │   └── action_item.py
│   │   ├── schemas/             # Pydantic request/response schemas
│   │   │   ├── meeting.py
│   │   │   ├── transcript.py
│   │   │   ├── summary.py
│   │   │   └── action_item.py
│   │   ├── routers/             # FastAPI APIRouter modules
│   │   │   ├── meetings.py
│   │   │   ├── transcripts.py
│   │   │   ├── summaries.py
│   │   │   ├── action_items.py
│   │   │   └── search.py
│   │   ├── services/            # Business logic layer
│   │   │   ├── meeting_service.py
│   │   │   ├── transcript_service.py
│   │   │   └── summary_service.py
│   │   └── repositories/        # Data access layer
│   │       ├── meeting_repo.py
│   │       └── base_repo.py
│   ├── alembic/                 # DB migrations
│   ├── seed.py                  # Database seeder
│   ├── requirements.txt
│   └── .env
│
└── README.md
```

---

## 4. Database Schema

```sql
-- Core entity: a recorded/imported meeting
CREATE TABLE meetings (
    id          TEXT PRIMARY KEY,          -- UUID v4
    title       TEXT NOT NULL,
    date        DATETIME NOT NULL,
    duration    INTEGER NOT NULL,          -- seconds
    bot_name    TEXT DEFAULT 'Fred',
    status      TEXT DEFAULT 'processed',  -- 'processing' | 'processed' | 'failed'
    source      TEXT DEFAULT 'upload',     -- 'upload' | 'paste' | 'seed'
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Participants (many-to-many via junction)
CREATE TABLE participants (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    email       TEXT,
    avatar_color TEXT DEFAULT '#7C3AED'
);

CREATE TABLE meeting_participants (
    meeting_id      TEXT REFERENCES meetings(id) ON DELETE CASCADE,
    participant_id  TEXT REFERENCES participants(id),
    PRIMARY KEY (meeting_id, participant_id)
);

-- Transcript lines (time-aligned utterances)
CREATE TABLE transcript_lines (
    id              TEXT PRIMARY KEY,
    meeting_id      TEXT NOT NULL REFERENCES meetings(id) ON DELETE CASCADE,
    participant_id  TEXT REFERENCES participants(id),
    speaker_name    TEXT NOT NULL,
    start_time      REAL NOT NULL,        -- seconds from start
    end_time        REAL NOT NULL,
    text            TEXT NOT NULL,
    sequence_number INTEGER NOT NULL,     -- ordering
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- AI-generated summary per meeting
CREATE TABLE summaries (
    id          TEXT PRIMARY KEY,
    meeting_id  TEXT UNIQUE NOT NULL REFERENCES meetings(id) ON DELETE CASCADE,
    overview    TEXT NOT NULL,             -- paragraph summary
    key_topics  TEXT NOT NULL,             -- JSON array of strings
    chapters    TEXT NOT NULL,             -- JSON array of {title, start_time, summary}
    sentiment   TEXT DEFAULT 'neutral',    -- 'positive' | 'neutral' | 'negative'
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Action items extracted from meeting
CREATE TABLE action_items (
    id          TEXT PRIMARY KEY,
    meeting_id  TEXT NOT NULL REFERENCES meetings(id) ON DELETE CASCADE,
    assignee    TEXT,
    text        TEXT NOT NULL,
    due_date    DATETIME,
    completed   BOOLEAN DEFAULT FALSE,
    priority    TEXT DEFAULT 'medium',    -- 'high' | 'medium' | 'low'
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_meetings_date ON meetings(date DESC);
CREATE INDEX idx_transcript_meeting ON transcript_lines(meeting_id, sequence_number);
CREATE INDEX idx_action_items_meeting ON action_items(meeting_id);
```

**Entity Relationship:**
```
meetings ──< meeting_participants >── participants
meetings ──< transcript_lines (speaker_name + participant_id FK)
meetings ──1 summaries
meetings ──< action_items
```

---

## 5. API Contract

### Meetings
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/meetings` | List all meetings (search, filter, sort, pagination) |
| `POST` | `/api/v1/meetings` | Create new meeting |
| `GET` | `/api/v1/meetings/{id}` | Get meeting detail (with participants) |
| `PATCH` | `/api/v1/meetings/{id}` | Update meeting metadata |
| `DELETE` | `/api/v1/meetings/{id}` | Delete meeting (cascades) |

### Transcripts
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/meetings/{id}/transcript` | Get all transcript lines |
| `POST` | `/api/v1/meetings/{id}/transcript/upload` | Upload .txt/.vtt/.json transcript |
| `GET` | `/api/v1/meetings/{id}/transcript/search?q=` | Search within transcript |

### Summaries
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/meetings/{id}/summary` | Get AI summary |
| `PATCH` | `/api/v1/meetings/{id}/summary` | Edit summary |

### Action Items
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/meetings/{id}/action-items` | List action items |
| `POST` | `/api/v1/meetings/{id}/action-items` | Create action item |
| `PATCH` | `/api/v1/action-items/{id}` | Update / complete action item |
| `DELETE` | `/api/v1/action-items/{id}` | Delete action item |

### Search
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/search?q=&type=meetings\|transcripts\|all` | Global search |

---

## 6. Frontend Component Architecture

```
AppLayout
├── Sidebar (nav links: Notebook, Channels, AskFred, Integrations, Settings)
├── Topbar (search bar, notifications, user avatar)
└── <children> (page content)

/meetings (Dashboard)
├── MeetingListHeader (title, "Add Meeting" CTA, sort/filter controls)
├── FilterBar (date range, participant filter, status filter)
├── MeetingGrid
│   └── MeetingCard × N
│       ├── MeetingMeta (title, date, duration, participants avatars)
│       ├── SummarySnippet (first line of overview)
│       └── ActionMenu (edit, delete)
└── EmptyState (when no meetings)

/meetings/[id] (Meeting Detail)
├── MeetingDetailHeader (title, date, participants, export button)
├── TabBar (Thread | Video | Soundbites)
└── MainContent (two-column)
    ├── LEFT: TranscriptPanel
    │   ├── TranscriptSearchBar
    │   └── TranscriptScroller
    │       └── TranscriptLine × N
    │           ├── SpeakerLabel + Avatar
    │           ├── Timestamp (clickable → seeks player)
    │           └── UtteranceText (highlighted on search match)
    └── RIGHT: SummaryPanel
        ├── OverviewSection
        ├── ChaptersSection (timeline/chapters)
        ├── KeyTopicsSection (badge chips)
        ├── ActionItemsSection
        │   └── ActionItemRow × N (checkbox, text, assignee, due date)
        └── MediaPlayerCard
            ├── WaveformVisualizer (animated placeholder)
            └── PlayerControls (play/pause, seek, speed)
```

---

## 7. Design System (Fireflies Brand)

```css
/* Design Tokens */
--color-bg-primary:     #0F0F13;   /* Very dark base */
--color-bg-secondary:   #1A1A24;   /* Card/panel background */
--color-bg-elevated:    #22222F;   /* Elevated surfaces */
--color-sidebar:        #13131A;   /* Sidebar dark */
--color-accent-purple:  #7C3AED;   /* Primary violet (Fireflies brand) */
--color-accent-violet:  #6D28D9;   /* Darker violet for hover */
--color-accent-light:   #A78BFA;   /* Light violet for text accents */
--color-text-primary:   #F1F0F5;   /* Primary text */
--color-text-secondary: #9CA3AF;   /* Secondary / muted text */
--color-border:         #2D2D3E;   /* Subtle borders */
--color-success:        #10B981;   /* Completed action items */
--color-warning:        #F59E0B;   /* Pending / medium priority */
--color-danger:         #EF4444;   /* Delete / high priority */

/* Typography */
--font-heading: 'DM Sans', sans-serif;    /* Exact Fireflies font */
--font-body:    'Inter', sans-serif;      /* Exact Fireflies font */
```

---

## 8. Seed Data Strategy

The seeder (`backend/seed.py`) will create:
- **6 meetings** with varying durations (15 min to 90 min)
- **3-5 participants** per meeting with realistic names
- **Full transcripts** (~40-80 utterances per meeting) with real-looking dialogue
- **AI summaries** with overview, 3-5 chapters, 4-8 key topics, sentiment
- **3-6 action items** per meeting (mix of completed and pending)

Example meetings:
1. "Q3 Product Roadmap Planning" — 60 min
2. "Engineering Sprint Retrospective" — 45 min
3. "Design Review: Dashboard Redesign" — 30 min
4. "Investor Update Call" — 90 min
5. "Onboarding: New Team Members" — 25 min
6. "Customer Success Weekly Sync" — 40 min

---

## 9. Execution Roadmap (Phased)

### Phase 1 — Backend Foundation (≈3 hrs)
- [ ] Initialize FastAPI project structure
- [ ] SQLAlchemy models + Alembic migrations
- [ ] Pydantic schemas for all entities
- [ ] Repository layer (CRUD base class + entity repos)
- [ ] Service layer (business logic)
- [ ] All API routers with full CRUD
- [ ] Global search endpoint (SQLite FTS or LIKE)
- [ ] CORS + middleware configuration
- [ ] Database seeder with rich mock data

### Phase 2 — Frontend Foundation (≈2 hrs)
- [ ] Initialize Next.js 14 with TypeScript
- [ ] Design token system (CSS variables in globals.css)
- [ ] Import Google Fonts (DM Sans + Inter)
- [ ] AppLayout: Sidebar + Topbar
- [ ] API client layer (typed fetch wrapper)
- [ ] React Query setup + QueryProvider
- [ ] TypeScript type definitions mirroring backend schemas

### Phase 3 — Core Pages (≈4 hrs)
- [ ] Meetings Dashboard (`/meetings`)
  - MeetingCard with hover effects
  - Search + filter bar
  - Sort by recency / duration
  - Empty state
- [ ] Create Meeting modal / page
  - Form: title, date, participants, paste transcript
  - File upload for .txt/.vtt
- [ ] Meeting Detail page (`/meetings/[id]`)
  - Header with metadata
  - Tabs: Thread | Video | Soundbites

### Phase 4 — Transcript + Player (≈3 hrs)
- [ ] TranscriptViewer with virtual scroll (for large transcripts)
- [ ] Speaker labels with color-coded avatars
- [ ] Timestamp click → seek player
- [ ] Transcript search with highlighting
- [ ] MediaPlayer (HTML5 audio + seek bar)
- [ ] Player → Transcript sync (highlight active utterance)

### Phase 5 — Summary & Action Items (≈2 hrs)
- [ ] Summary panel with overview, chapters, topics
- [ ] Action items with checkbox toggle, add, edit, delete
- [ ] In-line editing for action item text

### Phase 6 — Polish & Bonus Features (≈2 hrs)
- [ ] Toast notifications (create, update, delete)
- [ ] Export transcript (TXT / Markdown)
- [ ] Global search page
- [ ] Dark mode (already default—add toggle)
- [ ] Responsive layout
- [ ] Settings placeholder page
- [ ] Loading skeletons for all async states
- [ ] Error boundary + 404 pages

### Phase 7 — README + Deployment (≈1 hr)
- [ ] README with setup instructions, architecture, schema, API overview
- [ ] Docker Compose (optional nice-to-have)
- [ ] Deploy frontend to Vercel
- [ ] Deploy backend to Render / Railway

---

## 10. Code Quality Standards

| Standard | Implementation |
|---|---|
| **Single Responsibility** | Each module/component does one thing |
| **DRY** | Shared hooks, utilities, base repository class |
| **Type Safety** | 100% TypeScript on frontend; Pydantic on backend |
| **Error Handling** | Global error boundaries (FE), FastAPI exception handlers (BE) |
| **Separation of Concerns** | Router → Service → Repository (BE); Page → Component → Hook → API (FE) |
| **Naming Conventions** | PascalCase components, camelCase hooks/utils, snake_case Python |
| **Constants** | No magic strings; enums and constants files |
| **Environment Config** | `.env` files, `pydantic-settings`, `next.config.ts` |

---

## 11. Open Questions

> [!IMPORTANT]
> **Q1: Backend port preference?**
> I plan to run the FastAPI backend on `http://localhost:8000` and Next.js on `http://localhost:3000`. Is that acceptable, or do you need a specific port?

> [!IMPORTANT]
> **Q2: Include Docker Compose?**
> Should I add a `docker-compose.yml` to make local setup a single command? Recommended for the demo.

> [!NOTE]
> **Q3: Bonus features priority?**
> If time is limited, I'll prioritize: Export (TXT/Markdown) → Global Search → LLM "Ask a question" chat. Do you want me to implement all bonus features?

---

## 12. Verification Plan

### Automated
- Backend: `pytest` — test all CRUD endpoints, seeder, search
- Frontend: TypeScript compile check (`tsc --noEmit`)

### Manual
- Walk through all 5 core feature areas in browser
- Test transcript → player sync (click line → time jumps)
- Test search highlighting in transcript
- Test action item CRUD (add, complete, delete)
- Test meeting CRUD (create with form, edit, delete)
- Verify responsive layout at 1280px, 1440px, mobile
