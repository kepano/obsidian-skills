# LandPlan — Epic: Trees & Tree Stands

**Version:** 1.0
**Date:** April 5, 2026
**Status:** Requirements Defined
**Depends on:** 3D Models & Shadow Simulation epic (complete and tested)
**Reference files:** `LandPlanTreeSchema.json`, `speciesLibrary.json`, `TreeModelGenerationPrompt.md`, `TreeStandModule.md`, `example_javascript.txt`, `TreeStandJSExample.txt`

---

## 1. Overview

This epic adds two new object types to LandPlan — **Tree Models** (individual parametric trees placed at point locations) and **Tree Stands** (polygon areas representing dense plantings like forests, windbreaks, and orchards). Both are procedurally generated at runtime using Three.js, driven by a bundled species library and growth simulation rules. No pre-built glTF files are involved.

A **Growth Timeline slider** lets users project all trees and stands forward in time, visualizing how plantings will look years into the future. Combined with the existing shadow simulation, this allows users to answer questions like "What will the shadow from this oak tree line look like at 4 PM in 20 years?" — critical for spacing decisions, solar exposure planning, and windbreak design.

Trees and Tree Stands are separate from glTF/GLB 3D models. They are not part of the three-tier Model Library system (LandPlan public, user global, plan-level). They are a built-in procedural feature with their own section in the Model Palette.

---

## 2. Tree Models (Individual Trees)

### 2.1 Object Type

A Tree Model is a new placeable object on the map. It differs from glTF/GLB 3D model instances:

- Placed at a **point** location (lng, lat), not attached to a polygon footprint.
- Always renders **plumb to the earth** — vertical orientation regardless of terrain slope. There is no "Follow Terrain" option for trees.
- Size is **entirely determined by species parameters and age** — no manual scale controls. Users do not resize trees.
- Geometry is **procedurally generated** from species definitions, not loaded from a file.

### 2.2 Species Library

Six species ship at launch, conforming to `LandPlanTreeSchema`:

| Common Name | Scientific Name | Mature Age | Max Height | Max Crown Width |
|---|---|---|---|---|
| Northern Red Oak | *Quercus rubra* | 50 yr | 25 m | 20 m |
| Willow Oak | *Quercus phellos* | 40 yr | 23 m | 18 m |
| White Oak | *Quercus alba* | 60 yr | 28 m | 25 m |
| Pecan | *Carya illinoinensis* | 50 yr | 30 m | 20 m |
| Crape Myrtle | *Lagerstroemia indica* | 15 yr | 8 m | 6 m |
| Apple Tree | *Malus domestica* | 20 yr | 6 m | 6 m |

- Species definitions are stored as **static JSON** bundled in the web package (`packages/web/src/trees/speciesLibrary.json`), not fetched from the API at runtime.
- The species library is extensible — adding a new species requires only updating the JSON file, no code changes.

### 2.3 Parametric Mesh Generation

Trees are generated procedurally at runtime using Three.js:

- **Trunk:** `CylinderGeometry` with species-defined taper (`trunk.taper`) and base flare (`trunk.baseFlare`). Top radius narrower than bottom based on taper factor.
- **Crown:** Two primitive shapes (sphere, cone, ellipsoid, etc.) blended via vertex position interpolation (`THREE.MathUtils.lerp`). The blend ratio transitions through life stages (young → mature → old) using species-defined crown shape names and transition thresholds.
- **Vertex noise:** Random displacement applied to both trunk and crown vertices based on species `irregularity` parameters, using a seeded PRNG for deterministic results.
- **Vertex colors:** Crown vertices receive per-vertex color variation around the species' `crown.baseColor`, using HSL lightness offsets. No textures.
- **Materials:** `MeshStandardMaterial` for trunk and crown. Colors, roughness, and variation amounts are species-defined.
- **Triangle budget:** Each tree mesh must stay under **500 triangles**.
- **Output:** `THREE.Group` containing trunk mesh + crown mesh.

### 2.4 Growth Evaluation

The `evaluateTree(species, age, seed, environment)` function computes tree dimensions at a given age:

- **Age normalization:** `t = age / matureAge` (capped at 1.2), `tLife = age / maxAge` (capped at 1.0).
- **Growth curves:** Sigmoid (`1 / (1 + exp(-k * (age - t0)))`) or power (`(age / matureAge)^exponent`) curves control height, crown width, and trunk diameter progression. Curve type and parameters are species-defined.
- **Crown shape blending:** Crown transitions from `shapes.young` → `shapes.mature` → `shapes.old` using `smoothstep` interpolation between transition thresholds (`youngToMature`, `matureToOld`).
- **Crown flatness:** Interpolates between `flatness.min` and `flatness.max` over the tree's lifespan.
- **Irregularity:** Interpolates between `irregularity.min` and `irregularity.max` over the tree's lifespan (older trees are more irregular).
- **Environment mode:** Individual trees use `"open"` environment. Tree Stand evaluation uses `"forest"` (§3.3).

### 2.5 Placement & Interaction

- Users select a tree species from the Model Palette "Trees" category (§5), then click the map to place it.
- The `plantedYear` defaults to the current calendar year. Users can edit `plantedYear` in a properties panel to represent existing trees (e.g., set to 2006 for a 20-year-old oak).
- Trees can be selected, moved, and deleted like other plan objects.
- A properties panel shows: species name (read-only), planted year (editable), and current computed height/crown width (read-only, informational).

### 2.6 Shadow Integration

- Tree meshes (both trunk and crown) set `castShadow = true` and `receiveShadow = true`.
- Trees participate in the existing SunCalc-driven `DirectionalLight` shadow system from the 3D Models epic.
- Shadows are cast onto the ground plane, onto other trees, onto tree stands, and onto glTF/GLB models.
- Tree shadow rendering is controlled by the existing **Shadows** toggle and time-of-day/month sliders.
- The "3D Models" visibility toggle also hides/shows trees and their shadows.

---

## 3. Tree Stands (Forest Polygons)

### 3.1 Object Type

A Tree Stand is a polygon (area) object with 3D height. It represents dense plantings — forest blocks, windbreaks, orchards, groves. Unlike a glTF/GLB model instance (which attaches a loaded model to a polygon), a Tree Stand is a procedurally generated extruded volume with no external model file.

### 3.2 Definition

A Tree Stand is defined by:

- **polygon:** Array of [lng, lat] coordinate pairs. **IMPORTANT:** LandPlan uses [lng, lat] order everywhere — the ChatGPT reference code uses [lat, lon] and must be corrected during implementation.
- **plantedYear:** Year the stand was planted.
- **species:** Array of `{ id: string, weight: number }` — supports monoculture (single species, weight 1.0) and mixed species stands.
- **density:** 0.0–1.0 (default 0.7) — affects growth competition modeling and stand color intensity.

### 3.3 Stand Evaluation

The `evaluateTreeStand(stand, speciesLibrary, currentYear)` function computes the stand's aggregate properties:

- **Age:** `max(1, currentYear - plantedYear)`.
- **Per-species height:**
  - Calls `evaluateTree(species, age, seed, "forest")` for each species in the mix.
  - **Mature trees (age > matureAge):** Height capped by forest factor: `maxHeight * (0.75 + (1 - density) * 0.1)`. Denser stands = shorter trees.
  - **Young trees (age ≤ matureAge):** Height boosted by competition: `height * (1 + density * 0.25)`. Denser stands = young trees grow taller seeking light.
- **Weighted average height** across species based on mix weights.
- **Output:** `{ height, age, density, polygon, speciesMix }`.

### 3.4 Mesh Generation

The `buildTreeStandMesh()` function produces a single terrain-conforming 3D mesh per stand:

- **Polygon projection:** Stand polygon coordinates are projected to the Three.js scene's local coordinate system using `MercatorCoordinate.fromLngLat()`, consistent with glTF/GLB model placement.
- **Elevation:** Bottom vertices sit at ground elevation. Initially uses flat elevation (0) until DEM terrain data is implemented. The `getElevation(lng, lat)` interface is defined for future terrain conformance.
- **Extrusion:** Top vertices offset upward by the evaluated stand height, plus slight random variation per vertex for canopy irregularity.
- **Faces:** Side faces (connecting bottom and top vertex rings), triangulated top face, and bottom face.
- **Bevel:** Top vertices are pulled inward toward the polygon centroid by a small factor (≈8%) for a natural canopy edge profile.
- **Material:** `MeshStandardMaterial` with color blended from species `crown.baseColor` values weighted by species mix proportions. No textures.
- **One mesh per stand** — optimized for plans with multiple stands.

### 3.5 Placement & Interaction

- Users draw a Tree Stand polygon using the existing polygon drawing tools, then select "Tree Stand" as the polygon type.
- A configuration panel allows setting: species (selected from the species library), mix weights, density slider, and planted year.
- Tree Stands can be selected, edited (vertices moved/added/removed), and deleted.
- Species mix and density can be edited after placement.

### 3.6 Shadow Integration

- Tree Stand meshes set `castShadow = true` and `receiveShadow = true`.
- Tree Stand shadows are cast onto the ground, other stands, individual trees, and glTF/GLB models.
- Particularly valuable for visualizing shadow patterns from tree lines and windbreaks throughout the day.
- Controlled by the same Shadows toggle and sliders.

---

## 4. Growth Timeline Slider

### 4.1 Purpose

The Growth Timeline slider projects all trees and tree stands forward (or backward relative to maturity) in time. Key use cases:

- **Spacing decisions:** Will trees planted 15 feet apart crowd each other at maturity? Slide to +30 years to see crown overlap.
- **Shadow analysis:** How will a tree line's shadow pattern change as trees grow from 5 m to 25 m over 30 years?
- **Windbreak design:** Will this row of Willow Oaks provide adequate screening in 10 years?
- **Planning confidence:** See the property at planting time vs. 5, 10, 20 years, and maturity.

### 4.2 Behavior

- **Control type:** Slider with numeric display.
- **Range:** 0 to 50 years (fixed range).
- **Default position:** 0 (shows trees at their current age based on `plantedYear` and the current calendar year).
- **Projected age calculation:** `displayAge = (currentYear + sliderValue) - plantedYear`. A tree planted this year (2026) at slider +20 appears as a 20-year-old specimen.
- **Simultaneous update:** All Tree Models and Tree Stands on the plan update as the slider moves.
- **Minimum age:** Trees are always at least age 1, regardless of slider value.

### 4.3 Re-evaluation on Slider Change

When the slider value changes:

1. Each tree re-evaluates via `evaluateTree()` with the projected age → new height, crown width, trunk radius, crown shape blend.
2. Each tree stand re-evaluates via `evaluateTreeStand()` with the projected current year → new stand height.
3. **Geometry is regenerated** for the new dimensions.
4. Shadows (if enabled) update automatically since the meshes have changed size.

### 4.4 Performance

- **Debounce:** Slider changes are debounced (≈100ms) or applied on slider release to avoid per-pixel geometry rebuilds.
- **Geometry cache:** Evaluated geometries are cached by `(speciesId, age, seed)` tuple. If a tree is re-evaluated to an age that already has a cached geometry, reuse it.
- **Cache invalidation:** LRU eviction or clear-on-slider-release.

### 4.5 UI Placement

- The Growth Timeline slider appears in the **Shadow Controls panel** (`ShadowControls.tsx`), below the existing month and time-of-day sliders.
- Label: **"Growth Timeline"**
- Readout displays: `"2026 → 2046 (+20 years)"` (dynamically computed from current year + slider value).
- The Growth Timeline slider is always visible when trees or tree stands exist, regardless of whether shadows are toggled on. It controls tree size, not just shadow behavior.

### 4.6 Interaction with Shadow Controls

The Growth Timeline slider and shadow sliders work together:

- Set Growth Timeline to +20 years and shadow time to 4:00 PM in December → see the shadow cast by mature trees at a low winter sun angle.
- Set Growth Timeline to +0 and shadow time to noon in June → see minimal shadow from newly planted saplings.

---

## 5. Model Palette Integration

### 5.1 Trees Category

The existing `ModelPalette.tsx` component gains a **"Trees"** category section:

- Listed **above** user-uploaded glTF/GLB models (trees are a built-in feature, not user content).
- Each species entry displays: common name, scientific name, mature height (e.g., "25 m"), and a representative color swatch matching the species' crown color.
- Selecting a species enters **tree placement mode**: subsequent map clicks place trees of that species.
- Tree placement mode uses `'place-tree'` added to the `MapTool` union in `uiStore.ts`, with `placeTreeSpeciesId: string | null`.

### 5.2 Tree Stand Creation

Tree Stands are created via the existing polygon drawing tools, not via the Model Palette. After drawing a polygon, the user is prompted to choose the polygon type. "Tree Stand" is a new option that opens the Tree Stand configuration panel.

### 5.3 Separation from 3D Models

- Trees and Tree Stands are **not** part of the `Model3DFile` / `Model3DInstance` tables.
- They do not appear in the three-tier Model Library (current or future).
- The "3D Models" visibility toggle hides/shows trees and tree stands along with glTF/GLB models (single toggle for all 3D content).

---

## 6. Database Schema

### 6.1 New Table: `TreeModel`

```
TreeModel
  ├── id (UUID, PK)
  ├── planId → LandPlan (FK, NOT NULL)
  ├── speciesId (string — key into bundled species library, e.g., "red_oak")
  ├── plantedYear (int)
  ├── lng (float)                    ← IMPORTANT: lng first, matching LandPlan convention
  ├── lat (float)
  ├── seed (int, default 1)          ← deterministic PRNG seed for vertex noise/color variation
  ├── createdBy → User (FK)
  ├── createdAt / updatedAt
```

Relations: `TreeModel` belongs to `LandPlan`. `LandPlan` has many `treeModels`. `TreeModel` belongs to `User` via `createdBy`.

### 6.2 New Table: `TreeStand`

```
TreeStand
  ├── id (UUID, PK)
  ├── planId → LandPlan (FK, NOT NULL)
  ├── plantedYear (int)
  ├── density (float, default 0.7)
  ├── polygon (PostGIS GEOMETRY — Polygon, SRID 4326)    ← stored as PostGIS, not JSON
  ├── species (JSON — [{ id: "red_oak", weight: 0.6 }, ...])
  ├── seed (int, default 1)
  ├── createdBy → User (FK)
  ├── createdAt / updatedAt
```

Relations: `TreeStand` belongs to `LandPlan`. `LandPlan` has many `treeStands`. `TreeStand` belongs to `User` via `createdBy`.

**Design note:** Tree Stand polygons use PostGIS `GEOMETRY` type (like `MapObject.geometry`), not JSON arrays. This enables future spatial queries (e.g., "find all stands within this boundary"). The ChatGPT reference code stores polygons as JSON arrays — this must be converted to PostGIS during implementation.

### 6.3 Coordinate Convention

**IMPORTANT:** All coordinates use **[lng, lat]** order in database, API, and client code — consistent with GeoJSON (RFC 7946) and the rest of LandPlan. The ChatGPT reference implementations use `[lat, lon]` throughout. This must be corrected at implementation time. See `packages/api/CLAUDE.md` and `packages/web/CLAUDE.md` for the standing lng/lat vigilance rules.

---

## 7. API Endpoints

### 7.1 Tree Models

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| `POST` | `/plans/:planId/trees` | Create a tree. Body: `{ speciesId, plantedYear, lng, lat, seed? }` | `requirePlanWrite` |
| `GET` | `/plans/:planId/trees` | List all trees in the plan. | `requirePlanAccess` |
| `PATCH` | `/plans/:planId/trees/:treeId` | Update tree (move position, change plantedYear). | `requirePlanWrite` |
| `DELETE` | `/plans/:planId/trees/:treeId` | Delete a tree. | `requirePlanWrite` |

### 7.2 Tree Stands

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| `POST` | `/plans/:planId/tree-stands` | Create a tree stand. Body: `{ polygon (GeoJSON), plantedYear, species, density?, seed? }` | `requirePlanWrite` |
| `GET` | `/plans/:planId/tree-stands` | List all tree stands in the plan. | `requirePlanAccess` |
| `PATCH` | `/plans/:planId/tree-stands/:standId` | Update tree stand (polygon, species, density, plantedYear). | `requirePlanWrite` |
| `DELETE` | `/plans/:planId/tree-stands/:standId` | Delete a tree stand. | `requirePlanWrite` |

### 7.3 Species Library

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| `GET` | `/species` | Return the full species library JSON. | Public (no auth) |

This endpoint serves the bundled species library. While the web app bundles it locally, this endpoint exists for future mobile app use and for contributors/viewers who may not have the latest client bundle.

---

## 8. Web App Changes

### 8.1 New Files

| File | Location | Purpose |
|------|----------|---------|
| `speciesLibrary.json` | `packages/web/src/trees/` | Bundled species definitions (static JSON) |
| `evaluateTree.ts` | `packages/web/src/trees/` | Growth evaluation function |
| `buildTreeMesh.ts` | `packages/web/src/trees/` | Procedural mesh generation (trunk + crown) |
| `evaluateTreeStand.ts` | `packages/web/src/trees/` | Stand aggregate evaluation |
| `buildTreeStandMesh.ts` | `packages/web/src/trees/` | Stand extrusion mesh generation |
| `treeHelpers.ts` | `packages/web/src/trees/` | Shared utilities: `seededRandom`, `evaluateCurve`, `smoothstep`, `varyColor`, `applyVertexNoise`, `applyVertexColors`, `computeCentroid` |
| `index.ts` | `packages/web/src/trees/` | Re-exports |
| `TreePropertiesPanel.tsx` | `packages/web/src/components/trees/` | Edit planted year, view species info |
| `TreeStandConfigPanel.tsx` | `packages/web/src/components/trees/` | Configure species mix, density, planted year |
| `TreeRenderer.tsx` | `packages/web/src/components/trees/` | Manages all tree + stand meshes in the Three.js scene |
| `useTrees.ts` | `packages/web/src/hooks/` | React Query hooks for tree CRUD |
| `useTreeStands.ts` | `packages/web/src/hooks/` | React Query hooks for tree stand CRUD |

### 8.2 Modified Files

| File | Change |
|------|--------|
| `uiStore.ts` | Add `'place-tree'` to `MapTool` union. Add `placeTreeSpeciesId: string \| null`. Add `growthYears: number` (default 0). |
| `ModelPalette.tsx` | Add "Trees" category section above glTF/GLB models. Species list with placement mode. |
| `ShadowControls.tsx` | Add Growth Timeline slider (0–50 years) below existing month/time sliders. Visible when trees or stands exist. |
| `ModelRenderer.tsx` or `three-scene.ts` | Extend to accept tree and stand meshes into the shared Three.js scene so shadows interact across all 3D object types. |
| `PlanPage.tsx` | Mount `<TreeRenderer>`. Wire tree placement mode (map click → create tree). |

### 8.3 uiStore Extensions

```typescript
// Added to MapTool union
type MapTool = 'select' | ... | 'stamp-model' | 'place-tree'

// Added to uiStore state
placeTreeSpeciesId: string | null    // species to place when tool is 'place-tree'
growthYears: number                  // Growth Timeline slider value (0–50)

// Actions
setPlaceTreeSpeciesId: (id: string | null) => void
setGrowthYears: (years: number) => void
```

`growthYears` is per-session (not persisted to database). It is not included in `partialize`.

---

## 9. Rendering Architecture

### 9.1 Shared Scene

Tree meshes and Tree Stand meshes are added to the **same Three.js scene** used by `ModelRenderer.tsx` for glTF/GLB models. This is essential so that:

- Trees cast shadows **on** glTF/GLB models and vice versa.
- The "3D Models" visibility toggle hides all 3D content (trees, stands, glTF/GLB) together.
- A single shadow map covers all object types.

The `TreeRenderer.tsx` component manages tree/stand mesh lifecycle but adds them to the shared scene exposed by `three-scene.ts`.

### 9.2 Coordinate Projection

Tree positions use the same `MercatorCoordinate.fromLngLat()` projection used by `ModelRenderer.tsx` for glTF/GLB models. Tree Stand polygon vertices use the same projection, consistent with the `addModelToScene()` pattern in `three-scene.ts`.

### 9.3 Plumb Orientation

All trees render with Y-up (vertical in Three.js world space), equivalent to `plumb_to_earth` in the 3D Models Z Orientation terminology. There is no "Follow Terrain" option for trees.

### 9.4 Growth Timeline Re-rendering

When `uiStore.growthYears` changes:

1. `TreeRenderer.tsx` recomputes `displayAge` for every tree and stand.
2. For each tree: call `evaluateTree()` → `buildTreeMesh()` → replace the mesh in the scene.
3. For each stand: call `evaluateTreeStand()` → `buildTreeStandMesh()` → replace the mesh in the scene.
4. Call `map.triggerRepaint()`.

### 9.5 Performance

- **Triangle budget:** < 500 per individual tree. Stand meshes are proportional to polygon complexity (typically < 200 vertices).
- **Instancing:** For trees of the same species and same computed age, use `THREE.InstancedMesh` to batch-render identical geometries with different positions. At a given Growth Timeline slider position, same-species same-plantedYear trees produce identical geometry.
- **Geometry cache:** Cache by `(speciesId, computedAge, seed)`. Reuse when a tree's projected age matches a cached entry.
- **Debounce:** Growth Timeline slider changes debounced at ≈100ms or applied on slider release.
- **Target:** Acceptable performance with 50+ individual trees and 5+ tree stands on a single plan.

---

## 10. Permissions

Trees and Tree Stands follow the same permission rules as other plan objects (see `requirements.md` §2):

| Capability | Owner | Contributor | Viewer |
|---|---|---|---|
| View trees and stands on map | ✅ | ✅ | ✅ |
| Place individual trees | ✅ | ✅ | ❌ |
| Create tree stands | ✅ | ✅ | ❌ |
| Edit tree/stand properties | ✅ | ✅ | ❌ |
| Delete trees/stands | ✅ | ✅ (own only) | ❌ |
| Use Growth Timeline slider | ✅ | ✅ | ✅ |
| Use Shadow simulation controls | ✅ | ✅ | ✅ |

Contributors cannot delete trees or stands created by other users (consistent with existing `capturedBy` / `createdBy` rules for map objects).

---

## 11. Acceptance Criteria

### 11.1 Tree Models

- [ ] User can select a tree species from the "Trees" category in the Model Palette.
- [ ] Clicking the map places a tree of that species at the clicked location.
- [ ] The tree renders as a low-poly 3D model (trunk + crown) with species-appropriate shape, size, and colors.
- [ ] Tree is oriented plumb (vertical) regardless of map tilt or future terrain.
- [ ] User can edit `plantedYear` in a properties panel; tree re-renders at the new age.
- [ ] User can move a placed tree by dragging.
- [ ] User can delete a placed tree.
- [ ] Tree casts shadows onto the ground, other trees, tree stands, and glTF/GLB models.
- [ ] Tree receives shadows from other 3D objects.

### 11.2 Tree Stands

- [ ] User can draw a polygon and configure it as a Tree Stand.
- [ ] Stand configuration panel allows selecting species (from library), setting mix weights, density, and planted year.
- [ ] Tree Stand renders as a 3D extruded polygon with beveled canopy edges.
- [ ] Stand color blends species crown colors according to mix weights.
- [ ] Stand height reflects species growth evaluation with density-based competition modeling.
- [ ] User can edit species mix, density, and planted year after creation.
- [ ] Tree Stand casts and receives shadows.

### 11.3 Growth Timeline

- [ ] Growth Timeline slider appears in Shadow Controls panel when trees or stands exist.
- [ ] Slider range: 0–50 years. Default: 0.
- [ ] Readout shows projected year (e.g., "2026 → 2046 (+20 years)").
- [ ] Moving slider updates all tree and stand geometry in real time (debounced).
- [ ] At +0, a tree planted in 2026 appears as age 1 (current year). At +20, it appears as age 21.
- [ ] Growth Timeline and shadow sliders work together — user can see future shadow patterns.
- [ ] Slider is available to all roles (owner, contributor, viewer).

### 11.4 Model Palette

- [ ] "Trees" category appears in Model Palette above user-uploaded models.
- [ ] All six launch species are listed with name, scientific name, and mature height.
- [ ] Clicking a species enters placement mode with appropriate cursor.
- [ ] Subsequent map clicks place trees until the user switches tools.

### 11.5 Performance

- [ ] Individual tree mesh stays under 500 triangles.
- [ ] Plan with 50 trees and 5 tree stands renders without frame drops during orbit/pan.
- [ ] Growth Timeline slider responds without visible lag (debounced geometry rebuild).

### 11.6 Permissions

- [ ] Viewers see trees and stands but have no placement, edit, or delete controls.
- [ ] Contributors can place, edit (own only), and delete (own only) trees and stands.
- [ ] Growth Timeline slider is usable by all roles.

---

## 12. Out of Scope (This Epic)

- **Seasonal appearance** (fall colors, bare winter trees) — schema supports `seasonal: boolean` but rendering is deferred.
- **LOD (Level of Detail)** — schema includes LOD distance thresholds; implementation deferred until performance requires it.
- **DEM terrain conformance** — Tree Stands use flat elevation until DEM terrain is implemented. The `getElevation()` interface is defined.
- **Wind/environmental response** — `environmentResponse` schema fields exist but are not evaluated.
- **Visible branch geometry** — `branching` schema fields exist; initial implementation renders trunk + crown only.
- **GLTF export of procedural trees** — deferred.
- **Custom species creation by users** — deferred. Only the bundled library is available.
- **Individual-tree rendering within stands** — stands render as extruded polygons, not as collections of individual tree meshes. Deliberate simplification for performance.
- **Tree stand polygon import** (GeoJSON/KML → tree stand) — deferred.
- **Mobile app tree support** — deferred to mobile epic.

---

## 13. Implementation Sessions

### Session 1 — Tree Engine + Single Tree Rendering

**Goal:** A single procedural tree renders on the live map at a hardcoded coordinate.

**Tasks:**

1. Create `packages/web/src/trees/` module with: `speciesLibrary.json`, `evaluateTree.ts`, `buildTreeMesh.ts`, `treeHelpers.ts`, `index.ts`.
2. Port ChatGPT reference code to TypeScript. **Correct all [lat, lon] → [lng, lat].** Add missing utility functions: `evaluateCurve`, `smoothstep`, `primitive` (crown shape → geometry factory).
3. Create `TreeRenderer.tsx` — adds a hardcoded Red Oak (age 25) to the shared Three.js scene at a known coordinate. Gate with `import.meta.env.DEV`.
4. Verify tree renders, casts shadow, receives shadow from existing glTF/GLB models.

### Session 2 — Database + API

**Goal:** TreeModel and TreeStand tables exist. All API endpoints respond correctly.

**Tasks:**

1. Update Prisma schema: add `TreeModel` and `TreeStand` tables with relations.
2. Run migration.
3. Create `packages/api/src/routes/trees.ts` and `packages/api/src/routes/tree-stands.ts`. Follow `photos.ts` pattern for middleware.
4. Create/update `packages/api-client/src/endpoints/trees.ts` and `tree-stands.ts`.
5. Add `packages/shared/src/types/tree.ts` — TreeModel, TreeStand, TreeSpecies types.
6. Register routes.

### Session 3 — End-to-End Tree Placement

**Goal:** Place trees from the palette, persist, render across refresh.

**Tasks:**

1. Create `useTrees.ts` hook (React Query CRUD).
2. Add "Trees" category to `ModelPalette.tsx` with species list.
3. Add `'place-tree'` to `uiStore.ts` MapTool union.
4. Wire map click handler in `PlanPage.tsx` for tree placement.
5. Update `TreeRenderer.tsx` to render all trees from query data.
6. Remove DEV gate.

### Session 4 — Tree Stand Implementation

**Goal:** Draw, configure, and render Tree Stands.

**Tasks:**

1. Port `evaluateTreeStand` and `buildTreeStandMesh` to TypeScript in `packages/web/src/trees/`.
2. Create `useTreeStands.ts` hook.
3. Create `TreeStandConfigPanel.tsx`.
4. Wire polygon drawing → tree stand creation flow.
5. Update `TreeRenderer.tsx` to render stands.

### Session 5 — Growth Timeline + Properties + Polish

**Goal:** Growth Timeline slider works. Tree properties editable. Permission enforcement.

**Tasks:**

1. Add `growthYears` to `uiStore.ts`.
2. Add Growth Timeline slider to `ShadowControls.tsx`.
3. Wire `TreeRenderer.tsx` to recompute on `growthYears` change with debouncing.
4. Create `TreePropertiesPanel.tsx` (edit plantedYear).
5. Implement geometry caching.
6. Permission enforcement: hide placement/edit/delete controls for viewers.
7. `pnpm typecheck` and `pnpm build` clean.
8. Commit + push.

### Session Dependency

```
Session 1 (Tree Engine + Rendering Spike)
    └── Session 2 (DB + API)  ← can run in parallel with Session 1
            └── Session 3 (Tree Placement E2E)
                    └── Session 4 (Tree Stands)
                            └── Session 5 (Growth Timeline + Polish + Push)
```

---

## 14. Critical Files

| File | Session | Action |
|---|---|---|
| `packages/web/src/trees/speciesLibrary.json` | 1 | Create |
| `packages/web/src/trees/evaluateTree.ts` | 1 | Create |
| `packages/web/src/trees/buildTreeMesh.ts` | 1 | Create |
| `packages/web/src/trees/treeHelpers.ts` | 1 | Create |
| `packages/web/src/trees/evaluateTreeStand.ts` | 4 | Create |
| `packages/web/src/trees/buildTreeStandMesh.ts` | 4 | Create |
| `packages/web/src/components/trees/TreeRenderer.tsx` | 1→5 | Create, evolve |
| `packages/web/src/components/trees/TreePropertiesPanel.tsx` | 5 | Create |
| `packages/web/src/components/trees/TreeStandConfigPanel.tsx` | 4 | Create |
| `packages/web/src/hooks/useTrees.ts` | 3 | Create |
| `packages/web/src/hooks/useTreeStands.ts` | 4 | Create |
| `packages/shared/src/types/tree.ts` | 2 | Create |
| `packages/api/src/routes/trees.ts` | 2 | Create |
| `packages/api/src/routes/tree-stands.ts` | 2 | Create |
| `packages/api-client/src/endpoints/trees.ts` | 2 | Create |
| `packages/api-client/src/endpoints/tree-stands.ts` | 2 | Create |
| `packages/api/prisma/schema.prisma` | 2 | Extend |
| `packages/web/src/stores/uiStore.ts` | 3, 5 | Extend |
| `packages/web/src/components/models3d/ModelPalette.tsx` | 3 | Extend |
| `packages/web/src/components/shadow/ShadowControls.tsx` | 5 | Extend |
| `packages/web/src/routes/PlanPage.tsx` | 3→5 | Extend |

---

*This document should be read alongside `requirements_3d_models.md` (3D Models & Shadow Simulation), `architecture.md`, `build_roadmap.md`, and `requirements.md` (Plan Sharing).*
