# 21 · Script de démonstration — présentation du site à FT2E

> Déroulé pas-à-pas pour présenter le site **et** le back-office en direct, sur l'URL live `https://ft2e-v3.vercel.app`. Aucune machine locale requise. Durée cible : 15–20 min.
>
> ⚠ **Le nom de fichier est historique.** Il porte la date d'une réunion du 2 juillet 2026 ; le script, lui, a été **entièrement refait le 2026-08-16** et vaut pour la présentation à venir. Il est référencé sous ce nom dans `CLAUDE.md` — le renommer casserait le renvoi sans rien apporter.
>
> **Ce qui a changé depuis la version précédente, et pourquoi il fallait le changer** : le script faisait ouvrir en direct une fiche **supprimée du site** depuis le 2026-08-08 (« Maison Pierre Loti », l'une des huit fiches de démonstration retirées à la demande de FT2E), décrivait le design comme « Apple-style » alors que la charte v3 l'a remplacé, annonçait un choix d'hébergement que le dépôt ne porte pas, et ne disait pas un mot du dispositif visuel des fiches — les planches — qui est pourtant le principal travail des trois derniers mois.

## A. Pré-vol (la veille + 15 min avant)

- [ ] Le site répond : ouvrir `https://ft2e-v3.vercel.app/` en navigation privée (évite le cache).
- [ ] **Le déploiement porte bien le dernier code.** Ne pas se fier à un délai d'attente : vérifier un marqueur du build.
      `curl -s https://ft2e-v3.vercel.app/equipe/ | grep -o 'type="image/avif"' | wc -l` doit rendre **8**.
      (Le site est resté trois sessions en arrière sans que rien ne le signale, en août 2026.)
- [ ] 🔴 **BLOQUANT AU 2026-08-16 — la connexion au CMS ÉCHOUE.** `/admin/` répond bien `200` et l'interface s'affiche, mais **Se connecter** appelle `/api/auth`, qui rend `HTTP 500` : « Configuration OAuth manquante ». **La section C ne peut pas avoir lieu tant que ce n'est pas levé.**
      Contrôle, doit cesser de rendre `500` :
      `curl -s -o /dev/null -w "%{http_code}\n" "https://ft2e-v3.vercel.app/api/auth?provider=github"`
      Correction en trois gestes, **hors du dépôt** (callback GitHub + deux variables Vercel + redéploiement) : `docs/22-prise-en-main-decap.md` § 0.
      **Si ce n'est pas levé le jour J** : ne pas ouvrir `/admin/` en direct. Passer par la capture vidéo du plan B, et annoncer franchement « le raccordement du compte est une étape de configuration en cours » — ce qui est exact. Ouvrir l'interface pour buter sur une erreur coûte plus que de ne pas l'ouvrir.
- [ ] Une fois levé : `https://ft2e-v3.vercel.app/admin/` → **Se connecter** → autoriser GitHub → les cinq collections s'affichent. **Faire ce test AVANT la réunion** : la première autorisation GitHub n'est demandée qu'une fois, et on ne veut pas la découvrir devant le client.
- [ ] Être **déjà connecté à GitHub** dans le navigateur de présentation.
- [ ] Onglets prêts : 1) accueil, 2) une fiche de référence, 3) `/admin/`. Zoom navigateur 100 %.
- [ ] **Plan B** : si le réseau est mauvais, avoir une **capture vidéo** du parcours CMS enregistrée la veille.
- [ ] Ne PAS toucher au blocage d'indexation. Le site est volontairement `noindex` — voir la question type en § D, c'est un argument, pas une excuse.

## B. Tour du site public (~7 min)

Fil conducteur : **« sobre, technique, chaleureux »**. Le design se commente peu ; le laisser agir et parler du contenu.

1. **Accueil.** La planche de page posée sur son fond, la trame, le monogramme.
   Le **relevé** : `17` ans, `7` collaborateurs, `+1 686` logements étudiés, `+98` projets tertiaires — un seul chiffre en encre pleine, les autres en retrait. C'est une règle de la charte, pas un hasard de mise en page : la page défend un chiffre à la fois.
   Sous le titre, l'**appui de la fiche mise en avant** : un dessin FT2E, pas une photo.

2. **Société**, puis **Équipe.** Sept profils, traitement strictement identique pour tous — « une responsabilité portée collectivement ». *(Préciser : les portraits actuels sont des images de démonstration ; le reportage photographique est prévu en phase de production.)*

3. **Expertises.** Ouvrir une page pilier (CVC, ou Coordination SSI). Montrer le maillage interne : chaque expertise renvoie vers des fiches réelles.

4. **Références — le cœur de la démonstration.**
   - La **grille filtrable** : 23 fiches réelles, toutes sur une page. Le filtre par secteur réduit la grille, il ne pagine pas.
   - Ouvrir une fiche. **Suggestion : « Néréa, 90 logements » (Aytré)** — sa planche est l'une des plus riches du corpus. La crèche de l'Oranger (Périgny) est la fiche mise en avant sur l'accueil et fait un enchaînement naturel depuis le point 1.
   - **Le point à faire passer, et le seul qui demande une phrase préparée** : chaque fiche est illustrée par un **schéma de principe dessiné par FT2E à partir de sa propre matière technique** — topologie, flux, chiffres. Vingt-trois planches, vingt-trois mécanismes différents. Aucune ne reproduit la géométrie d'un ouvrage ni le plan d'un architecte.
     *Formulation possible* : « Nous avons écarté les photos de bâtiments et les extraits de plans. Les premières appartiennent aux architectes, les seconds ne se lisent plus une fois réduits. Chaque fiche porte donc un dessin qui explique ce que FT2E a fait — et rien d'autre. »
   - Cliquer l'**agrandissement** de la planche : c'est là que le détail se lit.
   - Descendre : cartouche technique, relevé encré, récit en quatre temps (enjeu → solution → particularités → résultat), fiches similaires.

5. **Contact.** Coordonnées réelles (35 Rue Nicolas Denys de Fronsac, 05 46 27 85 93). *(Préciser : le formulaire est complet à l'écran, son branchement e-mail est une étape de mise en production.)*

6. **Si la question de la qualité technique se pose** — ou pour clore le tour :
   mesuré le 2026-08-16 sur le déploiement, en simulation mobile, sur neuf pages :
   **performance 100/100 partout**, temps d'affichage du contenu principal **1,5 à 1,8 s**, **zéro décalage de mise en page**, accessibilité **100** sur sept pages et 96–97 sur deux (une dérogation documentée sur un élément décoratif masqué aux lecteurs d'écran).

> Rappeler une fois, sobrement : les **photographies** (équipe et secteurs) sont des images de démonstration marquées `[DÉMO]` en attendant le reportage. **Les 23 fiches, elles, sont réelles** — numéro d'affaire, commune, missions, chiffres, tous relevés sur vos dossiers.
> ⚠ Ne plus dire « les fiches marquées DÉMO » : il n'y en a plus aucune. Les huit fiches de démonstration ont été supprimées le 2026-08-08.

## C. Démonstration du back-office en direct (~7 min) — le moment clé

1. Ouvrir **`https://ft2e-v3.vercel.app/admin/`** → **Se connecter**.
2. Montrer les **cinq collections** — Projets, Actualités, Équipe, Expertises, Secteurs. « Tout le contenu du site se gère ici, sans toucher au code. »
3. Ouvrir **Projets** → une fiche → montrer le **formulaire structuré** (titre, numéro d'affaire, secteur, typologie, missions, lieu, récit) et l'**aperçu en direct**.
   ⚠ **Ne pas annoncer de champ « image »** : une fiche projet n'en a plus. Son visuel est sa planche, produite à part.
4. **Édition en direct** (l'effet à ne pas rater), au choix :
   - modifier une phrase du récit → **Publier** ;
   - expliquer : « cela enregistre dans le dépôt et **republie le site automatiquement** ». Recharger l'onglet public 1 à 2 min après.
   - *Prudence* : une modification anodine et réversible, sur un champ de prose — **jamais sur `secteur`, `typologie` ou `mission_ft2e`**, dont les valeurs sont contrôlées et dont une saisie libre ferait échouer la republication.
5. Montrer **Équipe** et **Actualités** : « vous ajoutez un membre ou une actualité en quelques champs ».

**Phrase de clôture** : « L'interface est prête et le contenu est le vôtre. Ce qui reste — vos photographies, le nom de domaine, l'ouverture aux moteurs de recherche — est une étape de configuration que nous calons ensemble. »

## D. Questions probables et réponses

| Question | Réponse |
|---|---|
| « C'est hébergé où ? » | Aujourd'hui sur Vercel, en démonstration. **Pour la production, deux options restent ouvertes et c'est à vous d'arbitrer** : garder Vercel avec le domaine `ft2e.fr`, ou migrer vers un hébergement français (OVHcloud) pour la souveraineté des données. Les deux sont documentées et chiffrées. ⚠ Ne pas annoncer OVH comme décidé — ce n'est pas tranché. |
| « Qui peut modifier le contenu ? » | Toute personne de FT2E à qui l'accès est donné ; connexion sécurisée par GitHub. Le mode d'accès définitif se choisit à la mise en production. |
| « Les photos sont-elles définitives ? » | Non. Les portraits d'équipe et les visuels de secteurs sont des images de démonstration, en attente du reportage. **Les dessins des fiches, eux, sont définitifs** — ce sont des pièces FT2E. |
| « Et les chiffres des fiches ? » | Réels, relevés sur vos dossiers d'affaires, avec le numéro d'affaire à l'appui. Ce qui a dû être tranché lors de la mise en fiche est signalé pour votre relecture. |
| « Quand est-ce en ligne sur ft2e.fr ? » | Dès votre feu vert : bascule du domaine, ouverture aux moteurs, redirections depuis l'ancien site. La procédure est écrite pas à pas. |
| « C'est référencé sur Google ? » | **Volontairement non**, pour l'instant. Tant que le site est en validation, il est fermé aux moteurs par trois verrous indépendants — pour éviter qu'une version de travail soit indexée puis reste dans les résultats. Cela s'ouvre en une manipulation, le jour de la mise en production. |
| « Pourquoi des dessins et pas des photos de chantier ? » | Deux raisons. Une photographie de bâtiment montre l'ouvrage de l'architecte, pas notre travail — et son droit d'auteur ne nous appartient pas. Un dessin de principe montre exactement ce que FT2E a conçu. |
| « Ça marche sur téléphone ? » | Oui, et les dessins aussi : chaque fiche porte **trois compositions différentes**, pas une image redimensionnée, servie selon la place disponible. |

## E. À NE PAS faire en direct

- Ne pas ouvrir « Maison Pierre Loti » ni aucune ancienne fiche de démonstration : **elles n'existent plus**.
- Ne pas décrire le design comme « Apple-style » : c'est la charte v1, remplacée. Dire « plans et profondeur », ou simplement ne pas nommer le style.
- Ne pas supprimer de fiche ni de membre pendant la démonstration.
- Ne pas modifier `config.yml` ni aucun réglage technique depuis l'interface.
- Ne pas annoncer une date de mise en ligne, ni un choix d'hébergement, sans validation interne.
- Ne pas présenter le `noindex` comme un défaut à corriger.

## F. Après la réunion

- Si une modification de test a été publiée : la **réverter** (un commit, ou ré-éditer dans `/admin`).
- Noter les retours FT2E, en particulier :
  - les **contenus réels** restant à fournir (photographies) ;
  - les **réceptions d'affaires** — quatorze fiches n'ont pas de date de réception au dossier et le site annonce une livraison par défaut. ⚠ Ce n'est pas indéfiniment tenable : un garde-fou fait **échouer le build au 1ᵉʳ janvier 2027**. C'est le bon moment pour demander les procès-verbaux ;
  - la relecture des points signalés `a_valider_ft2e` sur les planches.
- Point en suspens : l'**authentification définitive** du CMS au moment de la bascule de domaine.
