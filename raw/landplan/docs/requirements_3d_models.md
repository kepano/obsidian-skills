# LandPlan — Epic: 3D Models & Shadow Simulation

**Version:** 1.0
**Date:** March 29, 2026
**Status:** Draft
**Depends on:** Phase 3 Web App, Sharing Epic (permission model)
**Reference implementation:** [MapLibre + Three.js 3D model with shadow](https://maplibre.org/maplibre-gl-js/docs/examples/add-a-3d-model-with-shadow-using-threejs/)

---

## 1. Overview

This epic adds the ability to upload, place, and render 3D models on the map, anchored to polygon objects. Models are rendered using Three.js integrated with MapLibre GL JS via custom layers — the same approach demonstrated in the MapLibre reference example. The epic also includes shadow simulation driven by accurate sun position calculations, enabling users to evaluate solar exposure for planning purposes (solar panels, gardens, building orientation).

Three.js is already installed in the web app. The `packages/web/src/components/models3d/` directory exists but is not yet implemented. The backend `routes/models3d.ts` route module and `api-client/endpoints/models3d.ts` exist in the architecture but need implementation.

---

## 2. Core Concepts

### 2.1 Model–Polygon Relationship

Every 3D model is attached to a **polygon** map object. The polygon defines the model's footprint on the map:

- One model file per polygon (strict 1:1). Uploading a new file replaces the previous one.
- **Default scaling ("Uniform / Contain"):** The model is uniformly scaled so that its largest base dimension (X or Y) fits exactly within the polygon's bounding box, without distortion. The model's original aspect ratio is preserved across all three axes. For example, if the polygon is 10×5 meters and the model's native base is 5×5, the model scales to 5×5 — it does not stretch to fill the 10-unit axis. Z scales by the same uniform factor.
- **Alternate scaling ("Stretch to Fill"):** Available as a Fit Mode option in the Edit 3D Model Properties modal (§4). The model's X and Y axes are independently scaled to fill the polygon's bounding box. Z scales proportionally to the average of X and Y. This distorts the model's aspect ratio but ensures full polygon coverage.
- After the initial fit, the user can further adjust X, Y, and Z scale independently via sliders in the properties modal.
- Multiple polygon instances can reference the same model file (via the stamp/clone feature). Each instance has independent transform properties including Fit Mode.

### 2.2 File Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| glTF | `.gltf` (+ `.bin` + textures) | Text-based, TinkerCAD/Blender compatible. Three.js `GLTFLoader`. |
| GLB | `.glb` | Binary glTF. Single file, same loader. Auto-detected by file extension. |

Other formats (OBJ, FBX) are out of scope for this epic. glTF/GLB covers TinkerCAD, Blender, SketchUp (via export), and most modern 3D tools.

### 2.3 Storage

Model files are stored in the plan owner's Google Drive, in a `models/` subfolder within the plan's Drive folder (parallel to the existing `images/` subfolder). The same Drive delegation rules from the Sharing Epic apply: contributor uploads use the owner's stored OAuth tokens.

When a model is deleted from a polygon (replaced or polygon deleted), the Drive file is kept — only the database reference is removed. This avoids accidental data loss, since other instances may reference the same file or the user may want to re-use it.

> **Forward-compatibility note (Model Library — §16):** A future epic will add three library tiers: a LandPlan public library, a user-level global library, and per-plan libraries. To prepare for this, a `User_Model_Library/` folder will be created as a standard folder in the user's Google Drive alongside the plan folders. For this epic, all uploads go to the plan-level `models/` folder. The folder structure will be:
> ```
> LandPlan/
> ├── User_Model_Library/          ← future: user's global model library
> ├── {Plan Name}/
> │   ├── images/
> │   └── models/                  ← this epic: plan-level model storage
> ```

---

## 3. Model Upload & Attachment

### 3.1 Entry Point: Edit Polygon Tool

When a user selects a polygon and enters the **Edit Polygon** mode (existing tool), a new section appears in the edit panel:

**If no model is attached:**
- A file upload area: "Upload 3D Model (.gltf, .glb)" with drag-and-drop and file picker.
- Uploading a file immediately attaches the model to the polygon and renders it on the map — no additional save step.

**If a model is already attached:**
- A thumbnail/preview of the current model file name and format.
- A "Replace Model" button to upload a different file.
- An "Edit 3D Model Properties" button that opens the properties modal (§4).
- A "Remove Model" button that detaches the model from the polygon (removes DB reference, keeps Drive file).

### 3.2 Upload Flow

1. User selects a `.gltf` or `.glb` file.
2. File uploads to Cloud Storage (temp staging), then backend pushes to the owner's Google Drive `models/` folder.
3. Backend creates/updates the `Model3DInstance` record linking the polygon to the Drive file.
4. Frontend receives the response and immediately loads + renders the model on the map using Three.js.
5. If a `.gltf` file references external `.bin` or texture files, the upload should accept multiple files (or prompt the user to upload a `.glb` instead for simplicity). GLB is the recommended format since it's self-contained.

### 3.3 GLB Auto-Detection

The backend and frontend detect the format by file extension. Both `.gltf` and `.glb` are loaded via Three.js `GLTFLoader`, which handles both formats natively.

---

## 4. Edit 3D Model Properties Modal

Accessible from the Edit Polygon panel once a model is attached. This is a separate modal window titled **"Edit 3D Model Properties"**.

### 4.1 Properties

| Property | Control | Default | Description |
|----------|---------|---------|-------------|
| **Fit Mode** | Toggle: "Uniform (Contain)" / "Stretch to Fill" | Uniform (Contain) | See §2.1. Uniform preserves aspect ratio; Stretch fills the polygon bounding box. Changing this recalculates the base scale. |
| **Heading** | Rotation slider or numeric input (0°–360°) | 180° (south-facing) | Rotates the model around its vertical axis. |
| **Scale X** | Slider + numeric input | 1.0 (relative to Fit Mode base) | Additional scale multiplier along polygon's width axis. Applied on top of the Fit Mode calculation. |
| **Scale Y** | Slider + numeric input | 1.0 (relative to Fit Mode base) | Additional scale multiplier along polygon's depth axis. |
| **Scale Z** | Slider + numeric input | 1.0 (relative to Fit Mode base) | Additional vertical scale multiplier. |
| **Z Orientation** | Toggle: "Follow Terrain" / "Plumb to Earth" | Follow Terrain | See §4.2. |
| **Model File** | Display current filename + "Replace" button | — | Allows uploading a different model file. |

### 4.2 Z Orientation Modes

- **Follow Terrain:** The model is oriented to match the slope of the terrain at the polygon's location. The model's "up" axis aligns with the surface normal. Appropriate for: vehicles, roads, bridges, ground-hugging structures.
- **Plumb to Earth:** The model's "up" axis is aligned with the true vertical (away from Earth's center, perpendicular to the geoid). Appropriate for: trees, buildings, utility poles — anything that stands vertically regardless of terrain slope.

### 4.3 Real-Time Preview

All property changes (fit mode, heading, scale X/Y/Z, Z orientation) update the model's rendering on the map in real time as the user adjusts controls. Changes are persisted when the user closes the modal or clicks "Save".

---

## 5. Model Palette (Stamp/Clone Tool)

### 5.1 Appearance

Once at least one model has been uploaded to any polygon in the plan, a new tool appears in the right-side tool palette: **"Models"** (or a 3D cube icon).

The palette shows a scrollable list of all unique model files used across the entire plan (regardless of layer). Each entry displays:

- A small 3D thumbnail or icon of the model.
- The model's file name.
- The layer name of the source polygon (for context).

If the list exceeds the visible area, it scrolls vertically.

### 5.2 Stamp/Clone Workflow

1. User clicks a model in the palette.
2. A ghost/preview polygon (cloned from the source polygon's shape and size) follows the cursor on the map.
3. User clicks to place the polygon on the map.
4. The system creates a new polygon map object with:
   - The same geometry shape as the source polygon.
   - Placed on the **same layer** as the source polygon.
   - A new `Model3DInstance` record referencing the **same Drive file** (no file duplication).
   - Default model properties (heading 180°, scale 1.0/1.0/1.0, follow terrain).
5. The model renders immediately on the map.
6. The user can then edit the new polygon and its 3D model properties independently.

### 5.3 Instance Independence

Each stamped instance is fully independent:

- Its own polygon geometry (can be moved/reshaped after placement).
- Its own model properties (heading, scale, Z orientation).
- References the same model file in Google Drive (no duplication).
- Deleting one instance does not affect others.

---

## 6. 3D Models Visibility Toggle

Once any model exists in the plan, a **"3D Models"** button appears in the top toolbar. This is a simple on/off toggle:

- **On (default):** All 3D models are rendered on the map.
- **Off:** All 3D models are hidden. Polygons remain visible with their normal styling.

This toggle helps with rendering performance on complex plans and allows users to see the underlying map without visual clutter.

The toggle state is per-session (not persisted to the database). It applies globally to all models across all layers.

---

## 7. Shadow Simulation

### 7.1 Shadows Button & Tool Window

A **"Shadows"** button appears in the top toolbar (alongside the "3D Models" toggle). Clicking it opens a tool panel on the right side of the map.

### 7.2 Shadow Controls

| Control | Type | Range | Default |
|---------|------|-------|---------|
| **Shadows On/Off** | Toggle | — | Off |
| **Month** | Slider | January – December (12 stops) | Current month |
| **Time of Day** | Slider | 1:00 AM – 12:00 AM (midnight) | 12:00 PM (noon) |

### 7.3 Sun Position Calculation

Sun position (azimuth and altitude) is calculated using the **SunCalc** library (already in the architecture) with:

- **Latitude/Longitude:** The plan's center coordinates (`centerLat` / `centerLng` from the `LandPlan` record).
- **Date/Time:** Constructed from the slider values — the 15th of the selected month at the selected hour.

The calculated sun azimuth and altitude drive a Three.js `DirectionalLight` that casts shadows from all 3D models.

### 7.4 Shadow Rendering

- Shadows are cast by all visible 3D models onto the **ground plane** and onto **other models**.
- Uses Three.js shadow mapping integrated with the MapLibre custom layer (same pattern as the reference example).
- Shadow updates are **dynamic and real-time** — moving the sliders immediately updates the shadow positions on the map.
- When shadows are toggled off, the `DirectionalLight` shadow casting is disabled (performance optimization).

### 7.5 Shadow Visibility vs. 3D Models Toggle

- If "3D Models" is toggled off, shadows are also hidden (no models = no shadows).
- If "Shadows" is toggled off but "3D Models" is on, models render without shadow casting.

---

## 8. Rendering Architecture

### 8.1 Three.js + MapLibre Integration

Following the reference implementation pattern:

1. A MapLibre `CustomLayerInterface` hosts a Three.js scene.
2. The Three.js scene's camera and projection matrix are synced with MapLibre's camera on every frame.
3. Models are loaded via `GLTFLoader` and positioned using MapLibre's `MercatorCoordinate.fromLngLat()` to convert geographic coordinates to the scene's coordinate space.
4. A `DirectionalLight` is positioned based on SunCalc output for shadow casting.
5. A ground plane (invisible mesh) receives shadows.

### 8.2 Rendering in 2D and 3D Modes

Models render in **both** flat (2D) and 3D terrain modes. MapLibre supports camera pitch/tilt even without terrain enabled, so models are visible from an angled view in 2D mode. In 3D terrain mode, models are additionally placed at the correct terrain elevation.

### 8.3 Follow Terrain vs. Plumb to Earth

- **Follow Terrain:** The model's orientation is derived from the terrain surface normal at the polygon's center. In 2D mode (no terrain data), this is equivalent to Plumb to Earth.
- **Plumb to Earth:** The model's up vector is always (0, 0, 1) in the Three.js scene — straight up regardless of terrain slope.

### 8.4 Performance Considerations

- The "3D Models" visibility toggle allows users to disable rendering entirely.
- Shadow mapping is only active when the Shadows tool is enabled.
- Model geometry is cached after first load — multiple instances of the same model file share the loaded geometry (instanced rendering where possible).
- Consider using Three.js `LOD` (level of detail) for distant models in plans with many instances.

---

## 9. Permissions (Sharing Integration)

3D models follow the same permission rules as photos:

| Capability | Owner | Contributor | Viewer |
|------------|-------|-------------|--------|
| View 3D models on map | ✅ | ✅ | ✅ |
| Upload model to a polygon | ✅ | ✅ | ❌ |
| Edit model properties | ✅ | ✅ | ❌ |
| Replace/remove model from polygon | ✅ | ✅ | ❌ |
| Stamp/clone model instances | ✅ | ✅ | ❌ |
| Toggle 3D Models visibility | ✅ | ✅ | ✅ |
| Use Shadow simulation controls | ✅ | ✅ | ✅ |

Contributor uploads are stored in the plan owner's Google Drive `models/` folder using the owner's OAuth tokens (same delegation as photo uploads).

---

## 10. Database Changes

### 10.1 New Table: Model3DFile

Represents a model file stored in Google Drive. Multiple polygon instances can reference the same file.

```
Model3DFile
  ├── id (UUID)
  ├── planId → LandPlan (nullable — null for user-library and public-library models)
  ├── name (string — original filename)
  ├── format (gltf | glb)
  ├── driveFileId (Google Drive file ID, nullable — null for public library models served from CDN)
  ├── source (plan_upload | user_library | public_library, default plan_upload)
  ├── uploadedBy → User
  ├── createdAt
```

> **Forward-compatibility note:** The `planId` is nullable and `source` is an enum to support the planned Model Library feature (§16). For this epic, all records will have `source: plan_upload` and a non-null `planId`. The nullable fields and enum are included now so the library feature can be added later without a schema migration that alters existing data.

### 10.2 New Table: Model3DInstance

Represents a model placed on a specific polygon with its own transform properties.

```
Model3DInstance
  ├── id (UUID)
  ├── modelFileId → Model3DFile
  ├── polygonId → MapObject (the polygon this instance is attached to)
  ├── planId → LandPlan
  ├── fitMode (uniform | stretch, default uniform)
  ├── heading (float, degrees, default 180)
  ├── scaleX (float, default 1.0)
  ├── scaleY (float, default 1.0)
  ├── scaleZ (float, default 1.0)
  ├── zOrientation (follow_terrain | plumb_to_earth, default follow_terrain)
  ├── createdAt / updatedAt
```

### 10.3 Existing Table Changes

The existing `Model3D` table in the architecture can be replaced by the two tables above, which better model the file-vs-instance separation needed for the stamp/clone feature.

---

## 11. API Endpoints

### 11.1 Model Files

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/plans/:planId/models` | Upload a model file (multipart). Returns `Model3DFile` record. |
| `GET` | `/plans/:planId/models` | List all model files for the plan (for the palette). |
| `GET` | `/plans/:planId/models/:modelFileId/download` | Download/proxy the model file from Drive for rendering. |
| `DELETE` | `/plans/:planId/models/:modelFileId` | Delete the file record (keeps Drive file). Only if no instances reference it. |

### 11.2 Model Instances

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/plans/:planId/objects/:objectId/model-instance` | Attach a model to a polygon. Body: `{ modelFileId, heading?, scaleX?, scaleY?, scaleZ?, zOrientation? }` |
| `GET` | `/plans/:planId/objects/:objectId/model-instance` | Get the model instance for a polygon (if any). |
| `PATCH` | `/plans/:planId/objects/:objectId/model-instance` | Update model properties (heading, scale, zOrientation). |
| `DELETE` | `/plans/:planId/objects/:objectId/model-instance` | Detach model from polygon (removes instance record, keeps file). |
| `GET` | `/plans/:planId/model-instances` | List all model instances in the plan (for rendering). |

### 11.3 Stamp/Clone

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/plans/:planId/objects/:objectId/clone-with-model` | Clone a polygon and its model instance. Body: `{ center: {lng, lat} }`. Creates new polygon + instance on the same layer. Returns both records. |

---

## 12. Web App UI Changes

### 12.1 New/Modified Components

| Component | Location | Purpose |
|-----------|----------|---------|
| `ModelUploader.tsx` | `components/models3d/` | File upload for glTF/GLB, drag-and-drop + file picker. |
| `ModelPropertiesModal.tsx` | `components/models3d/` | Edit 3D Model Properties modal (heading, scale, Z orientation, replace file). |
| `ModelPalette.tsx` | `components/models3d/` | Scrollable list of models for stamp/clone. Right-side tool palette. |
| `ModelRenderer.tsx` | `components/models3d/` | Three.js custom layer — loads and renders all model instances on the map. |
| `ShadowControls.tsx` | `components/shadow/` | Shadow tool panel (on/off toggle, month slider, time slider). |
| `ShadowSimulator.tsx` | `components/shadow/` | Existing file — update to use SunCalc with plan coordinates and drive the DirectionalLight. |

### 12.2 Top Toolbar Additions

Two new buttons in the top toolbar:

- **"3D Models"** — Toggle visibility of all models. Only visible when the plan has at least one model instance.
- **"Shadows"** — Opens the Shadow Controls panel on the right. Only visible when the plan has at least one model instance.

### 12.3 Edit Polygon Panel Changes

The existing Edit Polygon panel gains a new section at the bottom:

- Model upload area (when no model attached).
- Model info + "Edit Properties" / "Replace" / "Remove" buttons (when model attached).

---

## 13. Acceptance Criteria

### 13.1 Model Upload & Display

- [ ] User can upload a `.gltf` file to a polygon via the Edit Polygon panel.
- [ ] User can upload a `.glb` file and it renders correctly.
- [ ] Model appears on the map immediately after upload — no additional save step.
- [ ] Model is stored in the owner's Google Drive `models/` folder.
- [ ] Model scales uniformly to fit within the polygon's bounding box without distortion (contain mode — aspect ratio preserved, Z proportional).
- [ ] Default heading is 180° (south-facing).
- [ ] Model renders in both 2D (flat) and 3D terrain modes.

### 13.2 Model Properties

- [ ] User can open "Edit 3D Model Properties" modal from the Edit Polygon panel.
- [ ] Fit Mode toggle switches between "Uniform (Contain)" and "Stretch to Fill" with real-time preview.
- [ ] In Uniform mode, model preserves aspect ratio and fits within the polygon without distortion.
- [ ] In Stretch mode, model fills the full polygon bounding box (may distort aspect ratio).
- [ ] Heading slider rotates the model in real time on the map.
- [ ] X, Y, Z scale sliders adjust the model dimensions independently in real time (applied on top of Fit Mode base).
- [ ] "Follow Terrain" orients the model to match the terrain slope.
- [ ] "Plumb to Earth" orients the model straight up regardless of terrain.
- [ ] User can replace the model file from the properties modal.
- [ ] Each polygon instance has independent properties (including Fit Mode).

### 13.3 Model Palette & Stamp/Clone

- [ ] Model palette appears in the tool palette when at least one model exists in the plan.
- [ ] Palette lists all unique model files across the plan.
- [ ] Clicking a model in the palette starts a placement mode with a ghost polygon preview.
- [ ] Clicking on the map places a cloned polygon + model instance.
- [ ] Cloned instance is on the same layer as the source polygon.
- [ ] Cloned instance references the same Drive file (no duplication).
- [ ] Cloned instance has default properties (independent from source).

### 13.4 Visibility Toggle

- [ ] "3D Models" button appears in the top toolbar when models exist.
- [ ] Toggling off hides all 3D models; toggling on shows them.
- [ ] Polygons remain visible when models are hidden.

### 13.5 Shadow Simulation

- [ ] "Shadows" button appears in the top toolbar when models exist.
- [ ] Shadows tool panel shows on/off toggle, month slider (Jan–Dec), time slider (1 AM–midnight).
- [ ] Sun position is calculated using SunCalc with the plan's center lat/lng.
- [ ] Shadows cast onto the ground plane and onto other models.
- [ ] Moving sliders updates shadows in real time.
- [ ] Shadows are hidden when "3D Models" visibility is off.

### 13.6 Permissions

- [ ] Contributors can upload, edit, replace, remove, and clone models.
- [ ] Viewers can see models and use shadow controls but cannot upload/edit/clone.
- [ ] Contributor uploads go to the plan owner's Google Drive.

### 13.7 Cleanup & Edge Cases

- [ ] Replacing a model removes the old DB reference but keeps the Drive file.
- [ ] Deleting a polygon with a model removes the instance record but keeps the Drive file.
- [ ] Deleting a polygon that was the source of clones does not affect the cloned instances.
- [ ] Plans with no models do not show the "3D Models" or "Shadows" toolbar buttons.

---

## 14. Out of Scope (This Epic)

- Model formats other than glTF/GLB (OBJ, FBX, STL) — server-side conversion from OBJ/STL is captured in the Model Library backlog (§16.3).
- Model upload file size limits (rely on Google Drive quotas for now).
- Model editing within LandPlan (no built-in 3D editor).
- Animation playback for animated glTF models.
- Shadow heatmap/overlay (quantified solar exposure analysis).
- Mobile app 3D model support.
- Model library (public, user-global, cross-plan) — captured as a backlog item in §16 below. Schema and storage are forward-compatible.
- Texture/material editing — default color and standard texture application is captured in the Model Library backlog (§16.3).

---

## 15. Implementation Order

1. **Database migration** — Create `Model3DFile` and `Model3DInstance` tables. Update Prisma schema.
2. **API endpoints** — Model file upload/list/download, instance CRUD, clone endpoint.
3. **Three.js + MapLibre integration** — `ModelRenderer.tsx` custom layer following the reference example. Load and render a single hardcoded model to validate the pipeline.
4. **Model upload UI** — `ModelUploader.tsx` in the Edit Polygon panel. End-to-end upload → render flow.
5. **Model properties modal** — `ModelPropertiesModal.tsx` with heading, scale, Z orientation controls + real-time preview.
6. **Model palette & stamp/clone** — `ModelPalette.tsx` tool, placement mode, clone API integration.
7. **Visibility toggle** — "3D Models" button in top toolbar.
8. **Shadow simulation** — `ShadowControls.tsx` panel, SunCalc integration, DirectionalLight shadow mapping.
9. **Permission enforcement** — Apply sharing permission checks to all model endpoints and UI controls.
10. **Performance optimization** — Geometry caching, instanced rendering, LOD for distant models.

---

## 16. Backlog: Model Library (Lower Priority)

This feature is **not part of the current epic** but is captured here to ensure the current design remains forward-compatible. The schema (`Model3DFile.source`, nullable `planId`) and folder structure (`User_Model_Library/`) are designed to make this addition straightforward.

### 16.1 Concept

Three tiers of model libraries, each progressively wider in scope:

| Tier | Scope | Storage | Managed By |
|------|-------|---------|------------|
| **Plan Library** | Models uploaded to a specific plan | Plan owner's Google Drive `{Plan}/models/` | Plan owner + contributors |
| **User Library** | User's personal collection, available across all their plans | User's Google Drive `User_Model_Library/` | The user |
| **LandPlan Public Library** | Curated common models (trees, fences, vehicles, buildings) available to all users | LandPlan CDN / Cloud Storage (not user Drive) | LandPlan (admin-managed) |

### 16.2 User Workflow (Future)

**Home Page → "My Model Library":**
- Browse/search the user's global library.
- Upload new models to the user library.
- Pull models from any of their plan `models/` folders into the user library (copies the file to `User_Model_Library/`).
- Browse the LandPlan public library and add models to their user library (copies from CDN to `User_Model_Library/`).

**Within a Plan → Model Palette:**
- The palette currently shows plan-level models only. In the library version, it would gain tabs or a source filter: "This Plan" / "My Library" / "LandPlan Library".
- Selecting a model from the user or public library for the first time in a plan would create a `Model3DFile` record with `source: user_library` or `source: public_library`.

### 16.3 Format Conversion & Default Materials

The library upload flow will accept additional file formats beyond glTF/GLB and convert them server-side:

| Input Format | Extension | Conversion |
|-------------|-----------|------------|
| OBJ | `.obj` (+ `.mtl`) | Server-side convert to glTF via a conversion pipeline (e.g., `obj2gltf` npm package or Blender headless). |
| STL | `.stl` | Server-side convert to glTF (e.g., Three.js `STLLoader` → `GLTFExporter`, or Blender headless). |
| glTF / GLB | `.gltf` / `.glb` | No conversion needed — stored as-is. |

After conversion, the user can apply a **default appearance** before saving to their library:

- **Default color:** A single solid color applied to the entire model (hex picker). Useful for STL files which carry no material data.
- **Standard texture:** Choose from a small set of LandPlan-provided textures (wood, concrete, metal, brick, grass, etc.) applied as a uniform material.
- **Keep original:** If the source file includes materials/textures (common with OBJ+MTL), preserve them as-is.

The converted glTF file with the applied material is what gets stored in Google Drive. The original source file is not retained.

> **Implementation note:** Format conversion should happen server-side (Cloud Run or a Cloud Function) to avoid shipping large conversion libraries to the browser. The conversion is a one-time operation during library upload, not during plan rendering — all models in plans are always glTF/GLB.

### 16.4 Google Drive Folder Setup

When a user first connects Google Drive, the setup flow should create the `User_Model_Library/` folder alongside the plan folders. This can be added proactively in the current epic (low cost) or deferred.

### 16.5 Forward-Compatibility Hooks in Current Epic

The following design decisions in the current epic ensure the library feature can be added without breaking changes:

- `Model3DFile.planId` is **nullable** — user-library and public-library models won't be tied to a plan.
- `Model3DFile.source` enum includes `user_library` and `public_library` values — no schema migration needed.
- `Model3DFile.driveFileId` is **nullable** — public library models may be served from a CDN instead of Drive.
- Drive file retention on delete — models are never deleted from Drive, so promoting a plan model to the user library won't create orphan references.
- The `Model3DInstance` → `Model3DFile` relationship is a foreign key, not a file path — changing where the file is stored doesn't affect instances.

---

*This document should be read alongside `architecture.md`, `build_roadmap.md`, and `requirements.md` (Sharing Epic).*
