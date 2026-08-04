# 04 · Spécifications des pages

Chacune des 8 pages du sitemap V1 est spécifiée ici de manière opérationnelle : objectif, blocs, contenus, métadonnées SEO, état actuel.

---

## Page 1 — **Accueil** (`/`)

### Objectif
Première impression. Donner en moins de 30 secondes une lecture juste de FT2E : identité, savoir-faire, références récentes, contact.

### Sitemap interne (9 blocs, de haut en bas)

1. **Hero**
   - Image forte de chantier emblématique (recommandation : Maison Pierre Loti ou un grutage CTA).
   - Titre éditorial sur 2 lignes max, ex. : *« L'ingénierie technique du bâtiment du Centre-Ouest atlantique. »*
   - Sous-titre : positionnement court (~ 30 mots).
   - CTA principal → `/contact`.
   - CTA secondaire → `/references`.
2. **Chiffres clés** — 4 chiffres animés au scroll : *Années d'expertise* / *Ingénieurs associés* / *Projets livrés* / *Logements conçus*. **Valeurs à fournir par FT2E.**
3. **Six expertises en cartes** — Audit · Thermique · CVC · Électricité · SSI · Exécution-BIM. Chaque carte : icône, titre, accroche 15 mots, lien.
4. **Trois secteurs phares** — Logement, Tertiaire institutionnel, Santé. Visuel + chiffre + lien.
5. **Références récentes** — 4 projets en grille (depuis `projets` avec `en_avant: true`, triés par `annee` desc.).
6. **L'équipe** — Photo collective, accroche humaine sur la pluridisciplinarité du bureau, lien vers `/equipe`.
7. **Bandeau partenaires** — Logos discrets des MOA et architectes (avec accord écrit obligatoire, voir `docs/13-glossaire-bet.md` § « Droits image »).
8. **CTA final** — « Un projet en tête ? Parlons-en. » + bouton vers `/contact`.
9. **Footer riche** — Coordonnées, plan, réseaux, mentions, sitemap (composant global).

### Métadonnées SEO

- `title` : `FT2E — Bureau d'études techniques, La Rochelle` (47 c.)
- `description` : `Bureau d'études fluides, thermique, électricité, SSI, BIM à La Rochelle. Au service des architectes et MOA depuis 2008.` (137 c.)
- `og_image` : `/og/accueil.jpg` (à produire — 1200×630)
- JSON-LD : `ProfessionalService` complet + `WebSite`.

### Critères de blocage
- Hero LCP < 1.5 s mobile.
- Image hero servie en AVIF, dimensions exactes, `loading="eager"`, `fetchpriority="high"`.

---

## Page 2 — **Société** (`/societe`)

### Objectif
Crédibilité et profondeur. Raconter FT2E sans flatterie : histoire, pluridisciplinarité, valeurs, démarche RGE, engagements.

### Blocs

1. **Hero court** — Photo bureau ou équipe.
2. **Histoire depuis 2008** — Récit synthétique (3–4 paragraphes), ancrage rochelais et pluridisciplinarité.
3. **Valeurs** — Liste illustrée des 4 piliers (Proximité, Expertise pluridisciplinaire, Engagement énergétique, Cohérence chantier).
4. **Approche & méthodologie** — Comment FT2E travaille : du DCE au DOE.
5. **Engagements environnementaux & qualité** — RT2012, RE2020, Effinergie+, NF Habitat HQE, démarche RGE, qualifications spécifiques.
6. **CTA** vers `/expertises` et `/contact`.

### Métadonnées
- `title` : `La société — FT2E` 
- `description` : factuelle, ≤ 160 c.
- JSON-LD : `AboutPage` + `Organization` (référence au `ProfessionalService`).

---

## Page 3 — **Équipe** (`/equipe`)

### Objectif
Visage humain. Présenter les 7 membres de l'équipe de manière uniforme (5 associés + 2 collaboratrices). Aucune distinction individuelle — le bureau est porté collectivement.

### Blocs

1. **Hero éditorial** — « Sept profils, une responsabilité partagée. »
2. **Photo collective** + texte sur la pluridisciplinarité.
3. **Grille de profils** — un par membre de la collection `equipe`, triés par `ordre`. Chaque carte : photo (ronde), prénom, rôle (Apple Blue uppercase), métier. Traitement visuel identique pour tous les profils.
4. **Bloc recrutement** — « Vous voulez rejoindre l'équipe ? » + CTA candidature + email RH.

### Métadonnées
- `title` : `L'équipe — FT2E` 
- JSON-LD : page liste de `Person`.

---

## Page 4 — **Expertises** (`/expertises`)

### Objectif
Vitrine de l'expertise pluridisciplinaire. Une page index + 6 sous-pages dédiées.

### Page index (`/expertises`)

1. Hero éditorial (composant `HeroPage`).
2. Grille des 6 expertises (mêmes cartes qu'en accueil mais avec accroche élargie).
3. CTA contact (« Quelle expertise pour votre projet ? »).

### Sous-pages expertise (`/expertises/[slug]`)

Pour chaque expertise (6 sous-pages) :

1. Hero — titre + accroche.
2. **Enjeu** — paragraphe libre.
3. **Livrables** — liste à puces.
4. **Méthodologie** — étapes-clés.
5. **Exemples chiffrés** — 2–3 chiffres ou cas réels (depuis `projets` filtrés par mission).
6. **FAQ** (optionnelle mais souhaitable pour GEO).
7. **3 projets représentatifs** (auto-sélection depuis `projets` où `mission_ft2e` contient le service).
8. CTA contact.

### Métadonnées (par service)
- `title` : `<Service> — FT2E`
- JSON-LD : `Service` (cf. `.claude/rules/seo-geo.md`).

---

## Page 5 — **Références** (`/references`)

### Objectif
Démontrer le volume et la diversité du portefeuille. Filtrabilité indispensable.

### Page liste (`/references`)

Filtres prévus par le PDF (p. 9) : **« Vue filtrable : par secteur (logement, tertiaire, santé, sportif, industriel) · par MOA · par année · par performance énergétique · par taille »**.

- **Filtres multiples** (côté client, *island* dédiée Preact) :
  - **Secteur** (chips multi-sélection : Logement · Tertiaire · Santé · Sport · Industriel · Patrimoine)
  - **MOA** (autocomplete sur les valeurs présentes dans la collection)
  - **Année** (slider d'intervalle ou range select 2008 → année courante)
  - **Performance énergétique** (chips multi-sélection : RT2012, RE2020, Effinergie+, NF Habitat HQE, BBC Rénovation, autre)
  - **Taille** (slider sur `surface_m2` : < 1 000 m², 1 000–5 000 m², > 5 000 m², ou intervalle libre)
- **Grille de cartes projet** — image, titre, secteur (capsule), MOA, année.
- **Tri** — par année (défaut desc.), par titre.
- Pagination ou *infinite scroll* si > 30 projets.
- **Compteur de résultats** au-dessus de la grille : *« 12 projets correspondent à vos critères »*.
- **Réinitialisation** des filtres en un clic.

**Typologie** (Neuf / Réhabilitation / Extension / Études d'exécution) est affichée sur la **fiche projet** mais **pas** dans les filtres de la liste — conformément au PDF.

### Fiche projet (`/references/[slug]`)

Gabarit standard de la fiche :

1. **En-tête** — image principale en pleine largeur, nom du projet, capsule secteur + typologie.
2. **Fiche technique** — MOA, architecte, lieu, surface, année, performance, mission FT2E.
3. **Récit projet** — corps Markdown (3–6 paragraphes : enjeu / solution / particularités / résultat).
4. **Galerie** — images AVIF/WebP, lazy-loaded, accessibles (alt obligatoire).
5. **Projets similaires** — 3 suggestions automatiques selon secteur et typologie.
6. CTA contact.

### Métadonnées (par projet)
- `title` : `<Titre projet> — Référence FT2E`
- `og_image` : `image_principale` du projet (1200×630 dérivée).
- JSON-LD : `CreativeWork` + `BreadcrumbList`.

---

## Page 6 — **Actualité** (`/actualites`)

### Objectif
Site vivant. Cadence cible : ≥ 1 publication par mois.

### Page liste (`/actualites`)

- Filtre par catégorie (`Chantier en cours`, `Livraison`, `Événement`, `Article technique`, `Vie du cabinet`).
- Cartes triées par date desc.
- Pagination 12 par page.

### Page article (`/actualites/[slug]`)

- En-tête : catégorie, date, titre, chapô, auteur.
- Image d'illustration.
- Corps Markdown.
- Articles liés (3 suggestions par catégorie commune).
- CTA contact contextuel.

### Métadonnées
- JSON-LD : `Article` ou `BlogPosting`.

---

## Page 7 — **Contact** (`/contact`)

### Objectif
Captation qualifiée. Pas un simple formulaire, mais un parcours à branches.

### Blocs

1. **Hero court** — « Parlons de votre projet. »
2. **Coordonnées & carte** — Adresse, téléphone, email, plages de disponibilité, carte Leaflet auto-hébergée (pas Google Maps RGPD).
3. **Formulaire à branches** :
   - Question 1 : « Vous êtes ? » → Architecte / Maître d'ouvrage / Candidat / Autre.
   - Question 2 (selon branche) : nature du projet (architecte/MOA) ou poste recherché (candidat).
   - Coordonnées (nom, email, téléphone facultatif).
   - Message libre.
   - RGPD : consentement explicite via case à cocher non pré-cochée.
4. **Réponse attendue** : « Réponse sous 48 h ouvrées. »

### Backend formulaire
- **Formspree** ou **n8n auto-hébergé** (à arbitrer en cadrage initial).
- Anti-spam : honeypot + rate-limit.
- Accusé de réception automatique vers le visiteur.

### Métadonnées
- `title` : `Contact — FT2E` 
- JSON-LD : `ContactPage`.

---

## Page 8 — **Accessibilité** (`/accessibilite`)

### Objectif
Conformité légale (déclaration d'accessibilité obligatoire pour service public, fortement recommandée sinon).

### Blocs

1. Déclaration de conformité (niveau atteint, date de l'audit).
2. État des contenus non accessibles (s'il y en a).
3. Voies de recours.
4. Contact accessibilité.

Modèle à reprendre depuis le générateur officiel : `https://accessibilite.numerique.gouv.fr/`.

---

## Pages utilitaires (sans menu)

- `/mentions-legales` — éditeur, hébergeur, propriété intellectuelle.
- `/politique-confidentialite` — RGPD, cookies (Plausible sans cookie donc bandeau minimal).
- `/sitemap.xml` — généré auto.
- `/admin` — interface Decap CMS (avec `noindex`).
