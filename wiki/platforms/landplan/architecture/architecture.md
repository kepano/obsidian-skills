---
title: LandPlan Architecture
tags: [landplan, architecture, backend, frontend, database]
created: 2026-04-18
updated: 2026-04-18
status: growing
---

# LandPlan Architecture

*Version: v1.4 (Planning epic delta). Source: `raw/landplan/docs/architecture.md`.*

---

## Monorepo Structure

| Package | Role |
|---------|------|
| `shared` | TypeScript types shared across packages |
| `api-client` | Typed API endpoint wrappers |
| `api` | Fastify server, Prisma migrations, business logic |
| `web` | React / Vite frontend |
| `mobile` | Mobile app (no changes in current epics) |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React / Vite / TypeScript |
| Backend | Node.js / Fastify |
| ORM | Prisma |
| Database | Cloud SQL for PostgreSQL 15 with PostGIS |
| File storage | Google Cloud Storage (GCS) — signed URLs; no file bytes proxied through API |
| Maps | MapLibre GL JS |
| 3D rendering | Three.js (custom MapLibre layer) |
| Auth | Firebase Auth (JWT) |
| Email | SendGrid / Resend |
| Geocoding | Nominatim (OSM) for jurisdiction reverse-geocode |
| Monorepo | pnpm workspaces |

---

## Data Model — Key Tables

### Plan (top-level entity)

One plan per property owner (1:1 with property). Key fields:
- `missionStatement` — markdown property vision
- `boundaryObjectId` — FK to the designated property boundary MapObject
- `jurisdiction` — jsonb: `{ country, state, county, city, village, other }`
- `parcelSource` — enum, reserved for future: `regrid | county_gis | user | null`
- `apn` — nullable string

### MapObject

All drawn features on the map. Extended with:
- `projectId` — nullable FK to Project (for map-project filtering and timeline slider)
- `captureMethod` — enum: `basemap_traced | kml_import | geojson_import | mobile_gps | mobile_rtk_single | mobile_rtk_dual | professional_survey | unknown`
- `basemapContext` — enum (only when `captureMethod = 'basemap_traced'`): `on_building | on_mapped_road | misaligned_imagery | rural_low_quality | unspecified`
- `accuracyMeters` — float, nullable; horizontal accuracy in metres
- `captureSource` — string, nullable (e.g., `"SparkFun RTK Torch"`, `"County GIS 2024"`)
- `capturedAt` — timestamp, nullable
- `accuracyNotes` — markdown, nullable

### Project

- `id, planId, title, objective (markdown), sequence (int), status (enum), plannedStartDate, estimatedDurationDays, plannedEndDate, budgetLowUsd, budgetHighUsd, roughActualCostUsd, projectColor`
- `templateSlug, templateVersion` — nullable; set when project instantiated from a template

### Activity

- `id, projectId, title, details (markdown), status, durationDays, plannedStartDate, plannedEndDate, completionDate, sortOrder, assignedStakeholderIds, mapObjectRefs, attachedDocs`

### ActivityDependency

`{ predecessorActivityId, successorActivityId, type: FS | SS | FF | SF }`. Scoped within a single project. Cycle prevention enforced at API layer.

### Stakeholder

`{ id, planId, name, email, roleLabel, linkedUserId, optedIn, notificationsEnabled }`

### ReferenceEntry

`{ id, planId, category (enum), title, jurisdictionLevel, notes, links, attachedDocs, source (user | system | agent), agentName, sourceTimestamp, status (active | stale | archived) }`

Reference categories: `zoning | rainwater | off_grid | permitting | public_land | site_services_utilities`

### QuotePackage / ContractorInvite / ContractorQuote

Contractor quoting flow. Contractors access via magic-link token (no account required).

### DIYEstimate

`{ id, projectId, name, includedActivityIds, materials, laborHours, laborRateUsd, toolRentals, notes, computedTotalUsd }`

### PlanFile (GCS storage)

`{ id, planId, objectKey, filename, mimeType, sizeBytes, context (photo | model | document | boundary), contextEntityId, uploadedBy, createdAt, deletedAt }`

### GCS Bucket Structure

```
plans/{planId}/property/ordinances/{fileId}_{filename}
plans/{planId}/property/boundary/{fileId}_{filename}
plans/{planId}/photos/{fileId}_{filename}
plans/{planId}/models/{fileId}_{filename}
plans/{planId}/projects/{projectId}/{fileId}_{filename}
plans/{planId}/projects/{projectId}/activities/{activityId}/{fileId}_{filename}
plans/{planId}/quote-packages/{packageId}/{fileId}_{filename}
```

### TreeModel / TreeStand

Procedural tree objects (not glTF/GLB). PostGIS GEOMETRY type for stands. Coordinate convention: **lng, lat** everywhere (not lat/lon).

### Project Templates

`ProjectTemplate`, `ProjectTemplateActivity`, `ProjectTemplateDependency` — read-only seed data; users instantiate copies.

---

## Roles & Access Control

| Role | Identifier | Access |
|------|-----------|--------|
| Owner | `owner` | Full control |
| Contributor | `contributor` | Edit (no plan settings/delete) |
| Viewer | `viewer` | Read-only |
| Stakeholder | `stakeholder` | Viewer + write on assigned activity status/notes |
| Contractor (Quote) | `contractor_quote` | Token-scoped; sees only their quote package scope |

### Contractor visibility scope (magic link)

Can see: project objective/title/status, their quoted activities, map objects linked to their project, unlinked map objects, objects on completed projects, property boundary, attached docs.

Cannot see: mission statement, reference info, other projects, other stakeholders, other quote packages.

---

## API Surface

All routes under Fastify, JWT-authenticated (Firebase Auth) unless noted.

Key route groups:
- `PATCH /plans/:planId/property` — mission, APN, jurisdiction
- `POST /plans/:planId/boundary` — promote map object to boundary; triggers Nominatim
- `GET/POST /plans/:planId/references` — reference entries
- `GET/POST/PATCH /plans/:planId/projects` — project CRUD + reorder
- `GET/POST/PATCH /projects/:id/activities` — activity CRUD + reorder + notes + dependencies
- `GET/POST /plans/:planId/stakeholders` — stakeholder management
- `POST /projects/:id/quote-packages` — contractor quoting
- `GET /contractor/:token` — magic-link landing (no JWT)
- `POST /contractor/:token/quote` — contractor quote submission
- `GET /projects/:id/flowchart` — Mermaid source string from dependency records
- `POST /plans/:planId/export` — plan export (zip download or Google Drive)
- GCS signed URL flow: `POST /plans/:planId/files/upload-url` → client uploads direct → `POST /plans/:planId/files/complete`

---

## Frontend Routing

| Route | Page | Notes |
|-------|------|-------|
| `/plan/:id` | `PlanPage.tsx` | Existing map; retained during Beta |
| `/plan/:id/map-beta` | `MapPage.tsx` | New Map Interface Beta (feature-flagged) |
| `/plan/:id/projects` | `ProjectPage.tsx` | Property Overview (default) + Portfolio + Detail |
| `/plan/:id/projects/:projectId` | `ProjectPage.tsx` sub-route | Project Detail |

### Shared Terra Contour Components (`web/src/components/terra/`)

`GlobalControlBar`, `IntegratedSidebar`, `StatusDot`, `ProjectColorSwatch`, `ActivityDetailDrawer`, `MermaidFlowchart`, `ProjectTimelineSlider`

### Zustand Stores

`projectStore`, `stakeholderStore`, `referenceStore`, `mapProjectFilterStore`

---

## Critical Coordinate Convention

**All coordinates are [lng, lat] order** — GeoJSON (RFC 7946) convention and used everywhere in the LandPlan codebase. Nominatim returns lat/lng; convert at the API boundary. Third-party reference implementations may use lat/lon — always correct before use.

---

## Open Architectural Decisions

- Nominatim hosting for production: self-host on GKE vs. paid mirror
- Mermaid bundle impact under Vite (measure after C3 lands)
- Magic link token format and signing key rotation on revoke
- Feature-flag mechanism for Map Beta (env var vs. user-level)
- `McpAgent` rows: statically seeded or created on first write

---

## Related

- [[epic-planning]] — schema additions for Planning epic
- [[epic-gcs-storage]] — GCS storage overhaul
- [[epic-trees]] — TreeModel / TreeStand schema
- [[epic-gps-accuracy-templates]] — MapObject accuracy field additions
- [[build-roadmap]] — implementation session plan
