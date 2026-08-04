# 12 · Cadrage des jalons

> Calendrier strictement aligné sur la **section 11 du PDF (p. 25)** — 13 semaines, 6 phases, 5 jalons de validation. Mise en ligne cible **fin août / début septembre 2026** sous réserve d'un démarrage début juin 2026.

## Vue d'ensemble

```
PHASE 1 · Sem. 1-2     ▸ Cadrage                          → Note de cadrage validée
PHASE 2 · Sem. 3-4     ▸ Architecture & contenu (wireframes) → Wireframes validés
PHASE 3 · Sem. 5-7     ▸ Design UI (maquettes haute fidélité) → Maquettes validées
PHASE 4 · Sem. 8-11    ▸ Développement                    → Site recette accessible
PHASE 5 · Sem. 12-13   ▸ Recettage et lancement            → Site en ligne
PHASE 6 · M+1 à M+3    ▸ Garantie                          → Bilan post-lancement
```

## Phase 1 — Cadrage (S1–S2)

### Activités (PDF p. 25)
- **Atelier de découverte** (1 h 30) avec l'équipe associée.
- **Audit fin de l'existant** — cf. `docs/15-audit-site-actuel.md`.
- **Étude concurrentielle locale** sur cinq BET de référence du bassin Centre-Ouest atlantique.
- **Définition du positionnement éditorial**.

### Spécificité de cette phase dans le contexte actuel
La **version liminaire est présentée en début de Phase 1** comme support de l'atelier de découverte. Ce qui est validé en atelier valide simultanément des éléments de la Phase 3 (design UI) et de la Phase 2 (architecture).

### Livrable
- ✅ **Note de cadrage validée**

### Critères de sortie
- Positionnement éditorial validé par l'équipe associée.
- Liste définitive des 30 fiches projets à reprendre.
- Interlocuteur principal désigné collégialement (PDF p. 24).

---

## Phase 2 — Architecture & contenu (S3–S4)

### Activités (PDF p. 25)
- **Sitemap définitif** (validation ou ajustements des 8 pages).
- **Wireframes des huit pages principales**.
- **Atelier de validation** (1 h 30).
- **Plan de rédaction** des 30 fiches projets + 6 articles SEO de lancement.

### Spécificité
La version liminaire ayant déjà été présentée, cette phase consiste essentiellement à **figer les ajustements** identifiés lors de la Phase 1 et à **structurer la production de contenus** (qui rédige quoi, sur quel délai).

### Livrable
- ✅ **Wireframes validés** (ou maquettes liminaires ajustées validées en place et lieu)

### Critères de sortie
- Plan de rédaction des 30 fiches projets validé (qui apporte quoi, quand).
- 6 sujets d'articles SEO arrêtés.
- Liste exhaustive des partenaires (MOA, architectes) à mentionner avec accord d'usage des logos.

---

## Phase 3 — Design UI (S5–S7)

### Activités (PDF p. 25)
- **Maquettes haute fidélité** (accueil + trois pages types).
- **Itérations**.
- **Design system complet**.
- **Atelier de validation** (1 h 30).

### Spécificité
Le design system est déjà implémenté dans la liminaire. Cette phase consiste à :
- **Affiner** les composants à partir des retours d'atelier Phase 1.
- **Produire les variations** non implémentées en liminaire (états hover/focus avancés, variantes mobiles fines, animations).
- **Valider formellement** le design system dans son ensemble.

### Livrable
- ✅ **Maquettes validées** + design system gelé

### Critères de sortie
- `tailwind.config.ts` figé pour la suite du projet.
- Tous les composants `primitives/` et `blocs/` validés en revue UI.
- Logo finalisé et intégré (sortie de la version placeholder de la liminaire).

---

## Phase 4 — Développement (S8–S11)

### Activités (PDF p. 25)
- **Intégration Astro**.
- **Configuration Decap CMS** (cf. `docs/08-configuration-decap.md`).
- **Reprise et structuration des trente fiches projets** (matière brute fournie par FT2E, structurée et reformulée par EuporIA — PDF p. 23).
- **Tests cross-browser et mobile**.

### Spécificité
La liminaire fournissant déjà les composants et le squelette de pages, l'effort se concentre sur :
- **Decap CMS** : configuration `public/admin/config.yml`, authentification GitHub, workflow éditorial.
- **Migration de contenu** : substitution des 8 fiches projets démo par les 30 réelles, photos professionnelles.
- **Reportage photo** (hors périmètre prestation EuporIA, mais à caler avec un photographe — PDF p. 11 budget indicatif 800 à 1 500 € HT).
- **Rédaction des 6 articles SEO de lancement**.

### Livrable
- ✅ **Site recette accessible** sur URL technique OVH (de type `ft2e-recette.ovh.net`).

### Critères de sortie
- 30 fiches projets réelles publiées et validées par FT2E.
- 6 articles SEO publiés.
- Decap CMS testé en édition par au moins un membre FT2E.
- Score Lighthouse mobile sur 5 routes échantillons : Perf ≥ 90, A11y 100, BP 100, SEO 100.

---

## Phase 5 — Recettage et lancement (S12–S13)

### Activités (PDF p. 25)
- **Corrections finales**.
- **Configuration domaine `ft2e.fr`**.
- **Mise en place des redirections 301** depuis `ft2e.myportfolio.com`.
- **Soumission Search Console**.
- **Formation 2 h** de l'équipe FT2E à Decap CMS.

### Activités complémentaires
- Branchement effectif du formulaire de contact (Formspree ou n8n).
- Activation de Plausible Analytics.
- Configuration email Pro (SPF/DKIM/DMARC) si non déjà actif.
- Bascule DNS de `ft2e.fr` au jour J.

### Livrable
- ✅ **Site en ligne** sur `https://ft2e.fr`

### Critères de sortie (revue finale)
- Aucun bug bloquant.
- Lighthouse cibles atteintes sur production.
- Anciennes URLs `ft2e.myportfolio.com` redirigées en 301.
- Sitemap soumis à Search Console.
- Plausible affiche les premières visites.
- Au moins un membre FT2E sait publier une actualité en autonomie.

---

## Phase 6 — Garantie (M+1 à M+3)

### Activités (PDF p. 25)
- **Correction des bugs résiduels**.
- **Suivi de l'indexation Google**.
- **Bilan d'un mois et de trois mois**.

### Livrable
- ✅ **Bilan post-lancement** documenté dans `docs/audits/bilan-m1.md` puis `docs/audits/bilan-m3.md`.

### Indicateurs suivis (PDF p. 19)
- Trafic organique mensuel (baseline 0, observation pure).
- Position moyenne sur les 20 mots-clés cibles.
- Nombre de demandes entrantes qualifiées via formulaire à branches.
- Taux d'apparition dans les réponses Perplexity / ChatGPT (mesure expérimentale).

### Critères de sortie de garantie (M+3)
- Aucun bug remonté non corrigé.
- Indexation Google ≥ 50 pages.
- Présence Search Console stable.
- FT2E autonome sur le CMS sans sollicitation d'EuporIA.

---

## Date cible de mise en ligne (PDF p. 25)

> **« Sous réserve d'un démarrage début juin 2026, la mise en ligne peut être visée fin août / début septembre 2026, juste avant la rentrée et la reprise des consultations dans le BTP. »**

| Étape | Date cible |
|---|---|
| Présentation de la liminaire | **Mai 2026** (avant démarrage Phase 1) |
| Atelier de cadrage initial (Phase 1) | **Début juin 2026** |
| Fin Phase 3 (design figé) | Fin juillet 2026 |
| Site recette accessible (fin Phase 4) | Mi-août 2026 |
| Mise en ligne `ft2e.fr` | **Fin août / début septembre 2026** |
| Bilan M+3 | Décembre 2026 |

---

## Cérémonies (PDF p. 24)

- **Trois ateliers de 1 h 30 chacun** : cadrage initial (Phase 1), validation wireframes (Phase 2), validation design (Phase 3). En présentiel à La Rochelle ou en visio. Ouverts à toute personne de l'équipe que le cabinet souhaite associer aux décisions.
- **Validation finale** avant mise en ligne par l'équipe associée selon ses modalités de gouvernance.
- **Garantie 3 mois** post-lancement.

## Risques et marges de manœuvre

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| Démarrage Phase 1 décalé au-delà de juin | moyenne | manque la fenêtre rentrée BTP | Présenter la liminaire en mai pour accélérer la décision |
| Disponibilité limitée FT2E pour collecte matière brute des 30 fiches | élevée | retard Phase 4 | Démarrer la collecte dès Phase 1, en parallèle |
| Demande d'évolution graphique tardive (Phase 4) | moyenne | retard 1 semaine | Design verrouillé fin Phase 3 avec PV de validation |
| Migration DNS mal maîtrisée | faible | downtime | Procédure documentée, TTL abaissé à J-2, fenêtre nocturne |
| Audit RGAA révèle des écarts importants | faible | retard 1 semaine | A11y intégrée dès la liminaire (cf. `.claude/rules/accessibility-rgaa.md`) |

## Engagement de réversibilité (PDF p. 24)

À tout moment, FT2E peut récupérer l'ensemble des livrables (code, contenus, médias, accès). La propriété intellectuelle des livrables réalisés appartient à FT2E.
