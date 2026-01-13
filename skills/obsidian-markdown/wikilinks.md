# Wikilinks in Obsidian Markdown

Wikilinks are Obsidian-specific links to other notes using double bracket syntax. They create bidirectional relationships between notes.

## Basic Links

Link to another note by name:

```markdown
[[Note Name]]
[[Note Name.md]]
[[Note Name|Display Text]]
```

The note will be linked even if the exact case doesn't match.

## Links to Headings

Link to a specific heading in a note:

```markdown
[[Note Name#Heading]]
[[Note Name#Heading|Custom Text]]
[[#Heading in same note]]
[[##Search all headings in vault]]
```

Use `#` to reference heading anchors. Multiple `#` signs search for matching headings across the vault.

## Links to Blocks

Link to a specific paragraph or block by its block ID:

```markdown
[[Note Name#^block-id]]
[[Note Name#^block-id|Custom Text]]
```

Define a block ID by adding `^block-id` at the end of a paragraph:

```markdown
This is a paragraph that can be linked to. ^my-block-id
```

For lists and quotes, add the block ID on a separate line:

```markdown
> This is a quote
> With multiple lines

^quote-id
```

## Search Links

Search for headings or blocks across the entire vault:

```markdown
[[##heading]] Search for headings containing "heading"
[[^^block]] Search for blocks containing "block"
```

## Display Text vs Link Text

Use pipe `|` to separate the link target from display text:

```markdown
[[Note Name|Show this text]] # Links to "Note Name" but displays "Show this text"
```

Without the pipe, the note name is displayed as-is.

## Unresolved Links

When you create a wikilink to a non-existent note, it appears with a question mark. You can click to create the note.

## Link Suggestions

When typing `[[`, Obsidian provides autocomplete suggestions based on:

- Existing notes
- Block IDs
- Headings
- Aliases (from note properties)

## Bidirectional Links

Wikilinks are bidirectional:

- Creating `[[Note A]]` in Note B automatically shows the backlink in Note A
- The Graph view displays these relationships visually
- Backlinks pane shows all notes linking to the current note
