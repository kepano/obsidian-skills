---
title: "Epic: Plan Export"
tags: [landplan, epic, export, portability, planned]
created: 2026-04-18
updated: 2026-04-18
status: seedling
epic: plan-export
priority: 3
---

# Epic: Plan Export

**Status:** Planned  
**Depends on:** [[epic-gcs-storage|GCS Storage Overhaul]] (complete)

---

## Objective

Let users export their full plan data as a portable zip download or to Google Drive. LandPlan is the operational home; export is the portability story.

Scope: browser zip download + Google Drive export. iCloud and Dropbox explicitly deferred.

---

## Export Contents

A full plan export contains:

1. **GeoJSON** (`{planId}_map.geojson`) — all map objects; each Feature includes geometry, properties, linked projectId, photo references. Separate Feature for property boundary.
2. **Photos** (`photos/{filename}`) — original files, EXIF preserved
3. **3D model files** (`models/{filename}`) — all GLB/glTF files
4. **Documents** (`documents/{context}/{filename}`) — all user-uploaded docs for projects, activities, quote packages, property reference entries
5. **Plan data JSON** (`{planId}_plan.json`) — plan metadata, boundary reference, projects array (with activities), stakeholders list, reference info entries, file manifest
6. **README.txt** — explains what each file/folder contains; mentions GeoJSON compatibility (QGIS, Google Earth, ArcGIS)

### Zip Structure

```
{planName}_{exportDate}/
├── README.txt
├── {planId}_map.geojson
├── {planId}_plan.json
├── photos/
├── models/
└── documents/
    ├── property/
    │   ├── ordinances/
    │   └── boundary/
    └── projects/
        └── {project-slug}/
            └── activities/
                └── {activity-slug}/
```

---

## API

`POST /plans/:planId/export`
- Owner or Contributor only
- Generates GeoJSON, plan JSON, README in memory
- Fetches all file object keys from `PlanFile` table
- **Streaming zip** (do not buffer full zip in memory; do not write temp files to API server)
- GCS file bytes streamed directly into the zip
- `Content-Disposition: attachment; filename="{planName}_{date}.zip"`
- For large plans: try streaming first; fall back to 202 + jobId + poll endpoint if impractical

---

## Export UI

### Browser Download

- "Export plan" option in plan settings or share menu
- Single button: "Download zip"
- Progress/spinner while generating; browser download on completion

### Google Drive Export

- Second option on same export panel: "Save to Google Drive"
- Requires user to grant Drive `files.create` OAuth scope (opt-in at export time; never requested proactively)
- On grant: API uploads zip to user's Drive root (or `LandPlan Exports/` folder)
- Shows resulting Drive file link on completion
- Drive OAuth token stored per-user; refreshable; revocable from account settings

---

## Access Control

- Owner / Contributor only (Viewers, Stakeholders, Contractors cannot export)
- Drive OAuth separate from any previous Drive connection

---

## What Does NOT Change

- GCS storage structure (export reads from GCS; nothing moved or deleted)
- Plan sharing, file upload, or any other feature

---

## Related

- [[epic-gcs-storage]] — the storage layer this reads from
- [[architecture]] — PlanFile table structure
- [[landplan-app]] — export is a utility feature (not a primary flow)
