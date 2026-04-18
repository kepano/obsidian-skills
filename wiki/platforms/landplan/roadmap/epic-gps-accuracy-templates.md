---
title: "Epic: GPS Accuracy, Project Templates & Utility Services"
tags: [landplan, epic, gps, accuracy, templates, utilities, planned]
created: 2026-04-18
updated: 2026-04-18
status: growing
epic: gps-accuracy-templates
priority: 2
---

# Epic: GPS Accuracy, Project Templates & Utility Services

**Status:** Planned  
**Version:** Draft v1.0  
**Scope derived from:** Stakeholder feedback, April 2026  
**Companion docs:** [[epic-planning]], [[architecture]], [[build-roadmap]]

---

## Objective

Five gaps identified during stakeholder review of the Planning epic:

1. **Coordinate accuracy is invisible** — the app treats a base-map trace (±30 m) the same as an RTK survey (±1 cm)
2. **GPS is undocumented in-product** — new users don't understand LandPlan's value scales with GPS data quality; KML/GeoJSON import path undiscoverable
3. **DIY Estimates undersell equipment rentals** — "tool rentals" implies hand tools; real land work involves excavators, skid-steers; rental durations not captured
4. **New users face a cold start on projects** — "What projects should I even have?" has well-understood answers for common land development patterns
5. **Site services & utilities have no home** — water, power, access, sewage, internet are the first questions any builder asks, but Reference Info had no category for them

---

## 1. Coordinate Accuracy Metadata

### MapObject Extension

New nullable fields on `MapObject`:

| Field | Type | Notes |
|-------|------|-------|
| `captureMethod` | enum | `basemap_traced | kml_import | geojson_import | mobile_gps | mobile_rtk_single | mobile_rtk_dual | professional_survey | unknown` |
| `basemapContext` | enum, nullable | Only when `captureMethod = 'basemap_traced'`: `on_building | on_mapped_road | misaligned_imagery | rural_low_quality | unspecified` |
| `accuracyMeters` | float, nullable | Best-estimate horizontal accuracy in metres |
| `captureSource` | string, nullable | e.g., `"SparkFun RTK Torch"`, `"County GIS 2024"` |
| `capturedAt` | timestamp, nullable | When coordinate was originally captured |
| `accuracyNotes` | markdown, nullable | Freeform context |

### Accuracy Tiers & Defaults

| Method | Default accuracy | Tier | Badge colour |
|--------|-----------------|------|-------------|
| `basemap_traced` | 15 m (context-aware, see below) | Rough | Amber or Red |
| `kml_import` / `geojson_import` | null (ask user) | Varies | Amber until set |
| `mobile_gps` | 3 m | Consumer | Amber |
| `mobile_rtk_single` | 0.15 m | Survey-grade | Green |
| `mobile_rtk_dual` | 0.01 m | Survey-grade | Green |
| `professional_survey` | 0.05 m | Survey-grade | Green |
| `unknown` | null | Unknown | Gray |

Tier thresholds: Red ≥ 10 m · Amber ≥ 0.5 m and < 10 m · Green < 0.5 m · Gray = null.

### Base-Map Context Accuracy

| Context | Typical accuracy | Tier |
|---------|-----------------|------|
| `on_building` | 2 m | Amber |
| `on_mapped_road` | 6 m | Amber |
| `misaligned_imagery` | 10 m | Red |
| `rural_low_quality` | 20 m | Red |
| `unspecified` (default) | 15 m | Red |

### Migration

Existing objects default to `captureMethod = 'basemap_traced'`, `basemapContext = 'unspecified'`, `accuracyMeters = 15.0`.

### UI

- **Accuracy badge:** small inline badge on every map object in properties panel (e.g., `± 6 m` + tier colour dot)
- **"Show accuracy" layer toggle** in Map Mode sidebar → renders accuracy radius ring around each object
- **Property Boundary** accuracy always shown prominently on Property Overview page
- **KML/GeoJSON import:** required source/accuracy step in import dialog
- **Contractor Quote Package views:** accuracy badges shown on all visible objects

---

## 2. In-Product GPS Education

- **Help article:** "About coordinate accuracy" — linked from accuracy badge tooltip, Property Overview, and import dialog. Covers: accuracy spectrum, how to get better data, how LandPlan uses accuracy for contractors.
- **Onboarding card:** On first boundary promotion — explains base-map tracing accuracy; dismissed forever per-user.
- No schema changes — content and UI only.

---

## 3. DIY Estimate Refinements

### Label Change

UI: "Tool Rentals" → "Equipment & Tool Rentals" (DB field stays `toolRentals`).

### Rental Line Item Extension

```
toolRentals: Array<{
  name: string,
  rentalType: 'flat' | 'daily' | 'weekly',  // default 'flat'
  costUsd: number,
  rentalDurationDays: number | null,         // required when rentalType != 'flat'
  neededByDate: string | null,               // ISO date
  notes: string | null
}>
```

Total computation: flat = costUsd; daily = costUsd × durationDays; weekly = costUsd × ceil(durationDays / 7).

---

## 4. Project Templates

### Model

Read-only seed data. Instantiating creates fresh `Project` + `Activity` records owned by the user. Subsequent edits don't affect the template; template updates don't propagate to existing instances.

### Tables

`ProjectTemplate`: `id, slug, title, category (utilities | structures | landscape | access | other), description (markdown), defaultObjective, defaultBudgetLowUsd, defaultBudgetHighUsd, defaultDurationDays, tags, version`

`ProjectTemplateActivity`: `id, templateId, title, details, defaultDurationDays, sortOrder, suggestedStakeholderRoleLabel`

`ProjectTemplateDependency`: `id, templateId, predecessorActivityId, successorActivityId, type (FS|SS|FF|SF)`

### Project Extension

`Project` gains: `templateSlug (nullable)`, `templateVersion (nullable)`

### Instantiation Flow

1. "Add Project" → picker: "Start from scratch" or "Use a template"
2. Templates grouped by category; preview shows activities and Mermaid dependency flowchart
3. User confirms → system creates Project + all Activities + all ActivityDependencies

### Initial Template Set (Phase 1)

| Slug | Title | Category |
|------|-------|----------|
| `septic-system` | New Septic System | utilities |
| `new-well` | New Well | utilities |
| `solar-ground-mount` | Ground-Mount Solar Array | utilities |
| `solar-rooftop` | Rooftop Solar Array | utilities |
| `orchard-planting` | Orchard Planting | landscape |
| `driveway-new` | New Driveway | access |
| `fence-perimeter` | Perimeter Fencing | other |
| `pond-excavation` | Pond Excavation | landscape |

Each ships with 5–12 activities and dependency chain. Seed content tracked separately in `templates_seed_content.md`.

---

## 5. Utility Services Reference Category

Adds a sixth reference category to [[epic-planning|Property Reference Information]]:

- **`site_services_utilities`** — "Site Services & Utilities"

Sub-topic hints (UI only; no schema change): Water, Power, Access, Sewage, Internet & Communications, Other.

On new plan creation (or first boundary confirmation): system seeds empty placeholder entries — one per sub-topic, `source = 'system'`, `notes = empty`, `status = active`. Acts as checklist; user fills in as they research. Users can delete any they don't need.

Natural target for MCP agents (e.g., Claude Coworker): "look up whether public water reaches this parcel."

---

## Phase 1 vs Phase 2

### Phase 1 (this epic)

All MapObject accuracy fields + migration; accuracy badge UI; "Show accuracy" layer; KML/GeoJSON import dialog step; contractor accuracy badges; help article + onboarding card; DIY rental extension; template tables + seed data; template picker UI; utility reference category + seeded entries.

### Phase 2 (deferred)

Per-feature accuracy from embedded KML/GeoJSON metadata; user-authored templates; shared/community templates; accuracy-aware buffer rendering; DB rename `toolRentals` → `equipmentRentals`; "Ordinances" Drive subfolder rename.

---

## Related

- [[epic-planning]] — the planning schemas this extends
- [[architecture]] — MapObject table this extends
- [[survey-mobile]] — mobile will write accuracy fields directly on capture
- [[survey-gps-receiver]] — hardware writes `mobile_rtk_single` or `mobile_rtk_dual` accuracy
