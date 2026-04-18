---
title: Terra Contour Design System
tags: [landplan, design, ui, frontend, terra-contour]
created: 2026-04-18
updated: 2026-04-18
status: evergreen
---

# Terra Contour — Design System

> [!abstract] North Star
> **The Digital Cartographer.** Moving away from cold, clinical GIS software toward a high-end editorial experience that feels as grounded as the land it maps. The user should feel like they are *surveying an estate*, not looking at a dashboard.

---

## Core Aesthetic

- **Intentional asymmetry** — text may overlap subtle topographic textures; reject rigid boxed-in SaaS layouts
- **High-contrast typography scales** — command authority
- **No explicit lines** — all spatial separation via background color shifts (see rules below)
- **Glassmorphism** for floating map utilities

---

## The "No-Line" Rule

**Prohibited:** 1px solid borders to section content. They make UI feel cheap.

Boundaries defined **solely** through background color shifts. A `surface-container-low` section sits against a `surface` background to create a clean break.

If a border is truly essential for accessibility: use `outline-variant` (`#c3c9b3`) at **20% opacity only** (the "Ghost Border" fallback).

---

## Color Palette

### Surface Hierarchy (stacked vellum layers)

| Token | Value | Usage |
|-------|-------|-------|
| `surface` | `#f8f9ff` | Primary canvas |
| `surface-container-low` | `#eef4ff` | Secondary sidebar / background sections |
| `surface-container` | `#e5eefe` | |
| `surface-container-high` | `#e0e9f8` | Active cards / elevated utility panels |
| `surface-container-highest` | `#dae3f2` | |
| `surface-variant` | `#dae3f2` | Glassmorphism base (at 70% opacity + 20px blur) |
| `surface-dim` | `#d2dbea` | |
| `surface-container-lowest` | `#ffffff` | Lifted cards |

### Primary (Forest Green)

| Token | Value |
|-------|-------|
| `primary` | `#466800` |
| `primary-container` | `#89b838` |
| `primary-fixed` | `#c0f36c` |
| `primary-fixed-dim` | `#a5d653` |
| `on-primary` | `#ffffff` |

**Signature CTAs:** Linear gradient from `primary` (`#466800`) to `primary-container` (`#89b838`) at 135°.

### Secondary / Tertiary / Error

| Token | Value |
|-------|-------|
| `secondary` | `#565f6c` |
| `secondary-container` | `#d7e0f0` |
| `tertiary` | `#536067` |
| `on-surface` | `#131c27` |
| `on-surface-variant` | `#434938` |
| `inverse-surface` | `#28313d` |
| `inverse-on-surface` | `#eaf1ff` |
| `inverse-primary` | `#a5d653` |
| `outline` | `#747966` |
| `outline-variant` | `#c3c9b3` |
| `error` | `#ba1a1a` |

> **Never use pure black `#000000`.** Use `on-surface` (`#131c27`) for all dark text.

---

## Typography

| Scale | Size | Usage |
|-------|------|-------|
| Display-LG | 3.5rem | Hero moments; tight letter-spacing (`-0.02em`) |
| Headline-MD | 1.75rem | Section titles; generous line-height |
| Body-LG | 1rem | Standard descriptive text |
| Label-SM | 0.6875rem | Map coordinates and metadata; always uppercase, `+0.05em` tracking |

- **Headline / Display / Label:** Plus Jakarta Sans
- **Body:** Manrope

---

## Elevation & Depth

- **Tonal Layering:** `surface-container-lowest` (`#ffffff`) card on `surface-container-low` (`#eef4ff`) = soft "lift"
- **Ambient shadow (floating elements):** `box-shadow: 0 12px 40px rgba(19, 28, 39, 0.06)`
- **Glassmorphism (floating map panels):** `surface-variant` at 70% opacity + 20px backdrop-blur

---

## Components

### Buttons

| Type | Spec |
|------|------|
| Primary | Gradient `#466800` → `#89b838`; radius `lg` (1rem); padding `1.4rem` horizontal |
| Secondary | `secondary-container` bg; no border |
| Tertiary | Text-only with icon; `primary` color |

### Input Fields

`surface-container-lowest` bg; Ghost Border (full `primary` on focus); radius `md` (0.75rem).

### Cards & Lists

**No dividers.** `spacing-3` (1rem) vertical whitespace between list items. Alternating `surface-container-low` / `surface-container-highest` backgrounds to distinguish data sets.

### Custom GIS Components

- **Layer Stack:** Floating glassmorphic panel (bottom-left). `label-md` items; selection chips highlight in `primary-fixed-dim` (`#a5d653`).
- **Tooltip / map annotation:** `inverse-surface` (`#28313d`) bg; `inverse-on-surface` text; `xl` (1.5rem) corner radius.

---

## Status Indicators

Small inline **color dot + text label**. No standalone status pills (explicitly deprecated). Implemented as the `StatusDot` shared Terra Contour component.

---

## Spacing & Corner Radius

- All corners: `md` (0.75rem) or `lg` (1rem). No sharp corners.
- If a section feels crowded: double the spacing token (e.g., `8` → `16`).
- Text-heavy content: narrow editorial column `max-width: 680px`. Maps and imagery: edge-to-edge.

---

## Do's and Don'ts

**Do:**
- Topographic line patterns (SVG) as hero background textures at 5% opacity
- Generous whitespace
- Align editorial content to a narrow column while letting maps go edge-to-edge

**Don't:**
- Use pure black `#000000`
- Use sharp corners
- Use "default" icons — all icons should have slightly rounded terminals, consistent 1.5px stroke weight

---

## Icons

Slightly rounded terminals, consistent 1.5px stroke weight throughout. Matches the humanist typography feel.

---

## Related

- [[stitch-designs]] — five named Stitch UI designs using this system
- [[landplan-app]] — the product this system styles
