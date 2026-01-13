# JSON Canvas Node Types

Nodes are objects placed on the canvas. There are four node types: `text`, `file`, `link`, and `group`.

## Z-Index Ordering

Nodes are ordered by z-index in the array:

- First node = bottom layer (displayed below others)
- Last node = top layer (displayed above others)

## Generic Node Attributes

All nodes share these attributes:

| Attribute | Required | Type        | Description                                   |
| --------- | -------- | ----------- | --------------------------------------------- |
| `id`      | Yes      | string      | Unique identifier for the node                |
| `type`    | Yes      | string      | Node type: `text`, `file`, `link`, or `group` |
| `x`       | Yes      | integer     | X position in pixels                          |
| `y`       | Yes      | integer     | Y position in pixels                          |
| `width`   | Yes      | integer     | Width in pixels                               |
| `height`  | Yes      | integer     | Height in pixels                              |
| `color`   | No       | canvasColor | Node color (see [Colors](colors.md))          |

## Text Nodes

Text nodes contain Markdown content.

```json
{
  "id": "6f0ad84f44ce9c17",
  "type": "text",
  "x": 0,
  "y": 0,
  "width": 400,
  "height": 200,
  "text": "# Hello World\n\nThis is **Markdown** content."
}
```

| Attribute | Required | Type   | Description                     |
| --------- | -------- | ------ | ------------------------------- |
| `text`    | Yes      | string | Plain text with Markdown syntax |

## File Nodes

File nodes reference files or attachments (images, videos, PDFs, notes, etc.).

```json
{
  "id": "a1b2c3d4e5f67890",
  "type": "file",
  "x": 500,
  "y": 0,
  "width": 400,
  "height": 300,
  "file": "Attachments/diagram.png"
}
```

```json
{
  "id": "b2c3d4e5f6789012",
  "type": "file",
  "x": 500,
  "y": 400,
  "width": 400,
  "height": 300,
  "file": "Notes/Project Overview.md",
  "subpath": "#Implementation"
}
```

| Attribute | Required | Type   | Description                                |
| --------- | -------- | ------ | ------------------------------------------ |
| `file`    | Yes      | string | Path to file within the system             |
| `subpath` | No       | string | Link to heading or block (starts with `#`) |

## Link Nodes

Link nodes display external URLs.

```json
{
  "id": "c3d4e5f678901234",
  "type": "link",
  "x": 1000,
  "y": 0,
  "width": 400,
  "height": 200,
  "url": "https://obsidian.md"
}
```

| Attribute | Required | Type   | Description  |
| --------- | -------- | ------ | ------------ |
| `url`     | Yes      | string | External URL |

## Group Nodes

Group nodes are visual containers for organizing other nodes.

```json
{
  "id": "d4e5f6789012345a",
  "type": "group",
  "x": -50,
  "y": -50,
  "width": 1000,
  "height": 600,
  "label": "Project Overview",
  "color": "4"
}
```

```json
{
  "id": "e5f67890123456ab",
  "type": "group",
  "x": 0,
  "y": 700,
  "width": 800,
  "height": 500,
  "label": "Resources",
  "background": "Attachments/background.png",
  "backgroundStyle": "cover"
}
```

| Attribute         | Required | Type   | Description                |
| ----------------- | -------- | ------ | -------------------------- |
| `label`           | No       | string | Text label for the group   |
| `background`      | No       | string | Path to background image   |
| `backgroundStyle` | No       | string | Background rendering style |

### Background Styles

| Value    | Description                                 |
| -------- | ------------------------------------------- |
| `cover`  | Fills entire width and height of node       |
| `ratio`  | Maintains aspect ratio of background image  |
| `repeat` | Repeats image as pattern in both directions |
