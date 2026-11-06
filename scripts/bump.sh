#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <major|minor|patch|x.y.z>" >&2
  exit 1
fi

files=(
  "plugins/obsidian/.claude-plugin/plugin.json"
  "plugins/obsidian/.codex-plugin/plugin.json"
  ".claude-plugin/marketplace.json"
)

current_version="$(sed -nE 's/^[[:space:]]*"version": "([0-9]+\.[0-9]+\.[0-9]+)".*/\1/p' "${files[0]}" | head -n 1)"
IFS=. read -r major minor patch <<< "$current_version"

case "$1" in
  major) new_version="$((major + 1)).0.0" ;;
  minor) new_version="$major.$((minor + 1)).0" ;;
  patch) new_version="$major.$minor.$((patch + 1))" ;;
  [0-9]*.[0-9]*.[0-9]*) new_version="$1" ;;
  *)
    echo "Usage: $0 <major|minor|patch|x.y.z>" >&2
    exit 1
    ;;
esac

for file in "${files[@]}"; do
  perl -0pi -e "s/\"version\": \"[0-9]+\\.[0-9]+\\.[0-9]+\"/\"version\": \"$new_version\"/" "$file"
done

echo "Updated version: $current_version -> $new_version"
