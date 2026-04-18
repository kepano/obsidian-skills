---
title: "Epic: 3D Models & Shadow Simulation"
tags: [landplan, epic, 3d, threejs, shadow, done]
created: 2026-04-18
updated: 2026-04-18
status: evergreen
epic: 3d-models
priority: 2
---

# Epic: 3D Models & Shadow Simulation

**Status:** Done  
**Version:** 1.0 (March 29, 2026)  
**Depends on:** Phase 3 Web App, [[epic-plan-sharing|Plan Sharing]] (permission model)

---

## Objective

Upload, place, and render 3D models (glTF/GLB) on the map, anchored to polygon objects. Include shadow simulation driven by accurate sun position calculations (SunCalc) for evaluating solar exposure.

Three.js already installed in web app. `packages/web/src/components/models3d/` existed but unimplemented before this epic.

---

## Core Concepts

### Model–Polygon Relationship

Every 3D model is attached to a **polygon** map object (strict 1:1):

- **Uniform / Contain (default):** Uniformly scaled so the largest base dimension fits inside the polygon bounding box. Aspect ratio preserved across all three axes.
- **Stretch to Fill (alternate):** X and Y axes independently scaled to fill bounding box; Z scales proportionally.
- After fit: user can further adjust X, Y, Z scale via sliders
- Multiple polygon instances can reference the same model file (stamp/clone); each instance has independent transform properties

### Supported Formats

| Format | Notes |
|--------|-------|
| `.glb` | Binary glTF; single file; recommended (self-contained) |
| `.gltf` | Text-based; may reference external `.bin` + textures |

### Storage

Model files stored in GCS per [[epic-gcs-storage]] (replaced original Google Drive storage). `objectKey` in the `Model3DInstance` record is the GCS key.

---

## 3D Model Library (Three Tiers — future epic)

Future epic will add: LandPlan public library, user-level global library, per-plan library. Architecture is forward-compatible (folder structure reserved).

---

## Shadow Simulation

- **Library:** SunCalc — computes sun azimuth and altitude for any lat/lng, date, and time
- **Three.js:** `DirectionalLight` positioned using SunCalc output; `castShadow` / `receiveShadow` on all models
- **Controls:** Month slider + time-of-day slider in Shadow Controls panel
- **Shadow map:** single shadow map covering all 3D content (models, trees, tree stands)

---

## Key Schema

### Model3DFile

Represents a physical file stored in GCS.

### Model3DInstance

Links a `Model3DFile` to a polygon `MapObject`. Stores transform properties (scale X/Y/Z, Fit Mode, rotation, Z orientation).

### Z Orientation Options

- `plumb_to_earth` — always vertical (used for trees)
- `follow_terrain` — tilts to match terrain slope

---

## Related

- [[epic-trees]] — trees and tree stands use the same Three.js scene and shadow system
- [[architecture]] — Three.js as a MapLibre custom layer
- [[epic-gcs-storage]] — storage layer models use
