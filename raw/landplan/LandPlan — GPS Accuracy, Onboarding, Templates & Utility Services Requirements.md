

**Status:** Draft v1.0
**Scope:** Adds coordinate accuracy metadata, in-product GPS education, DIY rental refinements, project templates, and utility services reference coverage. Derived from stakeholder feedback (April 2026 email thread). Designed to integrate cleanly with the Planning epic (`requirements_planning.md`) and the existing mapping data model.

**Companion documents:**

- `requirements_planning.md` — Planning epic (Property model, Projects, Activities, Stakeholders, Quote Packages).
- `architecture.md` (v1.4+) — data model, API surface, frontend structure.
- `build_roadmap.md` — sequenced session plan for Claude Code.

**Backlog items NOT covered here (low priority, recorded separately):**

- Generalized Quote Packages with `packageType` to support equipment rental vendors and materials quotes.
- “Developer Edition” — multi-parcel portfolios, entitlement tracking, pro formas.

-----

## 1. Overview

This epic addresses five gaps identified during stakeholder review of the Planning epic:

1. **Coordinate accuracy is invisible.** Every map object carries GPS coordinates, but the app treats a base-map-traced polygon (±30–100 ft) the same as an RTK-surveyed point (±1 cm). Owners, contributors, and especially contractors need to know what accuracy they’re looking at.
2. **GPS is a foundational concept, undocumented in-product.** New users don’t understand that LandPlan’s value scales with the quality of GPS data fed into it. The KML/GeoJSON import path — the bridge from professional surveys — is undiscoverable.
3. **DIY Estimates undersell equipment rentals.** The current “tool rentals” label implies hand tools; real land work involves excavators, skid-steers, and lifts. Rental durations aren’t captured.
4. **New users face a cold start on projects.** “What projects should I even have?” is a real question. Common land-development projects (septic, well, solar, orchard) have well-understood activity patterns that should be pre-built.
5. **Site services & utilities have no home.** Water, power, access, sewage, and internet are the first questions any builder asks, but Reference Info has no category for them.

**Guiding principles (inherited from Planning epic):**

- Forward-compatible schemas (mobile Survey app, future RTK integrations).
- Non-destructive by default.
- Keep the tone approachable; avoid surveying jargon in user-facing copy.

-----

## 2. Coordinate Accuracy Metadata

### 2.1 Motivation

Every coordinate in LandPlan has a lineage. A point pinned to a visible building in good aerial imagery is accurate to a couple of meters. A trace in a rural area with sparse OSM data and low-resolution imagery may be off by 20+ meters. A point captured via dual-receiver RTK is survey-grade at ~1 cm. Owners, contributors, and especially contractors need to know what accuracy they’re looking at. This becomes critical when the mobile Survey app (on the roadmap) ships, since it will produce coordinates across the full accuracy spectrum in a single plan.

### 2.2 Schema — extend `MapObject`

Add the following nullable fields to the existing `MapObject` table:

|Field           |Type               |Notes                                                                                                                                                                                                                                                          |
|----------------|-------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|`captureMethod` |enum               |One of: `basemap_traced`, `kml_import`, `geojson_import`, `mobile_gps`, `mobile_rtk_single`, `mobile_rtk_dual`, `professional_survey`, `unknown`. Default `basemap_traced` for objects created via map-draw tools; `unknown` for legacy objects until migrated.|
|`basemapContext`|enum, nullable     |Only meaningful when `captureMethod = 'basemap_traced'`. One of: `on_building`, `on_mapped_road`, `misaligned_imagery`, `rural_low_quality`, `unspecified`. Drives default `accuracyMeters` per §2.3.1.                                                        |
|`accuracyMeters`|float, nullable    |Best-estimate horizontal accuracy in meters. Populated automatically based on `captureMethod` defaults (see §2.3) or explicitly on import/capture.                                                                                                             |
|`captureSource` |string, nullable   |Freeform device or source identifier. Examples: `"SparkFun RTK Torch"`, `"County GIS 2024"`, `"Smith Surveying Co."`.                                                                                                                                          |
|`capturedAt`    |timestamp, nullable|When the coordinate was originally captured (not when the LandPlan record was created). Populated from GPS metadata where available.                                                                                                                           |
|`accuracyNotes` |markdown, nullable |Optional freeform context (e.g., “Walked in light tree cover, signal degraded”).                                                                                                                                                                               |

**Migration:** see §2.3.2.

### 2.3 Accuracy tiers & defaults

Applied automatically when `captureMethod` is set but `accuracyMeters` is not explicitly provided. Base-map tracing accuracy depends heavily on what the user is tracing against in the OSM/aerial base layer:

|Method                         |Default accuracy                              |Tier        |Badge color    |
|-------------------------------|----------------------------------------------|------------|---------------|
|`basemap_traced`               |15 m (see §2.3.1 for context-aware refinement)|Rough       |Amber or Red   |
|`kml_import` / `geojson_import`|null (ask user)                               |Varies      |Amber until set|
|`mobile_gps`                   |3 m                                           |Consumer    |Amber          |
|`mobile_rtk_single`            |0.15 m                                        |Survey-grade|Green          |
|`mobile_rtk_dual`              |0.01 m                                        |Survey-grade|Green          |
|`professional_survey`          |0.05 m                                        |Survey-grade|Green          |
|`unknown`                      |null                                          |Unknown     |Gray           |

Tier is derived, not stored:

- Red: `accuracyMeters >= 10`.
- Amber: `accuracyMeters >= 0.5` and < 10.
- Green: `accuracyMeters < 0.5`.
- Gray: `accuracyMeters` is null.

### 2.3.1 Base-map tracing — context-aware accuracy

Pin and trace accuracy against OSM/aerial base layers varies significantly by what the user is snapping to. Rather than a single 30 m default, the `basemap_traced` method uses a `basemapContext` sub-field (stored on the object, enum) that the user selects when creating the object, with the following defaults:

|Base-map context                                                                      |Typical accuracy|Tier |
|--------------------------------------------------------------------------------------|----------------|-----|
|`on_building` — pinning to a visible building in good aerial imagery                  |2 m             |Amber|
|`on_mapped_road` — pinning to a well-mapped road or road centerline                   |6 m             |Amber|
|`misaligned_imagery` — user notes that aerial imagery appears offset from ground truth|10 m            |Red  |
|`rural_low_quality` — rural area, sparse OSM data, or low-resolution imagery          |20 m            |Red  |
|`unspecified` — user did not specify (default for legacy objects and quick draws)     |15 m            |Red  |

Implementation notes:

- The object creation flow offers these contexts as a quick-pick dropdown, defaulting to `unspecified`. Users who want accurate estimates pick the matching context; users who don’t care accept the conservative 15 m default.
- `basemapContext` is nullable and only meaningful when `captureMethod = 'basemap_traced'`. Other capture methods ignore it.
- These defaults apply only when `accuracyMeters` is not explicitly provided. A user who manually enters a value always wins.
- The “Show accuracy” map layer (§2.4) renders the radius based on the effective `accuracyMeters`, so an object pinned to a building shows a 2 m ring while a rural area trace shows a 20 m ring — immediate visual feedback on data quality.

### 2.3.2 Migration

Existing objects default to `captureMethod = 'basemap_traced'`, `basemapContext = 'unspecified'`, `accuracyMeters = 15.0`, `captureSource = null`, `capturedAt = createdAt`. This replaces the previous 30 m assumption — more honest on average, since most existing objects were traced against buildings or mapped features, not rural wilderness. Users can refine the context and accuracy per-object via the properties panel.

### 2.4 UI — object accuracy badge

- Small inline badge on every map object in the properties panel: `± 6 m` with tier color dot, following the Terra Contour “small inline color dot + text label” pattern (no standalone pills).
- On the map canvas, accuracy is **not** rendered by default to avoid visual noise. A “Show accuracy” toggle in the Map mode sidebar (under Layers) renders a subtle ring around each object at its accuracy radius, color-coded by tier.
- The **Property Boundary** always shows its accuracy prominently in the Property Overview page (Projects mode), because it drives jurisdiction lookup and contractor spatial context.

### 2.5 Import flow — KML / GeoJSON

On file import, the existing import dialog gains a required step:

- “What is the source of this data?” with options matching the `captureMethod` enum, plus a freeform `captureSource` field.
- Optional `accuracyMeters` override, pre-filled from the selected method’s default.
- Applied as a batch to all features in the import. Individual features can be edited afterward.

GPS metadata embedded in GeoJSON/KML (`<accuracy>` tags, `gpx:hdop`, etc.) is parsed where available and used to pre-populate per-feature accuracy; the batch default acts as a fallback.

### 2.6 Contractor visibility

Contractor Quote Package views (see `requirements_planning.md` §8) display accuracy badges on all visible map objects. Contractors need this more than anyone — a driveway centerline marked ±15 m should not be bid as fixed-price without a site walk.

### 2.7 Forward compatibility

- Mobile Survey app writes `captureMethod`, `accuracyMeters`, `captureSource`, and `capturedAt` directly on creation. No schema change needed when it ships.
- MCP agents that import parcel data (e.g., Regrid) set `captureMethod = 'kml_import'` or a new `parcel_dataset` value and record the dataset name in `captureSource`.

-----

## 3. In-Product GPS Education

### 3.1 Help article — “About coordinate accuracy”

A single canonical help page, linked from:

- The accuracy badge tooltip on any map object (“Learn about accuracy →”).
- The Property Overview page, next to the boundary accuracy indicator.
- The KML/GeoJSON import dialog (“Why do we ask about your data source?”).

Content covers the accuracy spectrum (base-map tracing through dual RTK), how to get better data (hire a surveyor, use a consumer GPS app, add a Bluetooth RTK receiver), and how LandPlan uses accuracy data (visibility to contractors, boundary confidence, future mobile Survey app).

### 3.2 Onboarding card — first boundary

When a user promotes their first polyline to Property Boundary (see Planning epic §2.2), a one-time card appears:

> **Your boundary is a base-map tracing.**
> Its accuracy depends on what you traced against — roughly ±2 m if you snapped to visible buildings in clear aerial imagery, ±5–15 m on typical rural land, more in areas with sparse mapping. Plenty for planning and jurisdiction lookup, but not for siting a fence. When you’re ready for survey-grade coordinates, you can import a KML or GeoJSON from your surveyor, or capture points directly with our upcoming Survey app.
> [Learn more] [Got it]

Dismissed forever per-user. Does not reappear on boundary re-promotion.

### 3.3 Stakeholder overview document updates

The existing `LandPlan_Overview_for_Stakeholders.docx` gains a short section under “Capabilities Available Today” titled **“Accurate coordinates, when you need them”**, framing GPS as the foundational data layer and KML/GeoJSON import as the bridge from professional surveys. Copy should avoid the phrase “GPS data” in the abstract — concrete examples (surveyor export, county GIS download, field walk with a phone) land better.

### 3.4 No schema changes

This section is content and UI only. No database migrations.

-----

## 4. DIY Estimate Refinements

### 4.1 Rename “Tool Rentals” to “Equipment & Tool Rentals”

In `requirements_planning.md` §9 (DIY Estimate schema), the `toolRentals` field is renamed **in UI labels only** to “Equipment & Tool Rentals”. The database field name stays `toolRentals` to avoid a breaking migration; a code-level rename to `equipmentRentals` can happen in a future pass if desired.

### 4.2 Schema — extend rental line items

Current:

```
toolRentals: Array<{ name, costUsd }>
```

Extended:

```
toolRentals: Array<{
  name: string,
  rentalType: 'flat' | 'daily' | 'weekly',  // default 'flat' for backward compatibility
  costUsd: number,                           // flat cost, OR rate per period if rentalType != 'flat'
  rentalDurationDays: number | null,         // required when rentalType != 'flat'
  neededByDate: string | null,               // ISO date, optional
  notes: string | null
}>
```

### 4.3 Totals computation

`computedTotalUsd` updates to:

- For `flat` rentals: add `costUsd` directly.
- For `daily` rentals: add `costUsd × rentalDurationDays`.
- For `weekly` rentals: add `costUsd × ceil(rentalDurationDays / 7)`.

Materials and labor computations from Planning epic §9 are unchanged.

### 4.4 UI

Rental line item editor gains a `rentalType` dropdown. When `daily` or `weekly` is selected, duration and needed-by date fields become visible. Flat is the default so existing behavior is preserved for users who don’t need duration tracking.

### 4.5 Migration

Existing `toolRentals` entries are treated as `rentalType = 'flat'` with null duration. No data loss.

-----

## 5. Project Templates

### 5.1 Motivation

New land owners face a cold start: “what projects should I even have?” Common improvements — septic, well, solar, orchard, utility hookups — have well-understood activity patterns. Encoding them as templates compresses activation time and makes LandPlan feel like it knows something about land development.

### 5.2 Model

Templates are **read-only seed data**, not user-editable records. Instantiating a template creates fresh `Project` and `Activity` records owned by the user’s plan. Subsequent edits to the instantiated project do not affect the template, and template updates do not propagate to existing instances.

### 5.3 Schema — new tables

#### `ProjectTemplate`

|Field                   |Type             |Notes                                                                                         |
|------------------------|-----------------|----------------------------------------------------------------------------------------------|
|`id`                    |string PK        |                                                                                              |
|`slug`                  |string, unique   |e.g., `septic-system`, `new-well`, `solar-ground-mount`.                                      |
|`title`                 |string           |“New Septic System”                                                                           |
|`category`              |enum             |`utilities`, `structures`, `landscape`, `access`, `other`. Used for grouping in the picker UI.|
|`description`           |markdown         |Short overview shown in the template picker.                                                  |
|`defaultObjective`      |markdown         |Populates the project’s `objective` field on instantiation.                                   |
|`defaultBudgetLowUsd`   |integer, nullable|Typical low-end budget. Instantiated project may override.                                    |
|`defaultBudgetHighUsd`  |integer, nullable|                                                                                              |
|`defaultDurationDays`   |integer, nullable|Typical project duration.                                                                     |
|`tags`                  |string array     |Freeform, e.g., `["off-grid", "regulated", "phase-1"]`.                                       |
|`version`               |integer          |Incremented when template content changes. Stored on instantiation for traceability.          |
|`createdAt`, `updatedAt`|timestamp        |                                                                                              |

#### `ProjectTemplateActivity`

|Field                          |Type                |Notes                                                                 |
|-------------------------------|--------------------|----------------------------------------------------------------------|
|`id`                           |string PK           |                                                                      |
|`templateId`                   |FK → ProjectTemplate|                                                                      |
|`title`                        |string              |                                                                      |
|`details`                      |markdown, nullable  |                                                                      |
|`defaultDurationDays`          |integer, nullable   |                                                                      |
|`sortOrder`                    |integer             |Manual ordering within the template.                                  |
|`suggestedStakeholderRoleLabel`|string, nullable    |e.g., “Licensed Septic Installer” — hint text, not an auto-assignment.|

#### `ProjectTemplateDependency`

|Field                  |Type                        |Notes                                               |
|-----------------------|----------------------------|----------------------------------------------------|
|`id`                   |string PK                   |                                                    |
|`templateId`           |FK → ProjectTemplate        |                                                    |
|`predecessorActivityId`|FK → ProjectTemplateActivity|                                                    |
|`successorActivityId`  |FK → ProjectTemplateActivity|                                                    |
|`type`                 |enum                        |`FS`, `SS`, `FF`, `SF` — same as Planning epic §6.2.|

### 5.4 Project instantiation — `templateOrigin` on Project

Extend the `Project` schema from Planning epic §5.1 with:

|Field            |Type             |Notes                                                                                                                |
|-----------------|-----------------|---------------------------------------------------------------------------------------------------------------------|
|`templateSlug`   |string, nullable |The source template’s slug. Null for projects created from scratch.                                                  |
|`templateVersion`|integer, nullable|The template version at instantiation time. Enables “this project is based on an older template version” hints later.|

No backfill needed — existing projects carry nulls.

### 5.5 Instantiation flow

1. User clicks “Add Project” on the Project Portfolio Overview page.
2. Picker appears: “Start from scratch” or “Use a template”, with templates grouped by category.
3. On template selection, a preview shows the default activities and their dependencies (rendered as the same Mermaid flowchart used elsewhere).
4. User confirms. The system creates the `Project`, all `Activity` records, and all `ActivityDependency` records, copying titles, details, durations, and dependency types verbatim. `sequence` is set to the end of the plan’s stack. Status defaults to `planned` for all activities.
5. User lands on the Project Detail page, ready to customize.

### 5.6 Initial template set (Phase 1)

Seeded via migration or a dedicated admin tool. Not user-authorable in v1.

|Slug                |Title                   |Category |
|--------------------|------------------------|---------|
|`septic-system`     |New Septic System       |utilities|
|`new-well`          |New Well                |utilities|
|`solar-ground-mount`|Ground-Mount Solar Array|utilities|
|`solar-rooftop`     |Rooftop Solar Array     |utilities|
|`orchard-planting`  |Orchard Planting        |landscape|
|`driveway-new`      |New Driveway            |access   |
|`fence-perimeter`   |Perimeter Fencing       |other    |
|`pond-excavation`   |Pond Excavation         |landscape|

Each template ships with 5–12 activities and their dependency chain. Exact activity content is editorial work to be captured in a follow-up spec (`templates_seed_content.md`), not this requirements doc.

### 5.7 Future: user-authored and shared templates

Out of scope for this epic. The schema is deliberately designed to accommodate user-scoped templates later (add `ownerUserId`, `visibility` fields). Not addressed here.

-----

## 6. Utility Services Reference Category

### 6.1 Motivation

The Planning epic’s five fixed reference categories (Zoning, Rainwater, Off-Grid, Permitting, Public Land) don’t house the questions every builder asks first: Is there water? Is there power? Can a truck get here? Where does sewage go? Is there internet? These are reference questions — what utilities exist at this parcel, under what terms — distinct from the project work of connecting to them.

### 6.2 Schema change — extend reference category enum

In `requirements_planning.md` §3.1, the reference category enum expands from five to six values. Add:

- `site_services_utilities` — label: “Site Services & Utilities”

### 6.3 Sub-topic hints (UI only, no schema change)

When a user creates a reference entry under `site_services_utilities`, the entry form offers a non-binding “Topic” suggestion dropdown:

- Water (well / public)
- Power (grid / solar / other)
- Access (roads / driveways / easements)
- Sewage (septic / public / other)
- Internet & Communications (satellite / cell / fiber / DSL)
- Other

This populates the entry’s `title` field as a starting point (“Water — “ prefix) but does not create a separate structured field. Keeps §3.2 schema unchanged.

### 6.4 Starter entries on property creation

When a new plan is created (or when a boundary is first confirmed), the system seeds **empty placeholder reference entries** under the new category — one per sub-topic in §6.3, with `title` set (“Water”, “Power”, etc.), `notes` empty, and `status = active`. Entries act as checklist prompts; users fill them in as they research.

These seeded entries have `source = 'system'`, distinguishing them from user and agent entries per §3.2. Users can delete any they don’t need.

### 6.5 MCP agent fit

The `site_services_utilities` category is a natural target for MCP agents (e.g., Claude Coworker) to populate: “look up whether public water reaches this parcel”, “find the nearest electric utility service territory”. Identity is already tracked via the `agentName` field from Planning epic §3.2. No additional schema needed.

### 6.6 Contractor visibility

Reference entries remain invisible to contractors per Planning epic §8.4. No change.

-----

## 7. Drive Folder Structure

No changes. Reference entry attachments under the new category still store in `LandPlan_Files/{plan}/Property/Ordinances/` per Planning epic §4. (“Ordinances” as a folder name is slightly off-target for utility info, but renaming it would create migration pain — leave it alone and revisit if the folder structure is overhauled in a future epic.)

-----

## 8. Phase 1 / Phase 2 Split

### Phase 1 (this epic)

- `MapObject` accuracy fields (`captureMethod`, `basemapContext`, `accuracyMeters`, `captureSource`, `capturedAt`, `accuracyNotes`) with migration defaults.
- Context-aware `basemap_traced` defaults with per-context quick-pick in the object creation flow.
- Accuracy badge UI on object properties panel; “Show accuracy” layer toggle in Map mode sidebar.
- Boundary accuracy prominent on Property Overview.
- KML/GeoJSON import dialog — source/accuracy step.
- Contractor Quote Package views display accuracy badges.
- “About coordinate accuracy” help article; first-boundary onboarding card.
- Stakeholder overview doc updated with GPS-as-foundation section.
- DIY Estimate rental line item extended with `rentalType`, `rentalDurationDays`, `neededByDate`, `notes`; totals logic updated.
- `ProjectTemplate`, `ProjectTemplateActivity`, `ProjectTemplateDependency` tables.
- `Project.templateSlug` and `Project.templateVersion` fields.
- Template picker UI on “Add Project”; instantiation flow.
- Initial eight seeded templates (content TBD in `templates_seed_content.md`).
- `site_services_utilities` reference category.
- Sub-topic suggestion dropdown on reference entry form.
- System-seeded placeholder entries on new plan / boundary confirmation.

### Phase 2 (deferred)

- Per-feature accuracy parsing from embedded KML/GeoJSON metadata (batch-level import works in Phase 1; per-feature HDOP parsing is a refinement).
- User-authored project templates.
- Shared/community templates.
- Accuracy-aware buffer rendering on the map canvas (beyond the Phase 1 toggle — e.g., automatic dashed outlines for red-tier objects).
- DB-level rename of `toolRentals` to `equipmentRentals`.
- “Ordinances” Drive subfolder rename or restructure.

-----

## 9. Explicitly Deferred (low-priority backlog)

These are recorded for traceability but are not planned against any near-term epic:

- **Generalized Quote Packages with `packageType`** to support equipment rental vendors and materials quotes. Extension of Planning epic §8. Requires scoped-visibility rules per package type, different quote submission fields per type, and a vendor-type entity.
- **Developer Edition** — multi-parcel portfolios, entitlement tracking, pro formas, enterprise tone. Explicitly out of scope for LandPlan’s current positioning.

-----

## 10. Open Items for Implementation

- Exact accuracy thresholds for red/amber/green tiers and the per-context defaults in §2.3.1 — current proposals are starting points; may need adjustment after contractor feedback and real-world measurement.
- Whether `basemapContext` should be prompted every time an object is created, or only when the user explicitly wants better accuracy (current design: quick-pick dropdown defaulting to `unspecified`, so users who don’t care aren’t slowed down).
- Whether `kml_import` and `geojson_import` should be merged into a single `file_import` enum value (with `captureSource` carrying the distinction). Current proposal keeps them separate for query convenience.
- Template seed content — authoring the activity lists and dependencies for the eight initial templates is substantive editorial work, tracked separately in `templates_seed_content.md`.
- Whether system-seeded placeholder reference entries (§6.4) should be suppressible per-plan (e.g., a “skip starter entries” checkbox on plan creation). Default on seems right; worth revisiting after user feedback.
- Handling of the dismissed onboarding card (§3.2) when a user re-promotes a boundary months later — should it reappear if the new boundary has substantially different accuracy? Leave suppressed for now.

-----

## 11. Synchronization Checklist

After this epic is approved, update:

- `requirements_planning.md` — cross-reference §3.1 (add sixth category), §5.1 (add `templateSlug`, `templateVersion`), §9 (rental schema extension).
- `architecture.md` — add accuracy fields to MapObject, add three new template tables, update Project table, note accuracy-aware rendering path.
- `build_roadmap.md` — sequence: (1) accuracy schema + migration, (2) accuracy UI, (3) import dialog, (4) DIY rental extension, (5) template tables + seed data, (6) template picker UI, (7) utility reference category + seeded entries, (8) help content and onboarding.
- Root `CLAUDE.md` — add `IMPORTANT`-flagged note that all new `MapObject` creations must set `captureMethod` explicitly (no silent defaults from the API layer — only the migration uses defaults).
- `LandPlan_Overview_for_Stakeholders.docx` — add the GPS-as-foundation section per §3.3.