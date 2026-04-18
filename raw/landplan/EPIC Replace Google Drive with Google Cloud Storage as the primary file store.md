
## Context
LandPlan currently stores all user-uploaded files — photos, 3D models, documents,
boundary exports — on the plan owner's Google Drive via server-side OAuth token
delegation. We are replacing this with Google Cloud Storage (GCS) as the operational
store for all binary assets. Google Drive is being removed as a storage backend
entirely.

User research confirmed that users do not care about where files are physically stored.
They care that sharing works reliably and that they can export their data if they want
it. A separate Export epic will handle portability. This epic handles the infrastructure
replacement only.

There are no production users with existing Drive-linked data. This is a clean cut —
no migration needed.

## Objective
Remove all Google Drive file storage logic and replace it with GCS-backed storage
using signed URLs for uploads and downloads. The logical folder structure and
file-attachment patterns should be preserved; only the backing store changes.

## What to remove
- All server-side Google Drive OAuth token delegation used for file storage
- Drive API calls for upload, download, listing, and delete of plan files
- Any driveFileId fields actively used for storage routing (preserve nullable fields
  in schema where they exist for forward-compatibility notes, but stop writing to them)
- The requirement for users to connect Google Drive during onboarding (if currently
  enforced for file features)
- Any Drive-specific folder creation or naming logic

## What to build

### GCS bucket structure
Mirror the existing logical folder structure as GCS object key prefixes:

  plans/{planId}/property/ordinances/{fileId}_{filename}
  plans/{planId}/property/boundary/{fileId}_{filename}
  plans/{planId}/photos/{fileId}_{filename}
  plans/{planId}/models/{fileId}_{filename}
  plans/{planId}/projects/{projectId}/{fileId}_{filename}
  plans/{planId}/projects/{projectId}/activities/{activityId}/{fileId}_{filename}
  plans/{planId}/quote-packages/{packageId}/{fileId}_{filename}

Use a single GCS bucket per environment (dev/staging/prod), with IAM-controlled
access from the API service account. Do not use per-user or per-plan buckets.

### Upload flow
- Client requests a signed upload URL from the API
- API validates auth, checks plan membership and role, generates a GCS signed URL
  (PUT, 15-minute expiry) for the correct key prefix
- Client uploads directly to GCS using the signed URL — file bytes never pass
  through the API server
- Client notifies API on completion; API writes the file metadata record to the DB
  (fileId, planId, objectKey, filename, mimeType, sizeBytes, uploadedBy, createdAt)

### Download / serving flow
- Client requests a signed download URL from the API for a given fileId
- API validates auth and plan membership, generates a GCS signed URL (GET,
  60-minute expiry)
- Client uses the signed URL directly — no proxying through the API

### File metadata table
Create a PlanFile table (or equivalent name consistent with existing conventions):

  id              uuid PK
  planId          FK → Plan
  objectKey       string (GCS object key, immutable after upload)
  filename        string (original filename for display)
  mimeType        string
  sizeBytes       integer
  context         enum: photo | model | document | boundary
  contextEntityId nullable uuid (projectId, activityId, etc. for scoped files)
  uploadedBy      FK → User
  createdAt       timestamp
  deletedAt       nullable timestamp (soft delete)

### Delete flow
Soft-delete the DB record on user delete action. Schedule GCS object deletion
async (or via a nightly cleanup job) — do not block the API response on GCS delete.

### Access control
All signed URL generation must enforce plan role:
- owner and contributor: upload + download
- viewer and stakeholder: download only, for plans they are members of
- contractor_quote: download only, scoped to their quote package's files
No signed URL is ever issued without a valid session and role check.

### Autoclass
Enable GCS Autoclass on the bucket so objects transition automatically between
Standard, Nearline, and Coldline based on access patterns. No manual lifecycle
rules needed.

## What does NOT change
- The logical organization of files (which files belong to which plan, project,
  activity, etc.)
- File attachment patterns in the API and frontend — the surface area stays the same,
  only the backing store changes
- Photo EXIF/location metadata handling
- The 3D model attachment flow (objectKey replaces driveFileId as the file reference)

## Reference files to consult
Read architecture.md before starting. The Drive integration is documented there;
this epic supersedes that section. Update architecture.md to reflect GCS as the
file store once the implementation is complete.

## Definition of done
- No Drive API calls remain in the codebase for file storage purposes
- All file uploads go through the signed URL flow
- All file downloads use signed URLs
- Plan sharing works end-to-end without any Drive dependency
- The PlanFile table is the authoritative record of all files
- architecture.md updated to reflect the new storage model
- Existing photo capture, 3D model upload, and document attach flows all work
  against GCS in local dev using the GCS emulator or a dev bucket
