#!/bin/sh

set -eu

project="$1"
cd "$project"

[ -f "./hf.conf" ] || { echo "err ./hf.conf not found"; exit 1; }
. ./hf.conf

for item in $ARTIFACTS; do
    [ -e "$item" ] || { echo "err: missing artifact: $item" >&2; exit 1; }
    echo "$item"
done

uvx hf upload "$REPO_ID" . . \
  --repo-type "${REPO_TYPE:-model}" \
  --commit-message "Release $(basename "$(pwd)") snapshot"