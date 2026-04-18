---
title: LandPlan Survey GPS Receiver (Hardware)
tags: [landplan, hardware, gps, rtk, bluetooth, product]
created: 2026-04-18
updated: 2026-04-18
status: seedling
---

# LandPlan Survey GPS Receiver (Hardware)

> [!abstract] One-liner
> A physical device that connects to a smartphone via Bluetooth and a high-accuracy GPS/RTK antenna via USB, delivering survey-grade coordinates to [[survey-mobile]].

---

## What It Does

The LandPlan Survey GPS Receiver is a bridge device that turns a smartphone into a professional survey instrument. It provides a "poor man's RTK" option for landowners who want centimetre-level GPS accuracy without hiring a full survey crew.

### Core Capabilities (Concept)

- Connects to the [[survey-mobile|LandPlan Survey mobile app]] via Bluetooth
- Connects to an external RTK-capable GPS antenna via USB
- Provides `mobile_rtk_single` or `mobile_rtk_dual` accuracy (~0.15 m / ~0.01 m) per the [[epic-gps-accuracy-templates|accuracy metadata schema]]
- Optional 360° camera integration for ground-level imagery capture (Street View–style)
- Firmware TBD

---

## Status

**Concept only.** Hardware design not started.

The software ecosystem ([[landplan-app]], [[survey-mobile]]) is being built first. Hardware follows once the data model and mobile app are mature.

---

## Hardware Concept

| Component | Role |
|-----------|------|
| Embedded controller | Routes data between USB GPS receiver and Bluetooth |
| Bluetooth LE / BT Classic | Streams NMEA sentences to the mobile app |
| USB-A or USB-C port | Accepts off-the-shelf RTK GPS receivers (e.g., SparkFun RTK Torch) |
| Optional USB/HDMI port | 360° camera connection |
| Battery | Field-deployable; charge via USB-C |

Compatible GPS receivers in the accuracy schema include `"SparkFun RTK Torch"` as an example `captureSource`.

---

## Related

- [[survey-mobile]] — the mobile app this pairs with
- [[landplan-app]] — the web platform where captured data lands
- [[epic-gps-accuracy-templates]] — accuracy metadata model the device populates
