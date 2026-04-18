---
title: Change Log
tags: [meta, log]
created: 2026-04-17
updated: 2026-04-18
status: growing
---

# Change Log

> [!warning] Append-only
> Never overwrite or delete entries. Always add new entries at the **top** under today's date heading.

---

## 2026-04-18 — Full Ingest of raw/ Directory

**Session goal:** Process all content in `raw/` into cross-linked wiki pages. Confirm three LandPlan product names. Archive TinkerGIS.

**Product names confirmed:**
- LandPlan.app (website / web GIS platform)
- LandPlan Survey (iOS and Android mobile app)
- LandPlan Survey GPS Receiver (hardware RTK device)

**TinkerGIS:** Archived — evolved into LandPlan.app. `wiki/projects/tinkergis/README.md` updated to `archived` status.

**Created — LandPlan Products:**
- `wiki/platforms/landplan/products/landplan-app.md` — LandPlan.app capabilities, tech stack, epic status
- `wiki/platforms/landplan/products/survey-mobile.md` — LandPlan Survey mobile app (concept, planned)
- `wiki/platforms/landplan/products/survey-gps-receiver.md` — Hardware GPS Receiver (concept only)

**Created — Market:**
- `wiki/platforms/landplan/market/competitive-analysis.md` — Full competitor research (Land id®, PropertyIntel, STACK CT, onX Hunt); feature matrix; strategic implications
- `wiki/platforms/landplan/market/business-model.md` — Pricing strategy, revenue streams, competitive positioning

**Created — Design:**
- `wiki/platforms/landplan/design/terra-contour.md` — Terra Contour design system (colors, typography, components, rules)
- `wiki/platforms/landplan/design/stitch-designs.md` — Five named Stitch UI designs (New Map Interface, Property Overview, Project Portfolio Overview, Project Detail, Activity Detail Drawer)

**Created — Architecture:**
- `wiki/platforms/landplan/architecture/architecture.md` — Full architecture v1.4 (monorepo, tech stack, data model, API surface, routing, coordinate convention)

**Created — Roadmap (Epics):**
- `wiki/platforms/landplan/roadmap/epic-plan-sharing.md` — Plan Sharing epic (Done)
- `wiki/platforms/landplan/roadmap/epic-gcs-storage.md` — GCS Storage Overhaul epic (Done)
- `wiki/platforms/landplan/roadmap/epic-3d-models.md` — 3D Models & Shadow Simulation epic (Done)
- `wiki/platforms/landplan/roadmap/epic-trees.md` — Trees & Tree Stands epic (Done)
- `wiki/platforms/landplan/roadmap/epic-planning.md` — Planning epic (In-progress)
- `wiki/platforms/landplan/roadmap/epic-gps-accuracy-templates.md` — GPS Accuracy, Templates & Utility Services (Planned)
- `wiki/platforms/landplan/roadmap/epic-plan-export.md` — Plan Export (Planned)
- `wiki/platforms/landplan/roadmap/build-roadmap.md` — Claude Code session sequencing for Planning epic

**Created — Backlog:**
- `wiki/platforms/landplan/backlog/tags-system.md` — Tags / category system issues and proposed direction
- `wiki/platforms/landplan/backlog/feature-ideas.md` — All deferred and unscheduled feature ideas

**Updated:**
- `wiki/platforms/landplan/README.md` — confirmed product names, full platform knowledge map, epic status table
- `wiki/projects/tinkergis/README.md` — archived, redirect to LandPlan.app
- `wiki/meta/index.md` — added all new pages
- `wiki/meta/hot.md` — updated with current session state

**Raw files processed:**
- `raw/landplan/LandPlan Product Brainstorm.md`
- `raw/landplan/LandPlan.app.md`
- `raw/landplan/LandPlan Feature Roadmap.md`
- `raw/landplan/Market Evaluation.md`
- `raw/landplan/LandPlan Business Model.md`
- `raw/landplan/LandPlan Tags.md`
- `raw/landplan/LandPlan Help Guides and Training.md` (empty)
- `raw/landplan/LandPlan — GPS Accuracy, Onboarding, Templates & Utility Services Requirements.md`
- `raw/landplan/EPIC Replace Google Drive with Google Cloud Storage as the primary file store.md`
- `raw/landplan/EPIC Plan Export — browser zip download and Google Drive export.md`
- `raw/landplan/docs/DESIGN.md`
- `raw/landplan/docs/architecture.md`
- `raw/landplan/docs/requirements_planning.md`
- `raw/landplan/docs/requirements_trees.md`
- `raw/landplan/docs/requirements_3d_models.md`
- `raw/landplan/docs/requirements_sharing.md`
- `raw/landplan/docs/build_roadmap.md`
- `raw/landplan/docs/landplan-stitch-prompt-projects.md`
- `raw/directive/Directive Product Brainstorm.md` (stub only — no new wiki page; existing stub sufficient)
- `raw/fun-projects/Fun Projects Brainstorming.md` (stub only — no new wiki page)
- `raw/fun-projects/HomeAssistant.md` (empty)

---

## 2026-04-17 — Vault Initialisation

**Session goal:** Bootstrap the wiki skeleton from a blank slate.

**Created:**
- `wiki/meta/index.md` — master page index
- `wiki/meta/log.md` — this file
- `wiki/meta/hot.md` — recent context cache
- `wiki/platforms/landplan/README.md` — LandPlan platform hub (three products, names TBD)
- `wiki/projects/directive/README.md` — Directive project starter
- `wiki/projects/capo/README.md` — CAPO project starter
- `wiki/projects/midi-looper/README.md` — MIDI Looper project starter
- `wiki/projects/tinkergis/README.md` — TinkerGIS project starter
- `wiki/projects/home-assistant/README.md` — Home Assistant project starter

**Source material consulted:**
- `CLAUDE.md` — vault conventions and folder structure
- `Product Brainstorm.md` — product descriptions and links
- `LandPlan.app.md` — LandPlan feature roadmap stub
- `LandPlan Tags.md` — GIS tag categories in use

**Notes:** Product names for the three LandPlan products are not yet finalised; placeholders used in `wiki/platforms/landplan/README.md`.
