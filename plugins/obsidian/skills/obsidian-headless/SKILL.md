---
name: obsidian-headless
description: Sync and publish Obsidian vaults from the command line with Obsidian Headless (`ob`), without the desktop app. Use when the user wants to set up or run Obsidian Sync or Obsidian Publish on a server, in CI, or from a terminal, or change a vault's Sync or Publish settings.
---

# Obsidian Headless

Use Obsidian Headless (`ob`) to run Obsidian Sync and Obsidian Publish from the command line. It doesn't need the desktop app, so it works on servers, in CI, and in sandboxes. It's in open beta. Docs: https://help.obsidian.md/headless

`ob` only syncs and publishes files. To read or change notes without the app, edit the files directly and follow the obsidian-markdown skill. To control a running desktop app, use the obsidian-cli skill.

## Before using ob

Check availability with `ob --help`. If it is missing, explain that Obsidian Headless requires Node.js 22 or later and offer installation with `npm install -g obsidian-headless`. Run `ob <command> --help` for a command's options.

Sync and Publish each need an active subscription on the user's account.

Most commands accept `--json` for machine-readable output.

## Log in

`ob login` prints the account when already logged in. Otherwise it prompts for email, password, and a 2FA code, so ask the user to run it in their own terminal. Don't ask for their password or pass it with `--password`. `ob logout` clears the stored credentials.

## Vault paths

Commands act on the vault in the current directory, or the one given with `--path`. Pass `--path` so the target is explicit. Before a command that changes remote state, confirm the vault, site, and path from list or status output.

## Sync

Don't use the desktop app's Sync and Headless Sync for the same vault on the same device, because they cause conflicts. Ask the user to back up the vault folder before the first sync.

```bash
ob sync-list-remote                                  # remote vaults, including shared ones
ob sync-list-local                                   # vaults set up on this machine
ob sync-setup --vault "Research" --path ~/vaults/research
ob sync --path ~/vaults/research                     # sync once
ob sync --path ~/vaults/research --continuous        # keep syncing as files change
ob sync-status --path ~/vaults/research
ob sync-unlink --path ~/vaults/research              # disconnect and remove stored credentials
```

`--vault` takes a remote vault's name or ID. For an end-to-end encrypted vault, `sync-setup` prompts for the encryption password, so let the user enter it. Set `--device-name` to label this machine in version history.

`--continuous` runs until stopped, so start it in the background or as a service.

`ob sync-create-remote --name "Research"` creates a remote vault. Add `--encryption e2ee` for end-to-end encryption or `--encryption standard` for managed encryption.

### Sync settings

`ob sync-config --path <vault>` prints the vault's settings. Change them with:

- `--mode bidirectional|pull-only|mirror-remote`. `pull-only` ignores local changes and `mirror-remote` reverts them, so confirm before setting either.
- `--conflict-strategy merge|conflict`
- `--excluded-folders "Archive,Templates"`
- `--file-types image,audio,video,pdf,unsupported` for the attachment types to sync.
- `--configs` for the settings categories to sync, e.g. `app,appearance,core-plugin`.
- `--config-dir` when the vault's configuration folder isn't `.obsidian`.

An empty string clears a list option, e.g. `--excluded-folders ""`.

## Publish

```bash
ob publish-list-sites
ob publish-setup --site my-notes --path ~/vaults/research
ob publish --path ~/vaults/research --dry-run
ob publish --path ~/vaults/research --yes
```

`ob publish` includes only notes with `publish: true` in their properties. `--all` includes every file, so use it only when the user asks. Run `--dry-run` first and show the user the changes. Without `--yes`, `ob publish` waits for confirmation, so pass `--yes` once the user approves or for an unattended job they set up.

`ob publish-create-site --slug my-notes` creates a site at `publish.obsidian.md/my-notes`.

Run these with no options to print the current settings:

- `ob publish-config` sets folders to include or exclude with `--includes` and `--excludes`.
- `ob publish-site-options` sets the site name, home page, navigation, theme, and other display options. Run `ob publish-site-options --help` for the full list.

`ob publish-unlink` disconnects the vault from its site.
