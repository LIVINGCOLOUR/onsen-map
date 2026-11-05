#!/bin/sh
# サイト本体（index.html と data.json）を https://kakeyu.pages.dev に公開する。
set -e
cd "$(dirname "$0")"
D=$(mktemp -d)
cp index.html data.json "$D"/
npx wrangler pages deploy "$D" --project-name kakeyu --branch main --commit-dirty=true
rm -rf "$D"
