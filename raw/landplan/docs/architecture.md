# LandPlan — Architecture Notes for the Planning Epic

**Version:** v1.4 delta (applied on top of existing `architecture.md`)
**Companion docs:** `requirements_planning.md`, `landplan-stitch-prompt-projects.md`, `build_roadmap.md`

This document describes architectural additions and changes introduced by the Planning epic. It does not restate the baseline architecture — it augments it.

---

## 1. Monorepo Impact

No new packages. Work lands in existing packages:

- **`shared`** — new TypeScript types for Project, Activity, Dependency, Stakeholder, QuotePackage, QuoteInvite, ReferenceEntry, Jurisdiction, DIYEstimate. Status enum added. Role enums extended with `stakeholder` and `contractor_quote`.
- **`api-client`** — new endpoints listed in §3.
- **`api`** — Fastify route modules, Prisma migrations, Nominatim integration, transactional email templates.
- **`web`** — new `ProjectPage.tsx`, new `MapPage.tsx` (Beta), shared Terra Contour component library.
- **`mobile`** — no changes in this epic.

---

## 2. Data Model — Prisma Additions

Database: **Cloud SQL for PostgreSQL 15 with PostGIS**.

### 2.1 Plan (extended)
New columns on existing `Plan` table:
- `mission_statement` (text, markdown, nullable)
- `boundary_object_id` (FK → MapObject, nullable, unique)
- `jurisdiction` (jsonb: `{ country, state, county, city, village, other }`)
- `parcel_source` (enum, reserved: `regrid | county_gis | user | null`)
- `apn` (text, nullable)

### 2.2 New tables
- **`Project`** — `id, plan_id, title, objective, sequence (int), status (enum), planned_start_date, estimated_duration_days, planned_end_date, budget_low_usd, budget_high_usd, rough_actual_cost_usd, project_color, created_at, updated_at`
- **`Activity`** — `id, project_id, title, details, status (enum), duration_days, planned_start_date, planned_end_date, completion_date, sort_order (int), created_at, updated_at`
- **`ActivityDependency`** — `id, predecessor_activity_id, successor_activity_id, type (enum: FS | SS | FF | SF)`. Scoped within a single project. Cycle prevention enforced in the API layer.
- **`ActivityAssignment`** — `activity_id, stakeholder_id` (join table, many-to-many).
- **`ActivityMapObjectRef`** — `activity_id, map_object_id` (join table, soft reference; orphans preserved if map object is deleted).
- **`ActivityNote`** — `id, activity_id, author_actor_id, author_actor_type, body, created_at` (append-only log).
- **`Stakeholder`** — `id, plan_id, name, email, role_label, linked_user_id (nullable), opted_in (bool), notifications_enabled (bool)`.
- **`ReferenceEntry`** — `id, plan_id, category (enum: zoning | rainwater | off_grid | permitting | public_land), title, jurisdiction_level (enum), notes, links (jsonb array), attached_doc_ids (jsonb array), source (enum: user | system | agent), agent_name (nullable), source_timestamp, status (enum: active | stale | archived), created_at, updated_at`.
- **`QuotePackage`** — `id, project_id, name, included_activity_ids (jsonb array of activity ids within project), attached_doc_ids, created_by, created_at`.
- **`ContractorInvite`** — `id, package_id, contractor_name, contractor_email, magic_link_token, expires_at, status (enum), submitted_quote_id (nullable)`.
- **`ContractorQuote`** — `id, invite_id, overall_cost_usd, quote_expires_at (nullable), proposed_earliest_start_date (nullable), overall_notes, attached_doc_id (nullable), submitted_at`.
- **`ContractorQuoteLineItem`** — `id, quote_id, activity_id, amount_usd, notes`.
- **`DIYEstimate`** — `id, project_id, name, included_activity_ids (jsonb), materials (jsonb array), labor_hours, labor_rate_usd, tool_rentals (jsonb array), notes, computed_total_usd (generated column), created_at, updated_at`.

### 2.3 Status enum (shared across Project and Activity)
`planned | in_progress | blocked | on_hold | complete | cancelled`.

### 2.4 MapObject (extended)
- Add `project_id` column (nullable FK → Project) for the object-level project association used by Map mode filtering and the Project Timeline slider.

### 2.5 Actor model (for MCP identity)
Writes that update status or add reference entries capture `actor_type` and `actor_id`:
- `actor_type ∈ { user | mcp_agent }`
- `actor_id` references the user table for humans, or a new lightweight `McpAgent` table (`id, name, created_at`) for agent identities. First-class entry: "Claude Coworker".

Full audit history (§14 of requirements, deferred) will later roll up from these actor fields. For now they are captured on current rows so the history is complete once the audit feature ships.

---

## 3. API Surface

All routes under the existing Fastify server, JWT-authenticated via Firebase Auth unless noted.

### 3.1 Property / Plan
- `PATCH /plans/:planId/property` — update mission, APN, jurisdiction override
- `POST /plans/:planId/boundary` — promote a map object to boundary; triggers Nominatim re-check
- `GET /plans/:planId/jurisdiction-check` — returns whether the jurisdiction changed since last confirmation, plus the list of stale reference entries

### 3.2 Reference entries
- `GET /plans/:planId/references?category=...`
- `POST /plans/:planId/references`
- `PATCH /references/:id`
- `DELETE /references/:id`

### 3.3 Projects / Activities
- `GET /plans/:planId/projects`
- `POST /plans/:planId/projects`
- `PATCH /projects/:id`
- `PATCH /plans/:planId/projects/reorder` — bulk sequence update
- `GET /projects/:id/activities`
- `POST /projects/:id/activities`
- `PATCH /activities/:id`
- `POST /activities/:id/notes`
- `POST /activities/:id/dependencies` — API validates acyclicity before write
- `DELETE /activities/:id/dependencies/:depId`
- `PATCH /projects/:id/activities/reorder` — manual sort order
- `PATCH /map-objects/:id/project-link` — set or clear project association

### 3.4 Stakeholders
- `GET /plans/:planId/stakeholders`
- `POST /plans/:planId/stakeholders` — placeholder or invite-and-send
- `POST /stakeholders/:id/invite` — (re)send opt-in email
- `POST /auth/stakeholder-optin` — token-based opt-in landing

### 3.5 Quote Packages (backend scaffolding only in this epic)
- `POST /projects/:id/quote-packages`
- `POST /quote-packages/:id/invites`
- `GET /contractor/:token` — magic-link landing (no JWT, token-scoped)
- `POST /contractor/:token/quote` — submit quote with line items

### 3.6 DIY Estimates (backend scaffolding only)
- `POST /projects/:id/diy-estimates`
- `PATCH /diy-estimates/:id`

### 3.7 Mermaid flowchart
Generated server-side on demand from the activity + dependency records, returned as a Mermaid string the web client renders with the `mermaid` npm package.
- `GET /projects/:id/flowchart` — returns `{ mermaidSource: "flowchart TD\n..." }`

### 3.8 Nominatim integration
- Server-side call from the boundary-promotion route using the boundary centroid as the lookup point.
- Development: public Nominatim at 1 req/sec.
- Production: self-hosted Nominatim on Google Cloud or a paid mirror (decision tracked in the Open Items).

### 3.9 Transactional email
Reuses the SendGrid/Resend pipeline introduced in the Plan Sharing epic. New templates:
- Stakeholder opt-in invitation
- Activity assignment notification
- Contractor quote magic link

---

## 4. Frontend — Web

### 4.1 New pages and routes
- **`MapPage.tsx` (Beta)** at route `/plan/:id/map-beta` — the New Map Interface. Built as an independent page; existing `PlanPage.tsx` remains at `/plan/:id` during the Beta period.
- **`ProjectPage.tsx`** at route `/plan/:id/projects` with subroutes:
  - `/plan/:id/projects` — Property Overview (Mission section default) and Project Portfolio Overview sections
  - `/plan/:id/projects/:projectId` — Project Detail
- Global Map/Projects pill toggle navigates between `/plan/:id/map-beta` and `/plan/:id/projects`.

### 4.2 Shared Terra Contour components
Extracted to a new directory (e.g., `web/src/components/terra/`):
- `GlobalControlBar` (floating top-left, back + toggle + save-view + share)
- `IntegratedSidebar` (collapsible shell with slotted sections, logo footer)
- `StatusDot` (replaces status pills everywhere — consumers pass status enum)
- `ProjectColorSwatch`
- `ActivityDetailDrawer` (slide-in from right, used by both `MapPage` and `ProjectPage`)
- `MermaidFlowchart` (wraps the `mermaid` npm package; lazy-loaded)
- `ProjectTimelineSlider` (separate from existing Sun/Shadow slider)

Both pages compose these components; Claude Code should build the shared library first.

### 4.3 State management
Zustand stores added:
- `projectStore` — ranked project stack, current project detail, activities, dependencies
- `stakeholderStore`
- `referenceStore`
- `mapProjectFilterStore` — visibility toggles per project, project timeline slider position

### 4.4 Mermaid rendering
- Package: `mermaid` (npm).
- Dynamic import to avoid bundling into initial load (~500KB).
- Source string generated by the API; client only renders.

### 4.5 Map page — Beta isolation
- Feature flag (env-driven or user-level) to expose `/plan/:id/map-beta`.
- Old `PlanPage.tsx` untouched. After A/B validation, `MapPage.tsx` promotes to `/plan/:id`, `PlanPage.tsx` is removed, the Beta route retired. Cutover is Phase 2.

---

## 5. Google Drive Layout

Structure lands under the plan's existing `LandPlan_Files/{plan}/` folder, inheriting Plan Sharing permissions end-to-end:

```
LandPlan_Files/{plan}/
├── Property/
│   ├── Ordinances/
│   └── Boundary/
├── Projects/
│   └── {project}/
│       ├── <project-level docs>
│       └── Activities/
│           └── {activity}/
│               └── <activity-level docs>
└── QuotePackages/
    └── {package}/
```

Contributor uploads continue to use the plan owner's Drive tokens server-side, per the Sharing epic.

---

## 6. Security & Access Control

### 6.1 Role enum (extended)
`owner | contributor | viewer | stakeholder | contractor_quote`

### 6.2 Authorization rules (new)
- **Stakeholder:** plan-wide read. Write only on `Activity.status` and `ActivityNote` for activities in their `ActivityAssignment` set. A contributor-then-stakeholder retains contributor powers (role is additive, not downgrading).
- **Contractor (quote):** token-scoped, not session-scoped. Access enforced in the route handler by resolving the magic link token to a `ContractorInvite` and a derived visibility set:
  - Activities in the invite's quote package
  - Map objects linked to the project
  - Map objects not linked to any project
  - Map objects linked to projects with `status = 'complete'` (evaluated live)
  - The property boundary
  - Nothing else. No broader plan data leaks through this token.
- Token expiration: default 30 days from send; configurable at invite creation.

### 6.3 Cycle prevention
Dependency writes reject on detected cycles with a clear error payload consumable by the UI.

---

## 7. Known Coordinate Gotcha Reminder

lng/lat vs lat/lng remains flagged project-wide. All new geo logic — boundary centroid computation for Nominatim, map-object project-link operations, timeline reveal geometry — must conform to the existing convention documented in the root `CLAUDE.md`. Nominatim returns lat/lng in its response; convert to internal convention at the API boundary.

---

## 8. Open Architectural Decisions

Tracked here, to be resolved during build:
- Nominatim hosting model for production (self-host on GKE vs. paid mirror).
- Mermaid dynamic import chunking strategy under Vite.
- Magic link token format, signing key rotation on revoke.
- Whether `McpAgent` rows are seeded statically or created on first write.
- Cutover mechanics: feature-flag flip vs. route swap for retiring `PlanPage.tsx`.
