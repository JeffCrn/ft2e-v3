# Prompt — revue finale avant mise en ligne

À exécuter à la fin de la Phase 5 (recette & audits) avant la mise en
production. Cf. `docs/12-cadrage-jalons.md`.

```
Lis CLAUDE.md.

Tu vas piloter une revue complète du site ft2e-site avant mise en ligne.

PÉRIMÈTRE — toutes les routes publiques :
- /
- /societe
- /equipe
- /services et /services/[slug] x6
- /references et /references/[slug] x10 (les fiches phares)
- /actualites et /actualites/[slug] x1 (au moins l'article de lancement)
- /contact
- /accessibilite
- /mentions-legales
- /politique-confidentialite

PROCÉDURE — exécute dans l'ordre :

1. BUILD COMPLET
   - npm run lint
   - npm run typecheck
   - npm run build
   - Vérifier nombre de routes générées vs attendu.
   - Vérifier taille du bundle (du -sh dist/).

2. AUDIT TECHNIQUE EN PARALLÈLE — délègue à 3 sous-agents simultanément :
   - seo-reviewer → toutes les routes
   - a11y-auditor → toutes les routes
   - editorial-reviewer → revue du contenu visible

3. AUDIT LIGHTHOUSE
   - Utilise le skill lighthouse-audit.
   - Lance sur 5 routes échantillons : /, /references/<projet-phare>,
     /services/cvc, /equipe, /actualites/<article-lancement>.
   - Mode mobile et desktop.
   - Archive les rapports dans audits/<date>-lighthouse-final/.

4. VÉRIFICATIONS COMPLÉMENTAIRES
   - Tous les liens internes : pas de 404. Utilise un crawler local
     (par ex. `npx broken-link-checker http://localhost:4321`).
   - Tous les og:image existent (fichiers présents dans public/og/).
   - sitemap.xml généré et complet.
   - robots.txt cohérent avec stratégie GEO (.claude/rules/seo-geo.md).
   - .htaccess présent dans dist/ avec redirections 301 migration.
   - JSON-LD valide sur 3 pages tirées au sort (extraction + jq + schema validator).

5. CHECKLIST RGPD
   - Page /accessibilite publiée avec déclaration conforme.
   - Page /mentions-legales avec SIREN, hébergeur (OVH Roubaix), DPO.
   - Page /politique-confidentialite avec cartographie traitements.
   - Formulaire contact : consentement explicite non pré-coché, finalité claire.
   - Pas de tracker tiers (vérifier Network tab dans navigateur).

6. COMPILATION DU RAPPORT
   - Produit un fichier audits/<date>-revue-prelancement.md avec :
     - Table de scores Lighthouse par route.
     - Synthèse SEO (constats, blocages).
     - Synthèse a11y (conformité RGAA AA).
     - Synthèse éditoriale (corrections proposées).
     - Liste des TODO restants par criticité (blocage / majeur / mineur).
     - Recommandation finale : "GO" ou "NO-GO" pour la mise en ligne.

CRITÈRES DE GO :
- Aucun bug blocage.
- Lighthouse mobile : Perf ≥ 90, A11y 100, BP 100, SEO 100 sur les 5 routes
  échantillons.
- Aucune 404 interne.
- RGAA AA conforme avec déclaration publiée.
- RGPD conforme.
- Pages légales publiées et validées.

Si NO-GO : produire une liste d'actions priorisée avec estimation effort
pour chaque item bloquant.
```
