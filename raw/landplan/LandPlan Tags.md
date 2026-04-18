Here's what's in the database:

**Well-used (from the dropdown):**

| Category  | Count               |
| --------- | ------------------- |
| Photo     | 9                   |
| Structure | 8+1 (case mismatch) |
| Water     | 6+2 (case mismatch) |
| Gate      | 5                   |
| Hazard    | 4                   |
| Other     | 3                   |
| Marker    | 2                   |
| Tree      | 2                   |
| Shrub     | 1                   |
| Fence     | 1                   |
| Road      | 1                   |
| Path      | 1                   |
| Utility   | 1                   |

**Freeform / test data (not from the dropdown):**

- `RAVINE 1` through `RAVINE 9` — looks like test objects where the label was put in the category field
- `Driveway Lunch Hiking` — same issue
- `Service Road` — reasonable but not in the current list

**Notable gaps vs. the current dropdown list:**

- `Photo` is the top category but isn't in the dropdown at all — it appears to be set programmatically (likely when a photo-linked point is created)
- `Service Road` suggests users want road subtypes
- `Structure` / `Water` have case inconsistencies (`structure`, `water`) — worth normalising

Things worth considering for the next epic: consolidating the RAVINE/freeform entries, adding `Photo` as a real category or hiding it from the user-facing dropdown, and potentially splitting broad categories like `Structure` into subtypes.