---
title: LandPlan Survey (Mobile App)
tags: [landplan, mobile, ios, android, gps, survey, product]
created: 2026-04-18
updated: 2026-04-18
status: seedling
---

# LandPlan Survey (Mobile App)

> [!abstract] One-liner
> A native iOS and Android mobile app for collecting GPS measurements in the field and syncing them to [[landplan-app]].

---

## What It Does

LandPlan Survey lets a property owner walk their land and capture GPS points, lines, and polygons that sync directly into their LandPlan.app plan. It closes the gap between the office (web app) and the field (real ground-truth data).

### Core Capabilities (Planned)

- Capture GPS waypoints, distance polylines, and area polygons in the field
- Offline-first data collection; sync to [[landplan-app]] on connectivity
- Connect to [[survey-gps-receiver]] via Bluetooth for survey-grade accuracy
- Geolocated photo capture attached to map objects
- Write `captureMethod`, `accuracyMeters`, `captureSource`, and `capturedAt` directly — feeds into the [[epic-gps-accuracy-templates|GPS accuracy metadata]] system
- View existing plan objects on the mobile map for context

---

## Status

**Not yet started.** Explicitly deferred from the Planning epic and all current epics.

Data model in [[landplan-app]] is forward-compatible with mobile (accuracy fields, `captureMethod` enum, etc.).

---

## Platform Targets

- iOS (native)
- Android (native)

Stack TBD. Offline-first architecture required.

---

## Competitive Context

onX Hunt demonstrates consumer willingness to pay $30–100/yr for good mobile land tools. LandPlan Survey would give that same audience a connection back to their property plan — something onX never offers.

---

## Related

- [[landplan-app]] — the web platform this syncs with
- [[survey-gps-receiver]] — hardware for RTK accuracy
- [[epic-gps-accuracy-templates]] — accuracy metadata model that mobile will populate
