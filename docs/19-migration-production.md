# 19 · Migration vers la production sur ft2e.fr

> **Document à exécuter au moment de la mise en production.** À ne PAS exécuter avant validation explicite de FT2E.
>
> Le site est actuellement hébergé sur Vercel (`https://ft2e-v3.vercel.app`) en mode **démo client**, avec **indexation moteurs bloquée par triple sécurité** (commit `7e21628`, 2026-05-28). Ce document décrit la séquence exacte pour basculer en production sur `ft2e.fr` — y compris le revert du blocage SEO.
>
> ⚠ **L'hôte, corrigé le 2026-08-16.** Ce document nommait `ft2e-site.vercel.app` — le déploiement de la **v1**, qui n'est pas celui de ce dépôt. La confusion aurait été exécutée au pire moment : c'est ici que se règlent le domaine, les redirections 301 et le retrait du `noindex`.
>
> ⚠ Et `ft2e-site.vercel.app` **n'est pas une adresse morte** : mesuré le 2026-08-16, il répond `200` et sert encore le site v1 avec ses photographies d'ouvrages. `ft2e-v2.vercel.app` aussi. Voir § 6 bis.

## Pré-requis avant de démarrer

- [ ] FT2E a validé la version liminaire et donné le feu vert pour la mise en production.
- [ ] Le domaine `ft2e.fr` est bien enregistré (OVH ou autre registrar).
- [ ] Cible d'hébergement final décidée : **Vercel avec domaine custom** OU **migration vers OVHcloud Webhosting Pro** (`docs/09-deploiement-ovh.md`).
- [ ] Les contenus `[DÉMO]` ont été remplacés par les contenus réels OU FT2E accepte explicitement de basculer avec les contenus démo en attendant.
- [ ] Le formulaire Contact est branché (Formspree / n8n) OU FT2E accepte qu'il reste désactivé.
- [ ] Le reportage photographique professionnel est livré OU FT2E accepte de conserver temporairement les visuels démo IA.

## Décision préalable : Vercel ou OVH ?

| Choix | Pour | Contre |
|---|---|---|
| **Vercel + domaine ft2e.fr custom** | Déjà en place, déploiement continu fluide, CDN global, SSL automatique. | Hébergement hors France (US edge), dépendance à un acteur étranger. |
| **Migration vers OVHcloud Webhosting Pro** | Souveraineté française (PDF p. 28-29), conformité RGPD native. | Reconfiguration complète, perte du déploiement Vercel actuel. |

→ Si **Vercel** : exécuter §1 + §2 + §3.
→ Si **OVH** : exécuter §1 + §2 + §4. Voir `docs/09-deploiement-ovh.md` pour le détail OVH.

---

## §1 — Débloquer l'indexation (commun)

Trois fichiers à modifier dans l'ordre :

### 1.1 — `public/robots.txt`

Remplacer **tout** le contenu actuel par :

```
User-agent: *
Allow: /
Sitemap: https://ft2e.fr/sitemap-index.xml
```

Le contenu attendu après revert est déjà présent **en commentaire** dans le fichier actuel — copier-coller depuis ces lignes.

### 1.2 — `src/layouts/BaseLayout.astro`

Ligne ~21, la prop `noindex` :

```ts
// AVANT (mode démo)
noindex = true,

// APRÈS (production)
noindex = false,
```

Et retirer le commentaire « TEMPORAIRE » au-dessus de la ligne.

### 1.3 — `vercel.json`

- **Si on garde Vercel** : supprimer uniquement le bloc `headers` qui injecte `X-Robots-Tag`. Garder le fichier seulement si on y ajoute d'autres règles (sinon le supprimer entièrement).
- **Si on migre vers OVH** : supprimer le fichier `vercel.json` (inutile sur OVH).

### 1.4 — Vérifications après déploiement

```bash
# robots.txt — doit autoriser le crawl
curl https://ft2e.fr/robots.txt
# attendu : "User-agent: *" + "Allow: /" + "Sitemap: ..."

# Headers HTTP — X-Robots-Tag NE DOIT PLUS apparaître
curl -I https://ft2e.fr/ | grep -i x-robots
# attendu : aucune sortie

# HTML — meta robots NE DOIT PLUS contenir noindex
curl -s https://ft2e.fr/ | grep 'name="robots"'
# attendu : aucune sortie (le meta n'est plus injecté quand noindex=false)
```

---

## §2 — Nettoyer la configuration et la doc

### 2.1 — `astro.config.mjs`

Vérifier que `site` pointe bien sur `https://ft2e.fr` (la valeur actuelle, déjà correcte).

### 2.2 — `.env` ou variables d'environnement Vercel/OVH

Basculer `PUBLIC_MODE=liminaire` → `PUBLIC_MODE=production`. Effet : disparition automatique des `BadgeDemo` ([src/components/primitives/BadgeDemo.astro:7](src/components/primitives/BadgeDemo.astro#L7)) et activation du bouton de soumission du formulaire Contact ([src/components/blocs/FormulaireContact.astro:2](src/components/blocs/FormulaireContact.astro#L2)).

### 2.3 — `CLAUDE.md`

Section « Ce qui n'est pas en place » : retirer les mentions de mode démo et d'indexation bloquée. Section « Règles non négociables » : retirer la règle qui force le `noindex` global.

### 2.4 — `README.md`

Retirer les mentions de mode démo / indexation bloquée dans la section « Statut » ou « Pour passer en production ».

---

## §3 — Branche : on reste sur Vercel

### 3.1 — Ajouter le domaine

Dashboard Vercel → projet `ft2e-v3` → **Settings → Domains** → ajouter `ft2e.fr` et `www.ft2e.fr`.

### 3.2 — Configurer le DNS chez le registrar

- `A` record `ft2e.fr` → `76.76.21.21` (IP Vercel anycast — vérifier dans Vercel)
- `CNAME` record `www` → `cname.vercel-dns.com`

### 3.3 — Attendre la propagation DNS

Quelques minutes à 24 h selon le registrar. Vercel émet automatiquement le certificat SSL Let's Encrypt dès la propagation.

### 3.4 — Soumettre le sitemap

Google Search Console → propriété `https://ft2e.fr/` → Sitemaps → ajouter `https://ft2e.fr/sitemap-index.xml`.

---

## §4 — Branche : migration vers OVHcloud

Voir `docs/09-deploiement-ovh.md` en intégralité. Points complémentaires au revert SEO :

- Ajouter le fichier `public/.htaccess` (contenu fourni dans `docs/09-deploiement-ovh.md` § « Fichier `.htaccess` à déployer »). **Vérifier qu'il ne contient AUCUN header `X-Robots-Tag: noindex`** introduit par erreur.
- Configurer les **redirections 301** depuis `ft2e.myportfolio.com` ET depuis `ft2e-v3.vercel.app` vers les URLs équivalentes `ft2e.fr` — pour ne pas perdre le trafic acquis pendant la phase démo Vercel. ⚠ **`ft2e-v3`, pas `ft2e-site`** : ce dernier est le déploiement de la v1, dont les URLs de références ne correspondent plus (voir § 6 bis).
- Activer **Plausible Analytics** (RGPD-friendly).
- Soumettre le sitemap à Google Search Console.

---

## §5 — Vérifications post-migration (J+1 et J+7)

- [ ] `https://ft2e.fr` répond en HTTPS, certificat SSL valide.
- [ ] `robots.txt`, `sitemap.xml`, `sitemap-index.xml` accessibles.
- [ ] Aucune page ne renvoie 404 (audit Lighthouse ou Screaming Frog sur les 26 routes).
- [ ] Search Console : sitemap soumis avec succès, premières pages découvertes sous 48 h.
- [ ] Plausible : les visites sont bien enregistrées.
- [ ] Lighthouse mobile : Performance ≥ 90, Accessibilité = 100, Best Practices = 100, SEO = 100.
- [ ] Formulaire Contact : envoie bien un email à l'adresse FT2E.
- [ ] Photos équipe et 8 visuels projets : remplacés par le reportage pro OU conservés temporairement avec accord écrit FT2E.

---

## §6 bis — Les deux déploiements résiduels (mesuré le 2026-08-16)

> ⛔ **HORS PÉRIMÈTRE DU CHANTIER V3 — décision de l'utilisateur du 2026-08-16.**
> « Ces projets antérieurs ne sont plus concernés par quoi que ce soit. On traite la
> V3 et uniquement la v3. » Cette section **n'est plus un point ouvert** et ne se
> rouvre pas en session de chantier. Elle est conservée parce que le fait reste vrai
> et qu'il redevient opérationnel **le jour de la mise en production** — quand les
> redirections 301 et la levée du `noindex` se poseront — et à ce moment-là
> seulement.

⚠ **Ce dépôt n'est pas le seul à servir un site FT2E.** Les deux forks antérieurs
ont gardé leur déploiement Vercel, et **les deux répondent** :

| Hôte | Code | Ce qu'il sert | Indexation |
|---|---|---|---|
| `ft2e-site.vercel.app` | `200` | le site **v1**, avec ses photographies d'ouvrages (`/images/projets/<slug>/01.jpg`, **8 distincts sur `/references` seule**, 819 à 937 Ko chacune, servies en `200`) | `noindex` + `Disallow: /` |
| `ft2e-v2.vercel.app` | `200` | le site **v2**, mêmes visuels | `noindex` + `Disallow: /` |
| `ft2e-v3.vercel.app` | `200` | **ce dépôt** — planches dessinées, aucune photographie d'ouvrage | `noindex` + `Disallow: /` |

**Ce que cela change pour la question des visuels d'architecte.** Le chantier des
planches les a retirés de *ce* site parce qu'ils exposaient le bureau au droit
d'auteur des architectes. La programmation de réduction de dette (D2, question 2)
posait le reste de l'exposition comme un problème d'**historique git**, dont la
levée coûterait une réécriture invalidant tous les SHA. La mesure dit autre chose :
l'exposition la plus directe n'est pas archivée, elle est **servie en HTTP à qui
connaît l'URL**, et la lever coûte la suppression de deux déploiements — rien.

Le `noindex` limite l'exposition, il ne la supprime pas : il empêche le référencement,
pas l'accès. Et c'est un verrou de démonstration, pensé pour être **levé** un jour ;
s'il l'était par erreur sur `ft2e-site`, la v1 se retrouverait indexée avec ses
photographies.

**À exécuter au moment de la mise en production, avant de toucher au `noindex` :**

- [ ] Décider avec FT2E du sort de `ft2e-site` et `ft2e-v2` — suppression du projet
      Vercel, ou protection par mot de passe (Deployment Protection).
- [ ] Ne PAS se contenter de supprimer le domaine : un projet Vercel garde ses URLs
      de déploiement (`<projet>-<hash>.vercel.app`) tant que le projet existe.
- [ ] Vérifier après coup, par la mesure et non par le tableau de bord :
      `curl -s -o /dev/null -w "%{http_code}" https://ft2e-site.vercel.app/`.

---

## Pièges connus

1. **Cache navigateur et edge** — après revert, vider le cache local et tester en navigation privée. Vercel peut conserver un edge cache pendant ~quelques minutes ; forcer une redéploiement complet si besoin.

2. **`PUBLIC_MODE` oublié** — sans la bascule en `production`, les `BadgeDemo` continuent d'apparaître et le formulaire reste désactivé. C'est un piège silencieux : aucun warning au build.

3. **Sitemap stale côté Google** — Google peut mettre des semaines à abandonner d'éventuelles URLs `ft2e-v3.vercel.app` indexées (si jamais le robots.txt avait été contourné). Mettre une `301` Vercel → `ft2e.fr` au niveau projet Vercel et utiliser l'outil « Removal » de Search Console si nécessaire.

4. **Headers `X-Robots-Tag` persistants** — si on supprime `vercel.json` mais qu'on garde le projet Vercel, vérifier qu'aucun autre fichier (ex. `next.config`, `astro.config`) ne réinjecte ce header.

---

## Historique des décisions

- **2026-05-28** — Mise en place du blocage SEO triple-couche pendant la session de finalisation des visuels (Pierre Loti, références démo, équipe collective, portraits individuels). Commit `7e21628`.
- _À compléter au moment de la migration : date, commit de revert, validation FT2E._
