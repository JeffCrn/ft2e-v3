#!/usr/bin/env node
/**
 * Jeu de captures d'écran du site FT2E v3 — matière première d'une planche de
 * portfolio (format Behance).
 *
 * Usage :
 *     npm run build              # obligatoire : le script photographie `dist/`
 *     node scripts/captures/portfolio.mjs
 *
 * Options :
 *     --base <url>    photographier un site déjà servi (déploiement Vercel par
 *                     exemple) au lieu de démarrer `astro preview` en local
 *     --port <n>      port du serveur de prévisualisation local (défaut 4399)
 *     --route <frag>  ne traiter que les routes dont le dossier contient <frag>
 *
 * Trois objets par page, qui ne se substituent pas l'un à l'autre :
 *
 *   fenetre/       le cadre exact du palier (1920 × 1080 pour le 16:9) — ce que
 *                  le visiteur voit en arrivant, ligne de flottaison comprise ;
 *   page-entiere/  la page longue complète — la narration de défilement ;
 *   sections/      chaque `<section>` isolée — les gros plans de composants.
 *
 * ⚠ DEUX PIÈGES, dont aucun ne lève d'erreur (voir `preparer()`) :
 *
 *   1. `captureBeyondViewport` (le mécanisme de `fullPage`) agrandit la zone
 *      photographiée SANS faire défiler la page. L'`IntersectionObserver` qui
 *      révèle les `[data-plan]` ne se déclenche donc jamais, et les images en
 *      `loading="lazy"` ne sont jamais demandées. On obtient une image valide
 *      où des blocs sont à `opacity: 0` et des photographies sont vides.
 *   2. La barre de défilement de Chrome bureau CONSOMME 15 px de largeur utile
 *      (mesuré : viewport 390 → document 375), là où un téléphone la met en
 *      surimpression. `--hide-scrollbars` est donc une condition de fidélité
 *      des paliers étroits, pas une option cosmétique.
 */

import { spawn } from 'node:child_process';
import { execFileSync } from 'node:child_process';
import { mkdir, rm, writeFile } from 'node:fs/promises';
import { existsSync, readdirSync } from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import puppeteer from 'puppeteer-core';

const RACINE = path.resolve(import.meta.dirname, '..', '..');
const SORTIE = path.join(RACINE, 'livrables', 'captures-portfolio');

/** Espace insécable et espace fine insécable, en échappement : l'outil
 *  d'écriture du dépôt normalise les caractères littéraux. */
const NBSP = '\u00a0';
const FINE = '\u202f';

/**
 * Les cinq paliers, du téléphone au 16:9.
 *
 * `deviceScaleFactor: 2` partout — les images sortent au double, ce qu'attend
 * une planche de portfolio. Un palier ne reçoit la page entière et les sections
 * que si l'information ajoutée le justifie : les deux tablettes et le portable
 * servent à démontrer les bascules de mise en page, pas à tripler le corpus.
 */
const PALIERS = [
  { nom: 'mobile-390', largeur: 390, hauteur: 844, pageEntiere: true, sections: true },
  { nom: 'tablette-768', largeur: 768, hauteur: 1024, pageEntiere: true, sections: false },
  { nom: 'tablette-1024', largeur: 1024, hauteur: 768, pageEntiere: false, sections: false },
  { nom: 'portable-1440', largeur: 1440, hauteur: 900, pageEntiere: false, sections: false },
  { nom: 'bureau-1920', largeur: 1920, hauteur: 1080, pageEntiere: true, sections: true },
];

/**
 * Les quatorze routes retenues : les dix gabarits distincts du site, plus trois
 * fiches projet d'archétypes de planche différents, plus une page légale.
 *
 * Le site compte 46 routes, dont 23 fiches au même gabarit. Photographier les
 * vingt-trois donnerait vingt-trois fois la même démonstration ; les trois
 * retenues couvrent trois dessins de planche et trois longueurs de récit.
 */
const ROUTES = [
  { dossier: '01-accueil', route: '/', titre: 'Accueil' },
  { dossier: '02-societe', route: '/societe/', titre: 'Société' },
  { dossier: '03-equipe', route: '/equipe/', titre: 'Équipe' },
  { dossier: '04-expertises', route: '/expertises/', titre: 'Expertises — index' },
  { dossier: '05-expertise-cvc', route: '/expertises/cvc/', titre: 'Expertise — CVC' },
  { dossier: '06-secteur-logements', route: '/secteurs/logements/', titre: 'Secteur — Logements' },
  { dossier: '07-references', route: '/references/', titre: 'Références — grille filtrable' },
  {
    dossier: '08-fiche-nerea',
    route: '/references/logements-nerea-aytre/',
    titre: 'Fiche projet — Néréa, 90 logements',
  },
  {
    dossier: '09-fiche-passerelle-marans',
    route: '/references/passerelle-ecluse-carreau-d-or-marans/',
    titre: 'Fiche projet — Passerelle de Marans',
  },
  {
    dossier: '10-fiche-ehpad-coulonges',
    route: '/references/ehpad-coulonges-sur-autize-ssi/',
    titre: 'Fiche projet — EHPAD de Coulonges, coordination SSI',
  },
  { dossier: '11-actualites', route: '/actualites/', titre: 'Actualités — index' },
  {
    dossier: '12-article-lancement',
    route: '/actualites/2026-09-lancement-site/',
    titre: 'Article — lancement du site',
  },
  { dossier: '13-contact', route: '/contact/', titre: 'Contact' },
  { dossier: '14-mentions-legales', route: '/mentions-legales/', titre: 'Mentions légales' },
];

// ── Arguments ────────────────────────────────────────────────────────────────

function lireArguments(argv) {
  const opts = { base: null, port: 4399, route: null };
  for (let i = 0; i < argv.length; i += 1) {
    if (argv[i] === '--base') opts.base = argv[++i];
    else if (argv[i] === '--port') opts.port = Number(argv[++i]);
    else if (argv[i] === '--route') opts.route = argv[++i];
    else throw new Error(`Argument inconnu : ${argv[i]}`);
  }
  return opts;
}

// ── Chrome ───────────────────────────────────────────────────────────────────

/** Compare deux répertoires `win64-146.0.7680.153` par segments numériques. */
function comparerVersions(a, b) {
  const seg = (v) => v.replace(/^win64-/, '').split('.').map(Number);
  const [sa, sb] = [seg(a), seg(b)];
  for (let i = 0; i < Math.max(sa.length, sb.length); i += 1) {
    const d = (sb[i] ?? 0) - (sa[i] ?? 0);
    if (d) return d;
  }
  return 0;
}

/**
 * Trouve un Chrome exploitable, du plus spécifique au plus général.
 *
 * Le cache de puppeteer est préféré à l'installation système : c'est un binaire
 * dédié, jamais celui que l'utilisateur a sous les yeux — une capture ne doit
 * pas piloter le navigateur du poste (le redimensionnement d'une fenêtre
 * visible persiste et fait passer une page saine pour cassée).
 */
function chercherChrome() {
  if (process.env.CHROME_PATH && existsSync(process.env.CHROME_PATH)) {
    return process.env.CHROME_PATH;
  }

  const cache = path.join(os.homedir(), '.cache', 'puppeteer', 'chrome');
  if (existsSync(cache)) {
    const versions = readdirSync(cache)
      .filter((d) => d.startsWith('win64-') || d.startsWith('linux-') || d.startsWith('mac'))
      .sort(comparerVersions);
    for (const v of versions) {
      for (const rel of [
        ['chrome-win64', 'chrome.exe'],
        ['chrome-linux64', 'chrome'],
        ['chrome-mac-x64', 'Google Chrome for Testing.app', 'Contents', 'MacOS', 'Google Chrome for Testing'],
      ]) {
        const exe = path.join(cache, v, ...rel);
        if (existsSync(exe)) return exe;
      }
    }
  }

  for (const p of [
    'C:/Program Files/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    '/usr/bin/google-chrome',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  ]) {
    if (existsSync(p)) return p;
  }

  throw new Error(
    'Aucun Chrome trouvé. Poser CHROME_PATH, ou installer le navigateur de ' +
      'puppeteer : npx puppeteer browsers install chrome',
  );
}

// ── Serveur de prévisualisation ──────────────────────────────────────────────

async function joignable(url) {
  try {
    const r = await fetch(url, { redirect: 'manual' });
    return r.status < 500;
  } catch {
    return false;
  }
}

/**
 * Démarre `astro preview` par son point d'entrée, sans passer par `npm`.
 *
 * `npm run preview` traverserait `npm.cmd` et un shell : sous Windows le
 * processus enfant devient difficile à arrêter proprement. Appeler directement
 * `node node_modules/astro/bin/astro.mjs` évite les deux intermédiaires.
 */
async function demarrerPreview(port) {
  const entree = path.join(RACINE, 'node_modules', 'astro', 'bin', 'astro.mjs');
  if (!existsSync(entree)) throw new Error(`Point d'entrée Astro introuvable : ${entree}`);

  const proc = spawn(process.execPath, [entree, 'preview', '--port', String(port)], {
    cwd: RACINE,
    stdio: ['ignore', 'pipe', 'pipe'],
  });

  let journal = '';
  proc.stdout.on('data', (d) => (journal += d));
  proc.stderr.on('data', (d) => (journal += d));

  const base = `http://localhost:${port}`;
  const limite = Date.now() + 45_000;
  while (Date.now() < limite) {
    if (await joignable(`${base}/`)) return { proc, base };
    if (proc.exitCode !== null) {
      throw new Error(`astro preview s'est arrêté (code ${proc.exitCode}) :\n${journal}`);
    }
    await new Promise((r) => setTimeout(r, 400));
  }
  proc.kill();
  throw new Error(`astro preview n'a pas répondu sur ${base} en 45${NBSP}s :\n${journal}`);
}

// ── Préparation d'une page ───────────────────────────────────────────────────

/**
 * Amène la page à l'état photographiable, et RAPPORTE ce qui n'a pas abouti.
 *
 * Rien ici n'est décoratif :
 *   - `document.fonts.ready` : sans attente, Archivo et IBM Plex Mono ne sont
 *     pas encore substituées et la capture montre la police de repli ;
 *   - la passe de défilement amorce `loading="lazy"` et déclenche
 *     l'`IntersectionObserver` des `[data-plan]`, que `fullPage` ne déclenche
 *     jamais de lui-même ;
 *   - le décompte final des images incomplètes est REMONTÉ à l'appelant plutôt
 *     qu'avalé : une photographie vide dans une capture est indiscernable d'un
 *     choix de dessin.
 */
async function preparer(page, url) {
  const ennuis = [];

  await page.goto(url, { waitUntil: 'networkidle2', timeout: 60_000 });
  await page.evaluate(() => document.fonts.ready);

  await page.evaluate(async () => {
    const pas = Math.max(240, Math.round(window.innerHeight * 0.8));
    for (let y = 0; y < document.documentElement.scrollHeight; y += pas) {
      window.scrollTo(0, y);
      await new Promise((r) => setTimeout(r, 70));
    }
    window.scrollTo(0, 0);
    await new Promise((r) => setTimeout(r, 200));
  });

  try {
    await page.waitForFunction(() => Array.from(document.images).every((i) => i.complete), {
      timeout: 20_000,
    });
  } catch {
    const restantes = await page.evaluate(() =>
      Array.from(document.images)
        .filter((i) => !i.complete)
        .map((i) => i.currentSrc || i.src),
    );
    ennuis.push(`${restantes.length} image(s) non chargée(s) : ${restantes.slice(0, 3).join(', ')}`);
  }

  // Les plans doivent être posés : avec `prefers-reduced-motion` émulé, la
  // règle de `motion.css` les met à `opacity: 1` — un plan resté transparent
  // signale que l'émulation n'a pas pris, et cela doit se dire.
  const plansVoiles = await page.evaluate(
    () =>
      Array.from(document.querySelectorAll('[data-plan]')).filter(
        (el) => Number(getComputedStyle(el).opacity) < 0.99,
      ).length,
  );
  if (plansVoiles) ennuis.push(`${plansVoiles} bloc(s) [data-plan] encore transparent(s)`);

  return ennuis;
}

// ── Sections ─────────────────────────────────────────────────────────────────

/** Réduit un libellé lu dans le DOM à un fragment de nom de fichier. */
function ardoise(texte) {
  const brut = texte
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/^\s*\d+\s*[\u2014\u2013-]\s*/, '') // retire la numérotation de la pastille
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');

  // Couper sur un tiret, jamais au milieu d'un mot : `…-a-la-rochel` se lit
  // comme un fichier tronqué par accident, `…-a-la` comme un nom abrégé.
  return brut.length <= 48 ? brut : brut.slice(0, 48).replace(/-[^-]*$/, '');
}

/**
 * Décide si une `<section>` mérite son propre fichier.
 *
 * C'est le seul jugement éditorial du script : trop permissif, le dossier
 * `sections/` se remplit de bandes quasi vides (filets de séparation, ancres,
 * blocs repliés au palier étroit) et cesse d'être une galerie ; trop strict, il
 * escamote les blocs courts qui sont pourtant des composants à part entière
 * (le relevé encré d'une fiche fait moins de 200 px de haut au mobile).
 *
 * Le seuil retenu — 200 px de large, 80 px de haut — est mesuré sur les
 * quatorze routes : il retient tout ce qui porte un titre de section et écarte
 * les bandes de moins de deux modules de trame.
 */
function retenirSection(boite) {
  return Boolean(boite) && boite.width >= 200 && boite.height >= 80;
}

async function capturerSections(page, dossier, palier, manifeste) {
  let sections = await page.$$('main section');
  if (!sections.length) sections = await page.$$('section');

  let rang = 0;
  for (const section of sections) {
    const boite = await section.boundingBox();
    if (!retenirSection(boite)) continue;
    rang += 1;

    const libelle = await section.evaluate((el) => {
      // Le complément clair des titres de section est `aria-hidden` et purement
      // décoratif : il n'a pas à entrer dans le nom du fichier.
      const propre = (n) => {
        if (!n) return '';
        const clone = n.cloneNode(true);
        clone.querySelectorAll('[aria-hidden="true"]').forEach((x) => x.remove());
        return clone.textContent.replace(/\s+/g, ' ').trim();
      };

      // La pastille de section d'abord — mais JAMAIS celle d'un `<nav>` : le
      // fil d'Ariane du `HeroPage` est en mono lui aussi, et il nommerait tous
      // les héros « accueil-<page> », c'est-à-dire d'après la page précédente.
      const pastille = Array.from(el.querySelectorAll('.mono-label')).find(
        (p) => !p.closest('nav') && p.textContent.trim(),
      );
      if (pastille) return propre(pastille);

      const titre = propre(el.querySelector('h1, h2, h3'));
      if (titre) return titre;

      // Dernier recours : la légende d'un média — c'est ce qui nomme le mieux
      // un bloc d'illustration sans titre.
      return propre(el.querySelector('.cartouche-legende, .legende-media, figcaption'));
    });

    const nom = `${String(rang).padStart(2, '0')}-${ardoise(libelle) || 'section'}-${palier.nom}.png`;
    const chemin = path.join(dossier, 'sections', nom);
    await section.screenshot({ path: chemin });
    manifeste.push(path.relative(SORTIE, chemin).replaceAll('\\', '/'));
  }
  return rang;
}

// ── Programme ────────────────────────────────────────────────────────────────

function commitCourant() {
  try {
    return execFileSync('git', ['rev-parse', '--short', 'HEAD'], { cwd: RACINE })
      .toString()
      .trim();
  } catch {
    return 'inconnu';
  }
}

async function main() {
  const opts = lireArguments(process.argv.slice(2));
  const routes = opts.route
    ? ROUTES.filter((r) => r.dossier.includes(opts.route))
    : ROUTES;
  if (!routes.length) throw new Error(`Aucune route ne correspond à « ${opts.route} »`);

  if (!opts.base && !existsSync(path.join(RACINE, 'dist', 'index.html'))) {
    throw new Error('`dist/` est absent ou incomplet — lancer `npm run build` d\'abord.');
  }

  let serveur = null;
  let base = opts.base;
  if (!base) {
    process.stdout.write(`Démarrage d'astro preview sur le port ${opts.port}${FINE}…\n`);
    serveur = await demarrerPreview(opts.port);
    base = serveur.base;
  }
  process.stdout.write(`Site photographié : ${base}\n`);

  const chrome = chercherChrome();
  process.stdout.write(`Chrome : ${chrome}\n\n`);

  const navigateur = await puppeteer.launch({
    executablePath: chrome,
    headless: true,
    args: [
      '--hide-scrollbars', // ⚠ condition de fidélité des paliers étroits (voir en-tête)
      '--force-color-profile=srgb',
      '--font-render-hinting=none',
      '--disable-lcd-text', // antialiasing en niveaux de gris : pas de frange colorée
      '--no-sandbox',
    ],
  });

  const manifeste = [];
  const avertissements = [];
  const debut = Date.now();

  try {
    for (const { dossier, route, titre } of routes) {
      const cible = path.join(SORTIE, dossier);
      await rm(cible, { recursive: true, force: true });
      for (const sous of ['fenetre', 'page-entiere', 'sections']) {
        await mkdir(path.join(cible, sous), { recursive: true });
      }

      process.stdout.write(`${dossier}  ${route}\n`);

      for (const palier of PALIERS) {
        const page = await navigateur.newPage();
        await page.emulateMediaFeatures([
          // Le site traduit `reduce` par « tout est posé d'emblée » : l'état
          // réduit EST l'état final, donc la capture est déterministe.
          { name: 'prefers-reduced-motion', value: 'reduce' },
        ]);
        await page.setViewport({
          width: palier.largeur,
          height: palier.hauteur,
          deviceScaleFactor: 2,
        });

        const ennuis = await preparer(page, `${base}${route}`);
        ennuis.forEach((e) => avertissements.push(`${route} @ ${palier.nom} — ${e}`));

        const cadre = path.join(
          cible,
          'fenetre',
          `${palier.largeur}x${palier.hauteur}-${palier.nom}.png`,
        );
        await page.screenshot({ path: cadre, captureBeyondViewport: false });
        manifeste.push(path.relative(SORTIE, cadre).replaceAll('\\', '/'));

        let nbSections = 0;
        if (palier.pageEntiere) {
          const longue = path.join(cible, 'page-entiere', `${palier.nom}.png`);
          await page.screenshot({ path: longue, fullPage: true });
          manifeste.push(path.relative(SORTIE, longue).replaceAll('\\', '/'));
        }
        if (palier.sections) {
          nbSections = await capturerSections(page, cible, palier, manifeste);
        }

        const hauteur = await page.evaluate(() => document.documentElement.scrollHeight);
        process.stdout.write(
          `   ${palier.nom.padEnd(15)} page ${String(hauteur).padStart(5)}${NBSP}px` +
            `${palier.pageEntiere ? '  + page entière' : ''}` +
            `${palier.sections ? `  + ${nbSections} section(s)` : ''}\n`,
        );

        await page.close();
      }
    }
  } finally {
    await navigateur.close();
    serveur?.proc.kill();
  }

  const duree = Math.round((Date.now() - debut) / 1000);
  await ecrireLisezMoi({ routes, manifeste, avertissements, base, chrome, duree });

  process.stdout.write(`\n${manifeste.length} image(s) écrite(s) en ${duree}${NBSP}s\n`);
  process.stdout.write(`Dossier : ${SORTIE}\n`);
  if (avertissements.length) {
    process.stdout.write(`\n⚠ ${avertissements.length} avertissement(s) :\n`);
    avertissements.forEach((a) => process.stdout.write(`   ${a}\n`));
  }
}

// ── LISEZ-MOI engendré ───────────────────────────────────────────────────────

/**
 * Le LISEZ-MOI est ENGENDRÉ, jamais tapé : un inventaire écrit à la main se
 * désynchronise du dossier dès la première régénération, et c'est la copie qui
 * mène alors en erreur. Ce qu'il annonce, il l'a compté.
 */
async function ecrireLisezMoi({ routes, manifeste, avertissements, base, chrome, duree }) {
  const jour = new Date().toISOString().slice(0, 10);
  const compte = (motif) => manifeste.filter((f) => f.includes(motif)).length;

  const lignesRoutes = routes
    .map(({ dossier, route, titre }) => {
      const n = manifeste.filter((f) => f.startsWith(`${dossier}/`)).length;
      return `| \`${dossier}/\` | ${titre} | \`${route}\` | ${n} |`;
    })
    .join('\n');

  const lignesPaliers = PALIERS.map(
    (p) =>
      `| \`${p.nom}\` | ${p.largeur}${NBSP}×${NBSP}${p.hauteur} | ${p.largeur * 2}${NBSP}×${NBSP}${p.hauteur * 2} | ` +
      `${p.pageEntiere ? 'oui' : '—'} | ${p.sections ? 'oui' : '—'} |`,
  ).join('\n');

  const texte = `# Captures d'écran du site FT2E v3 — matière de portfolio

**Engendré le ${jour}** par \`scripts/captures/portfolio.mjs\` — commit \`${commitCourant()}\`,
source \`${base}\`, ${manifeste.length}${NBSP}images en ${duree}${NBSP}s.

> Ce fichier est **engendré à chaque exécution**. Ne pas le modifier à la main :
> la prochaine capture l'écrase. Ce qu'il annonce, il l'a compté.

## Ce que contient le dossier

Trois objets par page, qui ne se substituent pas l'un à l'autre :

| Sous-dossier | Ce que c'est | À quoi ça sert sur une planche |
|---|---|---|
| \`fenetre/\` | le cadre exact du palier, ligne de flottaison comprise | l'image d'ouverture — ce que le visiteur voit en arrivant |
| \`page-entiere/\` | la page longue complète, d'un seul tenant | la narration de défilement, à présenter dans un cadre d'appareil |
| \`sections/\` | chaque \`<section>\` isolée, nommée d'après son propre titre | les gros plans de composants et de détails de dessin |

Décompte : **${compte('/fenetre/')}** cadres, **${compte('/page-entiere/')}** pages entières,
**${compte('/sections/')}** sections.

## Les cinq paliers

| Palier | Viewport CSS | Image produite | Page entière | Sections |
|---|---|---|---|---|
${lignesPaliers}

\`deviceScaleFactor${NBSP}2\` partout : l'image sort au double du viewport, ce qu'attend une
planche de portfolio. Le palier \`bureau-1920\` est le **full${NBSP}HD 16:9** demandé — son cadre
fait 1920${NBSP}×${NBSP}1080 en pixels CSS, 3840${NBSP}×${NBSP}2160 en pixels d'image.

## Les quatorze pages

| Dossier | Page | Route | Images |
|---|---|---|---|
${lignesRoutes}

Le site compte **46 routes**, dont 23 fiches projet au même gabarit. Les trois fiches
retenues portent trois dessins de planche et trois longueurs de récit différents ;
les vingt autres donneraient vingt fois la même démonstration. Pour tout capturer,
étendre la table \`ROUTES\` du script.

## Comment c'est produit — et les deux pièges que ça évite

\`\`\`bash
npm run build                              # obligatoire : le script photographie dist/
node scripts/captures/portfolio.mjs        # démarre astro preview, capture, s'arrête
\`\`\`

Options : \`--base <url>\` pour photographier un site déjà servi (le déploiement Vercel
par exemple), \`--route <fragment>\` pour ne refaire qu'une page, \`--port <n>\` pour
déplacer le serveur local.

Navigateur employé : \`${chrome}\` — un binaire dédié, **jamais le Chrome du poste** :
imposer une taille de zone de rendu à une fenêtre visible persiste après le contrôle et
fait passer une page saine pour cassée.

Deux précautions, dont aucune ne se signalerait par une erreur si on l'omettait :

1. **Passe de défilement avant chaque capture.** \`captureBeyondViewport\` — le mécanisme
   de \`fullPage\` — agrandit la zone photographiée **sans faire défiler la page**.
   L'\`IntersectionObserver\` qui révèle les blocs \`[data-plan]\` ne se déclenche donc
   jamais, et les images en \`loading="lazy"\` (les huit portraits d'\`/equipe/\`) ne sont
   jamais demandées. Sans la passe, l'image est techniquement valide et montre des blocs
   à \`opacity${NBSP}0\` et des photographies vides.
2. **\`--hide-scrollbars\`.** La barre de défilement de Chrome bureau **consomme** 15${NBSP}px
   de largeur utile — un viewport de 390 rend un document de 375 — là où un téléphone la
   met en surimpression. Sans ce drapeau, tous les paliers étroits seraient 15${NBSP}px plus
   sévères que la réalité.

À quoi s'ajoute l'émulation de \`prefers-reduced-motion:${NBSP}reduce\` : le site le traduit
par « tout est posé d'emblée » (\`src/styles/motion.css\`), donc l'état réduit **est** l'état
final des quatre mouvements, et la capture devient déterministe au lieu de photographier
une transition en vol. Le script vérifie après coup qu'aucun \`[data-plan]\` n'est resté
transparent, et le dit s'il en reste.

## Ce que les captures ne montrent pas

- **Les quatre mouvements** (filet de flux 900${NBSP}ms, révélation de plan 760${NBSP}ms, les deux
  survols) : une image fixe ne peut pas les rendre. Pour une planche, les filmer à l'écran.
- **Les états de survol et de focus** : les captures sont prises au repos.
- **Les sept marqueurs \`[DÉMO]\`** des visuels de secteurs restent des images de
  démonstration générées par IA, en attente du reportage photographique.

## Avertissements de la dernière exécution

${avertissements.length ? avertissements.map((a) => `- ${a}`).join('\n') : '_Aucun._'}
`;

  await writeFile(path.join(SORTIE, 'LISEZ-MOI.md'), texte, 'utf8');
}

main().catch((e) => {
  process.stderr.write(`\n✗ ${e.message}\n`);
  process.exit(1);
});
