---
name: dataview
description: Create Dataview queries using DQL (Dataview Query Language), inline queries, and DataviewJS. Use when the user mentions Dataview, DQL, querying notes, listing notes by metadata, or creating dynamic views of vault content.
---

# Dataview Skill

This skill enables Claude Code to create valid Dataview queries for dynamically listing and aggregating notes in Obsidian.

## Overview

Dataview is a community plugin that treats an Obsidian vault as a database. It provides three query methods:
- **DQL (Dataview Query Language)** - SQL-like queries in code blocks
- **Inline queries** - Single-value queries embedded in text
- **DataviewJS** - JavaScript API for complex logic

## Data Sources

Dataview indexes metadata from:
- **Frontmatter** (YAML properties)
- **Inline fields** in note body
- **Implicit fields** (file metadata)
- **Tags** and **links**

### Inline Field Syntax

```markdown
Key:: Value
[Key:: Value]          Inline, hidden in reading view
(Key:: Value)          Inline, visible in reading view

Rating:: 8
Author:: [[Jane Smith]]
Status:: #in-progress
Due:: 2024-02-15
```

### Implicit Fields (Always Available)

| Field | Type | Description |
|-------|------|-------------|
| `file.name` | String | File name without extension |
| `file.folder` | String | Folder path |
| `file.path` | String | Full file path |
| `file.ext` | String | File extension |
| `file.link` | Link | Link to the file |
| `file.size` | Number | Size in bytes |
| `file.ctime` | Date | Creation time |
| `file.mtime` | Date | Modification time |
| `file.day` | Date | Date from daily note filename |
| `file.tags` | Array | All tags including nested |
| `file.etags` | Array | Explicit tags only |
| `file.inlinks` | Array | Incoming links |
| `file.outlinks` | Array | Outgoing links |
| `file.aliases` | Array | Aliases from frontmatter |
| `file.tasks` | Array | All tasks in file |
| `file.lists` | Array | All list items in file |
| `file.frontmatter` | Object | Raw frontmatter object |
| `file.starred` | Boolean | Is bookmarked |

### Task-Specific Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | String | Task status character |
| `checked` | Boolean | Is task checked |
| `completed` | Date | Completion date |
| `fullyCompleted` | Boolean | Task and subtasks done |
| `text` | String | Task text |
| `visual` | String | Text for display |
| `line` | Number | Line number |
| `lineCount` | Number | Lines the task spans |
| `path` | String | File path |
| `section` | Link | Section containing task |
| `tags` | Array | Tags in task |
| `outlinks` | Array | Links in task |
| `link` | Link | Link to task |
| `children` | Array | Subtasks |
| `task` | Boolean | Is a task |
| `subtasks` | Array | All subtasks |
| `real` | Boolean | Is real task vs list item |
| `header` | Link | Header above task |

## DQL Query Structure

```
```dataview
<QUERY-TYPE> <fields>
FROM <source>
WHERE <condition>
SORT <field> ASC/DESC
GROUP BY <field>
FLATTEN <field>
LIMIT <number>
```
```

### Query Types

| Type | Purpose | Output |
|------|---------|--------|
| `LIST` | Bullet list of links | List |
| `LIST WITHOUT ID` | List without file links | List |
| `TABLE` | Table with columns | Table |
| `TABLE WITHOUT ID` | Table without file column | Table |
| `TASK` | Interactive task list | Tasks |
| `CALENDAR` | Calendar by date field | Calendar |

## FROM Clause (Data Sources)

```sql
FROM ""                           -- All files in vault
FROM "Folder"                     -- Specific folder
FROM "Folder/Subfolder"           -- Nested folder
FROM #tag                         -- Files with tag
FROM #tag/nested                  -- Nested tags
FROM [[Note]]                     -- Files linking TO this note
FROM outgoing([[Note]])           -- Files this note links TO
FROM "Folder" AND #tag            -- Combine with AND
FROM "Folder" OR "Other"          -- Combine with OR
FROM -"Folder"                    -- Exclude folder
FROM #tag AND -#archived          -- Include and exclude
```

### Source Operators

| Operator | Description |
|----------|-------------|
| `AND` | Both conditions must match |
| `OR` | Either condition matches |
| `-` | Negate/exclude source |
| `"path"` | Folder or file path |
| `#tag` | Tag |
| `[[link]]` | Incoming links |
| `outgoing([[link]])` | Outgoing links |

## WHERE Clause (Filtering)

### Comparison Operators

| Operator | Description |
|----------|-------------|
| `=` | Equals |
| `!=` | Not equals |
| `<` | Less than |
| `>` | Greater than |
| `<=` | Less or equal |
| `>=` | Greater or equal |

### Logical Operators

| Operator | Description |
|----------|-------------|
| `AND` | Both conditions |
| `OR` | Either condition |
| `!` | Negation |

### Common WHERE Patterns

```sql
WHERE status = "active"
WHERE rating >= 4
WHERE file.mtime >= date(today) - dur(7 days)
WHERE contains(tags, "#project")
WHERE !completed
WHERE author = [[Jane Smith]]
WHERE file.name != "Index"
WHERE date >= date(2024-01-01) AND date < date(2024-02-01)
WHERE contains(file.folder, "Projects")
WHERE length(file.tags) > 0
WHERE any(file.tags, (t) => startswith(t, "#book"))
WHERE all(tasks, (t) => t.completed)
```

### Null/Empty Checks

```sql
WHERE field                       -- Field exists and truthy
WHERE !field                      -- Field missing or falsy
WHERE field = null                -- Field is null
WHERE field != null               -- Field is not null
```

## SORT Clause

```sql
SORT file.name ASC
SORT rating DESC
SORT file.mtime DESC
SORT status ASC, priority DESC    -- Multiple sorts
SORT date(due) ASC                -- Sort by parsed date
```

## GROUP BY Clause

```sql
GROUP BY status
GROUP BY file.folder
GROUP BY dateformat(file.ctime, "yyyy-MM")
GROUP BY choice(rating >= 4, "Good", "Other")
```

When grouped, access items via `rows` field:

```
```dataview
TABLE length(rows) AS Count, rows.file.link AS Files
FROM "Projects"
GROUP BY status
```
```

## FLATTEN Clause

Expands arrays into separate rows:

```sql
FLATTEN file.tags AS tag
FLATTEN authors AS author
FLATTEN file.lists.text AS item
```

## LIMIT Clause

```sql
LIMIT 10
LIMIT 5
```

## Functions Reference

### String Functions

| Function | Description |
|----------|-------------|
| `contains(str, substr)` | Check substring |
| `startswith(str, prefix)` | Check prefix |
| `endswith(str, suffix)` | Check suffix |
| `length(str)` | String length |
| `lower(str)` | Lowercase |
| `upper(str)` | Uppercase |
| `replace(str, pat, rep)` | Replace pattern |
| `regexreplace(str, pat, rep)` | Regex replace |
| `regexmatch(str, pattern)` | Regex match |
| `split(str, delim)` | Split to array |
| `join(array, delim)` | Join array |
| `substring(str, start, end)` | Substring |
| `truncate(str, len, suffix)` | Truncate with suffix |
| `padleft(str, len, char)` | Pad left |
| `padright(str, len, char)` | Pad right |
| `trim(str)` | Trim whitespace |

### Numeric Functions

| Function | Description |
|----------|-------------|
| `round(num, digits)` | Round number |
| `floor(num)` | Round down |
| `ceil(num)` | Round up |
| `abs(num)` | Absolute value |
| `min(a, b, ...)` | Minimum value |
| `max(a, b, ...)` | Maximum value |
| `sum(array)` | Sum of array |
| `product(array)` | Product of array |
| `average(array)` | Average of array |
| `minby(array, func)` | Min by function |
| `maxby(array, func)` | Max by function |

### Date Functions

| Function | Description |
|----------|-------------|
| `date(value)` | Parse to date |
| `date(today)` | Today's date |
| `date(now)` | Current datetime |
| `date(tomorrow)` | Tomorrow |
| `date(yesterday)` | Yesterday |
| `date(sow)` | Start of week |
| `date(eow)` | End of week |
| `date(som)` | Start of month |
| `date(eom)` | End of month |
| `date(soy)` | Start of year |
| `date(eoy)` | End of year |
| `dur(duration)` | Parse duration |
| `dateformat(date, fmt)` | Format date |
| `durationformat(dur, fmt)` | Format duration |
| `localtime(date)` | To local time |
| `striptime(date)` | Remove time component |

### Duration Syntax

```sql
dur(1 day)
dur(2 weeks)
dur(3 months)
dur(1 year)
dur(2 hours)
dur(30 minutes)
dur(1 day, 2 hours)
```

### Date Format Tokens

| Token | Description | Example |
|-------|-------------|---------|
| `yyyy` | 4-digit year | 2024 |
| `yy` | 2-digit year | 24 |
| `MM` | 2-digit month | 01-12 |
| `M` | Month | 1-12 |
| `MMMM` | Full month | January |
| `MMM` | Short month | Jan |
| `dd` | 2-digit day | 01-31 |
| `d` | Day | 1-31 |
| `EEEE` | Full weekday | Monday |
| `EEE` | Short weekday | Mon |
| `HH` | 24-hour | 00-23 |
| `hh` | 12-hour | 01-12 |
| `mm` | Minutes | 00-59 |
| `ss` | Seconds | 00-59 |
| `a` | AM/PM | AM |

### Array Functions

| Function | Description |
|----------|-------------|
| `length(array)` | Array length |
| `contains(array, val)` | Check membership |
| `econtains(array, val)` | Exact contains |
| `containsword(str, word)` | Contains word |
| `reverse(array)` | Reverse array |
| `sort(array)` | Sort ascending |
| `flat(array)` | Flatten nested |
| `slice(array, start, end)` | Slice array |
| `filter(array, func)` | Filter by predicate |
| `map(array, func)` | Transform elements |
| `all(array, func)` | All match predicate |
| `any(array, func)` | Any match predicate |
| `none(array, func)` | None match predicate |
| `nonnull(array)` | Remove nulls |
| `unique(array)` | Unique values |

### Lambda Syntax

```sql
filter(rows, (r) => r.status = "done")
map(file.tags, (t) => upper(t))
any(tasks, (t) => !t.completed)
all(authors, (a) => contains(a, "Smith"))
```

### Object Functions

| Function | Description |
|----------|-------------|
| `object(key, val, ...)` | Create object |
| `list(v1, v2, ...)` | Create list |
| `default(val, fallback)` | Default if null |
| `choice(cond, t, f)` | Ternary |
| `typeof(val)` | Get type |
| `meta(link)` | Get link metadata |
| `embed(link, display)` | Embed link |
| `link(path, display)` | Create link |
| `elink(url, display)` | External link |

### Utility Functions

| Function | Description |
|----------|-------------|
| `hash(val)` | Hash value |
| `localtime(date)` | To local timezone |
| `striptime(date)` | Remove time |

## Inline Queries

Single-value queries embedded in text:

```markdown
Today is `= date(today)`
Files in vault: `= length(filter(this.file.folder, (x) => x))`
Last modified: `= dateformat(this.file.mtime, "yyyy-MM-dd")`
Total tasks: `= length(filter(this.file.tasks, (t) => !t.completed))`

Progress: `= round(length(filter(this.file.tasks, (t) => t.completed)) / length(this.file.tasks) * 100)` %
```

### Inline Query Syntax

| Syntax | Description |
|--------|-------------|
| `` `= expression` `` | Evaluate expression |
| `this` | Current file |
| `this.field` | Field from current file |

## DataviewJS

JavaScript queries for complex logic:

````markdown
```dataviewjs
// List files modified today
const today = dv.date("today");
const files = dv.pages()
  .where(p => p.file.mtime >= today)
  .sort(p => p.file.mtime, "desc");

dv.list(files.map(p => p.file.link));
```
````

### DataviewJS API

#### Page Queries

```javascript
dv.pages()                        // All pages
dv.pages('"Folder"')              // From folder
dv.pages("#tag")                  // With tag
dv.pages("[[Link]]")              // Linking to
dv.page("path/to/note")           // Single page
dv.current()                      // Current file
```

#### Output Methods

```javascript
dv.list(items)                    // Bullet list
dv.taskList(tasks, groupByFile)   // Task list
dv.table(headers, rows)           // Table
dv.paragraph(text)                // Paragraph
dv.header(level, text)            // Header
dv.span(text)                     // Inline span
dv.el(tag, text, attrs)           // HTML element
dv.execute(source)                // Run DQL string
dv.executeJs(source)              // Run JS string
```

#### Utility Methods

```javascript
dv.date(input)                    // Parse date
dv.duration(input)                // Parse duration
dv.compare(a, b)                  // Compare values
dv.equal(a, b)                    // Check equality
dv.clone(value)                   // Deep clone
dv.parse(text)                    // Parse inline fields
dv.io.load(path)                  // Load file content
dv.io.csv(path)                   // Load CSV
dv.io.normalize(path)             // Normalize path
dv.array(items)                   // Create data array
dv.fileLink(path, embed, display) // Create file link
dv.sectionLink(path, section, embed, display) // Section link
dv.blockLink(path, block, embed, display) // Block link
```

#### DataArray Methods

```javascript
.where(predicate)                 // Filter
.filter(predicate)                // Alias for where
.map(func)                        // Transform
.flatMap(func)                    // Map and flatten
.mutate(func)                     // Mutate in place
.limit(n)                         // Limit results
.slice(start, end)                // Slice
.concat(other)                    // Concatenate
.indexOf(value)                   // Find index
.find(predicate)                  // Find first
.findIndex(predicate)             // Find first index
.includes(value)                  // Check inclusion
.join(sep)                        // Join to string
.sort(key, direction, comparator) // Sort
.groupBy(key)                     // Group
.groupIn(key)                     // Nested group
.distinct(key)                    // Unique values
.every(predicate)                 // All match
.some(predicate)                  // Any match
.none(predicate)                  // None match
.first()                          // First element
.last()                           // Last element
.to(type)                         // Convert type
.into(func)                       // Transform whole array
.forEach(func)                    // Iterate
.array()                          // To plain array
.expand(func)                     // Expand with function
```

### DataviewJS Examples

#### Table with Computed Columns

````markdown
```dataviewjs
const pages = dv.pages("#project")
  .where(p => p.status != "archived")
  .sort(p => p.priority, "desc");

dv.table(
  ["Project", "Status", "Due", "Days Left"],
  pages.map(p => [
    p.file.link,
    p.status,
    p.due,
    p.due ? Math.floor((dv.date(p.due) - dv.date("today")) / (1000 * 60 * 60 * 24)) : "N/A"
  ])
);
```
````

#### Grouped Task List

````markdown
```dataviewjs
const tasks = dv.pages("#project")
  .file.tasks
  .where(t => !t.completed)
  .groupBy(t => t.section);

for (let group of tasks) {
  dv.header(4, group.key);
  dv.taskList(group.rows, false);
}
```
````

#### Progress Bars

````markdown
```dataviewjs
const projects = dv.pages("#project");

for (let p of projects) {
  const tasks = p.file.tasks;
  const done = tasks.where(t => t.completed).length;
  const total = tasks.length;
  const pct = total > 0 ? Math.round(done / total * 100) : 0;

  dv.paragraph(`**${p.file.link}**: ${done}/${total} (${pct}%)`);
  dv.span(`<progress value="${pct}" max="100"></progress>`);
}
```
````

## Complete Examples

### Project Dashboard

````markdown
```dataview
TABLE
  status AS "Status",
  priority AS "Priority",
  due AS "Due Date",
  dateformat(file.mtime, "yyyy-MM-dd") AS "Updated"
FROM #project
WHERE status != "archived"
SORT priority DESC, due ASC
```
````

### Reading List

````markdown
```dataview
TABLE WITHOUT ID
  file.link AS "Book",
  author AS "Author",
  rating AS "Rating",
  dateformat(finished, "MMM yyyy") AS "Finished"
FROM #book
WHERE finished
SORT finished DESC
LIMIT 10
```
````

### Tasks Due This Week

````markdown
```dataview
TASK
FROM "Projects"
WHERE !completed
  AND due >= date(today)
  AND due <= date(today) + dur(7 days)
SORT due ASC
GROUP BY file.link
```
````

### Daily Notes Index

````markdown
```dataview
LIST WITHOUT ID
  file.link + " - " + default(summary, "No summary")
FROM "Daily Notes"
WHERE file.day >= date(today) - dur(30 days)
SORT file.day DESC
```
````

### Tag Cloud

````markdown
```dataviewjs
const tags = dv.pages()
  .flatMap(p => p.file.tags)
  .groupBy(t => t)
  .map(g => ({ tag: g.key, count: g.rows.length }))
  .sort(t => t.count, "desc")
  .limit(20);

dv.paragraph(tags.map(t =>
  `${t.tag} (${t.count})`
).join(" | "));
```
````

### Calendar Heatmap Data

````markdown
```dataview
CALENDAR file.day
FROM "Daily Notes"
WHERE file.day
```
````

### Files Modified Recently

````markdown
```dataview
TABLE
  dateformat(file.mtime, "yyyy-MM-dd HH:mm") AS "Modified",
  file.size AS "Size"
FROM ""
WHERE file.mtime >= date(today) - dur(7 days)
SORT file.mtime DESC
LIMIT 20
```
````

### Orphan Notes (No Incoming Links)

````markdown
```dataview
LIST
FROM ""
WHERE length(file.inlinks) = 0
  AND file.name != "Index"
SORT file.name ASC
```
````

### Notes Linking Here

````markdown
```dataview
LIST
FROM [[]]
SORT file.name ASC
```
````

## Common Patterns

### Handling Missing Fields

```sql
WHERE default(status, "none") = "active"
WHERE rating != null
WHERE !completed OR completed = null
```

### Date Comparisons

```sql
WHERE due = date(today)
WHERE due < date(today)                    -- Overdue
WHERE due >= date(today) AND due <= date(today) + dur(7 days)  -- This week
WHERE file.mtime >= date(today) - dur(30 days)  -- Last 30 days
WHERE dateformat(date, "yyyy-MM") = "2024-01"   -- Specific month
```

### Working with Arrays

```sql
WHERE contains(tags, "#important")
WHERE any(file.tags, (t) => startswith(t, "#project"))
WHERE length(file.outlinks) > 5
WHERE econtains(authors, "Smith")
```

### Aggregations in Groups

```sql
GROUP BY status
-- Then use: length(rows), sum(rows.field), etc.
```

## References

- [Dataview Documentation](https://blacksmithgu.github.io/obsidian-dataview/)
- [DQL Reference](https://blacksmithgu.github.io/obsidian-dataview/queries/dql-js-inline/)
- [Function Reference](https://blacksmithgu.github.io/obsidian-dataview/reference/functions/)
- [DataviewJS Reference](https://blacksmithgu.github.io/obsidian-dataview/api/intro/)
