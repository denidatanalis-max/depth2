# Depth Culture Design System

## Overview

**Depth Culture** is an Indonesian company's internal web application for managing and publishing corporate journals (Jurnal Perusahaan). It is a multi-role workflow platform built with Django + Bootstrap 5, featuring a rich dark maroon/gold visual identity.

**Source:** GitHub repository `denidatanalis-max/depth2` (https://github.com/denidatanalis-max/depth2)

### Product Summary
A single web product: an internal journal management system where employees submit research journals through a multi-stage approval workflow (Writer → Manager → Admin → Scoring → Tim Rekomendasi → Publication). Public-facing journal listing at `/publikasi/`.

---

## Tech Stack
- Python 3.11 / Django 4.2 LTS
- Bootstrap 5.3.3 + Bootstrap Icons 1.11.3
- SQLite (deployable to MySQL/PostgreSQL)
- django-crispy-forms + crispy-bootstrap5
- Deployed via cPanel (passenger_wsgi.py)

---

## User Roles
| Role | Indonesian Name | Responsibility |
|------|----------------|----------------|
| Writer | Supervisor / Penulis | Create & submit journals |
| Manager | Leader / Approver | Review title, abstract, PDF |
| Admin | Admin | Send to scoring, publish |
| Scoring | Penilai | Score on 4 criteria |
| Tim Rekomendasi | — | Final recommendation before publish |
| Super Admin | Super Admin | Full access + Django admin |

---

## CONTENT FUNDAMENTALS

### Language
All copy is in **Bahasa Indonesia**. Labels, navigation, button text, and system messages are Indonesian.

### Tone & Voice
- Formal-professional. No casual slang.
- System messages are direct and action-oriented: "Kirim ke Scoring", "Buat Jurnal Baru".
- Role-based greetings: "Selamat datang, [Nama]".
- Error/status messages are clear and specific: "Jurnal dikembalikan untuk revisi".

### Casing
- Title Case for page headings and brand name.
- Sentence case for labels and body copy.
- ALL CAPS for form labels (login screen): `USERNAME`, `PASSWORD`.

### Pronouns / POV
- Second person implied (no explicit "Anda" in most UI labels).
- Greeting uses full name: "Selamat datang, Budi Santoso".

### Emoji
- **Not used** anywhere in the UI. Bootstrap Icons exclusively.

### Example Copy Patterns
- Nav: "Dashboard", "Publikasi", "Buat Jurnal Baru", "Logout"
- Actions: "Ajukan ke Manager", "Upload PDF", "Kirim ke Scoring", "Publikasikan"
- States: "Menunggu Approval", "Perlu Revisi", "Diverifikasi"
- Empty state: "Belum ada jurnal. Mulai buat jurnal pertama Anda!"

---

## VISUAL FOUNDATIONS

### Color Palette
| Token | Value | Usage |
|-------|-------|-------|
| `--gold` | `#d4af37` | Primary accent — brand color, active states, links, card titles |
| `--gold-hover` | `#f0c84a` | Gold on hover |
| `--gold-dim` | `rgba(212, 175, 55, 0.3)` | Borders, dividers |
| `--red-primary` | `#7a0000` → `#b80000` | Button gradient, active sidebar bg |
| `--red-bright` | `#8b0000` / `#cc0000` | Hover states |
| `--bg-dark` | `rgba(5, 0, 0, 0.45)` | Full-page overlay on background image |
| `--bg-card` | `rgba(25, 5, 0, 0.50)` | Card background |
| `--bg-card-header` | `rgba(120, 10, 0, 0.50)` | Card header |
| `--bg-sidebar` | `rgba(60,0,0,0.68)` → `rgba(20,0,0,0.75)` | Sidebar gradient |
| `--text-primary` | `#fff8ee` | Body text — warm off-white |
| `--text-muted` | `rgba(255, 220, 170, 0.70)` | Muted/secondary text |
| `--text-warm` | `rgba(255, 220, 170, 0.85)` | Form labels |
| `--green-success` | `#004d1a` → `#006622` | Success button |
| `--stat-blue` | `#4da6ff` | Stat card accent |
| `--stat-green` | `#4dffaa` | Stat card accent |
| `--stat-orange` | `#ffb84d` | Stat card accent |
| `--stat-red` | `#ff6666` | Stat card accent |

### Background
- Full-bleed **photo background** (`background_login2.png`) — appears to be a dark atmospheric/nature image.
- Dark overlay `rgba(5, 0, 0, 0.45)` + `background-attachment: fixed`.
- All UI panels are semi-transparent with `backdrop-filter: blur(2–8px)`.

### Typography
- **Font Family**: `'Segoe UI', sans-serif` — system font, no custom web fonts.
- **Brand name**: Bold, letter-spacing 0.5–1px, `#d4af37` gold color.
- **Page titles**: `.page-title` — bold, gold, letter-spacing 0.5px.
- **Body**: `#fff8ee`, regular weight.
- **Labels**: 0.875rem, 500 weight, warm cream.
- **Form labels (login)**: 0.82rem, 600 weight, uppercase, letter-spacing 0.5px.
- **Small/muted**: 0.75–0.82rem.

### Spacing & Layout
- Sidebar: fixed 250px width, sticky, full-height.
- Content padding: `1.75rem`.
- Card radius: `12px`.
- Input/button radius: `8px`.
- Gap between elements: Bootstrap grid (row/col).

### Borders
- All borders: `rgba(212, 175, 55, 0.25–0.45)` — thin gold, semi-transparent.
- Cards have double-border effect: outer gold `rgba(212,175,55,0.3)` + inner box-shadow ring `rgba(139,0,0,0.2)`.
- Active sidebar nav: `border-left: 3px solid #d4af37`.

### Shadows
- Cards: `0 4px 24px rgba(0,0,0,0.5)` + inner ring `0 0 0 1px rgba(139,0,0,0.2)`.
- Buttons: `0 3px 14px rgba(120,0,0,0.5)`; hover: `0 5px 18px rgba(160,0,0,0.6)`.
- Brand icon: `filter: drop-shadow(0 0 10px rgba(212,175,55,0.4))`.

### Buttons
- **Primary / Danger**: Red gradient `#7a0000 → #b80000`, gold border, `#ffeebb` text.
- **Hover**: lighter gradient `#9a0000 → #cc0000`, brighter gold border, `translateY(-1px)`.
- **Active**: `translateY(0)`.
- **Secondary**: dark red semi-transparent bg.
- **Success**: deep green gradient.
- **Outline**: transparent bg, gold border + text; hover fills with dark red.

### Animations & Transitions
- Buttons: `transition: all 0.2s ease` with `translateY(-1px)` lift on hover.
- Nav links: `transition: all 0.2s ease`.
- No page transitions, no bounce, no JS animations.
- Focus ring: `0 0 0 3px rgba(212,175,55,0.15)` gold glow.

### Corner Radii
- Cards: `12px`
- Inputs, buttons, alerts: `8px–10px`
- Sidebar: no rounding (edge-to-edge)
- Stat card circles/badges: `50%`

### Scrollbar
- Custom: 6px wide, dark red thumb `rgba(139,0,0,0.6)`, near-black track.

### Cards
- Semi-transparent dark bg + gold border + backdrop blur.
- Card header: darker red tint, gold text.
- Stat cards: left border `4px solid` in accent color (blue/green/orange/red).

### Imagery
- One background photo (atmospheric, dark). No illustration assets.
- No brand logos or custom illustrations found.
- Icon-only identity via Bootstrap Icons.

### Color vibe
- Warm, cinematic dark. Maroon/burgundy + antique gold. Very formal, executive feeling.

---

## ICONOGRAPHY

### Icon System
- **Bootstrap Icons** (v1.11.3) via CDN: `https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css`
- Usage: `<i class="bi bi-{name}"></i>` inline HTML.
- **No custom icon font, no SVG sprite, no PNG icons.**
- Icons are used as decorative prefixes on nav items, buttons, headings, and empty states.

### Key Icons Used
| Icon class | Usage |
|------------|-------|
| `bi-journal-text` | Brand icon / logo substitute |
| `bi-speedometer2` | Dashboard nav |
| `bi-globe` | Publikasi nav |
| `bi-plus-circle` | Create new action |
| `bi-person-circle` | User identity |
| `bi-box-arrow-left` | Logout |
| `bi-box-arrow-in-right` | Login |
| `bi-eye` | View detail |
| `bi-pencil-fill` | Writer/edit |
| `bi-lock-fill` | Password field |
| `bi-person-fill` | Username field |
| `bi-journal-x` | Empty state |

### Emoji
- **Not used** in this product.

### Assets Available
- `assets/background_login2.png` — Full-bleed dark atmospheric background photo.

---

## File Index

```
/
├── README.md                    ← This file
├── SKILL.md                     ← Agent skill descriptor
├── colors_and_type.css          ← CSS custom properties for colors + typography
├── assets/
│   └── background_login2.png   ← Full-bleed background photo
├── preview/
│   ├── colors_primary.html      ← Primary color swatches
│   ├── colors_semantic.html     ← Semantic / UI color tokens
│   ├── colors_stat.html         ← Stat accent colors
│   ├── type_scale.html          ← Typography scale specimen
│   ├── type_labels.html         ← Label & UI text styles
│   ├── spacing_tokens.html      ← Spacing & radius tokens
│   ├── shadows_borders.html     ← Shadow & border system
│   ├── buttons.html             ← Button variants
│   ├── badges_alerts.html       ← Badge & alert variants
│   ├── cards.html               ← Card variants
│   ├── forms.html               ← Form input styles
│   ├── sidebar.html             ← Sidebar component
│   └── stat_cards.html          ← Stat card variants
└── ui_kits/
    └── depth_culture/
        ├── README.md
        └── index.html           ← Interactive UI kit (login → dashboard → journal detail)
```
