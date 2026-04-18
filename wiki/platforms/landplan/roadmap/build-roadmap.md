---
title: Build Roadmap — Planning Epic
tags: [landplan, roadmap, build, sessions, claude-code]
created: 2026-04-18
updated: 2026-04-18
status: growing
---

# Build Roadmap — Planning Epic

*Claude Code session sequencing for the [[epic-planning|Planning epic]]. Source: `raw/landplan/docs/build_roadmap.md`.*

---

## Session Tracks

### Track A — Data & Backend Foundations

| Session | Scope |
|---------|-------|
| A1 | Schema & migrations — all new Prisma models and enums from [[architecture]], extend Plan and MapObject, add McpAgent table, seed "Claude Coworker" |
| A2 | Core CRUD routes — Projects, Activities, ActivityDependencies (cycle prevention), Stakeholders, ReferenceEntries, Plan/property mutations |
| A3 | Nominatim integration — boundary-promotion hook, jurisdiction change detection, mark stale ReferenceEntries |
| A4 | Mermaid source generator — `GET /projects/:id/flowchart` returns `flowchart TD` string from dependency records |
| A5 | Email templates — stakeholder invite, activity assignment, contractor quote magic link; token-based opt-in landing endpoint |
| A6 | Quote Packages & DIY Estimates (backend only) — CRUD + magic-link contractor endpoints; no UI yet |
| A7 | Drive folder scaffolding — create project/activity/quote-package folder skeletons on creation |

### Track B — Shared Terra Contour Components

Build **before** consuming in either page to guarantee visual consistency across MapPage and ProjectPage.

| Session | Scope |
|---------|-------|
| B1 | Terra Contour design tokens — Tailwind theme extension (palette, Plus Jakarta Sans, corners, shadow scale) |
| B2 | `GlobalControlBar` — floating top-left; back arrow, Map/Projects pill toggle, save-view, share |
| B3 | `IntegratedSidebar` shell — collapsible, slot-based; LandPlan logo pinned at bottom |
| B4 | `StatusDot` and `ProjectColorSwatch` — no pill component; enforce via doc note or ESLint |
| B5 | `ActivityDetailDrawer` — slide-in from right; works identically from MapPage and ProjectPage |
| B6 | `MermaidFlowchart` — wraps mermaid npm, lazy-loaded via dynamic import; props: `source: string` |
| B7 | `ProjectTimelineSlider` — distinct visual from Sun/Shadow slider; range math per [[epic-planning]] §10.3 |

### Track C — Stitch Pull & Page Assembly

Pull each named design from Stitch MCP in its own session. Wire data after visual layer is in place.

| Session | Scope |
|---------|-------|
| C1 | Pull "Property Overview" → scaffold `ProjectPage.tsx`; Mission section active by default; wire mission statement, metadata, jurisdiction banner, reference info (read-only) |
| C2 | Pull "Project Portfolio Overview" → Portfolio section; drag-to-reorder wired to `PATCH /plans/:planId/projects/reorder`; project cards; "+ New Project" flow |
| C3 | Pull "Project Detail" → project subroute; header, objective, tabs (Activities default, Quote Packages, DIY Estimate, Docs placeholders); activities list + Mermaid side-by-side |
| C4 | Pull "Project Activity Detail Drawer" → wire notes logging, dependency editor, stakeholder assignment, doc attachments; works from both ProjectPage and MapPage |
| C5 | Pull "New Map Interface" → `MapPage.tsx` (Beta) at `/plan/:id/map-beta` under feature flag; integrated sidebar; port existing map canvas and mapping features from `PlanPage.tsx` |
| C6 | Map Projects filter + Project Timeline slider wiring — per-project object dim/desaturate toggle; property boundary always visible |

### Track D — Stakeholders & Agent Identity

| Session | Scope |
|---------|-------|
| D1 | Stakeholder management minimal UI — in-context add/invite dialogs on activity assignment; minimal list in Projects Mode sidebar |
| D2 | Stakeholder opt-in flow — email → landing page → account link or create → redirect to first assigned activity |
| D3 | MCP agent identity surfacing — reference entry badges; activity status changes display actor name/type in notes log |

### Track E — QA & Cutover Prep

| Session | Scope |
|---------|-------|
| E1 | Cycle-prevention edge cases — property-based tests on dependency graph (all four types, complex graphs) |
| E2 | Contractor magic link scoping tests — explicit test that contractor tokens can't reach non-scoped data; live evaluation test for completed-project object reveal |
| E3 | Beta feature flag & internal A/B — flag wiring; internal users flipped to MapPage first |
| E4 | **Phase 2** — Promote MapPage to `/plan/:id`, retire PlanPage, remove Beta flag (not this epic) |

---

## Suggested Ordering

1. **A1, A2** — schema and core CRUD
2. **B1–B4** — design tokens and base components (can run in parallel with A if second session available)
3. **A3, A4, A5** — Nominatim, Mermaid generator, email templates
4. **B5, B6, B7** — drawer, flowchart, timeline slider
5. **C1, C2** — Property Overview + Portfolio Overview
6. **C3, C4** — Project Detail + Activity Drawer
7. **A6, A7** — Quote Packages backend + Drive scaffolding
8. **C5, C6** — New Map Interface Beta + project filter/timeline wiring
9. **D1, D2, D3** — stakeholders and MCP identity
10. **E1, E2, E3** — QA and Beta rollout

---

## GPS Accuracy Epic — Build Sequence

When [[epic-gps-accuracy-templates|GPS Accuracy, Templates & Utilities]] is scheduled:

1. Accuracy schema + migration
2. Accuracy UI (badge, show-accuracy layer)
3. Import dialog accuracy step
4. DIY rental extension
5. Template tables + seed data
6. Template picker UI
7. Utility reference category + seeded entries
8. Help content and onboarding card

---

## Early Flags for Claude Code

- Nominatim hosting decision needed before production deploy
- `mermaid` bundle impact — measure after C3 lands
- Feature-flag mechanism (env var vs. user-level flag service)
- Whether `McpAgent` rows seeded statically or created on first write
- LandPlan logo asset may need a new variant for Terra Contour palette
- All new `MapObject` creations must set `captureMethod` explicitly (no silent API defaults — only migration uses defaults)

---

## Deferred to Phase 2 (Post-Planning Epic)

- Dedicated Contractor Quote Package UI
- Dedicated DIY Estimate editor UI
- Dedicated Stakeholder management screen
- `PlanPage.tsx` → `MapPage.tsx` cutover (E4)
- Mermaid Gantt view, drag-to-connect editing
- Parcel data integration, PAD-US public land detection
- Full audit history UI
- Cross-project dependencies

---

## Related

- [[epic-planning]] — the epic this roadmap implements
- [[architecture]] — data model and API surface
- [[stitch-designs]] — the five UI designs pulled in Track C
