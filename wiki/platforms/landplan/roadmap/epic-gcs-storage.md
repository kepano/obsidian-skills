---
title: "Epic: GCS Storage Overhaul"
tags: [landplan, epic, storage, gcs, google-cloud, done]
created: 2026-04-18
updated: 2026-04-18
status: evergreen
epic: gcs-storage
priority: 1
---

# Epic: GCS Storage Overhaul

**Status:** Done  
**Depends on:** Plan Sharing epic (permission model)

---

## Objective

Replace Google Drive as the file storage backend with Google Cloud Storage (GCS), using signed URLs for all file transfers. User research confirmed users care about reliable sharing and data portability, not where files are physically stored.

**Clean cut: no production users with Drive-linked data, so no migration needed.**

---

## What Was Removed

- All server-side Google Drive OAuth token delegation for file storage
- Drive API calls for upload, download, listing, and delete
- Active use of `driveFileId` fields for storage routing (nullable fields preserved in schema)
- Requirement for users to connect Google Drive during onboarding (for file features)
- Drive-specific folder creation or naming logic

---

## What Was Built

### GCS Bucket Structure

One bucket per environment (dev/staging/prod), IAM-controlled:

```
plans/{planId}/property/ordinances/{fileId}_{filename}
plans/{planId}/property/boundary/{fileId}_{filename}
plans/{planId}/photos/{fileId}_{filename}
plans/{planId}/models/{fileId}_{filename}
plans/{planId}/projects/{projectId}/{fileId}_{filename}
plans/{planId}/projects/{projectId}/activities/{activityId}/{fileId}_{filename}
plans/{planId}/quote-packages/{packageId}/{fileId}_{filename}
```

GCS Autoclass enabled — objects transition Standard → Nearline → Coldline automatically.

### Upload Flow (signed URL)

1. Client requests signed upload URL from API
2. API validates auth + plan membership + role → generates GCS signed URL (PUT, 15-min expiry)
3. Client uploads directly to GCS — **file bytes never pass through the API server**
4. Client notifies API on completion; API writes `PlanFile` metadata record to DB

### Download Flow

1. Client requests signed download URL for a `fileId`
2. API validates auth + plan membership → generates GCS signed URL (GET, 60-min expiry)
3. Client uses signed URL directly — no API proxying

### PlanFile Table

```
id            uuid PK
planId        FK → Plan
objectKey     string (GCS object key, immutable after upload)
filename      string (display name)
mimeType      string
sizeBytes     integer
context       enum: photo | model | document | boundary
contextEntityId nullable uuid (projectId, activityId, etc.)
uploadedBy    FK → User
createdAt     timestamp
deletedAt     nullable timestamp (soft delete)
```

### Access Control on Signed URLs

| Role | Upload | Download |
|------|--------|----------|
| Owner / Contributor | ✅ | ✅ |
| Viewer / Stakeholder | ❌ | ✅ (for plans they're members of) |
| Contractor (quote) | ❌ | ✅ (scoped to their package files only) |

---

## What Did NOT Change

- Logical file organization (which files belong to which plan/project/activity)
- File attachment patterns in API and frontend
- Photo EXIF/location metadata handling
- 3D model attachment flow (objectKey replaces driveFileId)

---

## Related

- [[architecture]] — PlanFile table details
- [[epic-plan-export]] — portability epic that builds on this storage layer
- [[epic-3d-models]] — 3D model uploads now use GCS
