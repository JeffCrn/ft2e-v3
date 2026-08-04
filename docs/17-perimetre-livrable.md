# 17 · Périmètre du livrable site

> Reprise fidèle de la section 10 du PDF (« Modalités du partenariat », pp. 23–24), restreinte au **périmètre site** uniquement. Ce document clarifie ce qui est dans le périmètre de la prestation site (gratuit pour FT2E) et ce qui ne l'est pas — afin que Claude Code ne sur-livre pas ni ne sous-livre.

## Périmètre couvert sans facturation (PDF p. 23)

Le PDF liste précisément, et dans l'ordre :

- **Audit stratégique complet** ← cf. `docs/15-audit-site-actuel.md`
- **Ateliers de cadrage** ← 3 ateliers d'1 h 30 (Phase 1, 2, 3 du calendrier)
- **Architecture d'information et wireframes** ← Phase 2 (S3–4)
- **Direction artistique et design system** ← Phase 3 (S5–7)
- **Développement complet du site (8 pages principales + 30 fiches projets de référence reprises)** ← Phase 4 (S8–11)
- **Intégration du CMS** ← Phase 4 (Decap CMS, S9)
- **Mise en ligne** ← Phase 5 (S12–13)
- **Configuration analytics et formulaire** ← Phase 5 (Plausible, Formspree ou n8n)
- **Formation 2 h de votre équipe à l'usage du CMS** ← Phase 5
- **Garantie et corrections de bugs pendant 3 mois après mise en ligne** ← Phase 6 (M+1 à M+3)

### Ce que la version liminaire couvre du périmètre

| Item PDF | Statut liminaire |
|---|---|
| Audit stratégique | Documenté dans `docs/15-audit-site-actuel.md` |
| Wireframes | Remplacés par directement le **dev de la liminaire** |
| Design system | **Final** dans `tailwind.config.ts` et composants |
| 8 pages principales | **Implémentées avec contenu de démo** |
| 30 fiches projets | **Représentées par 6 à 8 fiches de démo** |
| Intégration Decap | **Hors liminaire** — schémas Zod prêts |
| Mise en ligne | **Preview OVH technique uniquement** |
| Analytics + Formulaire | **UI uniquement**, backend non branché |
| Formation 2 h | **Hors liminaire** |
| Garantie 3 mois | **Sans objet à ce stade** |

## Ce qui n'est pas inclus (PDF p. 23)

Le PDF liste explicitement les exclusions. Aucune n'est à produire :

- ❌ **Refonte profonde du logo** (au-delà du nettoyage et de la vectorisation). → Logo placeholder en liminaire.
- ❌ **Photographies professionnelles** (portraits d'équipe, reportages chantier). → Placeholders Unsplash en liminaire.
- ❌ **Rédaction publicitaire des trente fiches projets** : FT2E fournit la matière brute, EuporIA structure et reformule. → En liminaire, on produit 6–8 fiches de démo ; en production, c'est FT2E qui apporte la matière brute des 30 réelles.
- ❌ **Hébergement annuel au-delà de 12 mois** (~80–150 € HT/an Webhosting Pro après).
- ❌ **Achat du nom de domaine ft2e.fr** (~12 €/an chez OVH — à acquérir par FT2E).
- ❌ **Production de contenus articles SEO post-livraison au-delà des six articles de lancement inclus**.
- ❌ **Engagement commercial post-pilote sur le système BET** : la phase pilote est sans suite obligatoire.

## Articles SEO inclus dans le périmètre site (PDF p. 23)

Le PDF inclut **6 articles de lancement** dans le périmètre site. Ils alimentent le **cocon sémantique** prévu en SEO (PDF p. 19 — un service génère 3 à 5 articles satellites).

Articles recommandés (à valider en cadrage) :

1. **RE2020 en logement collectif : trois leviers de conception** — satellite du service *Étude thermique*.
2. **Coordination SSI dans un ERP de 5ᵉ catégorie : ce qui change réellement** — satellite du service *Coordination SSI*.
3. **Choisir entre PAC aérothermique et géothermique : la grille de décision FT2E** — satellite du service *CVC*.
4. **Études d'exécution sur Revit : retours d'expérience avec les entreprises titulaires** — satellite du service *Études d'exécution & BIM*.
5. **Décret tertiaire 2030 : où en êtes-vous ?** — satellite du service *Audit & diagnostic*.
6. **IRVE et bornes de recharge : conception électrique en logement collectif neuf** — satellite du service *Électricité CFO/CFA*.

En **version liminaire**, **un seul article est produit** : *« Lancement du nouveau site FT2E »* (catégorie *Vie du cabinet*), de manière à montrer le gabarit d'article.

Les six articles techniques de lancement sont produits en Phase 4 du projet.

## Ce qui est attendu de FT2E pour le site (PDF p. 24, restreint au site)

Pour le passage en production (après validation de la liminaire) :

- **Un interlocuteur principal** désigné collégialement par l'équipe associée.
- **Trois ateliers d'1 h 30** (cadrage, wireframes/contenu, design).
- **Mise à disposition des éléments existants** : logo source si disponible, plaquettes, photos d'archives, **références projets brutes** (les 30 fiches).
- **Acquisition et délégation du nom de domaine `ft2e.fr`**.
- **Validation finale avant mise en ligne** par l'équipe associée selon ses modalités de gouvernance.

→ Voir `docs/12-cadrage-jalons.md` pour le calendrier détaillé.

## Engagement de réversibilité (PDF p. 24)

> **« Si à n'importe quel moment vous souhaitez interrompre, vous récupérez gratuitement l'ensemble des livrables produits jusque-là — codes sources du site, fichiers design, contenus rédigés, configuration du système BET, documentation. Le site, les contenus, le matériel, les données : tout vous appartient, du premier jour au dernier. »** (PDF p. 24)

Cet engagement s'applique **à la version liminaire elle-même**. À tout moment, l'équipe FT2E peut :
- Récupérer le dépôt Git complet.
- Continuer le projet avec un autre prestataire (le code est standard Astro + Decap, repris en quelques heures).
- Interrompre sans condition.

Cette posture doit transparaître dans la voix du projet et dans la conduite des ateliers de cadrage.
