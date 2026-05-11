---
name: defuddle
description: Extract clean markdown content from web pages using Defuddle CLI, removing clutter and navigation to save tokens. Use instead of WebFetch when the user provides a URL to read or analyze, for online documentation, articles, blog posts, or any standard web page. Do NOT use for URLs ending in .md — those are already markdown, use WebFetch directly.
---

# Defuddle

Use Defuddle CLI to extract clean readable content from web pages. Prefer over WebFetch for standard web pages — it removes navigation, ads, and clutter, reducing token usage.

If not installed: `npm install -g defuddle`

## Usage

Always use `--md` for markdown output:

```bash
defuddle parse <url> --md
```

Save to file:

```bash
defuddle parse <url> --md -o content.md
```

Extract specific metadata:

```bash
defuddle parse <url> -p title
defuddle parse <url> -p description
defuddle parse <url> -p domain
```

## Output formats

| Flag | Format |
|------|--------|
| `--md` | Markdown (default choice) |
| `--json` | JSON with both HTML and markdown |
| (none) | HTML |
| `-p <name>` | Specific metadata property |

## Handling slow or unresponsive URLs

The `defuddle` CLI has no built-in fetch timeout, so a slow or hung server can stall the call indefinitely. Always wrap the invocation with a shell-level timeout. **Default: 30 seconds.**

Linux / macOS / git-bash:

```bash
timeout 30 defuddle parse <url> --md
```

PowerShell (Windows):

```powershell
$job = Start-Job { defuddle parse <url> --md }
if (Wait-Job $job -Timeout 30) { Receive-Job $job } else { Stop-Job $job; Write-Error "defuddle timed out after 30s" }
Remove-Job $job -Force
```

If `timeout` exits with code 124 (Linux/macOS) or the PowerShell branch errors, treat the URL as unfetchable and fall back to `WebFetch` or report the failure to the user. Do not retry silently — a hung URL on retry will hang again.

Override the default for known-slow sources (long PDFs, large pages):

```bash
timeout 60 defuddle parse <url> --md
```
