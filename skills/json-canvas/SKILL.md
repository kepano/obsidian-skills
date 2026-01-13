---
name: json-canvas
description: Create and edit JSON Canvas files (.canvas) with nodes, edges, groups, and connections. Use when working with .canvas files, creating or editing visual canvases, mind maps, flowcharts, diagrams, graphs, or network visualizations in Obsidian.
allowed-tools: [Read, Write, Edit, Glob]
---

# JSON Canvas Skill

This skill enables agents to create and edit valid JSON Canvas files (`.canvas`) used in Obsidian and other applications.

## Overview

JSON Canvas is an open file format for infinite canvas data. Canvas files use the `.canvas` extension and contain valid JSON following the [JSON Canvas Spec 1.0](https://jsoncanvas.org/spec/1.0/).

### Current Version

JSON Canvas Specification: 1.0

### Supported in

- Obsidian (built-in Canvas app)
- Other applications following the spec

## File Structure

A canvas file contains two top-level arrays:

```json
{
  "nodes": [],
  "edges": []
}
```

- `nodes` (optional): Array of node objects representing elements on the canvas
- `edges` (optional): Array of edge objects connecting nodes

## Nodes

Nodes are objects placed on the canvas. There are four node types:

1. **text** - Text content with Markdown
2. **file** - Reference to files/attachments
3. **link** - External URL
4. **group** - Visual container for other nodes

For detailed node specifications, see [Node Types](node-types.md).

### Quick Reference: Node Properties

All nodes require:

- `id` - Unique identifier (16-char hex string)
- `type` - One of: `text`, `file`, `link`, `group`
- `x`, `y` - Position in pixels
- `width`, `height` - Dimensions in pixels

Optional:

- `color` - Preset ID (`"1"`-`"6"`) or hex color

See [Node Types](node-types.md) for type-specific attributes.

## Edges

Edges are lines connecting nodes with optional labels and styling.

### Quick Reference: Edge Properties

Required:

- `id` - Unique identifier
- `fromNode` - Source node ID
- `toNode` - Target node ID

Optional:

- `fromSide`, `toSide` - Connection sides (`top`, `right`, `bottom`, `left`)
- `fromEnd`, `toEnd` - Endpoint shapes (`none`, `arrow`)
- `color` - Preset ID or hex color
- `label` - Text label on edge

See [Edges](edges.md) for detailed specifications.

## Colors

Canvas elements support colors using presets or hex codes.

**Preset Colors:**

- `"1"` = Red, `"2"` = Orange, `"3"` = Yellow
- `"4"` = Green, `"5"` = Blue, `"6"` = Purple

**Hex Format:** `"#RRGGBB"` (e.g., `"#FF0000"`)

See [Colors](colors.md) for complete reference and usage examples.

## Layout Recommendations

### Node Sizing

| Type         | Width   | Height  |
| ------------ | ------- | ------- |
| Small text   | 200-300 | 80-150  |
| Medium text  | 300-450 | 150-300 |
| Large text   | 400-600 | 300-500 |
| File preview | 300-500 | 200-400 |
| Link preview | 250-400 | 100-200 |

### Best Practices

- Align nodes to 10-20px grid for cleaner layouts
- Space nodes 50-100px apart for readability
- Use groups with 20-50px padding to organize related nodes
- Coordinates can be negative (canvas is infinite)

For detailed validation rules and layout guidelines, see [Validation & Layout](validation.md).

## ID Generation

Node and edge IDs should be 16-character lowercase hexadecimal strings (64-bit random):

```
"6f0ad84f44ce9c17"
"a3b2c1d0e9f8g7h6"
"1234567890abcdef"
```

This format ensures compatibility with Obsidian and other canvas implementations.

## Examples

See [Examples](examples.md) for complete, runnable canvas files:

- **Research Mind Map** - Multi-document research canvas with supporting files
- **Flowchart** - Decision flow with conditional branching

## Reference Guides

- [Node Types](node-types.md) - Text, file, link, and group node specifications
- [Edges](edges.md) - Connection specifications and styling
- [Colors](colors.md) - Color system (presets and hex)
- [Validation & Layout](validation.md) - Validation rules and layout guidelines
- [Examples](examples.md) - Real-world canvas examples

## External Resources

- [JSON Canvas Spec 1.0](https://jsoncanvas.org/spec/1.0/) - Official specification
- [JSON Canvas GitHub](https://github.com/obsidianmd/jsoncanvas) - Project repository
