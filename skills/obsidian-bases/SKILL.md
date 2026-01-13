---
name: obsidian-bases
description: Create and edit Obsidian Bases (.base files) with views, filters, formulas, and summaries. Use when working with .base files, creating database or query views of notes, or when the user mentions Bases, table views, card views, list views, filters, formulas, or summaries in Obsidian.
allowed-tools: [Read, Write, Edit, Glob]
---

# Obsidian Bases Skill

This skill enables agents to create and edit valid Obsidian Bases (`.base` files) including views, filters, formulas, and all related configurations.

## Overview

Obsidian Bases are YAML-based files that define dynamic views of notes in an Obsidian vault. A Base file can contain multiple views, global filters, formulas, property configurations, and custom summaries.

## File Format

Base files use the `.base` extension and contain valid YAML. They can also be embedded in Markdown code blocks.

## Base Schema

Complete structure of a base file:

```yaml
# Global filters apply to ALL views
filters:
  and: []
  or: []
  not: []

# Define formula properties for all views
formulas:
  formula_name: "expression"

# Configure display names and settings
properties:
  property_name:
    displayName: "Display Name"

# Define custom summary formulas
summaries:
  custom_summary_name: "values.mean().round(3)"

# Define one or more views
views:
  - type: table | cards | list | map
    name: "View Name"
    limit: 10 # Optional
    order:
      - file.name
    filters: {}
    summaries: {}
```

## Filters

Filters narrow down which items appear in views. They can be global (all views) or per-view.

**Basic syntax:**

```yaml
filters: 'status == "done"'  # Single filter
filters:
  and:                       # AND logic
    - 'status == "done"'
    - 'priority > 3'
```

Supported operators: `==`, `!=`, `>`, `<`, `>=`, `<=`, `&&`, `||`, `!`

For complete filter syntax and patterns, see [Filters](filters.md).

## Formulas

Formulas compute dynamic values from properties. Define them once and use across all views.

**Example:**

```yaml
formulas:
  priority_label: 'if(priority == 1, "🔴 High", "🟢 Low")'
  days_due: 'if(due, ((date(due) - today()) / 86400000).round(0), "")'
```

Reference formulas in views using `formula.formula_name`.

For formula syntax and function reference, see [Formulas](formulas.md) and [Functions Reference](functions-reference.md).

## Properties

Configure display names and settings for properties in views:

```yaml
properties:
  author:
    displayName: "Book Author"
  formula.priority_label:
    displayName: "Priority"
```

Three types of properties:

- **Note properties** - From frontmatter: `author`, `status`, etc.
- **File properties** - Built-in: `file.name`, `file.mtime`, `file.tags`, etc.
- **Formula properties** - Computed: `formula.my_formula`

## Views

Display your data in multiple formats. Each view can have its own filters, ordering, and grouping.

**View types:**

- `table` - Column-based display with sorting, grouping, summaries
- `cards` - Visual card layout ideal for image-heavy content
- `list` - Simple list view for quick scanning
- `map` - Geographic visualization (requires location data)

For complete view documentation and options, see [Views](views.md).

## Summaries

Add aggregation rows to table views:

```yaml
summaries:
  priority: Average
  completed_date: Latest
  tasks_count: Sum
```

Available aggregation functions: `Sum`, `Count`, `Average`, `Min`, `Max`, `Median`, `Stddev`, `Earliest`, `Latest`, `Range`, `Checked`, `Unchecked`, `Empty`, `Filled`, `Unique`

## Embedding Bases

Embed a base file in Markdown notes:

```markdown
![[MyBase.base]]

![[MyBase.base#View Name]] # Specific view
```

## YAML Quoting Rules

- Use **single quotes** for formulas containing double quotes: `'if(done, "Yes", "No")'`
- Use **double quotes** for simple strings: `"My View Name"`
- Escape nested quotes properly in complex expressions

## Properties Reference

### File Properties

| Property      | Type   | Description        |
| ------------- | ------ | ------------------ |
| `file.name`   | String | File name          |
| `file.path`   | String | Full path to file  |
| `file.folder` | String | Parent folder path |
| `file.mtime`  | Date   | Modified time      |
| `file.ctime`  | Date   | Created time       |
| `file.tags`   | List   | All tags in file   |
| `file.links`  | List   | Internal links     |
| `file.size`   | Number | File size in bytes |

### Common Properties

The `this` keyword refers to:

- In main content area: the base file itself
- When embedded: the embedding file
- In sidebar: the active file in main content

## Reference Guides

- [Filters](filters.md) - Complete filter syntax and patterns
- [Formulas](formulas.md) - Formula syntax and common examples
- [Functions Reference](functions-reference.md) - All available functions and signatures
- [Views](views.md) - View types and configuration options
- [Examples](examples.md) - Real-world base file examples

## External Resources

- [Bases Syntax](https://help.obsidian.md/bases/syntax)
- [Functions](https://help.obsidian.md/bases/functions)
- [Views](https://help.obsidian.md/bases/views)
- [Formulas](https://help.obsidian.md/formulas)
