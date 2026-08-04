# Kickoff — démarrer une session Claude Code sur ft2e-site

Copie-colle ce message en début de session Claude Code, en remplaçant `<TÂCHE>` par ce que tu veux faire.

---

```
Tu travailles sur le site institutionnel FT2E (ft2e-site).

Avant toute action :
1. Lis CLAUDE.md à la racine.
2. Si la tâche concerne une page → lis docs/04-specifications-pages.md.
3. Si la tâche concerne un composant → lis docs/05-bibliotheque-composants.md.
4. Si la tâche concerne du contenu → lis docs/03-modele-contenu.md et .claude/rules/content-collections.md.
5. Si la tâche concerne du style → lis docs/02-design-system.md et .claude/rules/tailwind-design-tokens.md.

Tâche du jour :
<TÂCHE>

Procède :
- En mode plan d'abord si l'impact dépasse un seul fichier.
- En respectant les règles non négociables de CLAUDE.md.
- En invoquant les sous-agents et les commandes slash quand ils existent pour la tâche.
- En finissant par `npm run lint && npm run typecheck && npm run build` avant de me rendre la main.

Si une information manque, demande-la-moi. Ne devine jamais un nom propre, un chiffre métier ou une référence projet.
```

---

## Variantes

### Session courte, ciblée

```
Lis CLAUDE.md puis traite la demande suivante : <TÂCHE>.
Mode plan d'abord obligatoire.
```

### Session de revue

```
Lis CLAUDE.md.

Délègue à seo-reviewer + a11y-auditor + editorial-reviewer une revue
de la route <ROUTE>. Compile les résultats en un rapport synthétique.
```

### Session de création de fiche projet

```
Lis CLAUDE.md, puis utilise la commande /nouvelle-fiche-projet pour
créer la fiche du projet suivant :

Titre : <TITRE>
Secteur : <SECTEUR>
Typologie : <TYPOLOGIE>
MOA : <MOA>
Architecte : <ARCHI>
Lieu : <LIEU>
Surface : <m²>
Année : <ANNEE>
Performance : <PERF>
Mission FT2E : <LISTE>

Le récit projet sera fourni dans un second temps. Laisse des TODO explicites
en attendant.
```
