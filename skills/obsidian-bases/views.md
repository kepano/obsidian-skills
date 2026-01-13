# Obsidian Bases: Views

Views are different presentations of your data. Each base can contain multiple views of the same data with different filters, grouping, and display options.

## View Types

### Table View

Displays data in a table format with columns and rows.

```yaml
views:
  - type: table
    name: "Active Tasks"
    limit: 10 # Optional: limit results
    order:
      - file.name
      - status
      - priority
    groupBy:
      property: status
      direction: ASC
    filters:
      and:
        - 'status != "done"'
    summaries:
      priority: Average
```

**Table Features:**

- Column ordering with `order`
- Row grouping with `groupBy`
- Row limits with `limit`
- Summary rows with `summaries`
- Sortable columns
- Filterable by column values

### Card View

Displays each item as a visual card.

```yaml
views:
  - type: cards
    name: "Library"
    order:
      - cover
      - file.name
      - author
      - status
    filters:
      not:
        - 'status == "dropped"'
```

**Card Features:**

- Visual preview of properties
- Customizable field display order
- Grouped layout
- Good for image-heavy content

### List View

Simple list of matching items with key properties.

```yaml
views:
  - type: list
    name: "Quick List"
    order:
      - file.name
      - status
```

**List Features:**

- Compact display
- Quick scanning
- Title-focused
- Ideal for large datasets

### Map View

Displays items with geographic coordinates (requires location properties).

```yaml
views:
  - type: map
    name: "Locations"
    latitude: latitude_property
    longitude: longitude_property
```

**Map Features:**

- Geographic visualization
- Clustering
- Interactive pan/zoom
- Requires location data in frontmatter

## View Properties

All views support these common properties:

| Property    | Required | Description                                     |
| ----------- | -------- | ----------------------------------------------- |
| `type`      | Yes      | View type: `table`, `cards`, `list`, or `map`   |
| `name`      | Yes      | Display name for the view                       |
| `order`     | No       | Array of properties to display in order         |
| `filters`   | No       | View-specific filters (in addition to global)   |
| `groupBy`   | No       | Group results by property (table views)         |
| `limit`     | No       | Maximum number of items to display              |
| `summaries` | No       | Aggregation functions for columns (table views) |

## View Ordering

The `order` property controls which columns/fields display and in what sequence:

```yaml
order:
  - file.name
  - status
  - formula.priority_label
  - due
  - formula.days_until_due
```

Use property names (from frontmatter), file properties (`file.name`, `file.mtime`), or formulas (`formula.formula_name`).

## View Grouping

Group results by a property using `groupBy`:

```yaml
groupBy:
  property: status
  direction: ASC
```

- `property`: Which property to group by
- `direction`: `ASC` (ascending) or `DESC` (descending)

## View Limits

Limit the number of items displayed:

```yaml
limit: 50 # Show only first 50 items
```

Useful for views of large datasets or "recent items" views.

## View Summaries

Add aggregation rows to table views:

```yaml
summaries:
  priority: Average
  completed_date: Latest
  tasks_count: Sum
```

Available aggregation functions: `Sum`, `Count`, `Average`, `Min`, `Max`, `Median`, `Stddev`, `Earliest`, `Latest`, `Range`, `Checked`, `Unchecked`, `Empty`, `Filled`, `Unique`

See [Functions Reference](functions-reference.md) for details.
