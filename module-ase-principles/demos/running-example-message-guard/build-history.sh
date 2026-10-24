#!/bin/sh
# Replay the snapshots into a tagged git history.
#
#     build-history.sh TARGET_DIR
#
# Run from the directory that holds a0/ and a1/. The result is a RECONSTRUCTION: the first
# commit is the complete A0 snapshot, and each later commit applies one patch exported from the
# A1 build (a1/reference/history/), in order, tagged a1-specs, a1-scenarios, a1-trace, a1.
# The dates and the author are the replay's; the commit messages say so. The replayed a1 tree
# equals the a1/ snapshot except for the .patch files of a1/reference/history/ (the patches are
# not part of the commits, since they describe them). See a1/tooling/replay.md.
set -e
here=$(cd "$(dirname "$0")" && pwd)
target=${1:?usage: build-history.sh TARGET_DIR}
if [ -e "$target" ]; then
    echo "build-history: refusing to touch an existing path: $target" >&2
    exit 1
fi
mkdir -p "$target"
rsync -a --exclude .venv --exclude __pycache__ --exclude .pytest_cache --exclude .ruff_cache \
    --exclude .coverage "$here/a0/" "$target/"
cd "$target"
git init -q
git add -A
git -c user.name=replay -c user.email=replay@example.invalid commit -q \
    -m "a0: message guard, version A0" -m "Replayed from the a0 snapshot; a reconstruction, not the original history."
git tag a0
for patch in "$here"/a1/reference/history/*.patch; do
    if ! git -c user.name=replay -c user.email=replay@example.invalid am -q "$patch"; then
        echo "build-history: patch did not apply: $patch" >&2
        exit 1
    fi
    message=$(git log -1 --format=%B)
    git -c user.name=replay -c user.email=replay@example.invalid commit -q --amend \
        -m "$message" -m "Replayed from a1/reference/history/$(basename "$patch"); a reconstruction, not the original history."
    git tag "$(basename "$patch" .patch | sed 's/^[0-9]*-//')"
done
echo "build-history: $(git rev-list --count HEAD) commits in $target; tags: $(git tag | tr '\n' ' ')"
