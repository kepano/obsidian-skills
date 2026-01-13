# Obsidian Bases: Formulas

Formulas compute dynamic values from properties and other data. Defined in the `formulas` section of a base file.

## Formula Basics

```yaml
formulas:
  # Simple arithmetic
  total: "price * quantity"

  # Conditional logic
  status_icon: 'if(done, "✅", "⏳")'

  # String formatting
  formatted_price: 'if(price, price.toFixed(2) + " dollars")'

  # Date formatting
  created: 'file.ctime.format("YYYY-MM-DD")'

  # Complex expressions
  days_old: "((now() - file.ctime) / 86400000).round(0)"
```

## YAML Quoting Rules

- Use **single quotes** for formulas containing double quotes: `'if(done, "Yes", "No")'`
- Use **double quotes** for simple strings: `"My View Name"`
- Escape nested quotes properly in complex expressions

## Formula Functions

For a complete reference of available functions, see [Functions Reference](functions-reference.md).

### Global Functions

| Function      | Description                                         |
| ------------- | --------------------------------------------------- |
| `date()`      | Parse string to date. Format: `YYYY-MM-DD HH:mm:ss` |
| `duration()`  | Parse duration string                               |
| `now()`       | Current date and time                               |
| `today()`     | Current date (time = 00:00:00)                      |
| `if()`        | Conditional                                         |
| `min()/max()` | Smallest/largest number                             |
| `number()`    | Convert to number                                   |
| `link()`      | Create a link                                       |

### Date Arithmetic

Duration units: `y/year/years`, `M/month/months`, `d/day/days`, `w/week/weeks`, `h/hour/hours`, `m/minute/minutes`, `s/second/seconds`

```yaml
# Add/subtract durations
"date + \"1M\""           # Add 1 month
"date - \"2h\""           # Subtract 2 hours
"now() + \"1 day\""       # Tomorrow
"today() + \"7d\""        # A week from today

# Subtract dates for millisecond difference
"now() - file.ctime"

# Complex duration arithmetic
"now() + (duration('1d') * 2)"
```

## Formula Examples

### Status Indicators

```yaml
priority_label: 'if(priority == 1, "🔴 High", if(priority == 2, "🟡 Medium", "🟢 Low"))'
is_overdue: 'if(due, date(due) < today() && status != "done", false)'
```

### Date Calculations

```yaml
days_until_due: 'if(due, ((date(due) - today()) / 86400000).round(0), "")'
days_old: "((now() - file.ctime) / 86400000).round(0)"
day_of_week: 'date(file.basename).format("dddd")'
```

### String Operations

```yaml
formatted_date: 'file.ctime.format("MMM DD, YYYY")'
reading_time: 'if(pages, (pages * 2).toString() + " min", "")'
word_estimate: "(file.size / 5).round(0)"
```

### Counting and Stats

```yaml
link_count: "file.links.length"
tag_count: "file.tags.length"
has_content: "file.size > 100"
```

## Using Formulas in Views

Reference formulas in view properties using the `formula.` prefix:

```yaml
views:
  - type: table
    name: "Active Tasks"
    order:
      - file.name
      - status
      - formula.priority_label # Reference defined formula
      - due
      - formula.days_until_due # Reference another formula
```

## Performance Tips

- Keep formulas simple for faster calculation
- Use conditional logic to avoid unnecessary computations
- Cache repeated calculations by defining them once as formulas
- Avoid deeply nested conditions (keep 2-3 levels max)

For complete function signatures and advanced usage, see [Functions Reference](functions-reference.md).
