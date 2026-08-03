# Properties (Frontmatter) Reference

Properties use YAML frontmatter at the start of a note:

```yaml
---
title: My Note Title
date: 2024-01-15
tags:
  - project
  - important
aliases:
  - My Note
  - Alternative Name
cssclasses:
  - custom-class
status: in-progress
rating: 4.5
completed: false
due: 2024-02-01T14:30:00
---
```

## Property Types

| Type | Example |
|------|---------|
| Text | `title: My Title` |
| Number | `rating: 4.5` |
| Checkbox | `completed: true` |
| Date | `date: 2024-01-15` |
| Date & Time | `due: 2024-01-15T14:30:00` |
| List | `tags: [one, two]` or YAML list |
| Links | `related: "[[Other Note]]"` |

Once Obsidian assigns a type to a property name, that type applies to the same property name throughout the vault. The `tags` type is reserved for the `tags` property.

## Links and Lists

Quote internal links in YAML properties. Lists may contain text, numbers, and quoted internal links.

```yaml
related: "[[Other Note]]"
sources:
  - "[[Source One]]"
  - "[[Source Two]]"
```

Markdown formatting is not rendered in properties. Number properties must contain literal numbers rather than expressions.

## Default Properties

- `tags` - Note tags (searchable, shown in graph view)
- `aliases` - Alternative names for the note (used in link suggestions)
- `cssclasses` - CSS classes applied to the note in reading/editing view

## Tags

```markdown
#tag
#nested/tag
#tag-with-dashes
#tag_with_underscores
```

Tags can contain: letters (any language), numbers (not first character), underscores `_`, hyphens `-`, forward slashes `/` (for nesting).

In frontmatter:

```yaml
---
tags:
  - tag1
  - nested/tag2
---
```

## Current Limitations

- Nested properties are not supported in the properties UI; use Source mode when they must be inspected.
- Bulk property editing is not supported beyond the Properties view; use a reviewed script or community plugin when needed.
- Markdown inside property values is intentionally not rendered.
- Property names must be unique within a note.

## JSON Frontmatter

Obsidian can read JSON between frontmatter delimiters, but saves it back as YAML:

```json
---
{
  "tags": ["journal"],
  "publish": false
}
---
```

## Deprecated Default Names

Use `tags`, `aliases`, and `cssclasses`. The singular forms `tag`, `alias`, and `cssclass` are deprecated and are no longer supported as default properties in current Obsidian versions.
