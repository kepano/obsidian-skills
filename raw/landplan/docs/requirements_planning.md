# LandPlan — Planning Epic Requirements

**Status:** Draft v1.1
**Scope:** Adds the Planning half of LandPlan: Property model, Projects, Activities, Stakeholders, Contractor Quote Packages, DIY Estimates, map-integrated project timeline, and a Terra Contour visual refresh that introduces a new Projects mode alongside a Beta rebuild of the Map page.

**Companion documents:**
- `landplan-stitch-prompt-projects.md` — Google Stitch prompt covering the five named designs pulled into Claude Code via Stitch MCP.
- `architecture.md` (v1.4+) — data model, API surface, frontend structure.
- `build_roadmap.md` — sequenced session plan for Claude Code.

---

## 1. Overview

LandPlan has matured as a mapping tool. This epic introduces the Planning side: property-level vision and reference info, a sequenced stack of projects, activities with dependencies, stakeholder collaboration, and contractor quoting. A new time slider on the map reveals objects as projects progress, giving owners a visual forecast of their land over time.

**Guiding principles:**
- One property per plan.
- Non-destructive by default (boundary changes preserve history, soft map references).
- Trust is earned: contractors see only what they need, stakeholders are read-only until elevated.
- Forward-compatible schemas (parcel sources, MCP agents, audit history can layer in later).

---

## 2. Property Model

### 2.1 Property ↔ Plan relationship
- **One property per plan, 1:1.**
- Data model approach: keep `Plan` as the top-level entity. Add property fields directly to `Plan` (or a 1:1 `Property` sub-record) rather than renaming. Specifically, Plan gains:
  - `boundaryObjectId` (FK to a map object)
  - `jurisdiction` (JSON: country, state, county, city, village, other)
  - `parcelSource` (nullable enum, reserved for future: `regrid | county_gis | user | null`)
  - `apn` (nullable string, manual entry in v1)
  - `missionStatement` (markdown, the owner's vision for the property)

### 2.2 Property boundary
- User is instructed to draw a closed polyline around their property using the existing distance polyline tool and save it as a map object.
- User can then **promote** any saved closed polyline to "Property Boundary" via an action on the map object.
- Only one confirmed boundary per plan at a time.
- Re-promoting a different object replaces the boundary; the old object reverts to a normal map object.
- The property boundary is a special always-visible object (see §9, §10).

### 2.3 Jurisdiction auto-lookup
- On boundary confirmation (and on any subsequent boundary change), the app performs a reverse-geocode lookup using **Nominatim (OSM)** as the default service.
- Lookup populates: country, state, county, city, village/hamlet where available.
- **Re-check behavior:** If the jurisdiction changes after a boundary update, all existing reference info (§3) is preserved. Entries tied to the old jurisdiction are flagged with a **stale** badge and surfaced in a "Review jurisdiction changes" prompt. User decides what to keep, edit, or archive. No automatic deletion.
- Rate limit note: public Nominatim is 1 req/sec. Production deployment should target a self-hosted or paid mirror; Mapbox Geocoding is a reserved fallback.

### 2.4 Parcel data
- v1: manual APN entry only. `parcelSource` field reserved in schema for future integration (Regrid, county GIS, etc.) without migration.

---

## 3. Property Reference Information

Structured reference categories hang off the Property (Plan). Each category holds zero or more reference entries.

### 3.1 Categories (fixed set in v1)
1. Zoning
2. Rainwater Management
3. Off-Grid Rules & Restrictions
4. Permitting
5. Public Land (BLM, USACE, state/national forest, etc.)

### 3.2 Reference entry schema
Each entry has:
- `id`
- `category` (enum, one of the five above)
- `title`
- `jurisdictionLevel` (enum: `federal | state | county | city | village | other`)
- `notes` (markdown)
- `links` (array of `{ url, label }`)
- `attachedDocs` (array of Drive file IDs)
- `source` (enum: `user | system | agent`)
- `agentName` (nullable string, e.g., "Claude Coworker via LandPlan MCP")
- `sourceTimestamp`
- `status` (enum: `active | stale | archived`)
- `createdAt`, `updatedAt`

### 3.3 Sources
- **User:** manually entered.
- **System:** populated by LandPlan itself (e.g., jurisdiction-suggested entries — deferred to a later phase).
- **Agent:** added by an MCP agent such as Claude Coworker. Agent identity recorded in `agentName`.

### 3.4 Public land proximity
- v1: manual reference entries only (user or MCP agent adds links to BLM/USACE/public land docs).
- Automatic proximity detection via PAD-US deferred.

---

## 4. Drive Folder Structure

All planning artifacts store in the plan's existing `LandPlan_Files/{plan}/` folder, inheriting Plan Sharing permissions end-to-end. Structure is kept as flat as practical:

```
LandPlan_Files/{plan}/
├── Property/
│   ├── Ordinances/           # reference entry attachments, any category
│   └── Boundary/             # exported boundary files, legal docs
├── Projects/
│   └── {project}/
│       ├── <project-level docs>
│       └── Activities/
│           └── {activity}/
│               └── <activity-level docs>
└── QuotePackages/
    └── {package}/            # generated quote request docs, received quotes
```

Contributor uploads continue to use the plan owner's Drive tokens server-side, per the Sharing epic.

---

## 5. Projects

### 5.1 Project schema
- `id`
- `planId`
- `title`
- `objective` (markdown)
- `sequence` (integer, drag-to-reorder; the sole ordering axis in v1 — priority is deliberately excluded because it changes too often)
- `status` (enum, see §5.2)
- `plannedStartDate` (nullable date)
- `estimatedDurationDays` (nullable integer)
- `plannedEndDate` (nullable date; computed from start + duration, editable)
- `budgetLowUsd`, `budgetHighUsd` (ROM range)
- `roughActualCostUsd` (nullable)
- `attachedDocs` (Drive file IDs at `Projects/{project}/`)
- `createdAt`, `updatedAt`

### 5.2 Status enum (shared with activities)
`planned | in_progress | blocked | on_hold | complete | cancelled`

- Set manually by owners and contributors.
- May also be updated by MCP agents (see §11).
- **Project completion is NOT auto-set.** When all activities in a project reach `complete`, the UI surfaces a suggestion badge: *"All activities complete — mark project complete?"* The owner/contributor must confirm. This avoids surprising auto-transitions.

### 5.3 Sequencing
- Projects are ordered in a single ranked stack per plan.
- Drag up/down to re-sequence.
- Scheduling is informational in v1 — changing sequence does not reschedule dates.

---

## 6. Activities

### 6.1 Activity schema
- `id`
- `projectId`
- `title`
- `details` (markdown, optional)
- `status` (same enum as projects)
- `durationDays` (nullable integer; if null, activity is treated as a zero-duration milestone)
- `plannedStartDate`, `plannedEndDate` (nullable; informational)
- `completionDate` (nullable; drives the time slider)
- `sortOrder` (integer, manual within-project ordering, independent of dependencies)
- `assignedStakeholderIds` (array)
- `mapObjectRefs` (array of soft references to map objects; see §6.4)
- `attachedDocs` (Drive file IDs at `Projects/{project}/Activities/{activity}/`)
- `createdAt`, `updatedAt`

### 6.2 Dependencies
- Dependencies are **scoped within a single project** (no cross-project dependencies in v1).
- Four dependency types supported: **FS, SS, FF, SF** (finish-to-start, start-to-start, finish-to-finish, start-to-finish).
- Dependency record: `{ predecessorActivityId, successorActivityId, type }`.
- **Cycle prevention:** API validates on save and rejects any dependency creating a cycle with a clear error message.

### 6.3 Activity diagram (Mermaid)
- Dependencies are stored as structured records in the database.
- The web app renders them as a Mermaid `flowchart` by generating Mermaid syntax on the fly from the structured data.
- Editing happens in a form UI (add activity, pick predecessors + dependency type from a dropdown). Users do not hand-edit Mermaid.
- Library: `mermaid` npm package, rendering to SVG inline.
- A Gantt view and drag-to-connect editing are deferred to Phase 2.

### 6.4 Activity ↔ map object references
- Many-to-many. One activity may reference many map objects; one map object may be referenced by many activities.
- **Soft references:** If a referenced map object is deleted, the link is preserved as "orphaned" with a warning in the activity UI. No silent data loss.

---

## 7. Stakeholders

### 7.1 Model
Stakeholders are a **superset** that includes both LandPlan users and non-users (spouse, neighbor, contact-only contractors, etc.).

Stakeholder record:
- `id`
- `planId`
- `name`
- `email`
- `roleLabel` (freeform: "Spouse", "Electrician", "County inspector", etc.)
- `linkedUserId` (nullable — set if the stakeholder opts in and/or has a LandPlan account)
- `optedIn` (boolean)
- `notificationsEnabled` (boolean, default true on opt-in)

### 7.2 Access scope
- **Default:** Stakeholders invited to a plan get **read-only access to the whole plan** (Viewer equivalent), plus **write access to status and notes on activities assigned to them**.
- **If a stakeholder is already a Contributor on the plan**, they retain Contributor powers — the stakeholder role does not downgrade them.
- Schema role identifier: `stakeholder`. UI label: "Stakeholder".
- Effectively: `stakeholder` = Viewer + activity-write on assigned items.

### 7.3 Opt-in flow
- Stakeholders can be added as placeholder contacts (name + email) without invitation.
- When invited, they receive a transactional email (reusing SendGrid/Resend from the Sharing epic) with an opt-in link.
- On opt-in, they create or link a LandPlan account and can begin updating status/notes on assigned activities.
- Assignment notifications are sent by email on assignment; opt-out per stakeholder.
- Pending invites auto-apply on registration (matches Sharing epic pattern).

### 7.4 Stakeholder notes and status
- On any activity assigned to a stakeholder, they may:
  - Update `status`
  - Add notes (append-only log tied to their identity)
- They cannot edit activity titles, dependencies, map references, or any other field.

---

## 8. Contractor Quote Packages

### 8.1 Concept
A Quote Package is a named bundle of activities within a single project, sent to one or more contractors for bidding. Contractors get a time-limited magic link — no account required — and see only what they need to quote.

### 8.2 Quote Package schema
- `id`
- `projectId`
- `name` (e.g., "Septic install — first round")
- `includedActivityIds` (array; all within the same project)
- `attachedDocs` (Drive file IDs at `QuotePackages/{package}/`)
- `createdBy`, `createdAt`
- `contractorInvites` (array, see §8.3)

### 8.3 Contractor invite
- `id`
- `packageId`
- `contractorName`
- `contractorEmail`
- `magicLinkToken` (opaque, single-tenant)
- `expiresAt` (default: 30 days from send)
- `status` (enum: `sent | viewed | quote_submitted | expired | revoked`)

The same package can be sent to multiple contractors in parallel for comparative quoting.

### 8.4 Contractor access scope
Schema role identifier: `contractor_quote`. UI label: "Contractor (Quote)".

While the magic link is valid, a contractor can see:
- The project objective, title, and status
- The activities included in their specific quote package
- Map objects linked to the project
- **Map objects not linked to any project** (unlinked objects — existing site context)
- **Map objects linked to projects with status `complete`** (existing installed features)
- **The property boundary** (always visible to contractors — essential spatial context)
- Docs attached to their quote package

A contractor **cannot** see:
- The property mission statement
- Reference information (zoning, permitting, etc.)
- Other projects or their activities
- Other stakeholders
- Other quote packages
- The broader plan

**Live evaluation:** Completed-project visibility is evaluated live. If a project transitions to `complete` while a contractor's link is active, its linked objects become visible to the contractor mid-session.

Contractors **do not** automatically gain any further plan visibility after submitting a quote. They must be explicitly shared the Viewer role by the owner to see more. Trust is earned.

### 8.5 Quote submission
Contractors can submit exactly one quote per invite. The submission form captures:
- **Overall cost** (required, USD)
- **Quote expiration date** (optional)
- **Proposed earliest start date** (optional)
- **Per-activity line items**, for each activity the contractor chooses to quote on:
  - Amount (USD)
  - Notes (freeform)
- **Optional attached document** (PDF, image, etc., stored in the package's Drive folder)
- Free-text overall notes

Submitted quotes are visible to the plan owner and contributors in the Quote Package view, side-by-side when multiple contractors have responded.

---

## 9. DIY Estimate

A project (or an activity set within a project) may also have a DIY Estimate — structured, not freeform.

### 9.1 Schema
- `id`
- `projectId`
- `name`
- `includedActivityIds` (array)
- `materials` (array of `{ name, quantity, unit, unitCostUsd }`)
- `laborHours` (number)
- `laborRateUsd` (number, optional)
- `toolRentals` (array of `{ name, costUsd }`)
- `notes` (markdown)
- `computedTotalUsd` (derived)

Totals roll up automatically from materials + labor + rentals.

---

## 10. Map Integration

### 10.1 Project linkage on map objects
- Every map object gains an optional `projectId` field (single project, nullable).
- Map object properties panel includes a "Project" dropdown to select or clear the association.
- Objects not linked to any project behave as "always visible" in the project time slider.

### 10.2 Project filter panel
- A side panel lists all projects as checkboxes (multi-select), plus a special **"Unassigned"** toggle.
- Unchecked projects' objects are **dimmed/desaturated** on the map, not hidden — users keep spatial context.
- Linked objects display a small **project-colored badge or dot** for identification.
- The property boundary is always visible regardless of filter state.

### 10.3 Project time slider
A new time slider lives in the existing map time panel, **separate** from the sun/shadow time slider (they operate at different scales — hours-of-day vs. months-to-years).

**Range math:**
- **Left edge:** `min(project.plannedStartDate)` across all projects with dates set.
- **Right edge:** `max( max(project.plannedEndDate), max(activity.completionDate) )` across all projects/activities with dates set. This ensures the slider doesn't clip when activities run past their project's planned end.
- **Default position:** today's date.
- **Projects or activities without dates:** excluded from range calculation. Their linked map objects are treated as "always visible" (same as unlinked objects) until dates are assigned.

**Reveal logic:**
- Objects linked to an activity are revealed at that **activity's** completion date (not the project's).
- If an object is linked to multiple activities, it appears at the **earliest** activity completion date among them — the thing exists once installed; later activities merely modify it.
- Objects linked to activities with status `complete` are visible at the slider position `now` and later.
- Objects linked to `cancelled` activities are never revealed by the slider.
- Objects with no project/activity linkage, or linked to projects/activities without dates, are always visible.

---

## 11. MCP Agent Identity

MCP agents (e.g., Claude Coworker via LandPlan MCP) may:
- Add reference entries (sourced as `agent`, with `agentName` recorded).
- Update project and activity status.
- Potentially more, as the MCP surface grows.

**Identity:** Each MCP agent acts as its own first-class actor in the system, not as the plan owner. Its identity appears in any surface that shows "who did this" — activity status changes, reference entry provenance, etc. This preserves traceability and keeps humans and agents distinguishable.

Full audit history is deferred (§14), but agent identity on writes is required from day one so the history will be complete when it arrives.

---

## 12. Roles Summary

Consolidated role table across the Sharing and Planning epics:

| Role | Scope | Read | Write |
|---|---|---|---|
| `owner` | Plan | Everything | Everything |
| `contributor` | Plan | Everything | Everything except ownership transfer |
| `viewer` | Plan | Everything | Nothing (interactive measurement only, no save) |
| `stakeholder` | Plan | Everything | Status + notes on activities assigned to them |
| `contractor_quote` | Quote Package | Scoped subset (§8.4) | Their own quote submission only |

A `contributor` who is also added as a stakeholder retains contributor powers.

---

## 13. UI/UX — Terra Contour Design System

This epic ships with a full visual refresh under the **Terra Contour** design system ("The Digital Cartographer"). The refresh introduces a new **Projects mode** as the home for all planning features, alongside a **Beta rebuild of the Map page** that keeps the existing mapping functionality but delivers a dramatically cleaner menu structure integrated with the new project data.

### 13.1 Design system summary
- **Palette:** Forest green accent `#89B838`, deep teal/slate for branding, warm neutral backgrounds (sand, stone, warm gray).
- **Typography:** Plus Jakarta Sans throughout.
- **Surfaces:** Subtle shadows, generous rounded corners, warm neutral fills.
- **Icons:** Line-style, slightly rounded, consistent weight.
- **Hover states:** Interactive elements transition to forest green.
- **Status indicators:** Small inline color dots + text labels — **no standalone status pills** anywhere in the system.
- **Full spec:** see `landplan-stitch-prompt-projects.md`.

### 13.2 Unified navigation — Map mode ↔ Projects mode
A plan has two coordinated views: **Map mode** (spatial) and **Projects mode** (planning). Backend-wise they are separate pages to contain complexity; to the user they are two views of the same plan.

- **Floating Global Control Bar (top-left, both modes):** back arrow, prominent Map/Projects pill toggle, save-view (camera icon), share. Always in the same position.
- **Integrated collapsible left sidebar (both modes, shared visual treatment, different contents):**
  - **Projects mode sections:** Mission, Projects, Stakeholders, Reference Info, Docs.
  - **Map mode sections:** Layers, Saved Views, Structures, Plants, Projects (object filter — see §10), Time (Sun/Shadow + Project Timeline sliders).
- **LandPlan logo** pinned at the bottom of the sidebar in both modes.
- **Footer:** standard dark blue LandPlan footer with *"© 2026 Smart Farm Technologies. Surveying the Future."* on Projects mode pages only. No footer on the New Map Interface (logo-in-sidebar only, to preserve canvas space).

### 13.3 Mode-specific floating element rules
- **Projects mode:** traditional document feel. Left sidebar is the primary organizer. **No persistent floating panels on the right side.** Secondary content uses slide-in drawers from the right edge (the Project Activity Detail Drawer) or inline sections.
- **Map mode:** spatial complexity requires floating elements:
  - **Floating tools palette on the LEFT-CENTER:** Select, Object, Distance, Area, Import, Photo.
  - **Tool windows and edit modals on the RIGHT-CENTER:** Measure Area, Edit Tree Stand, Edit Tree Properties, and equivalent spatial editing UI.
  - **No Terrain Analysis panel** — explicitly excluded.

### 13.4 Named designs (Stitch MCP)
Claude Code will pull five named designs from Stitch MCP over a series of build sessions. Each maps to specific requirements sections above:

| Design name | Requirements coverage | Target code |
|---|---|---|
| **New Map Interface** | §10 (map filter, project timeline slider), map mode sidebar shell | `MapPage.tsx` (Beta) |
| **Property Overview** | §2 (property model), §3 (reference info), mission statement | `ProjectPage.tsx` — Mission section |
| **Project Portfolio Overview** | §5 (projects, sequencing, ranked stack) | `ProjectPage.tsx` — Projects section |
| **Project Detail** | §5 (project fields), §6 (activities, Mermaid flowchart), tab for Quote Packages (§8), DIY Estimate (§9), Docs | `ProjectPage.tsx` — project subroute |
| **Project Activity Detail Drawer** | §6 (activities), §7 (stakeholder notes/status), cross-mode drawer | Shared component |

### 13.5 Beta rollout for the New Map Interface
The refreshed Map page ships as an **independent Beta view** alongside the existing map page so it can be A/B tested before replacing the current implementation.

- New file: `MapPage.tsx` (Beta). Current `PlanPage.tsx` stays intact during the Beta period.
- Feature flag or route-level toggle (e.g., `/plan/:id/map-beta`) controls access.
- Shared visual components (sidebar shell, Global Control Bar, Activity Detail Drawer) are factored for reuse by the Projects mode (`ProjectPage.tsx`, greenfield) from day one so visual continuity is guaranteed once the Beta graduates.
- Cutover: after A/B validation, `PlanPage.tsx` is replaced by `MapPage.tsx` and the flag removed.

### 13.6 Frontend page structure
- **`MapPage.tsx`** (new, Beta) — all Map mode screens and Map Mode sidebar.
- **`ProjectPage.tsx`** (new, greenfield) — all Projects mode screens (Property Overview, Project Portfolio Overview, Project Detail subroute) and Projects Mode sidebar.
- **Shared components** — Global Control Bar, integrated sidebar shell, status-dot indicators, project color swatches, Activity Detail Drawer.

---

## 14. Phase 1 / Phase 2 Split

### Phase 1 (this epic)
- Property model, boundary promotion, jurisdiction auto-lookup (Nominatim), stale-flag re-check
- Structured reference categories with source tracking (user/system/agent)
- Projects (sequence, status, dates, budget range, rough actual, docs)
- Activities (duration in days, four dependency types, soft map refs, stakeholder assignment, docs, manual sort order)
- Mermaid flowchart rendering with cycle prevention
- Stakeholders (superset model, opt-in, email notifications)
- Contractor Quote Packages (magic link, scoped visibility, quote submission) — *backend + data model only; dedicated UI is a future Stitch pass*
- DIY Estimates (structured materials + labor + rentals) — *backend + data model only; placeholder tab on Project Detail*
- Map project filter panel (dim unlinked, colored badges)
- Map project time slider (activity-level reveal, separate from sun slider)
- MCP agent identity on writes
- Drive folder structure under `LandPlan_Files/{plan}/`
- **Terra Contour visual system** (palette, typography, shared components)
- **New Map Interface (Beta)** as `MapPage.tsx` alongside existing `PlanPage.tsx`
- **`ProjectPage.tsx`** greenfield with Property Overview, Project Portfolio Overview, Project Detail subroute
- **Project Activity Detail Drawer** as a shared component usable from both modes

### Phase 2 (deferred)
- **Dedicated Contractor Quote Package UI** (separate Stitch design pass — out of scope for this epic's Stitch prompt)
- **DIY Estimate editor UI** beyond placeholder tab
- **Stakeholder management screen** (full Stitch design pass)
- **Cutover from `PlanPage.tsx` to `MapPage.tsx`** after Beta A/B validation
- Mermaid Gantt view, drag-to-connect activity editing
- Parcel data integration (Regrid or equivalent)
- Public land proximity detection (PAD-US)
- System-sourced jurisdiction-suggested reference entries
- Actuals-vs-ROM budget tracking beyond a single rough actual field
- Cross-project dependencies
- Auto-reschedule on dependency slip

---

## 15. Explicitly Deferred

- **Audit/change history** on projects and activities (who changed what, when). Agent identity is captured on writes now so the future history will be complete.
- **Export epic** (exporting plans, projects, and reference data to PDF/external formats) — separate epic.
- **Contractor account creation** (contractors stay magic-link-only in v1).
- **`lastReviewedAt`** on reference entries.
- **Priority** as a separate axis from sequence on projects.

---

## 16. Open Items for Implementation

These are not blockers for the spec but need decisions during build:
- Nominatim hosting strategy (self-host vs. paid mirror) for production rate limits.
- Mermaid bundle size impact on the web app initial load — consider dynamic import.
- Magic link token format and rotation on revoke.
- Exact color palette for project badges (coordinate with marketing/branding initiative).

---

*End of draft. Ready for review and synchronization with `architecture.md`, `build_roadmap.md`, and the root `CLAUDE.md`.*
