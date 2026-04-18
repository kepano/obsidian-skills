# LandPlan — Google Stitch Prompt: Projects Ecosystem & New Map Interface

**Use with:** Google Stitch MCP (via Claude Code), following the same workflow as `landplan-stitch-prompt.md`.
**Output:** Web-first designs, desktop and responsive.

This prompt produces **five named designs** that Claude Code will pull from Stitch over a series of build sessions: **New Map Interface**, **Property Overview**, **Project Portfolio Overview**, **Project Detail**, and **Project Activity Detail Drawer**.

---

## 1. Core Aesthetic — Terra Contour ("The Digital Cartographer")

The LandPlan interface follows the **Terra Contour** design system. Refined, natural, and professional — drawing from high-quality architectural plans and topographic maps, not SaaS dashboards. Warm, calm, confident; a "trusted guide."

- **Primary palette:** Forest green accent `#89B838`, deep teal/slate for branding, warm neutral backgrounds (sand, stone, warm gray).
- **Typography:** Plus Jakarta Sans throughout. Humanist, clear, modern.
- **Surfaces:** Subtle shadows, generous rounded corners, warm neutral fills.
- **Icons:** Line-style, slightly rounded, consistent weight.
- **Hover states:** All interactive elements transition to forest green on hover.
- **Tagline:** *"LandPlan — Visualize the future of your property."*
- Avoid Google Earth aesthetics, avoid jargon, avoid tech/SaaS chrome.

**Status indicators:** Small inline color dots + text labels. **No standalone status pills** — explicitly deprecated.

---

## 2. Unified Navigation System

Map Mode and Projects Mode are two coordinated views of the same property plan. They share a **visual language** and feel like flipping between two modes of the same app, but they have **different sidebar contents** — they are not the same sidebar with a mode switch.

### A. Floating Global Control Bar (Top-Left, both modes)
Always in the same position on both Map and Projects pages:
- **Back arrow** — return to the main dashboard.
- **Map/Projects pill toggle** — prominent, high-visibility, labeled "Map" / "Projects". A first-class always-visible control inviting users to flip between spatial and planning views.
- **Utility actions** — camera icon ("Save View") and share icon, both with forest-green hover state.

No full-width top header on either view.

### B. Integrated Collapsible Left Sidebar (both modes, different contents)
A single organized rail in both modes with the **same visual treatment** (warm neutral surface, rounded corners, subtle shadow, collapse icon at the top, LandPlan logo fixed at the bottom replacing any user-profile bubbles). What lives *inside* the rail differs by mode:

**Projects Mode sidebar sections:**
1. Mission (property vision/overview)
2. Projects (ranked stack)
3. Stakeholders
4. Reference Info
5. Docs

**Map Mode sidebar sections:**
1. Layers (satellite, topography, etc.)
2. Saved Views (snapshots of locations/angles)
3. Structures (house icon — buildings, sheds)
4. Plants (orchards, gardens, timber stands)
5. Projects (object filtering by project association — see §4)
6. Time (Sun/Shadow slider + Project Timeline slider, stacked)

Each Map Mode section uses eye-icon visibility toggles at both section and item level. Projects Mode sections behave as document navigation, not visibility filters.

### C. Mode-Specific Floating Elements
- **Projects Mode:** more traditional and document-like. The left sidebar is the primary organizer. **Avoid persistent floating panels or modals on the right side.** Secondary content uses slide-in drawers from the right edge (e.g., Project Activity Detail Drawer) or inline sections — not floating windows.
- **Map Mode:** spatial complexity requires some floating elements. See §4 for exact placement.

### D. Footer
- **Projects Mode pages** (Property Overview, Project Portfolio Overview, Project Detail): standard dark blue LandPlan footer with copyright *"© 2026 Smart Farm Technologies. Surveying the Future."*
- **New Map Interface:** **no dark footer** — it takes up too much canvas. Show the LandPlan logo at the very bottom of the sidebar instead.

---

## 3. Projects Mode Design Standards

Projects Mode pages should feel like an **organized, well-crafted document**.

- **Header style:** clean, centered titles with clear secondary metadata (location, ID, status).
- **Mission statement treatment:** large, impactful, pull-quote scale typography for property-level vision content.
- **Project cards:** drag-to-reorder ranked stacks with inline status dots (color dot + text label, never pills).
- **Detail drawers:** slide-in from the right edge for activities or contextual details.
- **Large imagery cards** (where present) are fully clickable with a subtle scale effect on hover.

---

## 4. Map Mode Design Standards

Map Mode maximizes the spatial canvas while retaining core controls.

- **Sidebar content:** advanced object management with eye-icon visibility toggles at section and item level.
- **Floating map toolbar — LEFT-CENTER:** a narrow vertical pill container for active mapping tools: **Select, Object, Distance, Area, Import, Photo.** This is the tools palette. Keep it on the **left-center** of the page, not the right. *(Stitch tends to move this to the right — do not.)*
- **Tool windows and edit modals — RIGHT-CENTER:** contextual windows such as "Measure Area", "Edit Tree Stand", and "Edit Tree Properties" float on the **right side, vertically centered**. This is the right-side slot for spatial editing UI.
- **Do not include a Terrain Analysis panel.** Stitch has previously added elevation/slope/aspect analysis panels on the right rail — this is explicitly out of scope and must not appear in the New Map Interface design. The right-center slot is reserved for tool/edit windows only.
- **Time controls in sidebar Time section:** two sliders stacked and clearly distinguished:
  1. **Sun/Shadow slider** — hours of day, drives sun-path and shadow simulation.
  2. **Project Timeline slider** — months-to-years, progressively reveals map objects based on their linked activities' earliest completion dates. Left edge = earliest project start date across the plan; right edge = latest activity completion date; default position = today. Unlinked objects and objects on undated projects remain always visible.

---

## 5. The Five Named Designs

### 5.1 New Map Interface
The spatial view. Refresh of the existing map page visuals — **not new mapping features**; the functional feature set is unchanged. The menus are dramatically cleaner and integrate with the new project planning data.

- Floating Global Control Bar (top-left): back, Map/Projects toggle set to "Map", save-view, share.
- Integrated collapsible left sidebar with the six Map Mode sections (Layers, Saved Views, Structures, Plants, Projects, Time). LandPlan logo pinned at the bottom of the sidebar. **No dark footer.**
- **Projects section in the sidebar acts as an object filter** (not project management): list each project with a color swatch, name, inline status dot, and eye toggle. Section-level eye toggle controls all projects. Include a special "Unassigned" row for objects with no project linkage. Unchecked projects' objects dim/desaturate on the canvas (not hidden). Checked projects' objects show small project-colored dots. The property boundary is always visible with a distinct Terra Contour treatment.
- Time section at the bottom of the sidebar with the two stacked sliders (Sun/Shadow and Project Timeline), visually distinct so users never confuse hours-of-day with project timeline.
- **Floating tools palette on the LEFT-CENTER** (Select, Object, Distance, Area, Import, Photo).
- **Right-center slot reserved for tool windows and edit modals** (e.g., Measure Area, Edit Tree Stand, Edit Tree Properties). Show at least one example edit window to convey the pattern. No Terrain Analysis content.
- Map canvas fills the rest of the screen edge-to-edge.

### 5.2 Property Overview
Program-level view of the entire property — the mission statement page that helps stakeholders understand the owner's long-horizon vision and why projects are prioritized the way they are. Also the home for property-wide reference info that applies across all projects.

- Floating Global Control Bar (top-left), toggle set to "Projects".
- Projects Mode left sidebar (Mission, Projects, Stakeholders, Reference Info, Docs) with "Mission" as the active section.
- Main canvas content, top to bottom:
  - **Large impactful mission statement** — pull-quote scale typography, markdown-rendered, editable. Hero of the page.
  - **Property metadata block:** plan title, location (state/county/city/village), property acreage, boundary confirmation status, APN (if entered).
  - **Jurisdiction stale-flag banner** — visible only if the boundary changed and ordinance entries need review. Non-destructive, warm tone ("Jurisdiction changed — some reference entries may need review").
  - **Reference Info section** — the five categories (Zoning, Rainwater Management, Off-Grid Rules, Permitting, Public Land) as organized document-style subsections with entry counts, source badges (user/system/agent — e.g., small "added by Claude Coworker" label), and expand-to-see-entries interaction.
  - **Docs section** — property-level document attachments.
- Standard dark blue LandPlan footer with "© 2026 Smart Farm Technologies. Surveying the Future."

### 5.3 Project Portfolio Overview
The ranked stack of projects — primary Projects Mode landing page after Property Overview.

- Floating Global Control Bar (top-left), toggle set to "Projects".
- Projects Mode left sidebar with "Projects" as the active section.
- Main canvas: **drag-to-reorder ranked stack** of project cards, one per row, sequence number on the left edge. Each card shows: project title, objective one-liner, inline status (color dot + text), date range, budget range ($low–$high USD), activity count, assigned stakeholder avatars, a small project-color swatch, and optional rough-actual cost.
- Subtle inline completion prompt on cards where all activities are complete: *"All activities complete — mark project complete?"* Not a pill.
- Top of canvas: "+ New Project" action.
- Large imagery cards (where a project has a hero image) are fully clickable with subtle scale-on-hover.
- Standard dark blue LandPlan footer.

### 5.4 Project Detail
Clicking a project card opens this page.

- Floating Global Control Bar (top-left), toggle set to "Projects".
- Projects Mode left sidebar.
- Main canvas:
  - **Header:** project title (inline editable), inline status, sequence position, date range, budget range, rough actual cost.
  - **Objective block:** markdown-rendered vision for this project.
  - **Primary tabs:** Activities (default), Quote Packages, DIY Estimate, Docs.
  - **Activities tab** — two coordinated views:
    1. List view with drag handles (manual sort order); each row shows title, duration in days, assigned stakeholder avatar, inline status, linked map object count, dependency count.
    2. Mermaid `flowchart` rendering of the dependency graph (FS/SS/FF/SF dependencies). Read-only visualization; editing happens in the list's add-dependency dropdown.
    - Side-by-side on wide screens; toggleable on narrow screens.
- Standard dark blue LandPlan footer.

### 5.5 Project Activity Detail Drawer
A **slide-in panel from the right edge**, not a floating modal. Triggered from either Project Detail's activity list or from the New Map Interface when a map object linked to an activity is tapped.

- Activity title, inline status, duration in days, planned start/end, completion date.
- Assigned stakeholder with avatar and role label.
- Notes section — append-only log showing who wrote each note and when (stakeholders' notes appear here).
- Linked map objects as small chips with thumbnails; each tappable to fly the map to that object (when opened from the Map Interface).
- Dependencies: compact list of predecessors and successors with dependency-type labels (FS/SS/FF/SF).
- Attached docs (Drive files).
- "Open in Map" action (when opened from Project Detail) that flips to the Map Interface and highlights linked objects.
- The drawer renders consistently in both Projects Mode and Map Mode so it feels like the same component in both contexts.

---

## 6. Cross-Design Requirements

- **Project color swatches** are consistent across every design: sidebar, cards, map dots, drawer chips.
- **Drag affordances** are obvious but not heavy.
- **Empty states** are warm and encouraging ("No projects yet — what's the first thing you'd like to build?"), never scolding.
- **Sidebar collapse** pattern is identical in both modes.
- **Responsive:** desktop-primary. Project pages and the Activity Detail Drawer collapse gracefully at tablet widths.
- **Accessibility:** high contrast on status dots, focus rings on interactive elements, keyboard-navigable drag reordering.
- **Component reuse:** shared visual components (sidebar shell, top-left control bar, drawer) should look identical across both modes so Claude Code can reuse them between `MapPage.tsx` (currently `PlanPage.tsx`) and `ProjectPage.tsx`.

---

## 7. Out of Scope for This Design Pass

- Contractor Quote Package view (separate future Stitch pass).
- Stakeholder management screen.
- DIY Estimate editor internals (tab placeholder only in Project Detail).
- Quote comparison view for owners.
- Mobile app screens.
- Login, onboarding, registration flows.
- **Terrain Analysis panel — explicitly excluded from Map Mode.**

---

## 8. Beta Context (for Claude Code, not Stitch)

The New Map Interface will be built as an independent Beta view alongside the existing map page so it can be A/B tested before replacing the current map. This is a build-sequencing note for Claude Code — the Stitch designs themselves do not need to reflect any "beta" branding. Target page files: `MapPage.tsx` (new, Beta, replacing today's `PlanPage.tsx` at cutover) and `ProjectPage.tsx` (greenfield). Shared visual components should be factored for reuse across both.

---

*Generated for Google Stitch MCP. Initiate from Claude Code with the Stitch MCP server configured.*
