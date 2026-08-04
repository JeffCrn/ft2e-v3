---
description: Pilote la construction complète de la version liminaire (7 phases)
---

# Construire la version liminaire

Lance le pilote master pour construire la version liminaire complète du site FT2E selon les phases définies dans `prompts/build-version-liminaire.md`.

## Étapes

1. **Lis** `prompts/build-version-liminaire.md` intégralement.
2. **Vérifie** que tu es bien dans un dossier `ft2e-site/` avec le dossier de cadrage présent (CLAUDE.md, docs/, content-models/, etc.).
3. **Détecte** le mode :
   - Si l'utilisateur a écrit "yolo" dans son message → enchaîne les 7 phases en autonomie.
   - Sinon → procède phase par phase avec point de contrôle.
4. **Exécute** chaque phase en suivant strictement les instructions du prompt master.

## Critères d'acceptation finale

- Toutes les routes (≥ 26 pages) générées par `npm run build`
- Lighthouse mobile : Perf ≥ 90, A11y 100, BP 100, SEO 100 sur la home
- `[DÉMO]` apparent sur les contenus encore en démonstration
- Aucun lorem ipsum
- Équipe des 7 personnes nommée uniformément par prénom (pas de distinction)
- Rapport final dans `audits/liminaire-pret.md`

## Si quelque chose bloque

- Si une dépendance échoue à l'installation → essayer une alternative documentée dans `docs/01-architecture-technique.md`.
- Si Lighthouse stagne sous les cibles → diagnostiquer dans l'ordre : image hero trop lourde, polices, *islands* trop chargées.
- Si une information manque dans `docs/18-contenus-demonstration.md` → marquer `[À CONFIRMER FT2E]` et continuer.

## À ne pas faire

- Ne pas configurer Decap CMS (hors périmètre liminaire).
- Ne pas connecter le formulaire Contact à un backend réel.
- Ne pas inventer des noms, MOA ou chiffres absents du catalogue.
- Ne pas produire de portraits individuels de l'équipe.
