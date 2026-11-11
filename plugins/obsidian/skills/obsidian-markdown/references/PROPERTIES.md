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
| Tags | Only for the `tags` property |

Links go in Text or List properties: `related: "[[Other Note]]"`. Always quote wikilinks in YAML, because an unquoted `[[Other Note]]` is read as a nested list, not a link.

## Default Properties

- `tags` - Note tags (searchable, shown in graph view)
- `aliases` - Alternative names for the note, offered in link suggestions. A bare `[[Alias]]` doesn't resolve; write `[[Note|Alias]]`
- `cssclasses` - CSS classes applied to the note in reading/editing view

## Tags

```markdown
#tag
#nested/tag
#tag-with-dashes
#tag_with_underscores
```

Tags can contain: letters (any language), numbers, underscores `_`, hyphens `-`, forward slashes `/` (for nesting). A tag needs at least one non-numerical character (`#1984book`, not `#1984`), and a space ends it.

In frontmatter:

```yaml
---
tags:
  - tag1
  - nested/tag2
---
```
