# JSON Canvas Validation & Layout Guidelines

## ID Generation

Node and edge IDs must be unique strings. Obsidian generates 16-character hexadecimal IDs:

```json
"id": "6f0ad84f44ce9c17"
"id": "a3b2c1d0e9f8g7h6"
"id": "1234567890abcdef"
```

Format: 16-character lowercase hex string (64-bit random value). Tools should generate IDs in this format for compatibility.

## Validation Rules

1. All `id` values must be unique across nodes and edges
2. `fromNode` and `toNode` must reference existing node IDs
3. Required fields must be present for each node type
4. `type` must be one of: `text`, `file`, `link`, `group`
5. `backgroundStyle` must be one of: `cover`, `ratio`, `repeat`
6. `fromSide`, `toSide` must be one of: `top`, `right`, `bottom`, `left`
7. `fromEnd`, `toEnd` must be one of: `none`, `arrow`
8. Color presets must be `"1"` through `"6"` or valid hex color (see [Colors](colors.md))

## Layout Guidelines

### Positioning

- Coordinates can be negative (canvas extends infinitely)
- `x` increases to the right
- `y` increases downward
- Position refers to top-left corner of node

### Recommended Sizes

| Node Type    | Suggested Width | Suggested Height |
| ------------ | --------------- | ---------------- |
| Small text   | 200-300         | 80-150           |
| Medium text  | 300-450         | 150-300          |
| Large text   | 400-600         | 300-500          |
| File preview | 300-500         | 200-400          |
| Link preview | 250-400         | 100-200          |
| Group        | Varies          | Varies           |

### Spacing

- Leave 20-50px padding inside groups
- Space nodes 50-100px apart for readability
- Align nodes to grid (multiples of 10 or 20) for cleaner layouts
