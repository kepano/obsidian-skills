# LandPlan — Epic: Plan Sharing

**Version:** 1.0
**Date:** March 28, 2026
**Status:** Draft
**Depends on:** Phase 3 Web App (complete), backend `routes/sharing.ts` (complete)

---

## 1. Overview

Plan Sharing enables a plan owner to invite other users to view or contribute to their land plan. This is the first collaborative feature in LandPlan and is a prerequisite for gathering user feedback before the mobile app build. The backend sharing routes already exist; this epic covers the web UI, email notifications, permission enforcement across the full stack, and Google Drive access for contributors.

---

## 2. Roles & Permissions

LandPlan introduces three roles scoped to each plan:

| Capability | Owner | Contributor | Viewer |
|---|---|---|---|
| View map, layers, objects, photos, measurements | ✅ | ✅ | ✅ |
| Place/edit/delete objects | ✅ | ✅ | ❌ |
| Draw/edit polygons and lines | ✅ | ✅ | ❌ |
| Upload photos | ✅ | ✅ | ❌ |
| Import GeoJSON/KML files | ✅ | ✅ | ❌ |
| Upload 3D models (future) | ✅ | ✅ | ❌ |
| Create/rename layers | ✅ | ✅ | ❌ |
| Delete layers | ✅ | ❌ | ❌ |
| Edit layer symbology | ✅ | ✅ | ❌ |
| Reorder layers | ✅ | ✅ | ❌ |
| Use measurement tools (area, distance) | ✅ | ✅ | ✅ |
| Save/edit/delete measurements | ✅ | ✅ | ❌ |
| Create/edit/delete saved views | ✅ | ✅ | ❌ |
| Edit plan boundary | ✅ | ❌ | ❌ |
| Edit plan settings (name, center, zoom) | ✅ | ❌ | ❌ |
| Delete plan | ✅ | ❌ | ❌ |
| Invite guests (any role) | ✅ | ✅ | ❌ |
| Remove guests or change guest roles | ✅ | ❌ | ❌ |
| Leave a shared plan | N/A | ✅ | ✅ |

### 2.1 Role Rules

- Every plan has exactly one **Owner** — the user who created it. Ownership is not transferable in this epic.
- **Contributors** have full editing capabilities except: deleting layers, deleting objects created by other users, editing plan-level settings (name, boundary, center/zoom), and deleting the plan.
- **Viewers** have read-only access. All editing controls (toolbar buttons, context menus, drag handles) are hidden or disabled. Exception: viewers can use the measurement tools (area and distance) interactively, but the Save button on the measurement form is disabled.
- Both **Owner** and **Contributor** can invite new guests at any permission level (viewer or contributor).
- Only the **Owner** can remove a guest or change a guest's role between viewer and contributor.
- Guests (both viewer and contributor) can leave a shared plan at any time.

---

## 3. Functional Requirements

### 3.1 Share Dialog (`ShareDialog.tsx`)

**Entry point:** A share icon on each plan card on the dashboard, and a share button in the map view toolbar.

**Dialog contents:**

1. **Current members list** — Shows all users with access to the plan:
   - Owner row: avatar/initials, display name, email, "Owner" badge. Not removable.
   - Guest rows: avatar/initials, display name, email, role badge ("Contributor" or "View only").
     - Owner sees: role dropdown (to change between contributor/view-only) and a remove button (×) on each guest row.
     - Contributors see: the member list (read-only, no role change or remove controls).
     - Viewers see: the member list (read-only).

2. **Invite input** — An email text field + role selector (dropdown: "Contributor" or "View only") + "Invite" button. Visible to Owner and Contributor roles.

3. **Pending invites** — If an invited email does not match an existing LandPlan user, show the invite as "Pending" with the email and selected role. The owner can cancel pending invites.

4. **Leave plan** — For guest users, a "Leave plan" link/button at the bottom of the dialog. Triggers a confirmation dialog ("Are you sure you want to leave this plan? You will lose access unless re-invited.").

### 3.2 Invite Flow

1. Owner or Contributor opens the Share dialog and enters a guest's email address, selects a role, and clicks "Invite".
2. **Backend** checks if the email belongs to an existing LandPlan user:
   - **Existing user:** Creates a `PlanShare` record with `permission` set to `view` or `edit`. The plan immediately appears in the guest's "Shared with me" section.
   - **Non-existing user:** Creates a `PlanShare` record with the email and a `pending` status. The share auto-applies when the user registers with that email.
3. **Email notification** is sent to the invited email (see §3.5).
4. The Share dialog updates to show the new guest (or pending invite) without a full page reload.

### 3.3 Dashboard — "Shared with Me"

The dashboard (`routes/index.tsx`) currently shows "My Plans". Add a second section:

- **"Shared with me"** — Lists all plans where the current user is a guest (viewer or contributor).
- Each shared plan card shows:
  - Plan name
  - Owner's display name (e.g., "Owned by Jane Smith")
  - Permission badge: "View only" or "Contributor"
  - Share icon (opens Share dialog — behavior depends on the user's role per §3.1)
- Clicking a shared plan card opens the map view at the plan's saved center/zoom.
- The plan card context menu (or long-press on mobile-web) includes "Leave plan" for guests.

### 3.4 Permission Enforcement — Map View

When a **Viewer** opens a shared plan:

- All tool palettes (object placement, drawing, measurement, import) are **hidden**.
- Layer panel is visible but layer visibility toggles are the only interactive control; rename, reorder, symbology, and delete controls are hidden.
- Object popups show detail in read-only mode (no edit/delete buttons).
- Photo gallery is visible; photo upload button is hidden.
- Map style switcher and 3D terrain toggle remain functional (these are view preferences, not data mutations).
- Saved views are visible and navigable but the "Save view" button is hidden.
- Plan settings link is hidden.

When a **Contributor** opens a shared plan:

- All editing tools are available **except**: plan settings page, delete layer, and delete objects they did not create.
- The plan settings link in the sidebar is hidden.
- Layer delete button is hidden.
- Object delete button is hidden on objects where `capturedBy !== currentUser.id`.

### 3.5 Email Notifications

An invite email is sent when a user is shared on a plan. This requires setting up a transactional email service.

**Email provider:** Use a lightweight provider appropriate for the stack — e.g., Resend, SendGrid, or Amazon SES. Selection is an implementation detail; the requirement is reliable delivery with a verified sender domain (`landplan.app` or a subdomain like `mail.landplan.app`).

**Invite email contents:**

- **Subject:** "[Inviter name] shared a plan with you on LandPlan"
- **Body:**
  - Inviter name and the plan name
  - The permission level granted ("view" or "contribute")
  - A CTA button:
    - Existing user → links to the plan's map view
    - Non-existing user → links to the LandPlan registration page with an `?invite=<token>` query param so the share auto-applies after sign-up
- Keep the email template simple, plain-text-friendly, and branded with the LandPlan logo.

### 3.6 Google Drive Access for Contributors

All user-generated files (photos, future 3D models) are stored in the **plan owner's** Google Drive folder.

- When a **Contributor** uploads a photo or file, the backend uses the **plan owner's** stored Google Drive tokens to write to the owner's Drive folder for that plan.
- The contributor does **not** need to connect their own Google Drive.
- **Viewer** photo access: When a viewer browses photos, the backend serves thumbnails and full images using the owner's Drive tokens. The viewer sees photos in the gallery and in map popups as normal, but has no upload capability.
- **Edge case — owner's Drive disconnected:** If the plan owner has not connected Google Drive (or their tokens have expired), contributor photo uploads should fail gracefully with a message: "The plan owner's Google Drive is not connected. Photo upload is unavailable. Contact the plan owner." The upload button remains visible but the error is shown on attempt.

---

## 4. Data Model Changes

### 4.1 `PlanShare` Table Updates

The existing `PlanShare` table in the schema covers the core fields. Confirm/add:

```
PlanShare
  ├── id (UUID, PK)
  ├── planId → LandPlan (FK)
  ├── userId → User (FK, nullable — null when pending)
  ├── email (string — always stored, used for pending invites)
  ├── permission (enum: 'view' | 'edit')
  ├── status (enum: 'active' | 'pending')
  ├── invitedBy → User (FK — the user who created the invite)
  ├── invitedAt (timestamp)
  ├── acceptedAt (timestamp, nullable — set when pending invite resolves)
  ├── createdAt / updatedAt
```

- **Unique constraint:** `(planId, email)` — a user can only have one share record per plan.
- **Index:** `(email, status)` — for efficient lookup when a new user registers to auto-apply pending shares.
- **Index:** `(userId, status)` — for efficient "Shared with me" queries.

### 4.2 Registration Hook

When a new user registers, query `PlanShare` for rows matching their email with `status = 'pending'`. For each match, set `userId` to the new user's ID and `status` to `'active'`, and set `acceptedAt` to now.

---

## 5. API Changes

The backend `routes/sharing.ts` already implements core sharing endpoints. Verify and extend:

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `GET` | `/plans/:planId/shares` | List all shares for a plan | Owner, Contributor, Viewer |
| `POST` | `/plans/:planId/shares` | Create a new share (invite) | Owner, Contributor |
| `PATCH` | `/plans/:planId/shares/:shareId` | Update permission level | Owner only |
| `DELETE` | `/plans/:planId/shares/:shareId` | Remove a guest (owner) or leave (self) | Owner or the guest themselves |

### 5.1 Middleware: Permission Guard

Add a reusable middleware/helper that resolves the current user's role for a given plan:

- Check if `userId === plan.ownerId` → Owner
- Check `PlanShare` for `userId` + `planId` with `status = 'active'` → Contributor or Viewer
- No match → 403 Forbidden

Apply this guard to **all** plan-scoped routes (layers, objects, photos, measurements, paths, import, drive). Each route checks whether the resolved role meets the minimum required permission for that action.

### 5.2 Plans List Endpoint

Extend `GET /plans` (or add `GET /plans/shared`) to return plans shared with the current user, including the owner's display name and the user's permission level.

### 5.3 Email Sending

Add a backend service (`services/email.ts`) that sends transactional emails via the chosen provider. The invite endpoint (`POST /plans/:planId/shares`) calls this service after creating the share record.

---

## 6. Frontend Component Changes

### 6.1 New Components

| Component | Location | Description |
|---|---|---|
| `ShareDialog.tsx` | `components/sharing/` | Modal dialog per §3.1 |
| `MemberRow.tsx` | `components/sharing/` | Single row in the members list |
| `InviteForm.tsx` | `components/sharing/` | Email input + role selector + invite button |
| `PermissionBadge.tsx` | `components/ui/` | Reusable badge showing "Owner", "Contributor", or "View only" |

### 6.2 Modified Components

| Component | Change |
|---|---|
| `routes/index.tsx` (Dashboard) | Add "Shared with me" section; add share icon to all plan cards |
| `routes/plan/[planId].tsx` (Map view) | Read user role from plan context; pass to child components for conditional rendering |
| `LayerPanel.tsx` | Hide delete/rename/symbology/reorder controls for viewers; hide delete for contributors |
| `ObjectDetail.tsx` | Hide edit/delete for viewers; hide delete on others' objects for contributors |
| `MeasureTool.tsx` | Hide save/delete controls for viewers |
| `PhotoGallery.tsx` | Hide upload button for viewers |
| Tool palette components | Hide entirely for viewers |
| `planStore.ts` (Zustand) | Add `currentUserRole: 'owner' | 'contributor' | 'viewer'` to plan state |

### 6.3 Hooks

| Hook | Description |
|---|---|
| `useSharing.ts` | Fetch shares, invite, update role, remove, leave. Wraps `api-client/sharing.ts`. |
| `usePlanRole.ts` | Returns the current user's role for the active plan. Reads from `planStore`. |

---

## 7. Out of Scope (This Epic)

- Public share links (anyone-with-the-link access) — deferred as a nice-to-have.
- Real-time collaboration (live cursors, conflict resolution) — not needed for beta feedback.
- Ownership transfer.
- Notification center / in-app notification bell.
- Share permissions for the future mobile app (will be addressed in the mobile epic).
- 3D model viewing (separate epic, see §8).

---

## 8. Future Epic Reference: 3D Model Viewer

> *Not in scope for the sharing epic. Captured here for continuity with the build roadmap.*

The next epic after sharing adds the ability to upload, place, and view 3D models on the map. Models render on both flat 2D maps and on 3D terrain using the MapLibre + Three.js integration pattern demonstrated at: https://maplibre.org/maplibre-gl-js/docs/examples/add-a-3d-model-with-shadow-using-threejs/

Key capabilities:

- Upload glTF/GLB models (stored on plan owner's Google Drive)
- Place a model on the map at a specific lat/lng with rotation, scale, and elevation offset controls
- Render models in 2D mode (flat on map) and 3D terrain mode (floating at terrain elevation + offset)
- Shadow casting based on sun position (SunCalc integration)
- Model list panel with visibility toggles
- Contributor and Owner can add/edit/delete models; Viewers see models read-only (permission model from sharing epic applies)

---

## 9. Acceptance Criteria

### Sharing Core

- [ ] Plan owner can open Share dialog from dashboard plan card and from map view.
- [ ] Plan owner can invite a user by email with a chosen role (contributor or view-only).
- [ ] Contributor can invite a user by email with a chosen role.
- [ ] Invited existing user sees the plan in "Shared with me" immediately.
- [ ] Invited non-existing user receives an email; after registering, the plan appears in "Shared with me".
- [ ] Invite email is delivered with correct plan name, inviter name, permission level, and CTA link.
- [ ] Plan owner can change a guest's role between contributor and view-only.
- [ ] Plan owner can remove a guest.
- [ ] Guest can leave a shared plan (with confirmation).
- [ ] Pending invites are shown in the Share dialog and are cancellable by the owner.

### Permission Enforcement

- [ ] Viewer sees no editing controls in map view (tools, layer edit, object edit, photo upload) except measurement tools.
- [ ] Viewer can use measurement tools (area, distance) but the Save button is disabled.
- [ ] Viewer can toggle layer visibility, switch map styles, toggle 3D terrain, and navigate saved views.
- [ ] Contributor can edit objects, upload photos, create layers, import files, and save measurements.
- [ ] Contributor cannot delete layers, edit plan settings, delete the plan, or delete objects created by others.
- [ ] All plan-scoped API endpoints enforce role-based permissions server-side (not just UI hiding).

### Google Drive

- [ ] Contributor photo uploads are written to the plan owner's Google Drive using the owner's tokens.
- [ ] Viewer can browse and view photos stored on the owner's Drive.
- [ ] If owner's Drive is disconnected, contributor upload fails gracefully with an informative message.

### Dashboard

- [ ] Dashboard shows "Shared with me" section with correct plan name, owner name, and permission badge.
- [ ] Share icon appears on all plan cards (owned and shared).
- [ ] Shared plan cards include "Leave plan" in the context menu.

---

## 10. Implementation Notes

- **Backend sharing routes** (`routes/sharing.ts`) and **api-client endpoints** (`endpoints/sharing.ts`) already exist. Audit them against this spec before building UI — they may need the `status`, `email`, `invitedBy` fields and the permission guard middleware.
- **PlanShare schema** in Prisma may need a migration to add `status`, `email`, and `invitedBy` columns if not already present.
- **Transactional email** is a new infrastructure concern. Evaluate Resend (simple API, good DX) vs. SendGrid (more established). Either way, add a `MAIL_API_KEY` secret to Secret Manager and the Cloud Run env config.
- **DNS for email:** If using a custom sender domain, add SPF/DKIM/DMARC records to `dns.tf`.
- The `ShareDialog.tsx` stub already exists in the component tree at `components/sharing/`. It needs to be implemented.
- The `@landplan/shared` types package already has `SharePermission` in `types/user.ts`. Extend as needed.

---

## 11. Implementation Sessions

The epic is split into 6 focused sessions, each deployable to production independently.

| Session | Scope | Deploy? |
|---|---|---|
| **1** | Prisma schema migration (`PlanShare` v2) + `@landplan/shared` types | Yes — additive only |
| **2** | API rewrite: pending invites, contributor access, auth register auto-apply, fix api-client | Yes |
| **3** | Terraform secrets + Resend email service + DNS SPF/DKIM | Yes (Terraform first, then API image) |
| **4** | `planAccess.ts` middleware, replace 6 duplicated `canAccess` helpers across all routes | Yes — validate carefully |
| **5** | ShareDialog, MemberRow, InviteForm, PermissionBadge, useSharing hook, dashboard "Shared with me" | Yes |
| **6** | usePermissions hook, role-based conditional rendering across all map components | Yes — final E2E verification |

### Session 1 — Schema Migration + Shared Types ✅
**Files changed:**
- `packages/api/prisma/schema.prisma` — PlanShare updated (nullable userId, email, status, invitedBy; new unique constraint)
- `packages/api/prisma/migrations/20260328000000_planshare_v2/migration.sql` — idempotent SQL
- `packages/shared/src/types/user.ts` — added `PlanRole`, `ShareStatus`, updated `PlanShare`, added `PlanShareUpdateInput`

**Deployment verification:**
- Migration runs clean (check Cloud Run startup logs)
- `SELECT status, COUNT(*) FROM "PlanShare" GROUP BY status` — all existing rows show `active`
- All existing `GET /plans` requests return 200

### Session 2 — API Rewrite
**Files to change:**
- `packages/api/src/routes/sharing.ts` — full rewrite: pending invites, contributor access, new route map
- `packages/api/src/routes/auth.ts` — add pending share auto-apply on registration
- `packages/api/src/routes/plans.ts` — include shared plans; `acceptedAt` → `status`
- `packages/api/src/routes/layers.ts`, `objects.ts`, `photos.ts`, `paths.ts`, `measurements.ts`, `saved-views.ts` — change `acceptedAt: { not: null }` → `status: 'active'` in all local canAccess helpers
- `packages/api-client/src/endpoints/sharing.ts` — fix URL paths, add missing methods

**New route map:**
```
GET    /plans/:planId/shares           — owner or contributor
POST   /plans/:planId/shares           — owner or contributor (pending invite if email unknown)
PATCH  /plans/:planId/shares/:shareId  — owner only (change role)
DELETE /plans/:planId/shares/:shareId  — owner removes any share
DELETE /plans/:planId/shares/me        — any member leaves
GET    /plans/shared                   — plans shared with current user
```

### Session 3 — Infrastructure + Email
**Files to change:**
- `infra/terraform/secrets.tf` — add `MAIL_API_KEY` secret
- `infra/terraform/cloud-run.tf` — inject `MAIL_API_KEY` into API container
- `infra/terraform/dns.tf` — SPF + DKIM TXT records for `landplan.app`
- `packages/api/src/config/env.ts` — add optional `MAIL_API_KEY`, `MAIL_FROM`
- `packages/api/src/services/email.ts` — new Resend wrapper
- `packages/api/src/routes/sharing.ts` — wire email call into POST handler

**Deployment order:** `terraform apply` → populate secret via `gcloud secrets versions add MAIL_API_KEY` → deploy API image.

### Session 4 — Permission Enforcement Middleware
**Files to change:**
- `packages/api/src/middleware/planAccess.ts` — new: `requirePlanAccess`, `requirePlanWrite`, `requirePlanOwner`
- All route files — replace local helpers with middleware hooks

**Safety:** Owner access is always `plan.ownerId === request.userId` — never via `PlanShare`. Schema changes cannot lock out owners.

### Session 5 — Frontend ShareDialog + Dashboard
**New files:** `useSharing.ts`, `ShareDialog.tsx`, `MemberRow.tsx`, `InviteForm.tsx`, `PermissionBadge.tsx`
**Modified:** `planStore.ts` (add `currentUserRole`), `PlanPage.tsx` (Share button), `DashboardPage.tsx` (role badges)

### Session 6 — Frontend Permission Rendering
**New files:** `usePermissions.ts`
**Modified:** `PlanPage.tsx`, `MapToolbar.tsx`, `LayerPanel.tsx`, `ObjectDetail.tsx`, `MeasureTool.tsx`, `PhotoGallery.tsx`, `SavedViewsPanel.tsx`

---

## 12. Database Migration

Migration file: `packages/api/prisma/migrations/20260328000000_planshare_v2/migration.sql`

The migration is **idempotent** — safe to run multiple times and safe against a database with existing data. All DDL uses `IF NOT EXISTS` / `IF EXISTS`. New `NOT NULL` columns follow the three-step pattern: add nullable → backfill → enforce.

```sql
-- Step 1: Add new nullable columns
ALTER TABLE "PlanShare" ADD COLUMN IF NOT EXISTS "email"     TEXT;
ALTER TABLE "PlanShare" ADD COLUMN IF NOT EXISTS "status"    TEXT;
ALTER TABLE "PlanShare" ADD COLUMN IF NOT EXISTS "invitedBy" TEXT;

-- Step 2: Backfill
UPDATE "PlanShare" SET "email"  = "userEmail" WHERE "email"  IS NULL;
UPDATE "PlanShare" SET "status" = CASE
  WHEN "acceptedAt" IS NOT NULL THEN 'active'
  ELSE 'pending'
END WHERE "status" IS NULL;

-- Step 3: Enforce NOT NULL
ALTER TABLE "PlanShare" ALTER COLUMN "email"  SET NOT NULL;
ALTER TABLE "PlanShare" ALTER COLUMN "status" SET NOT NULL;

-- Step 4: Make userId nullable (drop FK, drop NOT NULL, re-add FK)
ALTER TABLE "PlanShare" DROP CONSTRAINT IF EXISTS "PlanShare_userId_fkey";
ALTER TABLE "PlanShare" ALTER COLUMN "userId" DROP NOT NULL;
ALTER TABLE "PlanShare" ADD CONSTRAINT "PlanShare_userId_fkey"
  FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- Step 5: invitedBy FK (nullable)
ALTER TABLE "PlanShare" ADD CONSTRAINT "PlanShare_invitedBy_fkey"
  FOREIGN KEY ("invitedBy") REFERENCES "User"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- Step 6: Swap unique constraint
DROP INDEX IF EXISTS "PlanShare_planId_userId_key";
CREATE UNIQUE INDEX IF NOT EXISTS "PlanShare_planId_email_key" ON "PlanShare"("planId", "email");

-- Step 7: Supporting indexes
CREATE INDEX IF NOT EXISTS "PlanShare_email_status_idx"  ON "PlanShare"("email",  "status");
CREATE INDEX IF NOT EXISTS "PlanShare_userId_status_idx" ON "PlanShare"("userId", "status");
```

### Production safety rules

| Rule | Detail |
|---|---|
| Idempotent DDL | Every statement uses `IF NOT EXISTS` or `IF EXISTS` |
| 3-step NOT NULL | Add nullable → backfill → `SET NOT NULL` |
| Never modify applied migrations | Prisma checksums will reject altered files |
| Constraint swap order | Drop old index before creating new one |
| FK before nullable | Drop FK → drop NOT NULL → re-add FK |
| Owner safety | Owner access via `ownerId` is independent of the share table at all times |
