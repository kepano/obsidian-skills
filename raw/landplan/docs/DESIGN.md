# Design System Strategy: The Digital Cartographer

## 1. Overview & Creative North Star
The "Creative North Star" for this design system is **The Digital Cartographer**. We are moving away from the cold, clinical nature of traditional GIS software and toward a high-end, editorial experience that feels as grounded as the land it maps.

This system breaks the "template" look by treating the screen like a physical drafting table. We reject the rigid, boxed-in layouts of standard SaaS. Instead, we use **intentional asymmetry**, where text elements might overlap subtle topographic textures, and **high-contrast typography scales** that command authority. The goal is to make the user feel like they are not just looking at data, but surveying an estate.

---

## 2. Colors: Tonal Depth & Organic Transitions
Our palette is rooted in the earth but polished for the screen. We use forest greens and moss tones for action, while warm neutrals provide a sophisticated canvas.

### The "No-Line" Rule
**Explicit Instruction:** You are prohibited from using 1px solid borders to section content. Traditional "dividers" make a UI feel cheap and cluttered. Boundaries must be defined solely through background color shifts. For example, a `surface-container-low` section should sit against a `surface` background to create a clean, modern break.

### Surface Hierarchy & Nesting
Treat the UI as a series of physical layers—like stacked sheets of fine vellum paper. Use the following tiers to define importance:
- **Surface (Base):** `#f8f9ff` (The primary canvas)
- **Surface-Container-Low:** `#eef4ff` (For secondary sidebar or background sections)
- **Surface-Container-High:** `#e0e9f8` (For active cards or elevated utility panels)

### The "Glass & Gradient" Rule
To escape the "flat" look, use **Glassmorphism** for floating map utilities. Apply `surface-variant` (`#dae3f2`) at 70% opacity with a `20px` backdrop-blur.

### Signature CTAs
Main action buttons or hero accents should not be flat. Use a subtle linear gradient from `primary` (`#466800`) to `primary-container` (`#89b838`) at a 135-degree angle. This provides a tactile, "living" quality to the moss-green tones.

### Color Tokens

| Token | Value |
|---|---|
| `background` | `#f8f9ff` |
| `surface` | `#f8f9ff` |
| `surface-bright` | `#f8f9ff` |
| `surface-dim` | `#d2dbea` |
| `surface-container-lowest` | `#ffffff` |
| `surface-container-low` | `#eef4ff` |
| `surface-container` | `#e5eefe` |
| `surface-container-high` | `#e0e9f8` |
| `surface-container-highest` | `#dae3f2` |
| `surface-variant` | `#dae3f2` |
| `surface-tint` | `#466800` |
| `primary` | `#466800` |
| `primary-container` | `#89b838` |
| `primary-fixed` | `#c0f36c` |
| `primary-fixed-dim` | `#a5d653` |
| `on-primary` | `#ffffff` |
| `on-primary-container` | `#2d4500` |
| `on-primary-fixed` | `#121f00` |
| `on-primary-fixed-variant` | `#344e00` |
| `secondary` | `#565f6c` |
| `secondary-container` | `#d7e0f0` |
| `secondary-fixed` | `#dae3f2` |
| `secondary-fixed-dim` | `#bec7d6` |
| `on-secondary` | `#ffffff` |
| `on-secondary-container` | `#5a6370` |
| `on-secondary-fixed` | `#131c27` |
| `on-secondary-fixed-variant` | `#3e4754` |
| `tertiary` | `#536067` |
| `tertiary-container` | `#9facb3` |
| `tertiary-fixed` | `#d7e5ec` |
| `tertiary-fixed-dim` | `#bbc9d0` |
| `on-tertiary` | `#ffffff` |
| `on-tertiary-container` | `#344047` |
| `on-tertiary-fixed` | `#111d23` |
| `on-tertiary-fixed-variant` | `#3c494f` |
| `on-surface` | `#131c27` |
| `on-surface-variant` | `#434938` |
| `on-background` | `#131c27` |
| `inverse-surface` | `#28313d` |
| `inverse-on-surface` | `#eaf1ff` |
| `inverse-primary` | `#a5d653` |
| `outline` | `#747966` |
| `outline-variant` | `#c3c9b3` |
| `error` | `#ba1a1a` |
| `error-container` | `#ffdad6` |
| `on-error` | `#ffffff` |
| `on-error-container` | `#93000a` |

---

## 3. Typography: The Editorial Voice
We use **Plus Jakarta Sans** for display and headlines. Its slightly humanist geometry feels modern yet approachable, avoiding the generic tech feel of Inter. **Manrope** serves as the body font for its exceptional legibility in data-heavy contexts.

| Scale | Size | Usage |
|---|---|---|
| Display-LG | `3.5rem` | Hero moments. Tight letter-spacing (`-0.02em`) for bold, confident statements. |
| Headline-MD | `1.75rem` | Section titles. Generous line-height for editorial breathability. |
| Body-LG | `1rem` | Standard descriptive text. Approachable and accessible. |
| Label-SM | `0.6875rem` | Map coordinates and metadata. Always uppercase, `+0.05em` tracking for a "technical blueprint" feel. |

- **Headline / Display font:** Plus Jakarta Sans
- **Body font:** Manrope
- **Label font:** Plus Jakarta Sans

---

## 4. Elevation & Depth
Depth is earned through **Tonal Layering**, not structural lines.

- **The Layering Principle:** Place a `surface-container-lowest` (`#ffffff`) card on a `surface-container-low` (`#eef4ff`) section. This creates a soft, natural "lift" that feels like a physical map overlay.
- **Ambient Shadows:** For floating elements (compass, layer picker): `box-shadow: 0 12px 40px rgba(19, 28, 39, 0.06)`. Uses `on-surface` (`#131c27`) at very low opacity to mimic natural ambient light.
- **The "Ghost Border" Fallback:** If a border is essential for accessibility, use `outline-variant` (`#c3c9b3`) at **20% opacity**. Never use 100% opaque borders.

---

## 5. Components: Bespoke GIS Elements

### Buttons
- **Primary:** Gradient from `#466800` to `#89b838`. Roundedness: `lg` (`1rem`). Large padding (`1.4rem` horizontal).
- **Secondary:** Surface-tinted. No border. Use `secondary-container` (`#d7e0f0`) background with `on-secondary-container` text.
- **Tertiary:** Text-only with an icon. Use `primary` color for the label.

### Input Fields & Search
Use `surface-container-lowest` (`#ffffff`) background. Subtle 1px "Ghost Border" that turns to full `primary` (`#466800`) on focus. Corner radius: `md` (`0.75rem`).

### Cards & Lists
**Strict Rule:** No dividers. Separate list items using `spacing-3` (`1rem`) of vertical whitespace. For card groups, use alternating background tones (`surface-container-low` vs `surface-container-highest`) to distinguish between different land parcels or data sets.

### Custom GIS Components
- **The Layer Stack:** A floating glassmorphic panel in the bottom-left. Items use `label-md` and selection chips that highlight in `primary-fixed-dim` (`#a5d653`).
- **The Tooltip:** Use `inverse-surface` (`#28313d`) background with `inverse-on-surface` text. Apply `xl` (`1.5rem`) corner radius to make map annotations feel organic.

---

## 6. Do's and Don'ts

### Do
- Use topographic line patterns (SVG) as background textures in hero sections at **5% opacity**.
- Use **Generous Whitespace**. If a section feels crowded, double the spacing token (e.g., move from `8` to `16`).
- Align text-heavy content to a narrow, editorial column (`max-width: 680px`) while letting maps and imagery go edge-to-edge.

### Don't
- Use pure black `#000000`. Use `on-surface` (`#131c27`) for all dark text.
- Use sharp corners. Stick to `md` (`0.75rem`) and `lg` (`1rem`) radius tokens.
- Use "default" icons. All icons should have slightly rounded terminals and a consistent `1.5px` stroke weight to match the humanist typography.
