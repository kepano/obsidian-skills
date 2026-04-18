
## Context
LandPlan stores all plan files in Google Cloud Storage (GCS), completed in the
Storage Overhaul epic. Users who want their data in a personal cloud (Drive,
iCloud, Dropbox, etc.) can export it on demand. This epic builds that export
capability. The product principle: LandPlan is the operational home for plan data;
export is the portability story.

Initial scope: browser zip download and Google Drive export. iCloud and Dropbox
are explicitly deferred.

## What to build

### Export contents
A full plan export contains:

1. **GeoJSON** — all map objects for the plan, each Feature including:
   - geometry (point, linestring, polygon as drawn)
   - properties: objectId, name, type, all user-set attributes, linked projectId
     if any, photo references
   - A separate Feature for the property boundary if set
   Export as a single FeatureCollection per plan: {planId}_map.geojson

2. **Photos** — all photos attached to the plan, as original files, preserving
   EXIF metadata. Organized in the zip as: photos/{filename}

3. **3D model files** — all GLB/glTF files attached to the plan:
   models/{filename}

4. **Documents** — all user-uploaded documents (PDFs, images, etc.) attached to
   projects, activities, quote packages, or property reference entries:
   documents/{context}/{filename}
   where context is the logical grouping (e.g., projects/barn-build, property/zoning)

5. **Plan data JSON** — a structured machine-readable export of the full plan:
   {planId}_plan.json

   This file should include:
   - Plan metadata (name, createdAt, missionStatement, jurisdiction, APN)
   - Property boundary reference (pointing to the GeoJSON file)
   - Projects array, each with: title, objective, sequence, status, dates, budget,
     and their activities array
   - Each activity: title, details, status, dates, dependencies, assigned stakeholders
   - Stakeholders list (name, email, roleLabel — no internal IDs)
   - Reference information entries (category, title, notes, links)
   - File manifest: list of all files included in the export with their context

6. **README.txt** — a plain-text file at the zip root explaining:
   - What LandPlan is
   - What each file/folder in the export contains
   - That GeoJSON can be opened in Google Earth, QGIS, ArcGIS, or any GIS tool
   - landplan.app URL

### Zip structure
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

### Export generation — API
POST /plans/:planId/export
- Auth required; owner or contributor role only
- Validates plan membership
- Generates the GeoJSON, plan JSON, and README in memory
- Fetches all file object keys from the PlanFile table for this plan
- Streams the zip to the response (do not buffer the full zip in memory;
  use a streaming zip library)
- Sets Content-Disposition: attachment; filename="{planName}_{date}.zip"
- GCS file bytes are streamed directly into the zip — do not write temp files
  to disk on the API server

For large plans this may take several seconds. Return a 202 with a jobId and
poll endpoint if streaming proves impractical, but try streaming first.

### Export UI — browser download
- "Export plan" option accessible from the plan settings or share menu
- Single button: "Download zip"
- Shows a progress/spinner while the API generates the export
- Browser initiates the download on completion
- No special UI beyond the trigger and loading state

### Export UI — Google Drive
- Second option on the same export panel: "Save to Google Drive"
- Requires the user to grant Drive write scope (files.create) via OAuth if not
  already granted — this is separate from any previous Drive connection and
  is opt-in at export time
- On grant, the API uploads the zip to the user's Drive root (or a
  LandPlan Exports/ folder if one exists or can be created) using the user's
  own OAuth token — the user's Drive, not a service account
- Show the resulting Drive file link on completion
- Drive scope is requested only when the user explicitly chooses this export path;
  never requested proactively

### Access control
- Export is owner/contributor only — viewers, stakeholders, and contractors
  cannot export
- Drive OAuth token is stored per-user and refreshed as needed; revocable by
  the user at any time from account settings

## What does NOT change
- The GCS storage structure — export reads from GCS, does not move or delete anything
- Plan sharing, file upload, or any other feature
- iCloud and Dropbox are explicitly out of scope for this epic

## Definition of done
- Browser zip download works for a plan with photos, models, documents, and projects
- GeoJSON export is valid and opens correctly in QGIS or geojson.io
- Plan JSON export contains complete project/activity/stakeholder data
- Google Drive export saves the zip to the user's Drive and returns a link
- Export is gated to owner/contributor roles
- Export panel is accessible from the plan UI without being prominent
  (this is a utility feature, not a primary flow)
