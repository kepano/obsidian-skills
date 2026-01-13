# JSON Canvas Colors

Canvas elements support color customization using either hex colors or preset color IDs.

## Hex Colors

Use standard 6-digit hex color codes:

```json
{
  "color": "#FF0000"
}
```

Format: `#RRGGBB` where each pair is a hexadecimal value (00-FF).

## Preset Colors

Use color ID strings `"1"` through `"6"`:

```json
{
  "color": "1"
}
```

| ID  | Color Name | Hex Code |
| --- | ---------- | -------- |
| `1` | Red        | #EB3B3B  |
| `2` | Orange     | #E8932F  |
| `3` | Yellow     | #E8C547  |
| `4` | Green      | #5DA22F  |
| `5` | Blue       | #4573D9  |
| `6` | Purple     | #A85EDF  |

## Usage

Colors can be applied to:

- **Nodes** - Set `color` property on any node
- **Edges** - Set `color` property on edge to change line color
- **Groups** - Set `color` property on group nodes for visual distinction

### Example: Colored Node

```json
{
  "id": "6f0ad84f44ce9c17",
  "type": "text",
  "x": 0,
  "y": 0,
  "width": 400,
  "height": 200,
  "text": "# Important",
  "color": "1"
}
```

### Example: Colored Edge

```json
{
  "id": "f67890123456789a",
  "fromNode": "node1",
  "toNode": "node2",
  "color": "4",
  "label": "connects to"
}
```

## Color Selection Tips

- Use contrasting colors to distinguish node types or categories
- Reserve red (#EB3B3B) for critical or error states
- Use green (#5DA22F) for completed or positive states
- Use yellow (#E8C547) for warnings or pending states
- Use blue (#4573D9) for informational content
- Mix hex colors with presets for visual consistency
