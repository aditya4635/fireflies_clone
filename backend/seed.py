"""
Database seeder — populates the database with 6 realistic meetings,
full transcripts, AI summaries, and action items for immediate demo use.

Run: python seed.py  (from the backend/ directory)
"""
import asyncio
import json
import uuid
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DATABASE_URL = "sqlite+aiosqlite:///./meetings.db"

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

# ---------------------------------------------------------------------------
# Seed data definitions
# ---------------------------------------------------------------------------

AVATAR_COLORS = [
    "#7C3AED", "#059669", "#DC2626", "#D97706", "#2563EB", "#DB2777",
    "#0891B2", "#65A30D", "#9333EA", "#EA580C",
]

MEETINGS = [
    {
        "id": "m1",
        "title": "Q3 Product Roadmap Planning",
        "date": datetime.now() - timedelta(days=2, hours=3),
        "duration": 3600,
        "bot_name": "Fred",
        "status": "processed",
        "source": "seed",
        "participants": [
            {"id": "p1", "name": "Sarah Chen", "email": "sarah@company.com", "avatar_color": "#7C3AED"},
            {"id": "p2", "name": "Marcus Williams", "email": "marcus@company.com", "avatar_color": "#059669"},
            {"id": "p3", "name": "Priya Sharma", "email": "priya@company.com", "avatar_color": "#DC2626"},
            {"id": "p4", "name": "James O'Brien", "email": "james@company.com", "avatar_color": "#D97706"},
        ],
        "transcript": [
            ("Sarah Chen", 0.0, 18.0, "Alright everyone, let's get started. Today we're planning the Q3 roadmap. We have a lot to cover so let's be efficient."),
            ("Marcus Williams", 18.5, 35.0, "Thanks Sarah. I've prepared a slide deck with the three major initiatives we're proposing. Should I walk everyone through it?"),
            ("Sarah Chen", 35.5, 42.0, "Yes please, go ahead Marcus."),
            ("Marcus Williams", 42.5, 90.0, "So our three pillars for Q3 are: one, the new onboarding flow redesign, two, the AI-powered meeting summaries feature, and three, mobile app performance improvements."),
            ("Priya Sharma", 91.0, 130.0, "I want to flag that the onboarding redesign is a significant lift. My team estimated it at six weeks minimum. We'd need to pull engineers from other projects."),
            ("James O'Brien", 131.0, 170.0, "From a product perspective, onboarding drop-off is our biggest issue right now. We're losing 40% of signups in the first 24 hours. It has to be a priority."),
            ("Sarah Chen", 171.0, 210.0, "James, can you share those metrics? I want to make sure we have the data to back this prioritization when we present to leadership."),
            ("James O'Brien", 211.0, 250.0, "Absolutely, I'll send over the cohort analysis. The data is pretty stark — users who don't complete onboarding in 24 hours almost never convert."),
            ("Marcus Williams", 251.0, 300.0, "For the AI summaries feature, we have a working prototype. It's generating pretty good results with GPT-4. The main challenge is latency — it currently takes about 45 seconds per meeting."),
            ("Priya Sharma", 301.0, 360.0, "45 seconds is way too slow for production. Users won't wait that long. Can we pre-generate in the background? Like, kick it off as soon as the meeting ends?"),
            ("Marcus Williams", 361.0, 400.0, "Yes, that's the plan. We run it asynchronously right after meeting ingestion. The user gets a notification when the summary is ready."),
            ("Sarah Chen", 401.0, 450.0, "I like that approach. What about the mobile performance work? Priya, your team owns that right?"),
            ("Priya Sharma", 451.0, 510.0, "Yes. We've identified three main bottlenecks: transcript rendering on long meetings, the search indexing, and cold start time. We think we can cut load time by 60% with targeted optimizations."),
            ("James O'Brien", 511.0, 560.0, "That would be huge. We have a lot of mobile users and the complaints about slow load times are the top category in our support tickets."),
            ("Sarah Chen", 561.0, 620.0, "Ok, let's talk resourcing. We need to decide how we're splitting the engineering capacity across these three initiatives."),
            ("Marcus Williams", 621.0, 670.0, "I'd suggest 40% on onboarding, 35% on AI summaries, and 25% on mobile perf. Onboarding needs the most design and frontend work."),
            ("Priya Sharma", 671.0, 720.0, "That split works for me as long as we get two senior engineers on the mobile work. It's complex and we can't afford regressions."),
            ("James O'Brien", 721.0, 760.0, "Agreed. The onboarding redesign also needs to go through UX research first. I'd like at least two weeks of user interviews before we start building."),
            ("Sarah Chen", 761.0, 820.0, "Good point. Let's schedule that research sprint to kick off next week. Marcus, can you coordinate with the design team?"),
            ("Marcus Williams", 821.0, 855.0, "On it. I'll set up a kickoff meeting for Monday morning."),
            ("Sarah Chen", 856.0, 920.0, "Great. Let's do a final recap of action items and then we can close out. Marcus is coordinating UX research kickoff, Priya is putting together the mobile engineering plan, and James is sending over the cohort analysis data."),
            ("James O'Brien", 921.0, 950.0, "I'll send that today before EOD."),
            ("Priya Sharma", 951.0, 990.0, "Engineering plan will be ready by Thursday."),
            ("Marcus Williams", 991.0, 1020.0, "And I'll have the kickoff scheduled before end of week."),
            ("Sarah Chen", 1021.0, 1060.0, "Perfect. Thanks everyone. Let's reconvene next Friday for a progress check. Have a good rest of your day."),
        ],
        "summary": {
            "overview": "The team conducted a comprehensive Q3 roadmap planning session focusing on three strategic initiatives: onboarding flow redesign, AI-powered meeting summaries, and mobile app performance improvements. Key discussions centered around resource allocation, timeline feasibility, and cross-team dependencies. The group agreed on a 40/35/25 engineering split across the initiatives and established clear action items for each team lead.",
            "key_topics": ["Q3 Roadmap", "Onboarding Redesign", "AI Summaries", "Mobile Performance", "Resource Allocation", "UX Research"],
            "chapters": [
                {"title": "Introduction & Agenda", "start_time": 0.0, "summary": "Sarah opens the meeting and sets the agenda for Q3 planning."},
                {"title": "Three Strategic Initiatives", "start_time": 42.5, "summary": "Marcus presents the three core Q3 pillars: onboarding redesign, AI summaries, and mobile performance."},
                {"title": "Initiative Deep Dives", "start_time": 91.0, "summary": "Team discusses feasibility, timelines, and technical challenges for each initiative."},
                {"title": "Resource Allocation", "start_time": 561.0, "summary": "Engineering capacity is split 40/35/25 across the three initiatives."},
                {"title": "Action Items & Close", "start_time": 856.0, "summary": "Final action items assigned and next check-in scheduled for following Friday."},
            ],
            "sentiment": "positive",
        },
        "action_items": [
            {"text": "Coordinate UX research kickoff meeting with design team for Monday", "assignee": "Marcus Williams", "priority": "high", "completed": False},
            {"text": "Send cohort analysis data showing 40% onboarding drop-off before EOD", "assignee": "James O'Brien", "priority": "high", "completed": True},
            {"text": "Prepare mobile engineering plan with two senior engineer requirements", "assignee": "Priya Sharma", "priority": "medium", "completed": False},
            {"text": "Schedule next Friday progress check-in with full team", "assignee": "Sarah Chen", "priority": "low", "completed": False},
        ],
    },
    {
        "id": "m2",
        "title": "Engineering Sprint Retrospective — Sprint 24",
        "date": datetime.now() - timedelta(days=5, hours=1),
        "duration": 2700,
        "bot_name": "Fred",
        "status": "processed",
        "source": "seed",
        "participants": [
            {"id": "p5", "name": "Alex Kumar", "email": "alex@company.com", "avatar_color": "#2563EB"},
            {"id": "p6", "name": "Lena Fischer", "email": "lena@company.com", "avatar_color": "#DB2777"},
            {"id": "p7", "name": "Tom Nguyen", "email": "tom@company.com", "avatar_color": "#0891B2"},
            {"id": "p2", "name": "Marcus Williams", "email": "marcus@company.com", "avatar_color": "#059669"},
        ],
        "transcript": [
            ("Alex Kumar", 0.0, 25.0, "Welcome to the Sprint 24 retro. Let's start with what went well, then what didn't, then improvements for next sprint."),
            ("Lena Fischer", 26.0, 65.0, "I want to call out the CI/CD pipeline improvements. Deployment time went from 18 minutes down to 6 minutes. That's a huge quality of life improvement."),
            ("Tom Nguyen", 66.0, 100.0, "Agreed. And the new PR review process — requiring two approvals for anything touching the database schema — caught a potential migration issue before it hit staging."),
            ("Alex Kumar", 101.0, 140.0, "Those are great wins. What about things that didn't go as planned? I'll start — we underestimated the complexity of the notification system. We carried over 3 story points."),
            ("Marcus Williams", 141.0, 185.0, "The carried-over work is becoming a pattern. This is the second sprint in a row where notification work spilled over. I think we need to break those stories down smaller."),
            ("Lena Fischer", 186.0, 230.0, "I had a blocker mid-sprint waiting for the design specs on the new dashboard. Two days were basically lost. We need earlier design handoffs."),
            ("Tom Nguyen", 231.0, 270.0, "The testing environment was also unstable for about a day and a half. We need better observability on the test infra so we catch those issues faster."),
            ("Alex Kumar", 271.0, 320.0, "Good points all around. For improvements — Marcus, can your team help define 'definition of ready' criteria that includes design specs being complete?"),
            ("Marcus Williams", 321.0, 365.0, "Absolutely. I'll draft a definition of ready document and circulate it before next sprint planning. That should prevent the design blocker situation."),
            ("Lena Fischer", 366.0, 410.0, "For the story sizing issue, I propose we cap user stories at 5 points. Anything larger gets broken down in refinement. Non-negotiable."),
            ("Tom Nguyen", 411.0, 450.0, "I like that. And for test infra, I'll set up Grafana dashboards for our test environment this sprint so we can see issues before they affect developers."),
            ("Alex Kumar", 451.0, 500.0, "These are all great action items. Let's do a quick team health check — how is everyone feeling about the sprint pace?"),
            ("Lena Fischer", 501.0, 535.0, "Honestly, the last two weeks felt a bit hectic. I'd appreciate a bit more buffer in the sprint for unplanned work."),
            ("Tom Nguyen", 536.0, 570.0, "Same. I think we're consistently over-committing by about 15%. Maybe we should reduce capacity by that amount when planning."),
            ("Marcus Williams", 571.0, 610.0, "That's a healthy thing to acknowledge. Let's plan for 85% theoretical capacity next sprint and see if we feel less stretched."),
            ("Alex Kumar", 611.0, 650.0, "Agreed. Thanks everyone, this was a productive retro. See you all at sprint planning on Monday."),
        ],
        "summary": {
            "overview": "Sprint 24 retrospective revealed strong process improvements (CI/CD speed, PR review policies) alongside recurring pain points (story spillover, design handoffs, test infra instability). The team agreed to implement a Definition of Ready, cap user stories at 5 points, reduce planned capacity to 85%, and set up better test infrastructure observability.",
            "key_topics": ["Sprint Retrospective", "CI/CD Pipeline", "Story Sizing", "Definition of Ready", "Test Infrastructure", "Team Health"],
            "chapters": [
                {"title": "What Went Well", "start_time": 0.0, "summary": "CI/CD improvements cut deploy time by 67%; new PR review policy caught a schema migration bug."},
                {"title": "What Didn't Go Well", "start_time": 101.0, "summary": "Story spillover, design handoff delays, and test infra instability identified as key friction points."},
                {"title": "Improvements for Next Sprint", "start_time": 271.0, "summary": "Definition of Ready, 5-point story cap, Grafana dashboards, and 85% capacity planning adopted."},
                {"title": "Team Health Check", "start_time": 451.0, "summary": "Team reports feeling over-committed; consensus to plan at 85% capacity going forward."},
            ],
            "sentiment": "neutral",
        },
        "action_items": [
            {"text": "Draft and circulate Definition of Ready document before next sprint planning", "assignee": "Marcus Williams", "priority": "high", "completed": False},
            {"text": "Set up Grafana dashboards for test environment observability", "assignee": "Tom Nguyen", "priority": "medium", "completed": False},
            {"text": "Update sprint planning template to reflect 85% capacity rule", "assignee": "Alex Kumar", "priority": "medium", "completed": True},
            {"text": "Enforce 5-point max story size rule in next refinement session", "assignee": "Lena Fischer", "priority": "low", "completed": False},
        ],
    },
    {
        "id": "m3",
        "title": "Design Review: Dashboard Redesign v2",
        "date": datetime.now() - timedelta(days=7, hours=2),
        "duration": 1800,
        "bot_name": "Fred",
        "status": "processed",
        "source": "seed",
        "participants": [
            {"id": "p8", "name": "Maya Patel", "email": "maya@company.com", "avatar_color": "#65A30D"},
            {"id": "p3", "name": "Priya Sharma", "email": "priya@company.com", "avatar_color": "#DC2626"},
            {"id": "p4", "name": "James O'Brien", "email": "james@company.com", "avatar_color": "#D97706"},
        ],
        "transcript": [
            ("Maya Patel", 0.0, 30.0, "Thanks for joining. Today we're reviewing the v2 designs for the dashboard. I want to get engineering and product alignment before we finalize."),
            ("James O'Brien", 31.0, 65.0, "The designs look really polished Maya. I especially love the new meeting card layout with the transcript snippet preview. That was a top user request."),
            ("Maya Patel", 66.0, 110.0, "Thank you! I spent a lot of time on the cards. The key interaction is hovering to reveal the action menu — edit, share, delete. Priya, any technical concerns?"),
            ("Priya Sharma", 111.0, 160.0, "The hover interaction is fine. My main concern is the real-time search filtering. The designs show instant results as you type, which means we need debounced API calls with a loading state."),
            ("Maya Patel", 161.0, 200.0, "How fast can we make that feel? Is 300ms debounce workable?"),
            ("Priya Sharma", 201.0, 240.0, "300ms should be fine. We can also cache recent search results in React Query, so repeated queries feel instant."),
            ("James O'Brien", 241.0, 285.0, "I want to make sure the empty state is really good. When someone has no meetings, it should guide them on what to do next, not just show a blank screen."),
            ("Maya Patel", 286.0, 330.0, "I've designed an empty state with a big CTA to connect your calendar or upload a first transcript. I'll share those screens in Figma after this call."),
            ("Priya Sharma", 331.0, 380.0, "One thing I noticed — the filters panel slides out from the left. That's going to conflict with our sidebar navigation on smaller screens. Can we make it a dropdown instead?"),
            ("Maya Patel", 381.0, 420.0, "Oh good catch. Let me rethink that. Maybe a filter bar above the list that collapses to a filter icon on mobile?"),
            ("Priya Sharma", 421.0, 455.0, "That would be much cleaner. And it's easier to implement responsively."),
            ("James O'Brien", 456.0, 500.0, "One more thing — the participant avatars in the meeting card. If there are more than 4 participants, do we show a '+3' overflow?"),
            ("Maya Patel", 501.0, 540.0, "Yes exactly. I show up to 4 avatars and then a count chip for the rest. The full list appears in a tooltip on hover."),
            ("Priya Sharma", 541.0, 580.0, "That's a nice pattern. I'll need the tooltip to be accessible — keyboard navigable and screen reader friendly."),
            ("Maya Patel", 581.0, 620.0, "Absolutely. I'll add that spec to the design notes. Let me also create a component inventory so engineering knows exactly which components need to be built."),
            ("James O'Brien", 621.0, 650.0, "Perfect. I think we're in good shape. When do we expect to start implementation?"),
            ("Priya Sharma", 651.0, 690.0, "If designs are finalized by end of week, we can start next Monday. Two week implementation sprint."),
            ("Maya Patel", 691.0, 730.0, "I'll have everything in Figma by Friday. Thanks both!"),
        ],
        "summary": {
            "overview": "Design review for the dashboard v2 focused on the new meeting card layout, real-time search UX, filter panel responsiveness, and participant avatar overflow handling. Engineering raised practical implementation concerns (debouncing, sidebar conflicts) that led to design revisions. Agreement reached to finalize designs by Friday for a two-week implementation sprint starting Monday.",
            "key_topics": ["Dashboard Redesign", "Meeting Card Layout", "Search UX", "Responsive Design", "Empty State", "Component Inventory"],
            "chapters": [
                {"title": "Design Walkthrough", "start_time": 0.0, "summary": "Maya presents the v2 dashboard designs, highlighting the new meeting card with transcript previews."},
                {"title": "Technical Feasibility", "start_time": 111.0, "summary": "Engineering reviews real-time search implementation with 300ms debounce and React Query caching."},
                {"title": "UX Refinements", "start_time": 241.0, "summary": "Empty state design, filter panel responsiveness, and participant avatar overflow patterns discussed and revised."},
                {"title": "Implementation Timeline", "start_time": 621.0, "summary": "Designs finalized by Friday; two-week implementation sprint starts Monday."},
            ],
            "sentiment": "positive",
        },
        "action_items": [
            {"text": "Share empty state and filter bar designs in Figma by Friday", "assignee": "Maya Patel", "priority": "high", "completed": True},
            {"text": "Create component inventory documenting all new components needed", "assignee": "Maya Patel", "priority": "medium", "completed": False},
            {"text": "Add accessibility specs for avatar tooltip to design notes", "assignee": "Maya Patel", "priority": "medium", "completed": False},
            {"text": "Plan two-week implementation sprint for dashboard v2", "assignee": "Priya Sharma", "priority": "high", "completed": False},
        ],
    },
    {
        "id": "m4",
        "title": "Investor Update Call — Series A",
        "date": datetime.now() - timedelta(days=10, hours=4),
        "duration": 5400,
        "bot_name": "Fred",
        "status": "processed",
        "source": "seed",
        "participants": [
            {"id": "p1", "name": "Sarah Chen", "email": "sarah@company.com", "avatar_color": "#7C3AED"},
            {"id": "p9", "name": "David Kaufman", "email": "david@vc-firm.com", "avatar_color": "#9333EA"},
            {"id": "p10", "name": "Rachel Torres", "email": "rachel@vc-firm.com", "avatar_color": "#EA580C"},
        ],
        "transcript": [
            ("Sarah Chen", 0.0, 45.0, "David, Rachel, thank you for making time today. We're really excited to share our Q2 results and give you a preview of where we're heading."),
            ("David Kaufman", 46.0, 80.0, "Likewise Sarah. We've been impressed with the trajectory. Let's dive right in."),
            ("Sarah Chen", 81.0, 150.0, "So to start with the headline numbers — we ended Q2 with 12,400 monthly active users, up 34% quarter over quarter. ARR is at $1.8 million, up from $1.1 million at the end of Q1."),
            ("Rachel Torres", 151.0, 195.0, "That growth rate is outstanding. What's driving the acceleration? Is it a specific channel or product change?"),
            ("Sarah Chen", 196.0, 270.0, "It's a combination of things. We launched our Slack integration in May which drove a significant inbound spike. And our word-of-mouth coefficient improved — users are inviting an average of 2.3 colleagues within their first two weeks."),
            ("David Kaufman", 271.0, 320.0, "The viral coefficient improving is really compelling. What's the net revenue retention look like?"),
            ("Sarah Chen", 321.0, 380.0, "NRR is at 118%, which we're proud of. The upsell motion from individual to team plans is working. Teams are sticky once they start using the transcript collaboration features."),
            ("Rachel Torres", 381.0, 430.0, "Strong. What's the biggest risk factor you see on the horizon?"),
            ("Sarah Chen", 431.0, 510.0, "Competition is always top of mind. Otter.ai recently raised a big round and is being very aggressive on pricing. We believe our AI summary quality and integrations are meaningfully ahead, but we need to keep innovating."),
            ("David Kaufman", 511.0, 570.0, "How much runway do you have at current burn?"),
            ("Sarah Chen", 571.0, 630.0, "We have 14 months of runway at current burn. We're forecasting profitability at around 18,000 MAU, which at current growth rates we'd hit in approximately 9 months."),
            ("Rachel Torres", 631.0, 690.0, "That's tight but achievable. Are you planning to raise before you hit profitability?"),
            ("Sarah Chen", 691.0, 760.0, "We're not in active fundraising mode right now, but we'd consider a strategic raise if the right partner came along, particularly someone who could open enterprise doors. That's the market segment we're most excited about."),
            ("David Kaufman", 761.0, 820.0, "Enterprise is smart. The compliance and security requirements are high, but the ACV is transformative. Do you have any enterprise design partners yet?"),
            ("Sarah Chen", 821.0, 880.0, "We have three enterprise pilots running — a law firm, a consulting company, and a healthcare group. Early feedback is very positive on the security controls we've built."),
            ("Rachel Torres", 881.0, 940.0, "This has been a great update Sarah. We're very pleased with the momentum. We'll share this with the rest of our partnership team and follow up next week."),
            ("Sarah Chen", 941.0, 980.0, "Wonderful. We'll send the formal board update deck with full metrics by end of week. Thank you both."),
        ],
        "summary": {
            "overview": "Investor update call covering Q2 performance metrics showing 34% QoQ MAU growth (12,400 MAU), ARR of $1.8M (up from $1.1M), NRR of 118%, and 14 months of runway. Discussion covered growth drivers (Slack integration, viral coefficient), competitive landscape (Otter.ai), path to profitability, and enterprise market opportunity with three active pilots.",
            "key_topics": ["Investor Relations", "Q2 Metrics", "ARR Growth", "NRR", "Enterprise Strategy", "Runway", "Competition"],
            "chapters": [
                {"title": "Q2 Performance Overview", "start_time": 0.0, "summary": "Sarah presents headline metrics: 12.4K MAU (+34% QoQ), $1.8M ARR."},
                {"title": "Growth Drivers Deep Dive", "start_time": 151.0, "summary": "Slack integration launch and improved viral coefficient (2.3 colleague invites) drove acceleration."},
                {"title": "Financial Health & Risk", "start_time": 271.0, "summary": "NRR of 118%, 14 months runway, profitability projected at 18K MAU (~9 months away)."},
                {"title": "Enterprise Strategy", "start_time": 761.0, "summary": "Three enterprise pilots (law, consulting, healthcare) with positive early feedback on security controls."},
            ],
            "sentiment": "positive",
        },
        "action_items": [
            {"text": "Send formal board update deck with full Q2 metrics by end of week", "assignee": "Sarah Chen", "priority": "high", "completed": True},
            {"text": "Prepare enterprise pilot case study summaries for investor deck", "assignee": "Sarah Chen", "priority": "medium", "completed": False},
        ],
    },
    {
        "id": "m5",
        "title": "New Team Member Onboarding — Engineering",
        "date": datetime.now() - timedelta(days=1, hours=5),
        "duration": 1500,
        "bot_name": "Fred",
        "status": "processed",
        "source": "seed",
        "participants": [
            {"id": "p5", "name": "Alex Kumar", "email": "alex@company.com", "avatar_color": "#2563EB"},
            {"id": "p11", "name": "Jordan Lee", "email": "jordan@company.com", "avatar_color": "#65A30D"},
        ],
        "transcript": [
            ("Alex Kumar", 0.0, 30.0, "Hey Jordan, welcome to the team! Really excited to have you join us. Today we'll do a quick architectural overview and get you set up with the dev environment."),
            ("Jordan Lee", 31.0, 60.0, "Thanks Alex! I've been reading through the docs and I have a bunch of questions. The codebase is bigger than I expected."),
            ("Alex Kumar", 61.0, 120.0, "Ha, yeah it's grown a lot in the last year. So at a high level — we have a Next.js frontend, a FastAPI Python backend, and PostgreSQL in production but SQLite for local dev."),
            ("Jordan Lee", 121.0, 155.0, "How is the code organized? I saw multiple service directories but wasn't sure of the boundaries."),
            ("Alex Kumar", 156.0, 230.0, "Good question. We follow a layered architecture: routers handle HTTP, services contain business logic, and repositories handle database access. Nothing should jump layers."),
            ("Jordan Lee", 231.0, 265.0, "Makes sense. How do you handle async operations? I noticed a lot of async/await in the services."),
            ("Alex Kumar", 266.0, 320.0, "Everything async all the way down. We use SQLAlchemy async with aiosqlite. For the frontend, React Query handles all server state. It makes data fetching and caching really clean."),
            ("Jordan Lee", 321.0, 360.0, "What about testing? What's the test strategy?"),
            ("Alex Kumar", 361.0, 420.0, "We test at three levels. Unit tests for services and utilities, integration tests for API endpoints using pytest-asyncio and httpx, and E2E tests with Playwright for critical user flows."),
            ("Jordan Lee", 421.0, 460.0, "That's comprehensive. How long does the full test suite take?"),
            ("Alex Kumar", 461.0, 500.0, "About 4 minutes for the full suite. We run unit and integration tests on every PR and the E2E tests nightly."),
            ("Jordan Lee", 501.0, 540.0, "What should I pick up as my first task? Something meaningful but not overwhelming?"),
            ("Alex Kumar", 541.0, 590.0, "I was thinking you could work on the export feature — PDF and Markdown export of transcripts. It's a self-contained feature with a clear scope, good tests to write, and touches all the layers."),
            ("Jordan Lee", 591.0, 620.0, "That sounds perfect. I'll start by reading the existing transcript service code today."),
            ("Alex Kumar", 621.0, 660.0, "Great. Ping me on Slack anytime — seriously, no question is too small when you're new. I'd rather you ask than be stuck."),
            ("Jordan Lee", 661.0, 690.0, "Really appreciate that. One last question — what's the deployment process look like?"),
            ("Alex Kumar", 691.0, 740.0, "We use GitHub Actions for CI. Every merge to main deploys to staging automatically. Production deploys require a manual approval step in the Actions UI."),
        ],
        "summary": {
            "overview": "Onboarding session for new engineer Jordan Lee covering system architecture (Next.js + FastAPI + SQLAlchemy), code organization principles (layered architecture), async patterns, testing strategy (unit/integration/E2E), and first task assignment (transcript export feature). Alex emphasized open communication culture and the PR-based CI/CD workflow.",
            "key_topics": ["Onboarding", "System Architecture", "Layered Architecture", "Testing Strategy", "Async Patterns", "CI/CD"],
            "chapters": [
                {"title": "Architecture Overview", "start_time": 0.0, "summary": "Stack introduction: Next.js frontend, FastAPI backend, PostgreSQL/SQLite database."},
                {"title": "Code Organization", "start_time": 121.0, "summary": "Layered architecture: routers → services → repositories. No layer skipping."},
                {"title": "Testing & CI/CD", "start_time": 321.0, "summary": "Three-level test strategy; 4-minute test suite; GitHub Actions CI with manual production gate."},
                {"title": "First Task Assignment", "start_time": 501.0, "summary": "Jordan assigned the transcript export feature (PDF/Markdown) as a first self-contained contribution."},
            ],
            "sentiment": "positive",
        },
        "action_items": [
            {"text": "Read transcript service code and understand existing patterns", "assignee": "Jordan Lee", "priority": "high", "completed": False},
            {"text": "Set up local development environment and run test suite", "assignee": "Jordan Lee", "priority": "high", "completed": True},
            {"text": "Create GitHub issue for transcript export feature with scope and acceptance criteria", "assignee": "Alex Kumar", "priority": "medium", "completed": False},
        ],
    },
    {
        "id": "m6",
        "title": "Customer Success Weekly Sync",
        "date": datetime.now() - timedelta(hours=6),
        "duration": 2400,
        "bot_name": "Fred",
        "status": "processed",
        "source": "seed",
        "participants": [
            {"id": "p4", "name": "James O'Brien", "email": "james@company.com", "avatar_color": "#D97706"},
            {"id": "p12", "name": "Nina Roberts", "email": "nina@company.com", "avatar_color": "#DB2777"},
            {"id": "p13", "name": "Carlos Mendez", "email": "carlos@company.com", "avatar_color": "#0891B2"},
        ],
        "transcript": [
            ("James O'Brien", 0.0, 30.0, "Let's kick off the weekly sync. Nina, you wanted to lead today — go for it."),
            ("Nina Roberts", 31.0, 80.0, "Thanks James. So this week was a mixed bag. We had two churn risks escalated to red status, but we also had our best NPS week of the quarter."),
            ("Carlos Mendez", 81.0, 120.0, "Which accounts are red? I wasn't looped in on one of them."),
            ("Nina Roberts", 121.0, 175.0, "Apex Manufacturing and Brightline Consulting. Apex is frustrated with the Zoom integration reliability — they had three meetings this week where the bot didn't join. Brightline is a pricing concern."),
            ("James O'Brien", 176.0, 220.0, "The Zoom bot issue is a known engineering bug. I talked to Marcus yesterday — there's a fix deployed to staging that should hit production Thursday."),
            ("Carlos Mendez", 221.0, 270.0, "That's good news. Can I tell Apex that? If they know a fix is coming this week, they might calm down."),
            ("James O'Brien", 271.0, 310.0, "Yes, absolutely. Tell them Thursday and we'll follow up Friday to confirm it's working for them."),
            ("Nina Roberts", 311.0, 360.0, "For Brightline, they're on a Team plan and feel like they're paying for features they don't use. They want a downgrade to Individual but that means a 60% revenue drop."),
            ("Carlos Mendez", 361.0, 410.0, "I spoke with their admin last week. Their actual pain point is they want custom branding on exported transcripts. That's not available on any plan right now."),
            ("James O'Brien", 411.0, 460.0, "Interesting. So it's not really a pricing objection, it's a missing feature objection. Custom branding is on the roadmap but not prioritized."),
            ("Nina Roberts", 461.0, 510.0, "Could we do a custom deal — keep them on Team pricing but commit to white-label exports in Q3 as a design partner? They might go for that."),
            ("James O'Brien", 511.0, 560.0, "I like that framing. Let's propose it. Carlos, can you get on a call with them this week and present that option?"),
            ("Carlos Mendez", 561.0, 595.0, "I'll reach out today to schedule for Wednesday or Thursday."),
            ("Nina Roberts", 596.0, 640.0, "Now for the good news — we ran our quarterly NPS survey and got a score of 52. Last quarter was 41. The feedback themes are speed of the AI summaries and the search quality."),
            ("James O'Brien", 641.0, 685.0, "52 is really strong for B2B SaaS. That's in world-class territory. Let's make sure we share those positive feedback quotes with the product and engineering teams — it's motivating."),
            ("Carlos Mendez", 686.0, 720.0, "I'll compile the best quotes and put them in the company Slack channel. Some of them are really heartfelt."),
            ("Nina Roberts", 721.0, 760.0, "Also, we have three customers who've offered to be case study subjects. I'll start the process of getting legal approval for those this week."),
            ("James O'Brien", 761.0, 800.0, "Excellent. Case studies will be gold for the enterprise push. Alright, let's close out. Good week overall despite the two fires. See you next week."),
        ],
        "summary": {
            "overview": "Customer success weekly sync addressed two red-status churn risks (Apex Manufacturing — Zoom bot bug, Brightline Consulting — missing custom branding feature) and celebrated an NPS improvement from 41 to 52. Key outcomes include a Thursday production fix for Apex, a proposed design partnership deal for Brightline, and plans to leverage new case study opportunities for the enterprise push.",
            "key_topics": ["Customer Success", "Churn Risk", "NPS Score", "Zoom Integration Bug", "Custom Branding", "Case Studies", "Enterprise Sales"],
            "chapters": [
                {"title": "Churn Risk Review", "start_time": 31.0, "summary": "Two red-status accounts: Apex (Zoom bot reliability) and Brightline (pricing/missing features)."},
                {"title": "Apex Manufacturing Resolution", "start_time": 176.0, "summary": "Engineering fix for Zoom bot deploys Thursday; CSM to communicate timeline to customer."},
                {"title": "Brightline Consulting Strategy", "start_time": 311.0, "summary": "Root cause is missing white-label export feature, not pricing. Design partner proposal planned."},
                {"title": "NPS Results & Wins", "start_time": 596.0, "summary": "NPS improved from 41 to 52; three case study candidates identified for enterprise marketing."},
            ],
            "sentiment": "neutral",
        },
        "action_items": [
            {"text": "Contact Apex Manufacturing to communicate Thursday production fix for Zoom bot", "assignee": "Carlos Mendez", "priority": "high", "completed": False},
            {"text": "Schedule call with Brightline Consulting to propose design partner deal for white-label exports", "assignee": "Carlos Mendez", "priority": "high", "completed": False},
            {"text": "Follow up with Apex on Friday to confirm Zoom bot fix is working", "assignee": "Carlos Mendez", "priority": "medium", "completed": False},
            {"text": "Compile best NPS feedback quotes and share in company Slack", "assignee": "Carlos Mendez", "priority": "low", "completed": True},
            {"text": "Begin legal approval process for three case study customers", "assignee": "Nina Roberts", "priority": "medium", "completed": False},
        ],
    },
]


# ---------------------------------------------------------------------------
# Seeder logic
# ---------------------------------------------------------------------------

async def seed(session: AsyncSession) -> None:
    from sqlalchemy import text

    # Drop and recreate all tables for a clean seed
    await session.execute(text("DELETE FROM summary_topics"))
    await session.execute(text("DELETE FROM topics"))
    await session.execute(text("DELETE FROM chapters"))
    await session.execute(text("DELETE FROM action_items"))
    await session.execute(text("DELETE FROM summaries"))
    await session.execute(text("DELETE FROM transcript_lines"))
    await session.execute(text("DELETE FROM meeting_participants"))
    await session.execute(text("DELETE FROM meetings"))
    await session.execute(text("DELETE FROM participants"))
    await session.execute(text("DELETE FROM workspaces"))
    await session.commit()

    all_participants: dict = {}

    from app.models.workspace import Workspace
    workspace = Workspace(id="ws_default", name="Acme Corp")
    session.add(workspace)
    await session.flush()

    for meeting_data in MEETINGS:
        # Create meeting
        from app.models.meeting import Meeting, MeetingStatus
        meeting = Meeting(
            id=meeting_data["id"],
            workspace_id="ws_default",
            title=meeting_data["title"],
            date=meeting_data["date"],
            duration=meeting_data["duration"],
            bot_name=meeting_data["bot_name"],
            status=MeetingStatus(meeting_data["status"]) if meeting_data["status"] == "failed" else MeetingStatus.COMPLETED,
            source=meeting_data["source"],
        )
        session.add(meeting)
        await session.flush()

        # Create / reuse participants
        for p_data in meeting_data["participants"]:
            from app.models.participant import Participant
            if p_data["id"] not in all_participants:
                participant = Participant(
                    id=p_data["id"],
                    name=p_data["name"],
                    email=p_data["email"],
                    avatar_color=p_data["avatar_color"],
                )
                session.add(participant)
                await session.flush()
                all_participants[p_data["id"]] = participant

            from app.models.meeting import meeting_participants_table
            await session.execute(
                meeting_participants_table.insert().values(
                    meeting_id=meeting.id, participant_id=p_data["id"]
                )
            )

        # Create transcript lines
        from app.models.transcript import TranscriptLine
        for seq, (speaker, start, end, text) in enumerate(meeting_data["transcript"]):
            tl = TranscriptLine(
                id=str(uuid.uuid4()),
                workspace_id="ws_default",
                meeting_id=meeting.id,
                speaker_name=speaker,
                start_time=start,
                end_time=end,
                text=text,
                sequence_number=seq,
            )
            session.add(tl)

        # Create summary
        from app.models.summary import Summary, SentimentEnum
        from app.models.chapter import Chapter
        from app.models.topic import Topic
        
        s_data = meeting_data["summary"]
        summary = Summary(
            id=str(uuid.uuid4()),
            workspace_id="ws_default",
            meeting_id=meeting.id,
            overview=s_data["overview"],
            sentiment=SentimentEnum(s_data["sentiment"]) if s_data.get("sentiment") else SentimentEnum.NEUTRAL,
        )
        session.add(summary)
        await session.flush()
        
        for ch_data in s_data["chapters"]:
            ch = Chapter(
                id=str(uuid.uuid4()),
                workspace_id="ws_default",
                summary_id=summary.id,
                title=ch_data["title"],
                start_time=ch_data["start_time"],
                summary_text=ch_data["summary"],
            )
            session.add(ch)
            
        for topic_name in s_data["key_topics"]:
            # Check if topic exists to avoid duplicates
            from sqlalchemy import select
            stmt = select(Topic).where(Topic.name == topic_name)
            res = await session.execute(stmt)
            topic = res.scalar_one_or_none()
            if not topic:
                topic = Topic(id=str(uuid.uuid4()), workspace_id="ws_default", name=topic_name)
                session.add(topic)
                await session.flush()
                
            from app.models.topic import summary_topics_table
            await session.execute(
                summary_topics_table.insert().values(
                    summary_id=summary.id, topic_id=topic.id
                )
            )

        # Create action items
        from app.models.action_item import ActionItem, ActionItemPriority
        for ai_data in meeting_data["action_items"]:
            ai = ActionItem(
                id=str(uuid.uuid4()),
                workspace_id="ws_default",
                meeting_id=meeting.id,
                text=ai_data["text"],
                assignee=ai_data["assignee"],
                priority=ActionItemPriority(ai_data["priority"]),
                completed=ai_data["completed"],
            )
            session.add(ai)

    await session.commit()
    print(f"[OK] Seeded {len(MEETINGS)} meetings with transcripts, summaries, and action items.")


async def main() -> None:
    # Import models to register with metadata
    import app  # noqa: F401
    from app.database import init_db

    await init_db()
    async with AsyncSessionLocal() as session:
        await seed(session)


if __name__ == "__main__":
    asyncio.run(main())
