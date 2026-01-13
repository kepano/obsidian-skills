# Properties and Tags in Obsidian Markdown

Properties (frontmatter) and tags add metadata to your notes for organization and querying.

## Properties (Frontmatter)

Properties use YAML at the start of a note before any content:

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

Properties are key-value pairs that can be queried and displayed in Bases views.

## Property Types

| Type        | Example                     | Notes                     |
| ----------- | --------------------------- | ------------------------- |
| Text        | `title: My Title`           | Single line text          |
| Number      | `rating: 4.5`               | Integer or decimal        |
| Checkbox    | `completed: true`           | Boolean: true or false    |
| Date        | `date: 2024-01-15`          | YYYY-MM-DD format         |
| Date & Time | `due: 2024-01-15T14:30:00`  | ISO 8601 format with time |
| List        | `tags: [one, two]`          | Array of values           |
| Links       | `related: "[[Other Note]]"` | Wikilinks to other notes  |

## Default Properties

These properties have special meaning in Obsidian:

| Property     | Purpose                                 |
| ------------ | --------------------------------------- |
| `tags`       | Categorize note with tags               |
| `aliases`    | Alternative names for wikilink matching |
| `cssclasses` | CSS classes for styling                 |

## Custom Properties

Define any property you need:

```yaml
---
author: John Doe
project: Website Redesign
status: in-progress
priority: high
reviewed: false
---
```

## Property Display in Obsidian

Properties appear in the Properties panel:

- Click properties panel icon to view/edit
- Inline editing for quick changes
- Type-aware form inputs (dates show calendar, etc.)

## Tags

Inline tags organize notes and create hierarchies.

### Tag Syntax

```markdown
#tag
#nested/tag
#tag-with-dashes
#tag_with_underscores
```

### Valid Tag Characters

- Letters (any language)
- Numbers (not as first character)
- Underscores `_`
- Hyphens `-`
- Forward slashes `/` (for nesting)

### Nested Tags

Create hierarchical tag structures:

```markdown
#projects/website/design
#projects/website/development
#reading/books/fiction
#reading/books/non-fiction
```

In the tag view, these display as a tree structure.

### Tags in Properties

Define tags in frontmatter for easier management:

```yaml
---
tags:
  - project
  - important
  - 2024
---
```

## Tag Usage

### Queries and Bases

Use tags to filter content:

```yaml
filters:
  and:
    - file.hasTag("project")
```

### Tag Pane

Browse and navigate:

- View all tags in vault
- See which notes have each tag
- Click to create new notes with that tag

### Graph View

Tags appear as connections between notes in the Graph view.

## Properties vs Tags

- **Properties**: Structured metadata (author, date, rating)
- **Tags**: Categorical labels (project, review, important)

Use both together for complete organization:

```yaml
---
title: Project Alpha
date: 2024-01-15
author: Alice
status: active
tags:
  - project
  - active
  - high-priority
---
```
