---
title: LandPlan.app
tags: [landplan, web-app, gis, land-management, product]
created: 2026-04-18
updated: 2026-04-18
status: growing
---

# LandPlan.app

> [!abstract] One-liner
> A website and GIS system for landowners to visualise the future of their property — combining interactive mapping with long-horizon project planning.

**Tagline:** *"LandPlan — Visualize the future of your property."*

---

## What It Does

LandPlan.app lets a property owner stand on their raw land and build a 5-to-15-year vision for it — with maps, 3D visualisation, projects, and contractor quoting. No existing tool serves this combination today (see [[competitive-analysis]]).

### Core Capabilities

| Domain | Feature |
|--------|---------|
| Mapping | Interactive GIS map over aerial/satellite imagery; draw and measure features |
| Objects | Annotate land with structures, water features, hazards, trees, fences, roads |
| 3D | Upload/place 3D models (glTF/GLB) anchored to polygon footprints |
| Trees | Procedurally generated tree models and tree stands with growth timeline |
| Shadows | Sun/shadow simulation via SunCalc; evaluate solar exposure at any time of day |
| Planning | Property mission statement; sequenced project stack; activities with dependencies |
| Collaboration | Role-based sharing (Owner / Contributor / Viewer / Stakeholder / Contractor) |
| Contractor quoting | Scoped magic-link quote packages; side-by-side bid comparison |
| DIY Estimates | Materials, labour, equipment rental cost breakdowns |
| Data export | GCS-backed storage; full plan export (GeoJSON + JSON + files as zip) |
| GPS accuracy | Coordinate accuracy metadata on every map object; accuracy badge UI |

---

## Tech Stack

- **Frontend:** React / Vite / TypeScript — `packages/web`
- **Backend:** Node.js / Fastify / Prisma — `packages/api`
- **Database:** Cloud SQL for PostgreSQL 15 with PostGIS
- **Storage:** Google Cloud Storage (GCS) via signed URLs
- **Maps:** MapLibre GL JS
- **3D:** Three.js integrated as a MapLibre custom layer
- **Auth:** Firebase Auth
- **Email:** SendGrid / Resend
- **Geocoding:** Nominatim (OSM reverse-geocode for jurisdiction lookup)
- **Code repo:** `/Users/timwebster/Documents/code/landplan/landplan`

---

## Design System

[[terra-contour]] — "The Digital Cartographer". Forest green primary (`#466800` / `#89B838`), warm neutral surfaces, Plus Jakarta Sans typography, glassmorphism map utilities. No 1px borders — boundaries defined by background tone shifts only.

---

## Product Modes

### Map Mode
Spatial view. Sidebar: Layers, Saved Views, Structures, Plants, Projects filter, Time (Sun/Shadow + Project Timeline sliders). Floating tools palette (left-centre): Select, Object, Distance, Area, Import, Photo.

### Projects Mode
Document-like planning view. Sidebar: Mission, Projects, Stakeholders, Reference Info, Docs. Pages: [[epic-planning#Property Overview]], [[epic-planning#Project Portfolio Overview]], [[epic-planning#Project Detail]].

---

## Epics (Completed → In-Progress)

| Epic | Status | Wiki |
|------|--------|------|
| Plan Sharing | Done | [[epic-plan-sharing]] |
| 3D Models & Shadow Simulation | Done | [[epic-3d-models]] |
| GCS Storage Overhaul | Done | [[epic-gcs-storage]] |
| Trees & Tree Stands | Done | [[epic-trees]] |
| Planning (Projects, Activities, Stakeholders, Quotes) | In-progress | [[epic-planning]] |
| GPS Accuracy, Templates & Utilities | Planned | [[epic-gps-accuracy-templates]] |
| Plan Export | Planned | [[epic-plan-export]] |

Build session sequencing: [[build-roadmap]]

---

## Competitive Position

The "map + planning for individual landowners" quadrant has no direct competitor today. Nearest overlap: Land id® (~$50/mo Pro) for mapping only. LandPlan targets $15–30/mo consumer SaaS.

Full analysis: [[competitive-analysis]]

---

## Related

- [[survey-mobile]] — field GPS companion app
- [[survey-gps-receiver]] — hardware RTK receiver
- [[business-model]] — pricing strategy and revenue model
