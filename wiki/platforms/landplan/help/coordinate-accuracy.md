---
title: "Help: About Coordinate Accuracy"
tags: [landplan, help, gps, accuracy, map-objects]
created: 2026-04-19
updated: 2026-04-19
status: seedling
---

# About Coordinate Accuracy

Every point, line, and polygon in your LandPlan map has coordinates — but not all coordinates are equally precise. This article explains what accuracy means, how LandPlan shows it, and how to get better data when it matters.

---

## Why Accuracy Matters

LandPlan is used for real planning decisions: siting a solar array, fencing a pasture, routing a driveway, or briefing a contractor. If your map shows a fence corner 20 metres from where it actually is, your plan is built on a faulty foundation.

Contractors in particular need to know how reliable your spatial data is. A driveway centreline marked ±15 m should not be bid at a fixed price without a site walk. LandPlan shows accuracy information on all map objects so contractors can make that call.

---

## The Accuracy Spectrum

| Method | Typical accuracy | LandPlan tier |
|--------|-----------------|--------------|
| Base-map tracing — snapping to a building in clear aerial imagery | ~2 m | Amber |
| Base-map tracing — snapping to a well-mapped road | ~6 m | Amber |
| Base-map tracing — rural area or low-quality imagery | 15–20 m | Red |
| Consumer GPS (phone app) | ~3 m | Amber |
| Single-receiver RTK (e.g., SparkFun RTK Torch, u-blox) | ~0.15 m | Green |
| Dual-receiver RTK | ~1 cm | Green |
| Professional survey (registered surveyor) | ~5 cm | Green |

**Tier colour key:**
- 🔴 **Red** — accuracy ≥ 10 m. Adequate for rough orientation; do not use for construction siting.
- 🟡 **Amber** — accuracy 0.5–10 m. Good for planning, boundary estimation, and reference.
- 🟢 **Green** — accuracy < 0.5 m. Survey-grade; suitable for construction, permit applications, and legal boundary records.
- ⚫ **Gray** — accuracy unknown. LandPlan has no information on how this data was captured.

---

## How LandPlan Shows Accuracy

### Accuracy badge on map objects

Every map object's properties panel shows a small badge such as `± 6 m` with a coloured dot matching its tier. This badge reflects the best-estimate horizontal accuracy for that object.

### "Show accuracy" layer

In Map Mode, turn on the **Show accuracy** toggle (Layers section of the sidebar) to see a coloured ring drawn around each object at its accuracy radius. Objects with tight accuracy have small rings; objects traced from rough imagery have large rings.

### Property boundary

Your property boundary accuracy is always shown on the **Property Overview** page because it drives your jurisdiction lookup and is the spatial context every contractor sees.

---

## How to Get Better Data

### Option 1 — Hire a registered surveyor

The most accurate option for legal purposes. Your surveyor will provide a certified boundary in KML, GeoJSON, or shapefile format. Import it into LandPlan using the **Import** tool and mark the source as "Professional survey."

### Option 2 — Download county GIS data

Many counties publish parcel boundaries as GIS downloads. These are typically accurate to 1–5 m. Import as KML or GeoJSON and mark the source as "County GIS."

### Option 3 — Use a consumer GPS app

Walk your boundary with a GPS app (Google Maps, Gaia GPS, etc.) and export as GPX or KML. Accuracy is typically 3–5 m — a big improvement over base-map tracing in rural areas.

### Option 4 — Add a Bluetooth RTK receiver

Receivers such as the SparkFun RTK Torch, Emlid Reach, or Bad Elf GNSS connect to your phone via Bluetooth and deliver sub-metre to centimetre accuracy. LandPlan's upcoming **Survey app** will capture RTK-grade coordinates directly. For now, export from your RTK app and import the KML or GeoJSON.

---

## Importing Data with Accuracy Information

When you import a KML or GeoJSON file, LandPlan will ask you:

1. **What is the source of this data?** — choose from the capture method list (survey, GPS app, county GIS, etc.)
2. **Accuracy override (optional)** — if you know the exact accuracy, enter it in metres

LandPlan applies this as a batch to all features in the import. You can refine individual features afterward in their properties panel.

If your file contains embedded accuracy metadata (HDOP tags, GPS accuracy fields), LandPlan will try to read it per-feature automatically.

---

## How LandPlan Uses Accuracy Data

- **Contractor Quote Packages** — accuracy badges are shown on all visible map objects so contractors know which data is reliable and which needs a site walk.
- **Property boundary** — boundary accuracy is prominently displayed on the Property Overview page.
- **Upcoming Survey app** — the LandPlan Survey mobile app will write accuracy data directly when capturing GPS coordinates in the field.

---

## Related

- [[coordinate-accuracy]] — this article (permalink)
- [[epic-gps-accuracy-templates]] — the epic that introduced accuracy metadata to LandPlan
- [[survey-mobile]] — upcoming mobile app that will capture RTK-grade coordinates directly
- [[survey-gps-receiver]] — LandPlan hardware RTK device (concept)
