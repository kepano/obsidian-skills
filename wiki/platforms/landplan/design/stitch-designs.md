---
title: Stitch UI Designs — Projects Ecosystem
tags: [landplan, design, stitch, ui, projects, map]
created: 2026-04-18
updated: 2026-04-18
status: growing
---

# Stitch UI Designs — Projects Ecosystem & New Map Interface

Five named designs produced via Google Stitch MCP for the [[epic-planning|Planning epic]]. Claude Code pulls each via Stitch MCP in its own build session.

Design system: [[terra-contour]]

---

## Shared Navigation System

### Floating Global Control Bar (top-left, both modes)
- Back arrow (return to dashboard)
- **Map / Projects pill toggle** — prominent, always visible; first-class navigation between spatial and planning views
- Utility actions: save-view (camera icon), share icon; forest-green hover state

No full-width top header on either view.

### Integrated Collapsible Left Sidebar (same visual shell, different contents)
Same treatment across both modes: warm neutral surface, rounded corners, subtle shadow, collapse icon at top, LandPlan logo fixed at bottom.

**Map Mode sidebar sections:**
1. Layers (satellite, topography, etc.)
2. Saved Views
3. Structures
4. Plants
5. Projects (object filter by project association — eye toggles, not project management)
6. Time (Sun/Shadow slider + Project Timeline slider, stacked, visually distinct)

**Projects Mode sidebar sections:**
1. Mission
2. Projects
3. Stakeholders
4. Reference Info
5. Docs

---

## The Five Designs

### 1. New Map Interface
*Route: `/plan/:id/map-beta` (Beta) → `/plan/:id` (post-cutover)*

Spatial view refresh — not new mapping features; functional feature set unchanged. Cleaner menus, integrated project data.

- Floating Global Control Bar (top-left); toggle set to "Map"
- Left sidebar with six Map Mode sections; LandPlan logo at bottom; **no dark footer**
- Projects section in sidebar = object filter (eye toggle per project, not PM UI); special "Unassigned" row; property boundary always visible with Terra Contour treatment
- Time section: two visually distinct stacked sliders (Sun/Shadow hours-of-day + Project Timeline months-to-years)
- **Floating tools palette on LEFT-CENTRE:** Select, Object, Distance, Area, Import, Photo
- **RIGHT-CENTRE slot:** tool windows and edit modals (Measure Area, Edit Tree Stand, Edit Tree Properties pattern); NOT a Terrain Analysis panel
- Map canvas edge-to-edge

### 2. Property Overview
*Route: `/plan/:id/projects` (Mission section default)*

Program-level mission statement page — stakeholders see the owner's long-horizon vision and why projects are prioritised the way they are.

- Floating Control Bar; toggle set to "Projects"
- Projects Mode sidebar; "Mission" active
- Main canvas (top to bottom):
  - Large pull-quote mission statement (hero, markdown-rendered, editable)
  - Property metadata: plan title, location, acreage, boundary confirmation status, APN
  - Jurisdiction stale-flag banner (warm tone; non-destructive)
  - Reference Info section — five categories (Zoning, Rainwater, Off-Grid, Permitting, Public Land) as document-style subsections; entry counts; source badges ("added by Claude Coworker")
  - Docs section
- Dark blue LandPlan footer: *"© 2026 Smart Farm Technologies. Surveying the Future."*

### 3. Project Portfolio Overview
*Route: `/plan/:id/projects` (Projects section)*

Ranked stack of projects — primary Projects Mode landing after Property Overview.

- Floating Control Bar; toggle set to "Projects"
- Sidebar with "Projects" active
- Main canvas: **drag-to-reorder ranked stack** of project cards, one per row
  - Each card: sequence number (left edge), project title, objective one-liner, status dot + text, date range, budget range, activity count, stakeholder avatars, project-color swatch, rough actual cost (optional)
  - Inline completion prompt when all activities done: *"All activities complete — mark project complete?"* — not a pill
- "+ New Project" action at top of canvas
- Standard dark blue LandPlan footer

### 4. Project Detail
*Route: `/plan/:id/projects/:projectId`*

- Floating Control Bar; toggle set to "Projects"
- Sidebar
- Main canvas:
  - Header: project title (inline editable), status dot, sequence position, date range, budget, rough actual cost
  - Objective block (markdown-rendered)
  - Primary tabs: **Activities** (default), Quote Packages, DIY Estimate, Docs
  - Activities tab — two coordinated views side-by-side:
    1. List view with drag handles; each row: title, duration days, assigned stakeholder avatar, status dot, linked map object count, dependency count
    2. Mermaid `flowchart` of dependency graph (FS/SS/FF/SF). Read-only; editing via list's add-dependency dropdown
- Standard dark blue LandPlan footer

### 5. Project Activity Detail Drawer
*Triggered from: Project Detail activity list OR New Map Interface (linked map object tapped)*

**Slide-in panel from right edge** (not a floating modal). Same component in both Map Mode and Projects Mode.

- Activity title, status dot, duration, planned start/end, completion date
- Assigned stakeholder with avatar and role label
- Notes: append-only log with author and timestamp (stakeholder notes appear here)
- Linked map objects as small chips with thumbnails; tappable to fly map to object
- Dependencies: compact predecessors/successors list with type labels (FS/SS/FF/SF)
- Attached docs
- "Open in Map" action (from Project Detail → flips to Map Interface, highlights linked objects)

---

## Cross-Design Requirements

- Project colour swatches consistent everywhere: sidebar, cards, map dots, drawer chips
- Drag affordances obvious but not heavy
- Empty states warm and encouraging ("No projects yet — what's the first thing you'd like to build?")
- Sidebar collapse pattern identical in both modes
- Responsive: desktop-primary; graceful collapse at tablet widths
- Accessibility: high contrast on status dots, focus rings, keyboard-navigable drag reordering

---

## Out of Scope (This Design Pass)

- Contractor Quote Package view (separate future Stitch pass)
- Stakeholder management screen
- DIY Estimate editor internals (tab placeholder only)
- Quote comparison view
- Mobile app screens
- Login, onboarding, registration flows
- **Terrain Analysis panel — explicitly excluded from Map Mode**

---

## Build Context

- New Map Interface built as isolated Beta at `/plan/:id/map-beta` under a feature flag; existing `PlanPage.tsx` untouched during Beta
- After A/B validation, `MapPage.tsx` promotes to `/plan/:id`, `PlanPage.tsx` retired

---

## Related

- [[terra-contour]] — the design system these designs use
- [[epic-planning]] — the planning epic these designs support
- [[build-roadmap]] — session sequencing for pulling and wiring each design
