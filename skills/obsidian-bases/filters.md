# Obsidian Bases: Filters

Filters narrow down results to show only matching items. They can be applied globally (to all views) or per-view.

## Filter Structure

### Single Filter String

```yaml
filters: 'status == "done"'
```

### AND - All Conditions Must Be True

```yaml
filters:
  and:
    - 'status == "done"'
    - "priority > 3"
```

### OR - Any Condition Can Be True

```yaml
filters:
  or:
    - 'file.hasTag("book")'
    - 'file.hasTag("article")'
```

### NOT - Exclude Matching Items

```yaml
filters:
  not:
    - 'file.hasTag("archived")'
```

### Nested Filters

Combine conditions with nested logic:

```yaml
filters:
  or:
    - file.hasTag("tag")
    - and:
        - file.hasTag("book")
        - file.hasLink("Textbook")
    - not:
        - file.hasTag("book")
        - file.inFolder("Required Reading")
```

## Filter Operators

| Operator       | Description           |
| -------------- | --------------------- |
| `==`           | equals                |
| `!=`           | not equal             |
| `>`            | greater than          |
| `<`            | less than             |
| `>=`           | greater than or equal |
| `<=`           | less than or equal    |
| `&&`           | logical and           |
| `\|\|`         | logical or            |
| <code>!</code> | logical not           |

## Common Filter Patterns

### Filter by Tag

```yaml
filters:
  and:
    - file.hasTag("project")
```

### Filter by Folder

```yaml
filters:
  and:
    - file.inFolder("Notes")
```

### Filter by Date Range

```yaml
filters:
  and:
    - 'file.mtime > now() - "7d"'
```

### Filter by Property Value

```yaml
filters:
  and:
    - 'status == "active"'
    - "priority >= 3"
```

### Combine Multiple Conditions

```yaml
filters:
  or:
    - and:
        - file.hasTag("important")
        - 'status != "done"'
    - and:
        - "priority == 1"
        - 'due != ""'
```
