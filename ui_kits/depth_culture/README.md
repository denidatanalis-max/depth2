# Depth Culture UI Kit

## Overview
Interactive hi-fi prototype of the Depth Culture internal journal management system (Django web app).

## Screens
1. **Login** — Split-panel login with brand panel + form
2. **Writer Dashboard** — Stat cards, journal table, create new
3. **Manager Dashboard** — Pending approvals, all writer journals
4. **Journal Detail** — Workflow tracker, action panel, activity log, scoring
5. **Create Journal** — Title + abstract form
6. **Public Journal List** — Published journals, public view

## How to Use
Open `index.html` in a browser. Use these demo credentials:
- `supervisor1` / `demo1234` → Writer dashboard
- `manager1` / `demo1234` → Manager dashboard
- `admin1` / `demo1234` → Writer-like dashboard (admin role)
- `scoring1` / `demo1234` → Writer-like dashboard (scoring role)

## Components
All components are inline in `index.html` as React+Babel. Key components:
- `Sidebar` — sticky sidebar with nav + user footer
- `Card` — glass card with optional header
- `Btn` — button with hover states (primary/success/warning/secondary/outline)
- `Badge` / `statusBadge` — role and status badges
- `Alert` — success/danger/warning/info alerts
- `FormField` — labeled input with optional icon prefix
- `JournalTable` — sortable journal listing
- `WriterDashboard`, `ManagerDashboard` — role dashboards
- `JournalDetail` — detail view with workflow stepper
- `CreateJournal` — new journal form
- `PublicJournals` — public listing

## Design Tokens
See `../../colors_and_type.css` for all CSS custom properties.
