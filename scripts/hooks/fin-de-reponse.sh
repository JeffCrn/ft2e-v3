#!/usr/bin/env bash
# Hook Stop — commit + push automatiques en fin de réponse Claude.
#
# Règles :
#   · ne fait rien si l'arbre de travail est propre ;
#   · npm run build d'abord — build rouge = ni commit ni push (règle CLAUDE.md) ;
#   · exclut livrables/ : le dépôt est public, rien n'y part sans décision explicite ;
#   · un seul passage à la fois (verrou), journal dans .git/fin-de-reponse.log
#     (dans .git/ précisément pour ne jamais être commité par ce hook).
set -u

repo="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$repo" || exit 0

log="$repo/.git/fin-de-reponse.log"
lock="$repo/.git/fin-de-reponse.lock"
mkdir "$lock" 2>/dev/null || exit 0
trap 'rmdir "$lock" 2>/dev/null' EXIT

[ -n "$(git status --porcelain -- . ':!livrables')" ] || exit 0

{
  echo "--- $(date '+%F %T') ---"
  if npm run build; then
    git add -A -- . ':!livrables'
    if git commit -m "chore(deploy): pousse l'état de fin de session" \
        -m "Commit et push automatiques (hook Stop, build vert contrôlé)." \
        -m "Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"; then
      git push
    fi
  else
    echo "build rouge — ni commit ni push"
  fi
} >>"$log" 2>&1
