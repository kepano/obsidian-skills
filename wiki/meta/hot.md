---
title: Hot Context Cache
tags: [meta, context]
created: 2026-04-17
updated: 2026-04-18
status: growing
---

# Hot Context Cache

> [!tip] Reading order
> Read this file first at the start of every session (~500 tokens). If more context is needed, check [[index]], then drill into the relevant product subfolder.

---

## Who

**Owner:** Tim Webster — independent product developer.
Working directory: `/Users/timwebster/Documents/SmartForestTech` (Obsidian vault, not a code project).

## What

This vault is the central knowledge base for two product tracks:

1. **[[wiki/platforms/landplan/README|LandPlan platform]]** — a suite of three GIS/land management products. Code at `/Users/timwebster/Documents/code/landplan/landplan`.
2. **Personal / side projects** — Directive (process hub), CAPO (whitepaper concept), MIDI Looper (Raspberry Pi), Home Assistant (Pi configs).

## The Three LandPlan Products (confirmed names)

1. **[[wiki/platforms/landplan/products/landplan-app|LandPlan.app]]** — web GIS + planning platform (main product, in active development)
2. **[[wiki/platforms/landplan/products/survey-mobile|LandPlan Survey]]** — iOS/Android field GPS app (planned, not started)
3. **[[wiki/platforms/landplan/products/survey-gps-receiver|LandPlan Survey GPS Receiver]]** — hardware RTK device (concept only)

> [!important] No TinkerGIS
> TinkerGIS no longer exists as a separate project — it evolved into LandPlan.app. The TinkerGIS wiki page is archived.

## Current Status (as of 2026-04-18)

- **Full `raw/` ingest complete** — all raw landplan docs processed into wiki pages
- **Planning epic** is in-progress; architecture v1.4 is the current data model
- **Completed epics:** Plan Sharing, GCS Storage, 3D Models, Trees & Tree Stands
- **Next planned epics:** GPS Accuracy + Templates, Plan Export
- **Build roadmap** for Planning epic: [[wiki/platforms/landplan/roadmap/build-roadmap|Build Roadmap]] (Track A through E)

## Key Conventions Reminder

- Frontmatter required: `title`, `tags`, `created`, `updated`, `status`
- Status: `seedling | growing | evergreen | archived`
- Internal links: always `[[wikilinks]]`, never `[text](url)`
- Tags: kebab-case (`#land-management`, `#raspberry-pi`)
- `log.md` is append-only — new entries go at the **top**
- Never write to `raw/`
- Coordinate convention in LandPlan code: **[lng, lat]** everywhere (not lat/lon)

## Where to Find Things

| Need | Go to |
|------|-------|
| LandPlan epic details | `wiki/platforms/landplan/roadmap/` |
| Data model / API | [[wiki/platforms/landplan/architecture/architecture]] |
| Design tokens / UI rules | [[wiki/platforms/landplan/design/terra-contour]] |
| Competitive intelligence | [[wiki/platforms/landplan/market/competitive-analysis]] |
| Build session plan | [[wiki/platforms/landplan/roadmap/build-roadmap]] |
| Unscheduled features | [[wiki/platforms/landplan/backlog/feature-ideas]] |

## Last Session

**2026-04-18** — Full ingest of `raw/` directory. Product names confirmed. TinkerGIS archived. 18 new wiki pages created across products, market, design, architecture, roadmap, and backlog subfolders. See [[log]] for full details.
