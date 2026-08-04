# ft2e-site — Version liminaire

Site institutionnel de **FT2E** — bureau d'études techniques pluridisciplinaire, La Rochelle.

**Prestataire** : EuporIA Factory (Jean-François Caron) — La Rochelle.
**Référentiel** : proposition stratégique mai 2026 (PDF).
**Cible finale** : `https://ft2e.fr` — mise en ligne fin août / début septembre 2026.

## Ce dossier — version liminaire

Ce dépôt construit une **version liminaire** du site : maquette navigable haute fidélité destinée à être présentée à l'équipe associée FT2E lors de l'atelier de cadrage initial. **Ce n'est pas encore le site de production** — les contenus sont marqués `[DÉMO]`, le CMS n'est pas configuré, le formulaire Contact n'est pas branché.

Cadrage central : **`docs/14-version-liminaire.md`**. À lire en priorité.

## Démarrage

```bash
npm install
cp .env.example .env       # PUBLIC_MODE=liminaire par défaut
npm run dev                # http://localhost:4321
npm run build              # build de production dans ./dist
npm run preview            # serve le build local
```

## Structure du dépôt

```
ft2e-site/
├── CLAUDE.md                  # mémoire principale Claude Code
├── README.md                  # ce fichier
├── .claude/                   # configuration Claude Code (rules, agents, skills, commands)
├── docs/                      # cadrage produit / technique / éditorial (19 fichiers)
│   ├── 14-version-liminaire.md     ← À LIRE EN PREMIER
│   ├── 15-audit-site-actuel.md
│   ├── 16-ecosysteme-clients.md
│   ├── 17-perimetre-livrable.md
│   └── 18-contenus-demonstration.md
├── adr/                       # Architecture Decision Records
├── content-models/            # schémas Zod des collections
├── content-templates/         # gabarits prêts à dupliquer
├── prompts/                   # prompts réutilisables
│   └── build-version-liminaire.md  ← prompt master
├── public/                    # statiques + interface Decap (V2)
└── src/                       # application Astro (à générer)
```

## Pour Claude Code

Toute session démarre par :
1. Lecture de **`CLAUDE.md`** à la racine.
2. Lecture de **`docs/14-version-liminaire.md`**.
3. Lecture des docs liés à la tâche en cours.

Conventions dans `.claude/rules/`. Commandes répétables dans `.claude/commands/`. Prompt master dans `prompts/build-version-liminaire.md`.

## Pour un développeur humain

Lire dans l'ordre :
1. `CLAUDE.md`
2. `docs/14-version-liminaire.md` — ce qu'est exactement la liminaire
3. `docs/15-audit-site-actuel.md` — pourquoi cette refonte
4. `docs/00-vision-produit.md` — vision globale
5. `docs/04-specifications-pages.md` — pages détaillées
6. `docs/12-cadrage-jalons.md` — calendrier 6 phases / 13 semaines

## Pour passer en production

Quand la liminaire aura été validée par FT2E :

1. `PUBLIC_MODE=production` dans `.env`
2. Substitution des fiches projets démo par les fiches FT2E réelles
3. Suppression du flag `demo: true` dans les fiches validées
4. Remplacement des images placeholder par les photos réelles
5. Logo final
6. Activation Formspree/n8n pour le formulaire
7. Configuration Decap CMS complète + formation équipe
8. Bascule DNS `ft2e.fr`
9. **Revert du blocage SEO triple-couche** (`robots.txt`, `vercel.json`, `noindex` par défaut dans `BaseLayout.astro`)

→ **Checklist exhaustive et ordonnée** : [`docs/19-migration-production.md`](docs/19-migration-production.md). Cf. aussi `docs/14-version-liminaire.md` § « Du liminaire au production ».

> ⚠️ **Site actuellement en démo client sur `https://ft2e-site.vercel.app` — indexation par les moteurs bloquée volontairement.** Ne pas débloquer sans validation FT2E.

## Contact

- **MOA** : équipe associée FT2E (interlocuteur principal à désigner collégialement)
- **Prestataire** : Jean-François Caron — `contact@euporia-factory.com`
