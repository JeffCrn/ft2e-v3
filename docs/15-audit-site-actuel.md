# 15 · Audit du site actuel `ft2e.myportfolio.com`

> Reprise fidèle du tableau d'audit de la **proposition stratégique de mai 2026** (section 02, page 5). Ces sept axes constituent le **socle justificatif** de chaque choix opposé dans le nouveau site. À chaque fois que Claude Code se demande pourquoi telle décision plutôt qu'une autre, la réponse est probablement ici.

## Synthèse en sept axes (PDF p. 5)

| Axe | Constat | Impact business | Réponse de la refonte |
|---|---|---|---|
| **Plateforme** | Adobe Portfolio est un outil pensé pour des artistes et photographes. Sous-domaine `ft2e.myportfolio.com`, personnalisation limitée, performance moyenne, pas d'accès au code. | Crédibilité B2B affaiblie. Aucun levier SEO local. Image décorrélée du sérieux d'un BET technique. | **Astro statique + OVHcloud + domaine propre `ft2e.fr`**. Accès complet au code et au SEO. |
| **Architecture** | Deux menus identiques empilés. La page « Qui nous sommes » est une simple ancre vide qui redirige vers présentation et actu. Hiérarchie peu lisible. | Perte de visiteurs sur la première navigation. Impression d'un site provisoire. | **Sitemap à 8 pages** clairement séparées, navigation plate, pas de doublon, pas d'ancre vide. |
| **Identité** | Logo en deux blocs PNG, pas de charte graphique cohérente, typographie générique imposée par la plateforme, pas de codes visuels propres au métier d'ingénierie. | Faible mémorisation de marque. Indifférenciation avec d'autres BET de la région. | **Design system Apple-style** : palette binaire noir/gris clair avec accent Apple Blue unique, Inter Variable, navigation glass, CTA pill, rythme cinématique (sections alternées noir/blanc/gris). |
| **Contenu** | Pages références = listes verticales d'images suivies de quelques lignes (MOA, architecte, année). Pas de mise en récit, pas de chiffres énergétiques, pas d'enseignements. | Le savoir-faire est sous-vendu. Les architectes prescripteurs ne trouvent pas la matière à se convaincre. | **Gabarit fiche projet** structuré : en-tête, fiche technique (10 champs), récit (enjeu/solution/particularités/résultat), galerie, projets similaires. |
| **SEO / GEO** | Méta description identique sur toutes les pages, pas de schema LocalBusiness, alt-text vides, pas de balisage technique, pas de connexion Google Business Profile. | Trafic organique très limité. Faible visibilité auprès des architectes hors réseau direct et des candidats ingénieurs. | **5 leviers** : JSON-LD `LocalBusiness`, cocon sémantique, géolocalisation sémantique, GBP nettoyé, réseau de liens entrants. Métadonnées uniques par page. |
| **Conversion** | Formulaire de contact à trois champs (nom, email, message). Aucune piste de qualification, pas de CTA différenciés selon le profil (architecte, MOA, candidat). | Toute demande entrante doit être requalifiée à la main. Pas de capture de leads froids. | **Formulaire à branches** : architecte / MOA / candidat / autre, avec questions spécifiques selon la branche. CTA différenciés dans le site. |
| **Mobile / perfs** | Adobe Portfolio rend correctement sur mobile mais sans optimisation poussée. Pas d'analytics propres. Aucune mesure de comportement. | Pilotage à l'aveugle. Aucun apprentissage continu sur ce qui fonctionne. | **Astro static + AVIF/WebP + tokens perf budget** (LCP < 1.8s mobile). **Plausible Analytics** RGPD-friendly, tableau de bord clair. |

## Constat structurant (PDF p. 6)

### Ce que le site actuel fait bien

Pour être complet, le site actuel n'est pas dépourvu de qualités. Il rend visible un volume substantiel de réalisations (logements, tertiaire, santé, sport), il liste l'équipe avec ses fonctions, et il est techniquement opérationnel. Pour un site mis en place avec des moyens limités, il a tenu sa promesse pendant plusieurs années.

> **« La refonte s'inscrit dans la continuité de ce socle, pas dans sa contestation. »** (PDF p. 6)

Cette phrase est l'**acte de diplomatie** central du projet. Elle doit transparaître dans la voix éditoriale du nouveau site : on ne renie pas le travail passé de FT2E sur son site, on lui donne enfin un cadre à la hauteur.

### Un site sous-dimensionné par rapport à l'entreprise

Le site actuel donne l'image d'une jeune structure en train de se chercher. La réalité de FT2E est inverse :

- **Dix-sept ans d'existence** (création en 2008).
- **Une équipe pluridisciplinaire de sept personnes** couvrant toute la chaîne technique du bâtiment.
- **Un carnet d'adresses dense** (voir `docs/16-ecosysteme-clients.md`).
- **Une présence forte** sur l'ensemble de la Charente-Maritime et au-delà.

> **« La refonte vise un seul objectif : que le site internet rende justice à la maturité réelle, à la profondeur d'expertise et à l'ancrage territorial du cabinet. »** (PDF p. 6)

C'est la **boussole** du projet. Toute décision (de l'architecture aux microcopies) doit être testable contre ce critère : *« cela aligne-t-il le digital sur ce que FT2E est devenue ? »*

## Trois conséquences directes (PDF p. 6)

Ces trois conséquences justifient seules la démarche. Tout le reste — design, performance, GEO — est de l'ordre du moyen.

1. **Crédibilité auprès des architectes prescripteurs** — un site qui parle leur langue (typologies, performances, BIM) crée la condition d'une prescription spontanée.
2. **Visibilité auprès des MOA institutionnels** — un site qui valorise les références publiques (OPH, communes, ports) facilite la requalification dans les listes restreintes.
3. **Attractivité auprès des candidats** — un site qui montre la culture d'équipe et la nature des projets capte les ingénieurs en phase de mobilité.

## Ce que Claude Code retient pour la liminaire

Quand un arbitrage est à faire, hiérarchie de priorité :

1. **Continuité diplomatique** : le nouveau site ne se moque pas de l'ancien. Pas d'ironie. Pas de « enfin un vrai site ».
2. **Densité maîtrisée** > volume brut : mieux vaut 8 fiches projets racontées avec soin que 30 listées plates.
3. **Trois audiences** simultanées : tout choix de design ou de microcopie doit pouvoir tenir devant l'architecte, le MOA, le candidat.
4. **Sérieux d'un BET technique** : sobre, technique, chaleureux. Jamais agence créative.
