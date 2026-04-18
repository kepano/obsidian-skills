# LandPlan — Planning Epic Build Roadmap

**Version:** v1.0 (Planning epic)
**Companion docs:** `requirements_planning.md`, `architecture.md` (v1.4), `landplan-stitch-prompt-projects.md`

This roadmap sequences Claude Code sessions for the Planning epic. Each session is scoped to roughly one working block. Sessions are ordered so backend foundations land before UI consumes them, shared components land before page-specific work, and the Beta Map Interface stays isolated from production until validated.

---

## Session Track A — Data & Backend Foundations

### A1. Schema & migrations
- Add all new Prisma models and enums from `architecture.md` §2.
- Extend `Plan` (mission, boundary, jurisdiction, parcelSource, apn).
- Extend `MapObject` with `project_id`.
- Add `McpAgent` table and seed "Claude Coworker".
- One consolidated migration.

### A2. Core CRUD routes
- Projects, Activities, ActivityDependencies (with cycle prevention), Stakeholders, ReferenceEntries.
- Plan/property mutation routes (mission, boundary promotion, jurisdiction re-check).
- Zod/shared-type validation, JWT auth, role-based authorization.

### A3. Nominatim integration
- Boundary-promotion hook calls Nominatim with boundary centroid.
- Jurisdiction change detection; mark affected ReferenceEntries as `stale`.
- Dev uses public Nominatim; production hosting decision deferred to Open Items.

### A4. Mermaid source generator
- `GET /projects/:id/flowchart` returns Mermaid `flowchart TD` source string from structured dependencies.
- Handles all four dependency types (FS/SS/FF/SF) as labeled edges.

### A5. Email templates & stakeholder opt-in
- Extend SendGrid/Resend integration with three new templates (stakeholder invite, activity assignment, contractor quote link).
- Token-based opt-in landing endpoint.

### A6. Quote Packages & DIY Estimates (backend only)
- Full CRUD + magic-link contractor endpoints.
- Contractor visibility rules enforced server-side per `architecture.md` §6.2.
- No UI in this session — backend scaffolding for future Stitch pass.

### A7. Drive folder scaffolding
- On project creation, create `LandPlan_Files/{plan}/Projects/{project}/` and `.../Activities/` skeleton.
- Quote package folders on creation.

---

## Session Track B — Shared Terra Contour Components

Build these **before** consuming them in either page. Landing this library early guarantees visual consistency across `MapPage` and `ProjectPage`.

### B1. Terra Contour design tokens
- Tailwind theme extension: palette, Plus Jakarta Sans, rounded corners, shadow scale.
- Pull from the Stitch "New Map Interface" design for exact color values.

### B2. `GlobalControlBar`
- Floating top-left: back arrow, Map/Projects pill toggle, save-view, share.
- Consumes a `mode: 'map' | 'projects'` prop; toggle navigates to the other page.

### B3. `IntegratedSidebar` shell
- Collapsible, slot-based. LandPlan logo pinned at bottom.
- Projects mode and Map mode each pass their own section list.

### B4. `StatusDot` and `ProjectColorSwatch`
- `StatusDot` accepts the shared Status enum, renders color dot + text label.
- No pill component exists; enforce via ESLint rule or doc note.

### B5. `ActivityDetailDrawer`
- Slide-in from right. Renders identically whether mounted under `MapPage` or `ProjectPage`.
- Shows activity title, status, duration, assignment, notes log, linked map objects, dependencies, docs, context-aware "Open in Map" action.

### B6. `MermaidFlowchart`
- Wraps `mermaid` npm, lazy-loaded via dynamic import.
- Props: `source: string`. Renders to SVG.

### B7. `ProjectTimelineSlider`
- Distinct visual treatment from the existing Sun/Shadow slider.
- Range math per `requirements_planning.md` §10.3 (left = min project start, right = max(project end, activity completion), default = today).

---

## Session Track C — Stitch Pull & Page Assembly

Pull each named design from Stitch MCP in its own session. Wire data after the visual layer is in place.

### C1. Pull and scaffold "Property Overview" → `ProjectPage.tsx`
- Stitch MCP pull: "Property Overview".
- Scaffold `ProjectPage.tsx` greenfield, Mission section active by default.
- Wire mission statement (markdown editor), property metadata, jurisdiction stale-flag banner, reference info subsections (read-only first pass).

### C2. Pull and scaffold "Project Portfolio Overview" → `ProjectPage.tsx` Projects section
- Stitch MCP pull: "Project Portfolio Overview".
- Drag-to-reorder ranked stack wired to `PATCH /plans/:planId/projects/reorder`.
- Project cards wired to project data.
- "+ New Project" flow.

### C3. Pull and scaffold "Project Detail" → `ProjectPage.tsx` project subroute
- Stitch MCP pull: "Project Detail".
- Header, objective block, tabs (Activities default, Quote Packages, DIY Estimate, Docs placeholders).
- Activities list + Mermaid flowchart side-by-side wired to the `/projects/:id/flowchart` endpoint.

### C4. Pull and wire "Project Activity Detail Drawer"
- Stitch MCP pull: "Project Activity Detail Drawer".
- Consume the drawer from both `ProjectPage` (Project Detail activity list) and `MapPage` (map object tap).
- Wire notes logging, dependency editor dropdown, stakeholder assignment, doc attachments.

### C5. Pull and scaffold "New Map Interface" → `MapPage.tsx` (Beta)
- Stitch MCP pull: "New Map Interface".
- New page at `/plan/:id/map-beta` under feature flag.
- Integrated sidebar with Map mode sections (Layers, Saved Views, Structures, Plants, Projects filter, Time).
- Port existing map canvas and mapping features from `PlanPage.tsx` (functional parity, not new features).
- Floating tools palette on **left-center**. Edit modals on **right-center**. No Terrain Analysis panel.

### C6. Map Projects filter + Project Timeline slider wiring
- Projects section in Map sidebar toggles per-project object visibility (dim/desaturate unchecked).
- Project Timeline slider reveals objects progressively by activity completion date.
- Property boundary always visible regardless of filters.

---

## Session Track D — Stakeholders & Agent Identity

### D1. Stakeholder management minimal UI
- No dedicated full screen in this epic (deferred to Phase 2).
- In-context add/invite dialogs on activity assignment fields and a minimal list within the Projects Mode sidebar "Stakeholders" section.

### D2. Stakeholder opt-in flow
- Email → landing page → account link or create → redirect into plan at their first assigned activity.

### D3. MCP agent identity surfacing
- Reference entry badges ("added by Claude Coworker").
- Activity status changes display actor name and type in the notes log.

---

## Session Track E — QA, Cutover Prep

### E1. Cycle-prevention edge cases
- Property-based tests on the dependency graph (four dependency types, complex graphs).

### E2. Contractor magic link scoping tests
- Explicit test that contractor tokens cannot reach non-scoped data.
- Live evaluation test for completed-project object reveal.

### E3. Beta feature flag & internal A/B
- Flag wiring.
- Internal users flipped to `MapPage.tsx` first; feedback loop before broader exposure.

### E4. Cutover (Phase 2 — not this epic)
- After Beta validation: promote `MapPage.tsx` to `/plan/:id`, retire `PlanPage.tsx`, remove the Beta flag.

---

## Suggested Session Ordering

1. **A1, A2** — schema and core CRUD.
2. **B1–B4** — design tokens and base components (in parallel with A if a second session is available).
3. **A3, A4, A5** — Nominatim, Mermaid generator, email templates.
4. **B5, B6, B7** — drawer, flowchart, timeline slider.
5. **C1, C2** — Property Overview + Portfolio Overview.
6. **C3, C4** — Project Detail + Activity Drawer.
7. **A6, A7** — Quote Packages backend + Drive scaffolding.
8. **C5, C6** — New Map Interface Beta + project filter/timeline wiring.
9. **D1, D2, D3** — stakeholders and MCP identity.
10. **E1, E2, E3** — QA and Beta rollout.

Cutover (E4) deferred to Phase 2.

---

## Explicitly Deferred to Phase 2

- Dedicated Contractor Quote Package UI (future Stitch pass).
- Dedicated DIY Estimate editor UI.
- Dedicated Stakeholder management screen.
- `PlanPage.tsx` → `MapPage.tsx` cutover.
- Mermaid Gantt view, drag-to-connect editing.
- Parcel data integration, PAD-US public land detection.
- Full audit history UI.
- Cross-project dependencies.

---

## Open Items Claude Code Should Flag Early

- Nominatim hosting decision before production deploy.
- `mermaid` bundle impact — measure after C3 lands.
- Exact feature-flag mechanism (env var vs. user-level flag service).
- Whether the LandPlan logo asset in the sidebar footer needs a new variant for the Terra Contour palette.
