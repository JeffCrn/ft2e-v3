# 06 · Stratégie SEO local & GEO

Cette stratégie est la traduction opérationnelle des cinq leviers mentionnés dans la proposition de partenariat.

## Cinq leviers structurants

### 1. Schéma JSON-LD `LocalBusiness` (et dérivés)

Implémentation détaillée dans `.claude/skills/json-ld-builder/SKILL.md` et `.claude/rules/seo-geo.md`.

**À renseigner par FT2E avant publication** :
- Adresse postale exacte.
- Téléphone direct (à valider : standard ou ligne dédiée).
- Horaires d'ouverture (souvent omis sur le site, mais utiles pour le GBP).

### 2. Cocon sémantique métier

Pour chaque service, **une page pilier + 3 à 5 articles satellites**.

#### Plan éditorial recommandé V1 (à valider avec FT2E)

| Service pilier | Articles satellites |
|---|---|
| Étude thermique RT/RE | RE2020 expliquée — Choisir entre STD et calcul réglementaire — ACV bâtiment : enjeux concrets |
| CVC | Choix d'une PAC en logement collectif — Géothermie ou aérothermie ? — Cas d'un dimensionnement réversible |
| Électricité CFO/CFA | NF C 15-100 dans le tertiaire — IRVE et bornes de recharge — Smart building : où s'arrêter |
| Coordination SSI | SSI dans un ERP de 5ᵉ catégorie — Désenfumage mécanique vs naturel — Calage SSI sur projet de réhab |
| Études d'exécution & BIM | Revit en exécution : retours d'expérience — Coordination MEP — DOE numérique : ce qu'attendent les MOA |
| Audit & diagnostic | Audit énergétique tertiaire et décret tertiaire — DPE : portée et limites |

Chaque article doit :
- Lier vers sa page pilier.
- Lier vers 1–2 projets pertinents.
- Lier vers 1 autre article du même cocon.

### 3. Géolocalisation sémantique

#### V1 (au lancement)

- Toutes les communes d'intervention mentionnées dans `areaServed` du `ProfessionalService`.
- Texte naturel intégrant La Rochelle, Rochefort, Royan, Saintes, Île de Ré, Île d'Oléron, Niort, La Roche-sur-Yon sur la page Société et le footer.

#### V2 (post-lancement, à roadmap)

- Pages dédiées : `/zone/<commune>` ou `/intervention/<commune>` pour les 8 communes principales.
- Chaque page liste projets locaux + accroche personnalisée + JSON-LD `Place`.

### 4. Google Business Profile (GBP)

Action externe au site, mais pilotée dans le cadre du partenariat :

1. **Audit** de la fiche existante (si elle existe, sinon création).
2. **Nettoyage** : photos, services, horaires, FAQ.
3. **Cadence** : 1 publication mensuelle (chantier, livraison, événement).
4. **Sollicitation d'avis** : process structuré (qui demander, quand, comment relancer).

Le suivi GBP est documenté hors du dépôt (canal de pilotage à définir avec FT2E).

### 5. Réseau de liens entrants

Cible V1 :

- **Architectes partenaires** : demander un lien depuis leur page « équipe BET » ou « partenaires » pour les projets co-réalisés.
- **MOA institutionnels** : OPH (La Rochelle, Habitat 17), communes, ports — souvent listent leurs prestataires.
- **Annuaires métier** : Syntec-Ingénierie, CINOV, qualifications RGE.
- **Presse locale** : Sud Ouest, Le Phare de Ré pour livraisons remarquables.

**Pas de liens achetés. Pas de PBN.** Tout lien doit être justifié par une relation existante.

## Mots-clés cibles V1

Liste prioritaire (≤ 20), à affiner en atelier de cadrage avec FT2E :

### Tête de longue traîne

- bureau études fluides La Rochelle
- BET thermique Charente-Maritime
- ingénierie CVC La Rochelle
- coordination SSI Charente-Maritime
- études exécution Revit La Rochelle
- BIM bâtiment La Rochelle

### Longue traîne réglementaire

- étude RE2020 logement collectif
- simulation thermique dynamique RE2020
- audit énergétique décret tertiaire

### Longue traîne géographique

- BET fluides Île de Ré
- BET fluides Île d'Oléron
- BET fluides Royan
- bureau d'études Rochefort
- ingénierie bâtiment Niort

### Concurrents directs (à veiller, pas à attaquer frontalement)

À identifier en atelier de cadrage : 5 BET de référence sur le territoire pour benchmark de positionnement.

## Indicateurs de pilotage

Source : Search Console + Plausible + audit manuel mensuel.

| Indicateur | Baseline | Cible M+3 |
|---|---|---|
| Trafic organique mensuel | 0 (site neuf) | à observer, pas promis |
| Pages indexées (Search Console) | 0 | ≥ 50 |
| Position moyenne sur 20 mots-clés cibles | n/a | top 30 sur ≥ 10 |
| Demandes entrantes qualifiées via formulaire | 0 | ≥ 2 / mois |
| Apparition dans réponses Perplexity / ChatGPT (mesure exp.) | 0 | mesurée et rapportée |

**Bilan à M+1 et à M+3** : produit dans `docs/audits/seo-m1.md` et `docs/audits/seo-m3.md`.

## Anti-patterns à éviter

- ❌ Mots-clés artificiellement répétés (keyword stuffing).
- ❌ Pages doorway (une par variation de mot-clé).
- ❌ Contenu généré sans relecture humaine.
- ❌ Échange de liens en chaîne.
- ❌ Faux avis sur GBP (sanctionné lourdement).

## Mesure d'impact GEO

Mesure expérimentale, sans méthode standard à ce jour. Approche proposée :

1. Lister 20 requêtes types posées à un assistant IA par un prospect (architecte, MOA, candidat).
2. Une fois par mois, poser ces requêtes à ChatGPT, Perplexity, Claude.
3. Mesurer la fréquence à laquelle FT2E est cité, le type de citation (lien direct, mention textuelle, paraphrase), et la justesse des informations restituées.
4. Documenter dans `docs/audits/geo-MM-YYYY.md`.
