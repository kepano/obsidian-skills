---
title: Tags System — Backlog
tags: [landplan, backlog, tags, map-objects, feature]
created: 2026-04-18
updated: 2026-04-18
status: seedling
---

# Tags System (Map Object Categories)

*From stakeholder review, April 2026. Current implementation uses a fixed category dropdown on map objects.*

---

## Current State (Database Snapshot)

### Well-used Categories (from the dropdown)

| Category | Count |
|----------|-------|
| Photo | 9 |
| Structure | 8+1 (case mismatch: `Structure` / `structure`) |
| Water | 6+2 (case mismatch: `Water` / `water`) |
| Gate | 5 |
| Hazard | 4 |
| Other | 3 |
| Marker | 2 |
| Tree | 2 |
| Shrub | 1 |
| Fence | 1 |
| Road | 1 |
| Path | 1 |
| Utility | 1 |

### Freeform / Test Data (not from dropdown)

- `RAVINE 1` through `RAVINE 9` — label put in category field (test data issue)
- `Driveway Lunch Hiking` — same issue
- `Service Road` — reasonable but not in current dropdown list

---

## Notable Gaps & Issues

1. **`Photo` is top category but not in the dropdown** — appears to be set programmatically when a photo-linked point is created. Should be either a real first-class category or hidden from user-facing dropdown.
2. **Case inconsistencies** — `Structure` / `structure`, `Water` / `water` — worth normalising.
3. **`Service Road` gap** — users want road subtypes (Road, Path, Service Road, Driveway).
4. **RAVINEs and other freeform data** — suggests users want an open text label field, not just a fixed category dropdown.

---

## Proposed Direction

Update categories to a **more flexible tagging framework** (open tags vs fixed category dropdown). Tags should not conflict with Layers or Views.

Photos are so common that they should be a top-visibility option — not buried as a custom layer. Consider extracting photos from the layers system.

---

## Considerations

- Avoid breaking existing category filters and layer groupings
- The new tagging framework needs to coexist with the [[epic-planning|Planning epic]]'s project associations
- Case normalisation should happen in a migration (consolidate `Structure` + `structure` → `Structure`)

---

## Related

- [[landplan-app]] — the product this affects
- [[epic-planning]] — project associations on map objects
