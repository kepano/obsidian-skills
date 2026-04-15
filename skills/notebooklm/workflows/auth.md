# Auth Workflow

Authenticate with NotebookLM via browser-based Google login using `notebooklm-py`.

## When Needed

Any `notebooklm` command returns auth errors or redirects to accounts.google.com.

## Step 1: Login

This opens a Chromium browser for interactive Google login. **User must run this themselves** (requires interactive browser).

```bash
cd ~/projects/notebooklm-loader && uv run notebooklm login
```

Flow:
1. Browser opens to Google login
2. User completes login + 2FA
3. Waits until NotebookLM homepage loads
4. User presses Enter in terminal
5. Cookies saved to `~/.notebooklm/storage_state.json`

## Step 2: Verify

```bash
cd ~/projects/notebooklm-loader && uv run notebooklm list
```

Should show notebook list without errors.

## Troubleshooting

**Browser doesn't open:** Playwright chromium may not be installed. Run:
```bash
cd ~/projects/notebooklm-loader && uv run playwright install chromium
```

**Wrong Google account:** Login opens a fresh browser profile at `~/.notebooklm/browser_profile`. If you need a different account, delete this folder first and re-login.

**Auth expires:** Google cookies typically last weeks. Re-run login when commands start failing.
