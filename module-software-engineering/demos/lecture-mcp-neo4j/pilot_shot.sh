#!/bin/sh
# Move the newest macOS screenshot to its place in the course repository.
#
#   pilot_shot.sh <name> [--dry-run]
#
# Names starting with "desktop-"   go to neo4j/resources/<name>.png
# Names starting with "mcp-neo4j-" go to module-software-engineering/slides/images/<name>.png
# The newest "Screenshot ... .png" in the macOS screenshot folder (your Desktop
# unless you changed it) is moved. The script refuses to overwrite a file.
set -eu
[ $# -ge 1 ] || { echo "usage: pilot_shot.sh <name> [--dry-run]" >&2; exit 2; }
name="${1%.png}"; dry="${2:-}"
root="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
shots="$(defaults read com.apple.screencapture location 2>/dev/null || true)"
[ -n "$shots" ] && [ -d "$shots" ] || shots="$HOME/Desktop"
case "$name" in
  desktop-*)   dest="$root/neo4j/resources/$name.png" ;;
  mcp-neo4j-*) dest="$root/module-software-engineering/slides/images/$name.png" ;;
  *) echo "name must start with desktop- or mcp-neo4j-" >&2; exit 2 ;;
esac
newest="$(ls -t "$shots"/Screenshot*.png "$shots"/Screen\ Shot*.png 2>/dev/null | head -1 || true)"
[ -n "$newest" ] || { echo "no Screenshot*.png found in $shots" >&2; exit 1; }
[ ! -e "$dest" ] || { echo "refusing to overwrite existing $dest" >&2; exit 1; }
echo "newest screenshot: $newest  (taken $(stat -f '%Sm' "$newest"))"
if [ "$dry" = "--dry-run" ]; then
  echo "would move to:     $dest"
else
  mkdir -p "$(dirname "$dest")"
  mv "$newest" "$dest"
  echo "moved to:          $dest"
fi
