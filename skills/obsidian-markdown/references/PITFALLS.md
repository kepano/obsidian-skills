# Silent failures when writing notes

These produce notes that open without error but render differently than written. Nothing in the file looks wrong, so they are easy to write by accident.

## A line starting with `=` becomes a Dataview query

With the Dataview plugin enabled, inline code whose contents begin with `=` is evaluated as an inline Dataview query instead of being displayed.

````markdown
Compare with `==` when checking equality.
````

The `==` above is read as an empty query, and the note shows `PARSING FAILED` in place of the code. Avoid starting inline code with `=`, or use a different delimiter when the literal text is required.

## Templater and the core Templates plugin use different syntax

The two templating engines are not interchangeable. A template written for one inserts as literal text under the other:

- Core Templates plugin: `{{title}}`, `{{date}}`, `{{time}}`.
- Templater: `<% tp.file.title %>`, `<% tp.date.now("YYYY-MM-DD") %>`.

Templater syntax pasted into a note is never evaluated -- it stays visible as literal `<% tp.file.title %>` text. Check which engine the vault uses before writing a template: `.obsidian/plugins/templater-obsidian/` means Templater is installed, and the core Templates plugin is toggled in `.obsidian/core-plugins.json`. If the vault's existing templates use `<% %>`, match that syntax.
