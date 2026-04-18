---
title: Feature Ideas — Backlog
tags: [landplan, backlog, features, ideas]
created: 2026-04-18
updated: 2026-04-18
status: seedling
---

# LandPlan Feature Ideas

*Unscheduled ideas and deferred features. Not committed to any epic.*

---

## From Epic Reviews (Explicitly Deferred)

### From GPS Accuracy epic

- **Generalized Quote Packages with `packageType`** — support equipment rental vendors and materials quotes; needs scoped-visibility rules, different quote submission fields, vendor-type entity
- **Developer Edition** — multi-parcel portfolios, entitlement tracking, pro formas, enterprise tone; out of scope for LandPlan's current consumer positioning

### From Trees epic

- Seasonal appearance (fall colors, bare winter trees) — schema `seasonal: boolean` reserved
- LOD (Level of Detail) — schema `lodDistanceThresholds` reserved
- DEM terrain conformance for Tree Stands — `getElevation()` interface defined; implementation deferred
- Wind / environmental response — schema fields exist but not evaluated
- Visible branch geometry — schema fields exist; only trunk + crown in Phase 1
- glTF export of procedural trees
- Custom species creation by users
- Individual-tree rendering within Tree Stands
- Tree stand polygon import from GeoJSON / KML
- Mobile app tree support

### From Planning epic

- Dedicated Contractor Quote Package UI (future Stitch pass)
- Dedicated DIY Estimate editor UI
- Dedicated Stakeholder management screen
- Mermaid Gantt view and drag-to-connect dependency editing
- Parcel data integration (Regrid, county GIS)
- PAD-US public land proximity detection
- Full audit history UI
- Cross-project activity dependencies

### From GPS Accuracy / Templates epic

- Per-feature accuracy parsing from embedded KML/GeoJSON metadata (HDOP)
- User-authored and shared project templates
- Accuracy-aware buffer rendering on map canvas

---

## Marketing & SEO / AEO Ideas

*From LandPlan.app brainstorm.*

- LandPlan Marketing + SEO / AEO strategy (no details captured yet)
- Help Guides and Training (end-user docs)

---

## Competitive Feature Gaps to Address

*Based on [[competitive-analysis]] — features competitors have that LandPlan should eventually prioritise:*

- Nationwide parcel data and ownership details
- Rich GIS layers: soil, floodplains, contours
- Mobile offline access (→ [[survey-mobile]])
- Map sharing by embed, link, or email (public share)

---

## Related

- [[competitive-analysis]] — market context for prioritisation
- [[landplan-app]] — the product
