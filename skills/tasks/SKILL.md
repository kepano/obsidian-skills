---
name: tasks
description: Create and query tasks using the Tasks plugin syntax including due dates, recurrence, priorities, and task queries. Use when the user mentions Tasks plugin, recurring tasks, task queries, or advanced task management in Obsidian.
---

# Tasks Plugin Skill

This skill enables Claude Code to create valid task syntax and queries for the Obsidian Tasks plugin.

## Overview

The Tasks plugin extends Obsidian's checkbox functionality with:
- Due dates, scheduled dates, start dates
- Recurrence rules
- Priorities
- Query blocks for dynamic task lists
- Custom statuses

## Task Syntax

### Basic Task Format

```markdown
- [ ] Task description
- [x] Completed task
```

### Task Components

A task can include multiple components in any order:

```markdown
- [ ] Task description 📅 2024-02-15 ⏫ 🔁 every week
```

| Emoji | Meaning | Format |
|-------|---------|--------|
| 📅 | Due date | `📅 YYYY-MM-DD` |
| ⏳ | Scheduled date | `⏳ YYYY-MM-DD` |
| 🛫 | Start date | `🛫 YYYY-MM-DD` |
| ➕ | Created date | `➕ YYYY-MM-DD` |
| ✅ | Done date | `✅ YYYY-MM-DD` |
| ❌ | Cancelled date | `❌ YYYY-MM-DD` |
| 🔁 | Recurrence | `🔁 every ...` |
| ⏫ | High priority | `⏫` |
| 🔼 | Medium priority | `🔼` |
| 🔽 | Low priority | `🔽` |
| ⏬ | Lowest priority | `⏬` |
| 🆔 | ID | `🆔 abc123` |
| ⛔ | Depends on | `⛔ abc123` |

### Alternative Text Formats

Instead of emojis, you can use text:

| Emoji | Text Alternative |
|-------|------------------|
| 📅 | `[due:: YYYY-MM-DD]` |
| ⏳ | `[scheduled:: YYYY-MM-DD]` |
| 🛫 | `[start:: YYYY-MM-DD]` |
| ➕ | `[created:: YYYY-MM-DD]` |
| ✅ | `[completion:: YYYY-MM-DD]` |
| ❌ | `[cancelled:: YYYY-MM-DD]` |
| ⏫ | `[priority:: high]` |
| 🔼 | `[priority:: medium]` |
| 🔽 | `[priority:: low]` |
| ⏬ | `[priority:: lowest]` |

## Dates

### Date Formats

```markdown
📅 2024-02-15
📅 2024-02-15
⏳ 2024-02-10
🛫 2024-02-01
```

Dates must be in `YYYY-MM-DD` format.

### Date Types

| Date | Purpose |
|------|---------|
| **Due** (📅) | When task must be completed |
| **Scheduled** (⏳) | When you plan to work on it |
| **Start** (🛫) | When task becomes available |
| **Created** (➕) | When task was created |
| **Done** (✅) | When task was completed |
| **Cancelled** (❌) | When task was cancelled |

### Examples

```markdown
- [ ] Submit report 📅 2024-02-15
- [ ] Start project 🛫 2024-02-01 📅 2024-02-28
- [ ] Review document ⏳ 2024-02-10 📅 2024-02-12
- [ ] Call client 📅 2024-02-15 ➕ 2024-02-01
```

## Priorities

### Priority Levels

| Priority | Emoji | Value |
|----------|-------|-------|
| Highest | ⏫ | 1 |
| High | 🔺 | 2 |
| Medium | 🔼 | 3 |
| None | (none) | 4 |
| Low | 🔽 | 5 |
| Lowest | ⏬ | 6 |

### Examples

```markdown
- [ ] Critical bug fix ⏫
- [ ] Important feature 🔼
- [ ] Nice to have 🔽
- [ ] Someday maybe ⏬
```

## Recurrence

### Recurrence Syntax

```markdown
🔁 every <interval>
🔁 every <n> <period>
🔁 every <period> when done
🔁 every <period> on <day>
```

### Recurrence Periods

| Period | Aliases |
|--------|---------|
| `day` | `daily` |
| `week` | `weekly` |
| `month` | `monthly` |
| `year` | `yearly`, `annually` |

### Recurrence Examples

```markdown
- [ ] Daily standup 🔁 every day 📅 2024-02-15
- [ ] Weekly review 🔁 every week 📅 2024-02-16
- [ ] Monthly report 🔁 every month 📅 2024-02-28
- [ ] Annual review 🔁 every year 📅 2024-12-31

- [ ] Every 3 days 🔁 every 3 days 📅 2024-02-15
- [ ] Biweekly 🔁 every 2 weeks 📅 2024-02-15
- [ ] Quarterly 🔁 every 3 months 📅 2024-03-31

- [ ] Every Monday 🔁 every week on Monday 📅 2024-02-19
- [ ] Every Mon/Wed/Fri 🔁 every week on Monday, Wednesday, Friday 📅 2024-02-16
- [ ] First of month 🔁 every month on the 1st 📅 2024-03-01
- [ ] Last Friday 🔁 every month on the last Friday 📅 2024-02-23
```

### When Done vs Fixed Schedule

```markdown
- [ ] Water plants 🔁 every week 📅 2024-02-15
```
When completed, next due = previous due + 1 week

```markdown
- [ ] Water plants 🔁 every week when done 📅 2024-02-15
```
When completed, next due = completion date + 1 week

### Ordinal Days

```markdown
🔁 every month on the 1st
🔁 every month on the 15th
🔁 every month on the last
🔁 every month on the last day
🔁 every month on the first Monday
🔁 every month on the second Tuesday
🔁 every month on the third Wednesday
🔁 every month on the fourth Thursday
🔁 every month on the last Friday
```

## Task Dependencies

### ID and Dependencies

```markdown
- [ ] First task 🆔 task1
- [ ] Second task ⛔ task1
- [ ] Third task ⛔ task1,task2
```

Tasks with dependencies are blocked until dependencies are completed.

## Custom Statuses

### Default Statuses

| Status | Character | Type |
|--------|-----------|------|
| Todo | `[ ]` | `TODO` |
| Done | `[x]` | `DONE` |

### Common Custom Statuses

| Status | Character | Type | Meaning |
|--------|-----------|------|---------|
| In Progress | `[/]` | `IN_PROGRESS` | Working on it |
| Cancelled | `[-]` | `CANCELLED` | Won't do |
| Forwarded | `[>]` | `TODO` | Moved to later |
| Scheduled | `[<]` | `TODO` | Scheduled |
| Question | `[?]` | `TODO` | Need info |
| Important | `[!]` | `TODO` | High priority |
| Star | `[*]` | `TODO` | Favorite |
| Quote | `["]` | `TODO` | Quote |
| Info | `[i]` | `TODO` | Information |
| Idea | `[I]` | `TODO` | Idea/lightbulb |
| Pro | `[p]` | `TODO` | Pro argument |
| Con | `[c]` | `TODO` | Con argument |

### Examples

```markdown
- [ ] Not started
- [/] In progress
- [x] Completed
- [-] Cancelled
- [>] Deferred
- [?] Waiting for info
```

## Task Queries

### Query Block Structure

````markdown
```tasks
<filters>
<sort>
<group>
<display options>
```
````

### Filter Types

#### Boolean Filters

```
done
not done
has due date
no due date
has start date
no start date
has scheduled date
no scheduled date
has created date
no created date
has done date
no done date
has cancelled date
no cancelled date
is recurring
is not recurring
has id
no id
has depends on
no depends on
is blocked
is not blocked
```

#### Date Filters

```
due today
due before today
due after today
due on 2024-02-15
due before 2024-02-15
due after 2024-02-15
due in 2024-02
due in 2024

scheduled today
scheduled before today
scheduled after today
scheduled on 2024-02-15

starts today
starts before today
starts after today
starts on 2024-02-15

created today
created before today
created after today
created on 2024-02-15

done today
done before today
done after today
done on 2024-02-15
```

#### Relative Date Filters

```
due this week
due next week
due last week

due this month
due next month
due last month

due this year

# Relative with numbers
due in 7 days
due in 2 weeks
due in 3 months
```

#### Text Filters

```
description includes meeting
description does not include optional
description regex matches /^Call/

path includes Projects
path does not include Archive

heading includes Tasks
heading does not include Done

tags include #work
tags do not include #personal
tag includes #work
tag does not include #personal

folder includes Projects
folder does not include Archive

filename includes daily
filename does not include template
```

#### Priority Filters

```
priority is highest
priority is high
priority is medium
priority is none
priority is low
priority is lowest

priority above none
priority below medium
priority is not none
```

#### Recurrence Filters

```
is recurring
is not recurring
recurrence includes week
recurrence does not include month
```

#### Status Filters

```
status.name includes in progress
status.type is TODO
status.type is DONE
status.type is IN_PROGRESS
status.type is CANCELLED
status.type is NON_TASK
```

### Combining Filters

```
# AND (implicit)
due today
path includes Projects

# OR
(due today) OR (scheduled today)
(path includes Work) OR (path includes Personal)

# NOT
NOT done
NOT (path includes Archive)

# Complex
(due today) OR (scheduled today)
NOT done
path includes Projects
```

### Sort Options

```
sort by due
sort by due reverse
sort by scheduled
sort by start
sort by created
sort by done
sort by priority
sort by priority reverse
sort by path
sort by description
sort by status
sort by status.name
sort by urgency
sort by urgency reverse
sort by tag
sort by filename
sort by heading
sort by recurring
```

Multiple sorts:
```
sort by priority
sort by due
sort by description
```

### Group Options

```
group by due
group by scheduled
group by start
group by created
group by done
group by priority
group by path
group by folder
group by filename
group by heading
group by status
group by status.name
group by status.type
group by recurrence
group by recurring
group by tags
group by root
```

### Display Options

```
hide task count
hide backlink
hide priority
hide created date
hide start date
hide scheduled date
hide due date
hide done date
hide cancelled date
hide recurrence rule
hide edit button
hide postpone button
hide urgency

show task count
show backlink
show priority
show created date
show start date
show scheduled date
show due date
show done date
show cancelled date
show recurrence rule
show edit button
show postpone button
show urgency
show id
show depends on

short mode
full mode

explain
```

### Limit Results

```
limit 10
limit to 5 tasks
limit groups to 3
limit groups 5
```

## Complete Query Examples

### Due Today or Overdue

````markdown
```tasks
(due before tomorrow) OR (due today)
not done
sort by priority
sort by due
```
````

### This Week's Tasks

````markdown
```tasks
due after last Sunday
due before next Sunday
not done
group by due
sort by priority
```
````

### Project Tasks

````markdown
```tasks
path includes Projects/Website
not done
sort by priority reverse
sort by due
hide backlink
```
````

### Waiting/Blocked Tasks

````markdown
```tasks
status.name includes waiting
not done
group by path
```
````

### Recently Completed

````markdown
```tasks
done after 7 days ago
sort by done reverse
limit 20
```
````

### High Priority Without Dates

````markdown
```tasks
priority above none
no due date
not done
sort by priority reverse
```
````

### Recurring Tasks Overview

````markdown
```tasks
is recurring
not done
group by recurrence
sort by due
```
````

### Tasks by Tag

````markdown
```tasks
tags include #work
not done
group by tags
sort by due
```
````

### Unscheduled Tasks

````markdown
```tasks
no scheduled date
no start date
not done
has due date
sort by due
limit 10
```
````

### Tasks Created This Week

````markdown
```tasks
created after last Monday
not done
group by created
sort by priority reverse
```
````

### Multi-file Dashboard

````markdown
## 🔴 Overdue
```tasks
due before today
not done
sort by due
limit 10
```

## 📅 Today
```tasks
due today
not done
sort by priority reverse
```

## 📆 This Week
```tasks
due after today
due before in 7 days
not done
group by due
sort by priority
```

## ⏳ Scheduled
```tasks
scheduled before tomorrow
no due date
not done
sort by scheduled
```
````

### Exclude Certain Paths

````markdown
```tasks
not done
path does not include Templates
path does not include Archive
sort by due
```
````

### Specific Heading

````markdown
```tasks
heading includes Action Items
not done
sort by priority reverse
```
````

## Task Formats Reference

### Complete Task Example

```markdown
- [ ] Complete project report 📅 2024-02-28 ⏳ 2024-02-20 🛫 2024-02-15 ⏫ 🔁 every month ➕ 2024-02-01 🆔 report1
```

### Minimal Task

```markdown
- [ ] Simple task
```

### Task with All Date Types

```markdown
- [ ] Full lifecycle task 🛫 2024-02-01 ⏳ 2024-02-10 📅 2024-02-15 ➕ 2024-01-15
```

### Completed Recurring Task

```markdown
- [x] Weekly review 📅 2024-02-09 ✅ 2024-02-09 🔁 every week
```

### Cancelled Task

```markdown
- [-] Cancelled meeting 📅 2024-02-15 ❌ 2024-02-10
```

## Common Patterns

### GTD Weekly Review

````markdown
## Weekly Review

### Inbox Processing
```tasks
path includes Inbox
not done
```

### Waiting For
```tasks
status.name includes waiting
not done
group by path
```

### Next Actions
```tasks
tags include #next
not done
sort by due
```

### Someday/Maybe
```tasks
path includes Someday
not done
limit 10
```
````

### Daily Note Task Section

```markdown
## Today's Tasks

### Scheduled for Today
```tasks
scheduled on {{date:YYYY-MM-DD}}
not done
sort by priority reverse
```

### Due Today
```tasks
due on {{date:YYYY-MM-DD}}
not done
sort by priority reverse
```

### Completed Today
```tasks
done on {{date:YYYY-MM-DD}}
short mode
```
```

### Project Task List

````markdown
## Project: Website Redesign

### Active
```tasks
path includes Projects/Website
not done
is not blocked
sort by priority reverse
sort by due
```

### Blocked
```tasks
path includes Projects/Website
is blocked
not done
```

### Completed
```tasks
path includes Projects/Website
done
sort by done reverse
limit 10
```
````

## Urgency

Tasks are automatically scored for urgency based on:
- Priority
- Due date proximity
- Overdue status
- Scheduled date
- Start date

View with: `show urgency`

Sort with: `sort by urgency reverse`

## References

- [Tasks Documentation](https://publish.obsidian.md/tasks/)
- [Tasks GitHub](https://github.com/obsidian-tasks-group/obsidian-tasks)
- [Query Examples](https://publish.obsidian.md/tasks/Queries/About+Queries)
