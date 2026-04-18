---
title: TinkerGIS
tags: [tinkergis, gis, tauri, rust, leaflet, desktop]
created: 2026-04-17
updated: 2026-04-17
status: seedling
---

# TinkerGIS

> [!abstract] Summary
> TinkerGIS is a lightweight desktop GIS application built with Tauri (Rust backend) and Leaflet (web-based map renderer). It targets users who want native-app performance and offline capability for GIS tasks without the weight of QGIS or ArcGIS.

---

## What It Is

TinkerGIS sits at the intersection of Tim's GIS domain expertise (shared with the [[wiki/platforms/landplan/README|LandPlan platform]]) and a desire for a fast, hackable, cross-platform desktop tool. Built with Tauri, it ships as a native binary with a Rust core while using Leaflet and web technologies for the map UI — keeping the interface flexible without sacrificing performance.

## Tech Stack

- **Shell / build system:** Tauri
- **Backend:** Rust
- **Map renderer:** Leaflet (HTML/JS)
- **Target platforms:** macOS, Windows, Linux

## Status

Personal / exploratory project. Early development. See [[wiki/meta/log|log]] for recent activity.

## Related

- [[wiki/platforms/landplan/README|LandPlan]] — shares GIS domain; TinkerGIS may inform LandPlan tooling choices
- [[wiki/meta/hot|Hot Context]]
