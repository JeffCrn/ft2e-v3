# ft2e-v3 — Site internet FT2E

Site institutionnel de **FT2E** — bureau d'études techniques pluridisciplinaire, La Rochelle (depuis 2008).

**v3 = fork de `ft2e-v2`** : contenus, collections et CMS identiques ; le design system passe à la charte v3 « plans et profondeur » (« FT2E Charte graphique » document 10 · révision 2, août 2026, bundle `branding-v3/`) — rampe monochrome 197° inchangée, relief par trois rangs d'ombre à l'encre translucide, filets 1 px hiérarchisés par l'opacité, trame 28 px, planche de page 1440 px posée sur calcaire, bouton principal en aplat encre.

- **Prestataire** : EuporIA Factory (Jean-François Caron) — La Rochelle.
- **Déploiement de démo** : `https://ft2e-v3.vercel.app` (Vercel, statique).
- **Cible finale** : `https://ft2e.fr`.

> ⚠️ **Site en démo client — indexation par les moteurs bloquée volontairement** (robots.txt, `X-Robots-Tag`, `noindex` global). Ne pas débloquer sans validation FT2E — procédure de revert : `docs/19-migration-production.md`.

## Démarrage

```bash
npm install
cp .env.example .env       # PUBLIC_MODE=liminaire par défaut
npm run dev                # http://localhost:4321
npm run build              # build de production dans ./dist
npm run preview            # sert le build local
```

## Repères

| Besoin | Fichier |
|---|---|
| Mémoire principale Claude Code | `CLAUDE.md` — à lire en premier |
| Design tokens stricts (charte v3) | `.claude/rules/tailwind-design-tokens.md` |
| Spec charte v3 « plans et profondeur » | `docs/superpowers/specs/2026-08-06-ft2e-charte-v3-plans-profondeur.md` |
| Recettes CSS (rampe, plans, composants) | `src/styles/global.css` |
| Spécifications page-par-page | `docs/04-specifications-pages.md` |
| Contenus de démonstration (`[DÉMO]`) | `docs/18-contenus-demonstration.md` |
| Migration vers `ft2e.fr` (revert SEO inclus) | `docs/19-migration-production.md` |

Conventions dans `.claude/rules/`, commandes répétables dans `.claude/commands/`, cadrage complet dans `docs/`.

## Contact

- **MOA** : équipe associée FT2E (interlocuteur principal à désigner collégialement).
- **Prestataire** : Jean-François Caron — `contact@euporia-factory.com`
