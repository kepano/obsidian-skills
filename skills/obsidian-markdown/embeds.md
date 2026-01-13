# Embeds in Obsidian Markdown

Embeds include content from other files or external sources directly in your note.

## Embed Notes

Include the full content or a section from another note:

```markdown
![[Note Name]]
![[Note Name#Heading]]
![[Note Name#^block-id]]
```

The embedded content appears inline and updates automatically when the source changes.

## Embed Images

Display images from your vault:

```markdown
![[image.png]]
![[image.png|640x480]] Width x Height
![[image.png|300]] Width only (maintains aspect ratio)
```

Supported formats: PNG, JPEG, GIF, SVG, BMP, WebP

### Sizing

- `![[image.png|width]]` - Set width (height auto scales)
- `![[image.png|width x height]]` - Set both dimensions

## External Images

Embed images from URLs:

```markdown
![Alt text](https://example.com/image.png)
![Alt text|300](https://example.com/image.png)
```

The `![Alt text]()` syntax works the same way as regular Markdown.

## Embed Audio

Play audio files from your vault:

```markdown
![[audio.mp3]]
![[audio.ogg]]
![[podcast.wav]]
```

Supported formats: MP3, WAV, OGG, OPUS, 3GP, FLAC

## Embed PDF

Include PDF documents (with optional page selection):

```markdown
![[document.pdf]]
![[document.pdf#page=3]]
![[document.pdf#height=400]]
```

Supported properties:

- `#page=N` - Start on specific page (1-indexed)
- `#height=pixels` - Set height in pixels

## Embed Search Results

Display dynamic search results:

````markdown
```query
tag:#project status:done
```
````

This runs a search and displays matching results as a list.

## Embed Lists

Include a specific list from another note:

```markdown
![[Note#^list-id]]
```

Define a list with a block ID in the source:

```markdown
- Item 1
- Item 2
- Item 3

^list-id
```

## Embedded Files Display

When embedding, Obsidian shows:

- For notes: The full content (or section if heading/block specified)
- For images: The visual image
- For audio/video: A playback player
- For PDF: A document viewer
- For other files: A link to download

## Recursive Embedding Limits

Obsidian prevents infinite recursion when files embed each other. Deeply nested embeds are handled gracefully.
