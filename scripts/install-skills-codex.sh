#!/usr/bin/env bash
#
# Install obsidian-skills for Codex native skill discovery.
#
# Syncs each skill from skills/ into the Codex skills directory
# (default: ~/.agents/skills/obsidian-skills).
#
# Usage:
#   ./scripts/install-skills-codex.sh [options]
#
# Options:
#   --skills-dir PATH   Target skills directory (default: ~/.agents/skills/obsidian-skills)
#   --dry-run           Print actions without writing anything
#   -h, --help          Show this help message
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_DIR="${HOME}/.agents/skills/obsidian-skills"
DRY_RUN="false"

usage() {
    cat <<EOF
Install obsidian-skills for Codex native skill discovery.

Usage:
  scripts/install-skills-codex.sh [options]

Options:
  --skills-dir PATH   Target skills directory (default: ~/.agents/skills/obsidian-skills)
  --dry-run           Print actions without writing anything
  -h, --help          Show this help message
EOF
}

log() {
    printf '[install-skills] %s\n' "$*"
}

die() {
    printf '[install-skills] Error: %s\n' "$*" >&2
    exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --skills-dir)
            SKILLS_DIR="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN="true"
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            die "Unknown option: $1"
            ;;
    esac
done

# Validate repo structure
[[ -d "$REPO_ROOT/skills" ]] || die "skills/ directory not found under repo root: $REPO_ROOT"

# Collect skill names
mapfile -t SKILL_NAMES < <(find "$REPO_ROOT/skills" -maxdepth 1 -mindepth 1 -type d -exec basename {} \; | sort)
[[ ${#SKILL_NAMES[@]} -gt 0 ]] || die "No skills found in $REPO_ROOT/skills"

sync_skill() {
    local skill="$1"
    local src="$REPO_ROOT/skills/$skill"
    local dst="$SKILLS_DIR/$skill"

    if [[ "$DRY_RUN" == "true" ]]; then
        log "DRY-RUN: sync $src -> $dst"
        return
    fi

    mkdir -p "$dst"
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "$src/" "$dst/"
    else
        local tmp_dst
        mkdir -p "$(dirname "$dst")"
        tmp_dst="$(mktemp -d)"
        if cp -a "$src/." "$tmp_dst/"; then
            rm -rf "$dst"
            mv "$tmp_dst" "$dst"
        else
            rm -rf "$tmp_dst"
            die "Failed to copy $src to $dst"
        fi
    fi
}

if [[ "$DRY_RUN" == "true" ]]; then
    log "DRY-RUN mode — no files will be written"
fi

log "Installing obsidian-skills to: $SKILLS_DIR"

for skill in "${SKILL_NAMES[@]}"; do
    log "Syncing skill: $skill"
    sync_skill "$skill"
done

if [[ "$DRY_RUN" == "false" ]]; then
    log "Done. Skills installed to: $SKILLS_DIR"
    log "Restart Codex to discover the new skills."
fi
