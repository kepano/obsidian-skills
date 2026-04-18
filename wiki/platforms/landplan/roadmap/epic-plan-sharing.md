---
title: "Epic: Plan Sharing"
tags: [landplan, epic, sharing, collaboration, done]
created: 2026-04-18
updated: 2026-04-18
status: evergreen
epic: plan-sharing
priority: 1
---

# Epic: Plan Sharing

**Status:** Done  
**Version:** 1.0 (March 28, 2026)  
**Depends on:** Phase 3 Web App (complete), backend `routes/sharing.ts` (complete)

---

## Objective

Enable a plan owner to invite other users (Viewer or Contributor) to view or contribute to their land plan. First collaborative feature; prerequisite for gathering user feedback before the mobile app build.

---

## Roles & Permissions

| Capability | Owner | Contributor | Viewer |
|-----------|-------|------------|-------|
| View map, layers, objects, photos, measurements | ✅ | ✅ | ✅ |
| Place / edit / delete objects | ✅ | ✅ | ❌ |
| Upload photos | ✅ | ✅ | ❌ |
| Import GeoJSON / KML | ✅ | ✅ | ❌ |
| Upload 3D models | ✅ | ✅ | ❌ |
| Create / rename layers | ✅ | ✅ | ❌ |
| Delete layers | ✅ | ❌ | ❌ |
| Edit plan boundary / settings | ✅ | ❌ | ❌ |
| Delete plan | ✅ | ❌ | ❌ |
| Invite guests (any role) | ✅ | ✅ | ❌ |
| Remove guests / change roles | ✅ | ❌ | ❌ |
| Leave a shared plan | N/A | ✅ | ✅ |
| Use measurement tools (interactive) | ✅ | ✅ | ✅ |
| Save measurements | ✅ | ✅ | ❌ |

### Role Rules

- Every plan has exactly one **Owner** (the creator; not transferable in this epic)
- Contributors have full editing except: deleting layers, deleting others' objects, editing plan-level settings, deleting the plan
- Viewers: read-only; editing controls hidden/disabled
- Owner and Contributor can both invite new guests
- Only Owner can remove guests or change guest roles
- Guests can leave a plan at any time

---

## Key Flows

### Share Dialog (`ShareDialog.tsx`)

Entry: share icon on plan card (dashboard) and share button in map view toolbar.

- Current members list with role badges (Owner not removable)
- Invite input: email field + role dropdown (Contributor / View only) + Invite button
- Pending invites visible (owner can cancel)
- "Leave plan" link for guests

### Invite Flow

1. Owner/Contributor enters email + role → clicks Invite
2. Backend checks if email belongs to existing user:
   - Existing user: `PlanShare` record created; plan appears immediately in guest's "Shared with me"
   - Non-user: pending `PlanShare`; auto-applies when user registers
3. Email notification sent via SendGrid/Resend

---

## Related

- [[architecture]] — role enum and authorization rules
- [[epic-planning]] — extends role model with Stakeholder and Contractor roles
