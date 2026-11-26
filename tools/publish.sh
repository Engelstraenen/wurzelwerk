#!/bin/zsh
# GitHub Pages veröffentlichen ohne subtree split (Masterfile V2.77): gh-pages = ein Commit aus main:site
set -e
cd "$(dirname "$0")/.."
C=$(git commit-tree "$(git rev-parse main:site)" -m pages)
[ ${#C} -eq 40 ] || { echo "Commit leer, Abbruch"; exit 1; }
git -c http.postBuffer=524288000 push -qf origin "${C}:refs/heads/gh-pages"
git ls-remote origin gh-pages | cut -c1-12
