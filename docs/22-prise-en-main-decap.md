# 22 · Prise en main du CMS par FT2E

> **À qui s'adresse ce document.** À l'équipe FT2E qui va rédiger sur le site, pas à qui l'a construit. La configuration technique du CMS est décrite ailleurs (`docs/08-configuration-decap.md`) ; ce document-ci explique **comment s'en servir**.
>
> Le CMS s'appelle **Decap**. Il n'a pas de base de données : chaque publication écrit un fichier dans le dépôt du site, et le site se reconstruit tout seul. C'est ce qui explique le délai d'une à deux minutes entre « Publier » et l'apparition en ligne — et c'est aussi ce qui fait que rien n'est jamais perdu, chaque version étant conservée.

---

## 0. ⚠ Prérequis bloquant — à faire AVANT toute prise en main

**En l'état, la connexion au CMS échoue.** Mesuré sur le déploiement le 2026-08-16 :

| Ce qui marche | Ce qui ne marche pas |
|---|---|
| `https://ft2e-v3.vercel.app/admin/` répond `200`, l'interface s'affiche | Le bouton **Se connecter** appelle `/api/auth`, qui répond **`HTTP 500`** |
| `admin/config.yml` est à jour et correct | Message exact : « Configuration OAuth manquante : definir `OAUTH_GITHUB_CLIENT_ID` dans les variables d'environnement Vercel. » |

**Rien n'est en cause dans le site.** Le code d'authentification (`api/auth.js`, `api/callback.js`) est en place et juste ; ce qui manque vit **hors du dépôt**, dans deux consoles d'administration. Trois gestes, dans cet ordre :

1. **GitHub → Settings → Developer settings → OAuth Apps** — sur l'application utilisée par le site, régler l'*Authorization callback URL* sur exactement :
   `https://ft2e-v3.vercel.app/api/callback`
2. **Vercel → projet `ft2e-v3` → Settings → Environment Variables** — ajouter, sur l'environnement *Production* :
   - `OAUTH_GITHUB_CLIENT_ID` — le *Client ID* de l'OAuth App ;
   - `OAUTH_GITHUB_CLIENT_SECRET` — un *Client secret* généré sur cette même App.
3. **Redéployer** (les variables d'environnement ne sont lues qu'au déploiement).

**Contrôle, en une commande** — doit cesser de répondre `500` :

```bash
curl -s -o /dev/null -w "%{http_code}\n" "https://ft2e-v3.vercel.app/api/auth?provider=github"
```

⚠ **À refaire le jour du changement de domaine.** La callback contient l'adresse du site : le jour où il passe sur `ft2e.fr`, elle devient `https://ft2e.fr/api/callback`, faute de quoi la connexion cesse de fonctionner du jour au lendemain.

> Cet avertissement figurait en commentaire dans `public/admin/config.yml` depuis le 2026-08-10. Un commentaire n'échoue jamais : il a traversé six sessions de travail sans être exécuté. C'est pour cela qu'il est ici, avec sa commande de contrôle.

---

## 1. Se connecter

1. Aller sur **`https://ft2e-v3.vercel.app/admin/`**.
2. Cliquer **Se connecter**. Une fenêtre GitHub s'ouvre.
3. Autoriser l'application — **une seule fois par personne et par navigateur**.
4. Les cinq collections apparaissent dans la colonne de gauche.

**Qui peut se connecter ?** Toute personne disposant d'un accès en écriture au dépôt GitHub `JeffCrn/ft2e-v3`. Ajouter un rédacteur, c'est lui donner cet accès — il n'y a pas de gestion de comptes séparée dans le CMS.

---

## 2. Les cinq collections, et laquelle toucher

| Collection | Ce qu'elle contient | Fréquence attendue |
|---|---|---|
| **Actualités** | Les articles. Une seule pour l'instant. | **C'est par là qu'il faut commencer.** |
| **Équipe** | Les sept profils. | Rare — arrivée, départ, changement de fonction. |
| **Projets / Références** | Les 23 fiches d'affaires. | À chaque nouvelle affaire publiable. ⚠ Voir § 5. |
| **Expertises** | Les quatre métiers. | Très rare — ce sont des pages de fond. |
| **Secteurs** | Les sept secteurs d'activité. | Très rare, même raison. |

---

## 3. Modifier un texte existant — le geste de base

1. Ouvrir la collection, cliquer l'entrée.
2. Modifier le champ. L'**aperçu de droite se met à jour en direct**.
3. **Publier** (bouton en haut).
4. Attendre **1 à 2 minutes**, puis recharger la page publique.

Si la page publique n'a pas changé après trois minutes, c'est que la reconstruction a échoué — voir § 7.

---

## 4. Écrire une actualité

**Nouveau → Actualités.** Les champs, dans l'ordre où ils se remplissent :

| Champ | Ce qu'on y met |
|---|---|
| **Titre** | 50 à 70 signes, factuel. Pas d'accroche publicitaire. |
| **Chapô** | Deux à trois phrases qui annoncent l'article sans le résumer entièrement. |
| **Date** | La date de publication. Elle s'affiche en clair sur le site. |
| **Auteur** | Facultatif. « L'équipe FT2E » par défaut. |
| **Catégories** | Liste fermée : choisir, ne pas inventer. |
| **Corps** | Le texte. Sous-titres avec `##`, jamais `#`. |

**La voix.** Sobre, technique, chaleureuse. Pas de superlatif, pas de point d'exclamation, pas d'emoji, pas d'anglicisme évitable (« mémoire technique » plutôt que *pitch*). Les chiffres et les sigles se citent juste : `RE2020` et non `RE 2020`, `m²` et non `m2`.

---

## 5. Créer une fiche de référence — ⚠ ce qu'il faut savoir avant

Une fiche d'affaire n'est **pas** un article. Deux règles la gouvernent, et le CMS ne peut pas les deviner à votre place.

### a. Le numéro d'affaire se relève, il ne se fabrique pas

Le champ **Référence** porte le numéro FT2E en graphie `NN-NNN` — `22-033`, par exemple. Il se relève **sur une pièce du dossier** (cartouche de plan, page de garde) et jamais sur le nom d'un répertoire.

Le champ **Année** est le millésime que ce numéro encode — le `22` de `22-033`, l'année d'**ouverture**. Le site refuse de se reconstruire si les deux se contredisent. L'année de **réception**, elle, va dans **Année de livraison**, et seulement une fois la réception prononcée sur pièce.

### b. Le visuel ne se téléverse pas

**Il n'y a pas de champ « image » sur une fiche projet, et c'est voulu.** Chaque fiche est illustrée par une **planche** — un schéma de principe dessiné à partir de la matière technique de l'affaire. Une planche se compose hors du CMS, en cinq fichiers, par une procédure décrite dans `docs/superpowers/specs/2026-08-12-planches-references-protocole.md`.

Le champ **Planche** attend simplement le chemin du dessin, en graphie stricte :
`/images/projets/<nom-de-la-fiche>/planche.svg`

⚠ **Créer une fiche sans que sa planche existe fait échouer la publication du site entier.** Concrètement : demander la planche d'abord, créer la fiche ensuite.

### c. Les listes fermées

**Secteur**, **Typologie**, **Missions FT2E**, **Statut** sont des menus déroulants. Choisir dans la liste. Une valeur saisie hors liste — même à une apostrophe près — fait échouer la publication.

---

## 6. Remplacer une photographie d'équipe

Champ **Photo** de la collection Équipe : le téléversement se fait depuis le CMS, qui dépose le fichier au bon endroit tout seul.

**Ne jamais déposer une photographie à la main dans `public/images/equipe/`** : elle n'apparaîtrait pas. Le site optimise ses images depuis un autre répertoire, et le CMS y est déjà réglé.

Le champ **Texte alternatif** est obligatoire : c'est la description lue par les lecteurs d'écran. « Portrait de Mathieu » suffit ; une photo sans description est un défaut d'accessibilité.

---

## 7. Quand quelque chose ne va pas

| Symptôme | Cause la plus probable | Geste |
|---|---|---|
| **Se connecter** ne fait rien, ou affiche une erreur | La configuration OAuth du § 0 | Lancer la commande de contrôle du § 0 |
| La modification n'apparaît pas après 3 min | La reconstruction a échoué, souvent une valeur hors liste ou une planche absente | Vérifier les champs du § 5.c, puis prévenir |
| Un champ refuse d'être vidé | Il est obligatoire | Ne pas contourner : le champ porte quelque chose que le site affiche |
| L'aperçu est différent du site | L'aperçu ne rejoue pas toute la mise en page | Se fier au site publié |

**Rien n'est jamais perdu.** Chaque publication est une version enregistrée : une modification malheureuse se défait, y compris plusieurs jours après.

---

## 8. Ce qui ne se fait pas depuis le CMS

- **Les planches** — voir § 5.b.
- **Les pages de fond** (accueil, société, contact, mentions légales) : leur texte vit dans le code, parce que leur mise en page est dessinée sur mesure. Une modification passe par une demande.
- **La structure** : ajouter un champ, un secteur, une catégorie. Ce sont des changements de schéma, qui se répercutent simultanément dans le code et dans le CMS.
- **L'ouverture aux moteurs de recherche** : elle est verrouillée volontairement tant que le site est en validation, par trois sécurités indépendantes. Procédure de levée : `docs/19-migration-production.md`.

---

## 9. Ce qui reste à faire côté FT2E

- [ ] **Débloquer la connexion** (§ 0) — préalable à tout le reste.
- [ ] Désigner **qui rédige**, et lui ouvrir l'accès au dépôt.
- [ ] Faire une **première publication d'essai** sur l'actualité existante, avant la formation, pour vérifier la chaîne de bout en bout.
- [ ] Fournir les **photographies** (équipe et secteurs) : sept portraits, une vue collective, sept visuels de secteurs. Les images actuelles sont des démonstrations.
- [ ] Relever les **dates de réception** des affaires : quatorze fiches n'en portent pas, et le site annonce une livraison par défaut. ⚠ Ce n'est pas indéfiniment tenable — un garde-fou fera **échouer la reconstruction au 1ᵉʳ janvier 2027**.
