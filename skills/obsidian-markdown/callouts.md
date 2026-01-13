# Callouts in Obsidian Markdown

Callouts are styled blocks that highlight important information.

## Basic Callout

```markdown
> [!note]
> This is a note callout.

> [!info] Custom Title
> This callout has a custom title.

> [!tip] Title Only
```

Callouts use blockquote syntax (`>`) with a type in square brackets.

## Foldable Callouts

Make callouts collapsible:

```markdown
> [!faq]- Collapsed by default
> This content is hidden until expanded.

> [!faq]+ Expanded by default
> This content is visible but can be collapsed.
```

- `-` = Collapsed by default
- `+` = Expanded by default
- No symbol = Always expanded

## Nested Callouts

Combine callouts for layered information:

```markdown
> [!question] Outer callout
>
> > [!note] Inner callout
> > Nested content
```

## Supported Callout Types

| Type       | Aliases                | Icon             | Color  |
| ---------- | ---------------------- | ---------------- | ------ |
| `note`     | -                      | Pencil           | Blue   |
| `abstract` | `summary`, `tldr`      | Clipboard        | Teal   |
| `info`     | -                      | Info             | Blue   |
| `todo`     | -                      | Checkbox         | Blue   |
| `tip`      | `hint`, `important`    | Flame            | Cyan   |
| `success`  | `check`, `done`        | Checkmark        | Green  |
| `question` | `help`, `faq`          | Question mark    | Yellow |
| `warning`  | `caution`, `attention` | Warning triangle | Orange |
| `failure`  | `fail`, `missing`      | X                | Red    |
| `danger`   | `error`                | Zap              | Red    |
| `bug`      | -                      | Bug              | Red    |
| `example`  | -                      | List             | Purple |
| `quote`    | `cite`                 | Quote            | Gray   |

## Custom Callouts (CSS)

Define custom callout types in vault CSS:

```css
.callout[data-callout="custom-type"] {
  --callout-color: 255, 0, 0;
  --callout-icon: lucide-alert-circle;
}
```

Then use like any built-in type:

```markdown
> [!custom-type]
> Custom callout content
```

## Styling and Formatting

Callouts support all Markdown formatting inside:

```markdown
> [!tip] **Bold** and _italic_
>
> - List items
> - Work too
>
> `code` and [links](https://example.com)
```

## Nested Structure

Each `>` starts a new line in the callout. Blank lines preserve the nesting:

```markdown
> [!note]
> First paragraph
>
> Second paragraph (same callout)
>
> > [!warning] Nested callout
> > Different type
```

## Common Patterns

**Code examples:**

````markdown
> [!example] Code Example
>
> ```python
> def hello():
>     return "world"
> ```
````

**Warnings:**

```markdown
> [!warning] Important
> This action cannot be undone.
```

**Tips and hints:**

```markdown
> [!tip] Pro tip
> You can use the `Ctrl+Shift+A` shortcut.
```
