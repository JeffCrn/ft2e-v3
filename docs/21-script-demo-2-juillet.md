# 21 · Script de démonstration — présentation FT2E du 2 juillet 2026

> Déroulé pas-à-pas pour présenter le site **et** le back-office en direct, sur l'URL live `https://ft2e-v3.vercel.app`. Aucune machine locale requise. Durée cible : 15–20 min.

## A. Pré-vol (la veille + 15 min avant)

- [ ] Le site répond : ouvrir `https://ft2e-v3.vercel.app/` (navigation privée pour éviter le cache).
- [ ] La connexion CMS fonctionne : `https://ft2e-v3.vercel.app/admin/` → **Se connecter** → autoriser GitHub → les collections s'affichent. **Faire ce test AVANT la réunion** (la 1ʳᵉ autorisation GitHub n'est demandée qu'une fois).
- [ ] Être **déjà connecté à GitHub** dans le navigateur de présentation (évite la saisie de mot de passe devant le client).
- [ ] Onglets prêts : 1) accueil, 2) `/admin/`. Zoom navigateur ~100–110 %.
- [ ] **Plan B** : si le wifi est mauvais, avoir une **capture vidéo** (screencast) du parcours CMS enregistrée la veille.
- [ ] Ne PAS toucher au blocage d'indexation (le site doit rester `noindex` — ne pas le mentionner comme un problème, c'est volontaire).

## B. Tour du site public (~7 min)

Fil conducteur : « sobre, technique, chaleureux ». Laisser parler le design.

1. **Accueil** — hero, chiffres clés (17 ans, 7 collaborateurs), rythme des sections, animations au scroll. Souligner : performance, esthétique Apple-style, 100 % responsive.
2. **Société** puis **Équipe** — « 7 profils, une responsabilité partagée », traitement uniforme. *(Mentionner que les portraits définitifs seront faits par un photographe pro en production.)*
3. **Expertises** — une page pilier (ex. CVC ou Coordination SSI), montrer la FAQ et le maillage.
4. **Références** — la grille filtrable, puis ouvrir une fiche projet (ex. **Maison Pierre Loti**). Expliquer le gabarit Enjeu → Solution → Particularités → Résultat.
5. **Contact** — coordonnées réelles (35 Rue Nicolas Denys de Fronsac, 05 46 27 85 93), formulaire (préciser : branchement e-mail prévu en production).

> Rappeler une fois, sobrement : les fiches marquées **[DÉMO]** et les visuels sont des **exemples** ; le reportage et les contenus réels arrivent en phase de production.

## C. Démonstration du back-office en direct (~7 min) — le moment clé

1. Ouvrir **`https://ft2e-v3.vercel.app/admin/`** → **Se connecter**.
2. Montrer les **5 collections** (Projets, Actualités, Équipe, Expertises, Secteurs) — « tout le contenu du site se gère ici, sans toucher au code ».
3. Ouvrir **Projets / Références** → cliquer une fiche (ex. Maison Pierre Loti) → montrer le **formulaire structuré** (titre, secteur, mission, image, récit) et l'**aperçu en direct**.
4. **Édition live** (effet « waouh »), au choix :
   - Modifier un petit champ (ex. une phrase du récit) → **Publier**.
   - Expliquer : « ça enregistre dans le dépôt et **republie le site automatiquement** ». Recharger l'onglet public ~1–2 min après pour montrer la mise à jour.
   - *Prudence démo* : faire une modification anodine et réversible ; on pourra la retirer après.
5. Montrer **Équipe** et **Actualités** → « vous ajoutez un membre ou une actualité en quelques champs ».

**Phrase de clôture** : « L'interface est prête. La mise en production définitive — hébergement souverain, vos contenus réels, vos photos — est une étape de configuration que nous calons ensemble. »

## D. Questions probables & réponses

| Question | Réponse |
|---|---|
| « C'est hébergé où ? » | Démo sur Vercel ; **cible : hébergement souverain français (OVH)** pour la production. |
| « Qui peut modifier le contenu ? » | Toute personne de FT2E à qui on donne l'accès ; connexion sécurisée. En production on choisit le mode d'accès le plus simple pour vous. |
| « Les photos / chiffres sont-ils définitifs ? » | Non, ce sont des exemples [DÉMO] ; reportage pro et données validées en production. |
| « Quand est-ce en ligne sur ft2e.fr ? » | Dès votre feu vert : bascule du domaine, déblocage de l'indexation, contenus réels. Procédure déjà documentée. |
| « C'est référencé sur Google ? » | Volontairement **non** pour l'instant (phase de validation) ; activé à la mise en production. |

## E. À NE PAS faire en direct

- Ne pas supprimer de fiche ni de membre pendant la démo.
- Ne pas modifier `config.yml`, ni les réglages techniques.
- Ne pas promettre de date de mise en ligne sans validation interne.

## F. Après la réunion

- Si une modification de test a été publiée pendant la démo : la **réverter** (un commit, ou ré-éditer dans `/admin`).
- Noter les retours FT2E (contenus réels à fournir, infos légales : forme juridique, SIREN, directeur de publication).
- Point en suspens : remontée de l'**authentification définitive** au moment de la bascule OVH (à planifier avec EuporIA).
