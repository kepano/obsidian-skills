---
title: "Epic: Trees & Tree Stands"
tags: [landplan, epic, trees, threejs, procedural, done]
created: 2026-04-18
updated: 2026-04-18
status: evergreen
epic: trees
priority: 2
---

# Epic: Trees & Tree Stands

**Status:** Done  
**Version:** 1.0 (April 5, 2026)  
**Depends on:** [[epic-3d-models|3D Models & Shadow Simulation epic]]

---

## Objective

Add two new object types — **Tree Models** (individual parametric trees at point locations) and **Tree Stands** (polygon areas of dense planting). Both procedurally generated at runtime using Three.js. Includes a **Growth Timeline slider** to project all trees and stands forward in time.

Key use case: *"What will the shadow from this oak tree line look like at 4 PM in 20 years?"*

---

## Tree Models (Individual Trees)

### Characteristics

- Placed at a **point** (lng, lat); not attached to a polygon
- Always renders **plumb to earth** (vertical; no Follow Terrain option)
- Size entirely determined by species parameters and `plantedYear` — no manual scale controls
- Procedurally generated geometry (Three.js), not loaded from file

### Species Library (6 at launch)

| Common Name | Scientific Name | Mature Age | Max Height | Max Crown Width |
|-------------|----------------|-----------|-----------|----------------|
| Northern Red Oak | *Quercus rubra* | 50 yr | 25 m | 20 m |
| Willow Oak | *Quercus phellos* | 40 yr | 23 m | 18 m |
| White Oak | *Quercus alba* | 60 yr | 28 m | 25 m |
| Pecan | *Carya illinoinensis* | 50 yr | 30 m | 20 m |
| Crape Myrtle | *Lagerstroemia indica* | 15 yr | 8 m | 6 m |
| Apple Tree | *Malus domestica* | 20 yr | 6 m | 6 m |

Static JSON bundled at `packages/web/src/trees/speciesLibrary.json`. Extending = add entry to JSON only.

### Mesh Generation

- **Trunk:** `CylinderGeometry` with taper + base flare
- **Crown:** Two primitive shapes blended via `THREE.MathUtils.lerp` through life stages (young → mature → old)
- **Vertex noise:** Seeded PRNG for deterministic irregularity
- **Vertex colors:** Per-vertex HSL variation; no textures
- **Budget:** < 500 triangles per tree
- **Output:** `THREE.Group` (trunk + crown)

### Growth Evaluation

`evaluateTree(species, age, seed, environment)`:
- Sigmoid or power growth curves control height, crown width, trunk diameter
- Crown shape blends from young → mature → old shapes via `smoothstep`
- Forest environment (for Tree Stands) vs open environment (individual trees)

---

## Tree Stands (Forest Polygons)

- Polygon area defined by [lng, lat] coordinate pairs (**lng first always**)
- Represents: forest blocks, windbreaks, orchards, groves
- Defined by: polygon, plantedYear, species mix `[{ id, weight }]`, density (0.0–1.0)
- One mesh per stand (extruded polygon); beveled canopy edge; species colors blended by mix weights
- PostGIS `GEOMETRY` type in DB (enables spatial queries); **not** JSON arrays

### Stand Evaluation

`evaluateTreeStand(stand, speciesLibrary, currentYear)`:
- Mature trees (age > matureAge): height capped by forest factor — denser stands = shorter
- Young trees (age ≤ matureAge): height boosted by competition — denser stands = faster vertical growth
- Weighted average height across species

---

## Growth Timeline Slider

- Range: 0–50 years. Default: 0 (current age based on plantedYear + current year)
- Readout: `"2026 → 2046 (+20 years)"` (dynamically computed)
- All tree and stand geometry regenerated on slider change (debounced ~100ms)
- Lives in Shadow Controls panel (`ShadowControls.tsx`); visible whenever trees or stands exist
- Available to all roles (Owner, Contributor, Viewer)

---

## Database Schema

### TreeModel

```
id         UUID PK
planId     FK → Plan
speciesId  string (key into species library)
plantedYear int
lng        float  ← lng first (not lat!)
lat        float
seed       int (default 1; PRNG seed for deterministic noise)
createdBy  FK → User
createdAt / updatedAt
```

### TreeStand

```
id         UUID PK
planId     FK → Plan
plantedYear int
density    float (default 0.7)
polygon    PostGIS GEOMETRY (SRID 4326)
species    JSON: [{ id: string, weight: number }]
seed       int
createdBy  FK → User
createdAt / updatedAt
```

---

## Rendering Architecture

- Tree and stand meshes share the **same Three.js scene** as glTF/GLB models → shadows cross all 3D object types
- Coordinate projection: `MercatorCoordinate.fromLngLat()` — same as ModelRenderer
- Managed by `TreeRenderer.tsx`

### Performance

- Triangle budget: < 500 per tree; < 200 vertices per stand (proportional to polygon complexity)
- `THREE.InstancedMesh` for trees of the same species and age at a given slider position
- Geometry cache by `(speciesId, computedAge, seed)`; LRU eviction
- Target: acceptable performance with 50+ trees and 5+ stands

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/plans/:planId/trees` | Create tree |
| GET | `/plans/:planId/trees` | List all trees |
| PATCH | `/plans/:planId/trees/:treeId` | Update (move, plantedYear) |
| DELETE | `/plans/:planId/trees/:treeId` | Delete |
| POST | `/plans/:planId/tree-stands` | Create stand |
| GET | `/plans/:planId/tree-stands` | List all stands |
| PATCH | `/plans/:planId/tree-stands/:standId` | Update (polygon, species, density, plantedYear) |
| DELETE | `/plans/:planId/tree-stands/:standId` | Delete |
| GET | `/species` | Return species library JSON (public, no auth) |

---

## Permissions

| Capability | Owner | Contributor | Viewer |
|-----------|-------|------------|-------|
| View trees and stands | ✅ | ✅ | ✅ |
| Place individual trees | ✅ | ✅ | ❌ |
| Create tree stands | ✅ | ✅ | ❌ |
| Edit tree/stand properties | ✅ | ✅ | ❌ |
| Delete trees/stands | ✅ | ✅ (own only) | ❌ |
| Use Growth Timeline slider | ✅ | ✅ | ✅ |
| Use Shadow simulation | ✅ | ✅ | ✅ |

---

## Out of Scope (This Epic)

Seasonal appearance, LOD, DEM terrain conformance, wind response, visible branch geometry, glTF export of procedural trees, custom species by users, individual-tree rendering within stands, GeoJSON/KML → tree stand import, mobile app tree support.

---

## Related

- [[epic-3d-models]] — shadow system this builds on
- [[architecture]] — TreeModel / TreeStand schema, coordinate convention
