---
title: "Epic: Planning (Projects, Activities, Stakeholders, Quotes)"
tags: [landplan, epic, planning, projects, activities, stakeholders, in-progress]
created: 2026-04-18
updated: 2026-04-18
status: growing
epic: planning
priority: 1
---

# Epic: Planning

**Status:** In-progress  
**Version:** Draft v1.1  
**Companion docs:** [[stitch-designs]], [[architecture]], [[build-roadmap]]

---

## Objective

Add the planning side of LandPlan.app: property-level vision and reference info, a sequenced project stack, activities with dependencies, stakeholder collaboration, contractor quoting, and DIY estimates. A new Project Timeline slider on the map reveals objects as projects progress.

**Guiding principles:**
- One property per plan
- Non-destructive by default (boundary changes preserve history; soft map references)
- Trust is earned: contractors see only what they need; stakeholders are read-only until elevated
- Forward-compatible schemas (parcel sources, MCP agents, audit history can layer in later)

---

## 1. Property Model

- `Plan` extended with: `missionStatement`, `boundaryObjectId`, `jurisdiction`, `parcelSource`, `apn`
- User promotes a closed polyline to "Property Boundary"; only one boundary per plan
- On boundary promotion: Nominatim (OSM) reverse-geocode auto-populates jurisdiction (country, state, county, city, village)
- If jurisdiction changes after boundary update: existing reference entries flagged `stale`; user reviews, no auto-deletion

---

## 2. Property Reference Information

Five fixed categories (six with [[epic-gps-accuracy-templates|GPS Accuracy epic]] addition):

1. Zoning
2. Rainwater Management
3. Off-Grid Rules & Restrictions
4. Permitting
5. Public Land (BLM, USACE, state/national forest)
6. Site Services & Utilities *(added in GPS Accuracy epic)*

Each entry: `category, title, jurisdictionLevel, notes (markdown), links, attachedDocs, source (user | system | agent), agentName, sourceTimestamp, status (active | stale | archived)`.

---

## 3. Projects

### Schema

`id, planId, title, objective (markdown), sequence (int), status, plannedStartDate, estimatedDurationDays, plannedEndDate, budgetLowUsd, budgetHighUsd, roughActualCostUsd, projectColor, templateSlug, templateVersion`

### Status Enum (shared with Activities)

`planned | in_progress | blocked | on_hold | complete | cancelled`

Project completion is **NOT auto-set** — UI surfaces a suggestion badge when all activities are complete; owner/contributor must confirm.

### Sequencing

Single ranked stack per plan. Drag-to-reorder. Scheduling informational in v1 (changing sequence does not reschedule dates).

---

## 4. Activities

`id, projectId, title, details (markdown), status, durationDays, plannedStartDate, plannedEndDate, completionDate, sortOrder, assignedStakeholderIds, mapObjectRefs, attachedDocs`

### Dependencies

- Scoped within a single project (no cross-project dependencies in v1)
- Four dependency types: **FS, SS, FF, SF** (finish-to-start, start-to-start, finish-to-finish, start-to-finish)
- API validates and rejects dependency writes that create cycles

### Activity ↔ Map Object References

Many-to-many; **soft references** — if a referenced map object is deleted, link preserved as "orphaned" with a warning.

### Mermaid Flowchart

Dependencies stored as structured records; rendered as a Mermaid `flowchart TD` (not hand-edited). API endpoint: `GET /projects/:id/flowchart`.

---

## 5. Stakeholders

`id, planId, name, email, roleLabel (freeform), linkedUserId (nullable), optedIn, notificationsEnabled`

### Access Scope

`stakeholder` role = Viewer + write on `Activity.status` and `ActivityNote` for assigned activities. Does not downgrade existing Contributors.

### Opt-in Flow

1. Add as placeholder contact (name + email; no invitation required)
2. Invite sends transactional email with opt-in link
3. On opt-in: create or link LandPlan account; land on first assigned activity
4. Assignment notifications by email; opt-out per stakeholder

---

## 6. Contractor Quote Packages

### Concept

Named bundle of activities within a single project, sent to one or more contractors for bidding. Contractors access via time-limited **magic link** — no account required.

### Schema

`QuotePackage`: `id, projectId, name, includedActivityIds, attachedDocs, createdBy, createdAt`

`ContractorInvite`: `id, packageId, contractorName, contractorEmail, magicLinkToken, expiresAt (default 30 days), status (sent | viewed | quote_submitted | expired | revoked)`

### Contractor Access Scope

**Can see:**
- Project objective, title, status
- Activities in their specific quote package
- Map objects linked to the project
- Unlinked map objects (existing site context)
- Map objects on projects with `status = 'complete'`
- Property boundary
- Docs attached to their quote package

**Cannot see:** mission statement, reference info, other projects, other stakeholders, other quote packages, broader plan.

Completed-project visibility is **evaluated live** — if a project transitions to `complete` while contractor's link is active, its objects become visible mid-session.

### Quote Submission

Per invite; captures: overall cost (USD), quote expiration date, proposed start date, per-activity line items (amount + notes), optional attached doc, free-text overall notes.

---

## 7. DIY Estimates

Structured cost estimate for a project or activity set.

`id, projectId, name, includedActivityIds, materials [{ name, quantity, unit, unitCostUsd }], laborHours, laborRateUsd, toolRentals [{ name, costUsd }], notes (markdown), computedTotalUsd (derived)`

Equipment rental extension: `toolRentals` extended with `rentalType (flat | daily | weekly)`, `rentalDurationDays`, `neededByDate`, `notes` per [[epic-gps-accuracy-templates]].

---

## 8. Map Integration

### Project Timeline Slider

- In Map Mode sidebar Time section; visually distinct from Sun/Shadow slider
- Left edge = earliest project start date; right edge = latest activity completion date; default = today
- Progressively reveals map objects based on linked activities' earliest completion dates
- Unlinked objects and objects on undated projects always visible

### Map Project Filter

- In Map Mode sidebar Projects section: eye toggle per project
- Unchecked projects' objects dim/desaturate on canvas (not hidden)
- Property boundary always visible

---

## 9. MCP / Agent Identity

Writes that update status or add reference entries capture `actor_type (user | mcp_agent)` and `actor_id`. First-class agent: "Claude Coworker". Full audit history deferred but actor fields captured now.

---

## UI Pages (from [[stitch-designs]])

- Property Overview — mission statement hero, metadata, reference info
- Project Portfolio Overview — drag-to-reorder ranked stack of project cards
- Project Detail — header, objective, tabs (Activities + Mermaid, Quote Packages, DIY Estimate, Docs)
- Activity Detail Drawer — slide-in from right; works in both Map and Projects mode

---

## Deferred to Phase 2

- Dedicated Contractor Quote Package UI (future Stitch pass)
- Dedicated DIY Estimate editor UI
- Dedicated Stakeholder management screen
- `PlanPage.tsx` → `MapPage.tsx` cutover
- Mermaid Gantt view, drag-to-connect editing
- Parcel data integration, PAD-US public land detection
- Full audit history UI
- Cross-project dependencies

---

## Related

- [[stitch-designs]] — five UI designs for this epic
- [[architecture]] — full schema and API surface
- [[build-roadmap]] — session sequencing
- [[epic-gps-accuracy-templates]] — extends planning schemas
