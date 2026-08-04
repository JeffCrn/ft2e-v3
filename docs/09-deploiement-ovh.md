# 09 · Déploiement sur OVHcloud

> Cette section reprend strictement la **configuration retenue dans l'annexe A du PDF** (pp. 28–29). En cas de divergence avec ce document, le PDF gagne.
>
> ⚠️ **État actuel** : le site est hébergé sur **Vercel** (`https://ft2e-site.vercel.app`) en démo client, avec indexation moteurs bloquée. Le présent document reste valide comme cible long terme. **La séquence exacte de migration (Vercel ou OVH) — y compris le revert du blocage SEO — est consolidée dans `docs/19-migration-production.md`**, à exécuter au feu vert FT2E.

## Pourquoi OVHcloud (PDF p. 28)

- **Souveraineté** — Datacenters en France (Roubaix, Strasbourg, Gravelines), conformité RGPD native, juridiction française. Vos données et celles de vos visiteurs ne quittent pas le territoire.
- **Performance** — Connectivité excellente sur le territoire français — temps de chargement de premier ordre pour les visiteurs, qu'ils soient à La Rochelle, Paris ou Bordeaux. Rendu critique par la prévalence du mobile sur la consultation B2B.
- **Coût maîtrisé** — Formule Webhosting Pro à environ 80 à 100 € HT/an tout inclus. Pas de surprise tarifaire, pas de coût caché, pas de facturation à la consommation.
- **Robustesse** — SLA de 99,9 %, redondance des serveurs, sauvegardes automatiques quotidiennes incluses, reprise après incident en moins d'une heure pour les cas standard.

## Configuration retenue (PDF p. 28)

| Composant | Détail |
|---|---|
| **Domaine** | `ft2e.fr` — enregistrement chez OVH (~12 €/an), configuration DNS sur les serveurs OVHcloud. Migration et redirection 301 de l'ancienne URL `ft2e.myportfolio.com`. |
| **Offre d'hébergement** | **OVHcloud Webhosting Pro** — 250 Go d'espace disque, 10 sites possibles, base de données MySQL incluse (non utilisée mais disponible), PHP 8.x, **Node.js disponible**. Coût : ~80 € HT/an. |
| **Certificat SSL** | Let's Encrypt automatique inclus, renouvelé tous les 90 jours sans intervention. HTTPS forcé sur l'ensemble du site. |
| **Email professionnel** | Conservation de `ft2e@ft2e.fr` avec **MX OVH Email** (5 boîtes incluses jusqu'à 10 Go chacune dans la formule Pro). Configuration **SPF, DKIM et DMARC** pour la délivrabilité. |
| **Sauvegardes** | Sauvegardes automatiques quotidiennes (J-1 à J-7) incluses. **Double sauvegarde via Git** : chaque modification du site est versionnée dans le dépôt source. Restauration possible à n'importe quel point dans le temps. |
| **Déploiement** | **Déploiement continu via Git** : chaque commit sur la branche principale déclenche une **recompilation Astro et un déploiement automatique**. Délai de mise en ligne d'une modification : moins de deux minutes. |
| **Monitoring** | Plausible Analytics (RGPD-friendly, hébergé en UE). UptimeRobot ou équivalent pour la disponibilité (gratuit). Alertes par email en cas d'indisponibilité. |

## Mécanique de déploiement continu

Le PDF affirme la disponibilité de Node.js sur Webhosting Pro et un déploiement continu via Git. Trois implémentations possibles selon ce qu'OVH expose effectivement :

### Option A — Déploiement via webhook Git natif OVH

Si OVH Webhosting Pro expose l'intégration Git native (à confirmer à l'ouverture de l'hébergement) :

1. Connecter le dépôt GitHub à l'hébergement via le manager OVH.
2. Configurer la commande de build : `npm ci && npm run build`.
3. Configurer le dossier de sortie : `dist/` → `/www/`.
4. Chaque `push` sur `main` déclenche build + déploiement.

### Option B — GitHub Actions vers OVH via SFTP

Si l'intégration Git native n'est pas disponible ou pas adaptée :

```yaml
# .github/workflows/deploy.yml
name: Deploy to OVH

on:
  push:
    branches: [main, recette]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm run build

      - name: Lighthouse mobile (home + 1 fiche projet)
        run: |
          npx -y @lhci/cli@latest autorun --config=.lighthouserc.cjs

      - name: Deploy via SFTP (main → production)
        if: github.ref == 'refs/heads/main'
        uses: SamKirkland/FTP-Deploy-Action@v4
        with:
          server: ${{ secrets.OVH_SFTP_HOST }}
          username: ${{ secrets.OVH_SFTP_USER }}
          password: ${{ secrets.OVH_SFTP_PASSWORD }}
          local-dir: ./dist/
          server-dir: /www/
          protocol: ftps
          security: strict
          exclude: '**/.git*/**'
          # Ne pas supprimer admin/ ni images/ déjà uploadées
          dangerous-clean-slate: false

      - name: Deploy recette
        if: github.ref == 'refs/heads/recette'
        uses: SamKirkland/FTP-Deploy-Action@v4
        with:
          server: ${{ secrets.OVH_SFTP_HOST }}
          username: ${{ secrets.OVH_SFTP_USER_RECETTE }}
          password: ${{ secrets.OVH_SFTP_PASSWORD_RECETTE }}
          local-dir: ./dist/
          server-dir: /www-recette/
          protocol: ftps
          security: strict
```

### Option C — Build local par OVH si Node.js exposé

Le PDF indique que Node.js est disponible sur Webhosting Pro. Si l'environnement permet l'exécution de scripts Node post-réception du push Git, on peut envisager un build serveur natif (moins commun en mutualisé, à valider techniquement avec OVH au moment de la mise en place).

> **Arbitrage en début de Phase 4** : à la mise en place de l'hébergement, vérifier directement avec le support OVH ou la documentation de l'offre Webhosting Pro l'option exacte disponible. Le PDF affirme « Node.js disponible » et « déploiement continu via Git » — ces deux affirmations conditionnent l'option retenue.

## Fichier `.htaccess` à déployer

À placer dans `public/.htaccess` pour qu'il soit copié dans `dist/` au build.

```apache
# ─── Force HTTPS ────────────────────────────────
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# ─── Force domaine canonique (sans www) ─────────
RewriteCond %{HTTP_HOST} ^www\.ft2e\.fr [NC]
RewriteRule ^(.*)$ https://ft2e.fr/$1 [L,R=301]

# ─── Cache statiques ────────────────────────────
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/avif "access plus 1 year"
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType image/jpeg "access plus 1 month"
  ExpiresByType image/png "access plus 1 month"
  ExpiresByType image/svg+xml "access plus 1 year"
  ExpiresByType text/css "access plus 1 year"
  ExpiresByType application/javascript "access plus 1 year"
  ExpiresByType font/woff2 "access plus 1 year"
  ExpiresByType text/html "access plus 1 hour"
</IfModule>

# ─── Compression ─────────────────────────────────
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml text/xml application/json
</IfModule>

# ─── Headers de sécurité ────────────────────────
<IfModule mod_headers.c>
  Header set Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"
  Header set X-Content-Type-Options "nosniff"
  Header set X-Frame-Options "SAMEORIGIN"
  Header set Referrer-Policy "strict-origin-when-cross-origin"
  Header set Permissions-Policy "geolocation=(), camera=(), microphone=(), payment=()"
  Header set Content-Security-Policy "default-src 'self'; img-src 'self' data: https://images.unsplash.com; style-src 'self' 'unsafe-inline'; script-src 'self' https://plausible.io; connect-src 'self' https://plausible.io; font-src 'self' data:; frame-ancestors 'self';"
</IfModule>

# ─── 404 ────────────────────────────────────────
ErrorDocument 404 /404.html

# ─── Redirections 301 depuis ft2e.myportfolio.com ──
# À compléter en phase de migration depuis l'URL mapping établi.
```

## Migration depuis Adobe Portfolio (PDF p. 29)

En trois phases, sans interruption de service :

### Phase 1 — Recette
- Le nouveau site est déployé sur une URL technique (type `ft2e-recette.ovh.net`) pendant les phases de test.
- L'ancien site reste accessible sur `ft2e.myportfolio.com`.
- Les visiteurs ne voient aucun changement.

### Phase 2 — Bascule
- Au jour J, les enregistrements DNS basculent vers OVH.
- Le site répond désormais sur `ft2e.fr`.
- Les redirections 301 depuis `ft2e.myportfolio.com` redirigent les visiteurs vers les nouvelles URLs équivalentes — **aucun lien existant ne se casse**.

### Phase 3 — Observation
- Les premiers retours Search Console arrivent sous **4 à 6 semaines**.
- **L'ancien sous-domaine peut être conservé en redirection pendant 12 à 24 mois pour préserver la valeur SEO acquise** (PDF p. 29).
- Bilan d'indexation à M+1, M+3 (Phase 6 du projet, cf. `docs/12-cadrage-jalons.md`).

### Préalable au démarrage de la Phase 5

Lister toutes les URLs publiques actuelles de `ft2e.myportfolio.com` via :

```bash
# Crawl du site existant
wget --recursive --no-clobber --page-requisites --html-extension --convert-links \
  --restrict-file-names=windows --domains=ft2e.myportfolio.com \
  --no-parent https://ft2e.myportfolio.com/
```

Produire `migration/url-mapping.csv` :

```csv
ancienne_url,nouvelle_url,statut
https://ft2e.myportfolio.com/,https://ft2e.fr/,200
https://ft2e.myportfolio.com/projets,https://ft2e.fr/references,301
…
```

## Email professionnel — SPF/DKIM/DMARC

Configuration **obligatoire** à la mise en place (PDF p. 28) :

### SPF
Enregistrement TXT à la racine du domaine :
```
v=spf1 include:mx.ovh.com -all
```

### DKIM
Activation via le manager OVH Email Pro. Récupérer la clé publique générée par OVH et la déclarer en TXT dans la zone DNS :
```
selector1._domainkey.ft2e.fr   IN TXT  "v=DKIM1; k=rsa; p=<clé publique OVH>"
```

### DMARC
Enregistrement TXT pour `_dmarc.ft2e.fr` :
```
v=DMARC1; p=quarantine; rua=mailto:dmarc@ft2e.fr; pct=100; adkim=s; aspf=s
```

Démarrer en `p=quarantine` puis durcir à `p=reject` après 30 jours d'observation sans incident.

## Sauvegarde — défense en profondeur

1. **OVH** : sauvegarde quotidienne automatique J-1 à J-7 (offre Webhosting Pro).
2. **Git** : tout le code et tout le contenu `src/content/` est versionné. Sauvegarde **par construction**.
3. **Médias** : `public/images/` versionné dans Git tant que le poids cumulé reste < 100 MB. Au-delà, Git LFS ou rsync vers un autre stockage (à arbitrer en Phase 4).

## Coût annuel récapitulatif (PDF p. 29)

| Poste | Coût annuel HT |
|---|---|
| Domaine `ft2e.fr` | ~12 € |
| Hébergement Webhosting Pro | ~80 € |
| Email Pro (déjà existant ou inclus) | 0 à 30 € |
| SSL et sauvegardes | inclus |
| **Total annuel à compter du 13ᵉ mois** | **100 à 130 €** |

> **« La première année est couverte par le périmètre de la proposition. »** (PDF p. 29)

## Monitoring post-déploiement

- **Uptime** : UptimeRobot, ping toutes les 5 min, alerte email.
- **Performance** : tâche planifiée GitHub Action — Lighthouse hebdomadaire sur 5 routes clés, archivé dans `audits/`.
- **Erreurs JS client** : compte gratuit Sentry (V1.1, pas obligatoire en V1).
- **Plausible** : tableau de bord. Possibilité de le rendre public ou de restreindre selon souhait FT2E.
- **Search Console** : revue mensuelle pendant la garantie (couverture, requêtes, position moyenne).

## Rollback

En cas de bug bloquant après déploiement :

```bash
# Option 1 — revert Git + redéploiement auto
git revert <hash-fautif>
git push origin main

# Option 2 — récupération de sauvegarde OVH
# Via le manager OVH : Hébergements → Sauvegardes → Restaurer
```

**Toujours** garder une sauvegarde locale du `dist/` du dernier déploiement validé avant un push de production majeur.

## Souveraineté et indépendance (PDF p. 29)

> **« L'ensemble du dispositif — code source, contenus, base de fichiers Markdown, configuration — est versionné dans un dépôt Git que vous possédez. Si demain vous souhaitez quitter OVH pour un autre hébergeur, la migration prend une demi-journée : le site est portable par construction. »**

C'est le **fil rouge** de la doctrine de non-dépendance.
