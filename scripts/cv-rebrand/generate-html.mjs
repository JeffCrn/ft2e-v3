// Génère les CV HTML (design system « Ingénierie de l'invisible ») avant impression PDF.
// Usage : node scripts/cv-rebrand/generate-html.mjs <dossier-sortie>
import { mkdirSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { cvs } from './data.mjs';

const outDir = resolve(process.argv[2] ?? 'livrables/cv-ft2e/html');
mkdirSync(outDir, { recursive: true });

const font = (rel) => pathToFileURL(resolve('node_modules', rel)).href;
const ARCHIVO = font('@fontsource-variable/archivo/files/archivo-latin-wdth-normal.woff2');
const ARCHIVO_EXT = font('@fontsource-variable/archivo/files/archivo-latin-ext-wdth-normal.woff2');
const PLEX400 = font('@fontsource/ibm-plex-mono/files/ibm-plex-mono-latin-400-normal.woff2');
const PLEX500 = font('@fontsource/ibm-plex-mono/files/ibm-plex-mono-latin-500-normal.woff2');

const esc = (s) => s.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');

const css = `
@font-face { font-family: 'Archivo Variable'; src: url('${ARCHIVO_EXT}') format('woff2-variations'); font-weight: 100 900; font-stretch: 62% 125%; unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF; }
@font-face { font-family: 'Archivo Variable'; src: url('${ARCHIVO}') format('woff2-variations'); font-weight: 100 900; font-stretch: 62% 125%; }
@font-face { font-family: 'IBM Plex Mono'; src: url('${PLEX400}') format('woff2'); font-weight: 400; }
@font-face { font-family: 'IBM Plex Mono'; src: url('${PLEX500}') format('woff2'); font-weight: 500; }

:root {
  --encre: #08131f; --marine: #16324f; --marine-surface: #0e2233;
  --cool-white: #edf0f2; --paper: #f7f9fa; --slate: #4a6076; --mist: #8fa2b4;
  --copper: #c46a38; --bright-copper: #e08a50; --copper-text: #a04e20;
  --line: rgba(74, 96, 118, .35); --line-strong: #4a6076;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
@page { size: A4; margin: 0; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body {
  width: 210mm; min-height: 296mm; display: flex; flex-direction: column;
  background: var(--cool-white);
  font-family: 'Archivo Variable', 'Archivo', sans-serif;
  font-weight: 330; color: var(--slate);
}
.mono { font-family: 'IBM Plex Mono', monospace; }
.mono-label { font-family: 'IBM Plex Mono', monospace; font-weight: 500; text-transform: uppercase; letter-spacing: .14em; }

/* ── Header encre ── */
header { background: var(--encre); border-top: 1.4mm solid var(--copper); padding: 8mm 12mm 7mm; color: var(--cool-white); }
.cartouche-top { display: flex; justify-content: space-between; align-items: baseline; border-bottom: .3mm solid rgba(143,162,180,.28); padding-bottom: 2.4mm; margin-bottom: 5.5mm; }
.cartouche-top .ft2e { font-size: 8pt; color: var(--cool-white); }
.cartouche-top .bl { font-size: 6.2pt; color: var(--mist); font-weight: 400; }
.eyebrow { font-size: 6.6pt; color: var(--copper); margin-bottom: 2.6mm; }
h1 { font-stretch: 125%; font-weight: 700; text-transform: uppercase; letter-spacing: -.01em; line-height: .98; font-size: 25pt; color: var(--cool-white); }
.titre { font-stretch: 112%; font-weight: 600; text-transform: uppercase; letter-spacing: .005em; font-size: 10.6pt; color: var(--cool-white); margin-top: 2.8mm; }
.fonction { font-family: 'IBM Plex Mono', monospace; font-weight: 400; font-size: 7.4pt; color: var(--mist); margin-top: 1.8mm; }
.meta-row { display: flex; gap: 3mm; align-items: center; margin-top: 4.2mm; flex-wrap: wrap; }
.meta-exp { font-size: 6.6pt; color: var(--mist); font-weight: 400; }
.chip { font-size: 6.6pt; color: var(--bright-copper); border: .3mm solid var(--copper); padding: 1.1mm 2.2mm; }

/* ── Corps ── */
.corps { flex: 1; display: grid; grid-template-columns: 58mm 1fr; gap: 7mm; padding: 7mm 12mm 5mm; }

/* Sidebar cartouche */
aside { position: relative; align-self: start; }
.cartouche { border: .3mm solid var(--line-strong); background: var(--line); display: grid; gap: .3mm; }
.cell { background: var(--paper); padding: 3.6mm 4mm 4mm; }
.cell h2 { font-size: 6.6pt; color: var(--slate); margin-bottom: 2.6mm; display: flex; align-items: center; gap: 1.6mm; }
.cell h2::before { content: ''; width: 1.6mm; height: 1.6mm; background: var(--copper); flex: none; }
.contact-row { display: flex; flex-direction: column; margin-bottom: 2mm; }
.contact-row .k { font-size: 5.8pt; color: var(--slate); font-weight: 400; opacity: .75; }
.contact-row .v { font-family: 'IBM Plex Mono', monospace; font-size: 7.6pt; color: var(--marine); font-variant-numeric: tabular-nums; }
.form-item { margin-bottom: 2.8mm; }
.form-item .annee { font-size: 6.4pt; color: var(--copper-text); }
.form-item .t { font-size: 7.8pt; font-weight: 430; color: var(--marine); line-height: 1.3; margin-top: .5mm; }
.form-item .l { font-size: 7pt; line-height: 1.35; color: var(--slate); margin-top: .4mm; }
.chips { display: flex; flex-wrap: wrap; gap: 1.4mm; }
.chips span { border: .26mm solid var(--line); font-size: 6.1pt; font-weight: 400; padding: 1mm 1.8mm; color: var(--slate); background: var(--cool-white); }
/* équerres cuivre */
.coin { position: absolute; width: 4mm; height: 4mm; border: .5mm solid var(--copper); }
.coin.tl { top: -1mm; left: -1mm; border-right: 0; border-bottom: 0; }
.coin.br { bottom: -1mm; right: -1mm; border-left: 0; border-top: 0; }

/* Sections principales */
main section + section { margin-top: 5.5mm; }
main h2 { border-top: .3mm solid var(--copper); padding-top: 2.4mm; display: flex; align-items: baseline; gap: 3.4mm; margin-bottom: 3.4mm; }
main h2 .h { font-stretch: 112%; font-weight: 600; text-transform: uppercase; letter-spacing: -.005em; font-size: 11pt; color: var(--marine); }
main h2 .a { font-size: 6.2pt; color: var(--slate); font-weight: 400; }

.timeline { list-style: none; border-left: .3mm solid var(--line); margin-left: 1mm; }
.timeline li { position: relative; padding-left: 4.6mm; padding-bottom: 3.1mm; }
.timeline li:last-child { padding-bottom: .5mm; }
.timeline li::before { content: ''; position: absolute; left: -1.15mm; top: 1mm; width: 2mm; height: 2mm; background: var(--copper); }
.timeline .annee { font-size: 6.6pt; color: var(--copper-text); }
.timeline .rt { font-stretch: 112%; font-weight: 600; text-transform: uppercase; font-size: 8.6pt; color: var(--marine); line-height: 1.15; margin-top: .6mm; }
.timeline .lieu { font-family: 'IBM Plex Mono', monospace; font-size: 6.8pt; color: var(--slate); margin-top: .4mm; }
.timeline .detail { font-size: 7.9pt; line-height: 1.4; margin-top: .7mm; }

.exp { list-style: none; }
.exp > li { margin-bottom: 3.6mm; }
.exp .periode { font-size: 6.6pt; color: var(--copper-text); }
.exp .poste { font-stretch: 112%; font-weight: 600; text-transform: uppercase; font-size: 8.8pt; color: var(--marine); margin-top: .6mm; }
.exp .org { font-family: 'IBM Plex Mono', monospace; font-size: 6.8pt; color: var(--slate); margin-top: .4mm; }
.exp ul { list-style: none; margin-top: 1mm; }
.exp ul li { position: relative; padding-left: 3.4mm; font-size: 7.9pt; line-height: 1.42; }
.exp ul li::before { content: ''; position: absolute; left: 0; top: 1.55mm; width: 1.5mm; height: .35mm; background: var(--copper); }

/* Footer */
footer { border-top: .3mm solid var(--line); margin: 0 12mm; padding: 2.6mm 0 4mm; display: flex; justify-content: space-between; }
footer span { font-size: 5.9pt; color: var(--slate); font-weight: 400; }

/* Densité (profils chargés) */
body.compact header { padding: 5mm 12mm 4mm; }
body.compact .cartouche-top { margin-bottom: 3.5mm; padding-bottom: 1.8mm; }
body.compact .eyebrow { margin-bottom: 1.8mm; }
body.compact h1 { font-size: 20pt; }
body.compact .titre { font-size: 9.6pt; margin-top: 2mm; }
body.compact .meta-row { margin-top: 2.6mm; }
body.compact .corps { padding-top: 4mm; gap: 6mm; }
body.compact main h2 { margin-bottom: 2.4mm; padding-top: 1.8mm; }
body.compact main h2 .h { font-size: 10pt; }
body.compact .timeline li { padding-bottom: 1.4mm; }
body.compact .timeline .rt { font-size: 8.1pt; }
body.compact .exp .poste { font-size: 8.3pt; }
body.compact .timeline .detail, body.compact .exp ul li { font-size: 7.1pt; line-height: 1.28; }
body.compact .exp > li { margin-bottom: 1.7mm; }
body.compact .form-item { margin-bottom: 1.8mm; }
body.compact .form-item .t { font-size: 7.4pt; }
body.compact main section + section { margin-top: 3mm; }
body.compact .cell { padding: 2.8mm 3.2mm 3.2mm; }
body.compact footer { padding: 2mm 0 3mm; }

/* Profils très chargés : réduction homothétique (~6 %) pour tenir la page A4.
   zoom (et non transform) : la pagination d'impression suit la taille de layout. */
body.dense { zoom: .94; width: calc(210mm / .94); min-height: calc(295mm / .94); }
`;

function densite(cv) {
  return cv.realisations.length + cv.experiences.reduce((n, e) => n + e.points.length, 0);
}

function html(cv) {
  const d = densite(cv);
  const compact = d > 18 ? ' class="compact dense"' : d > 15 ? ' class="compact"' : '';
  return `<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>CV FT2E — ${esc(cv.prenom)} ${esc(cv.nom)}</title>
<style>${css}</style>
</head>
<body${compact}>
  <header>
    <div class="cartouche-top mono-label">
      <span class="ft2e">FT2E</span>
      <span class="bl">ingénierie fluide · thermique · énergie · électricité</span>
    </div>
    <p class="eyebrow mono-label">curriculum vitæ — équipe ft2e, la rochelle</p>
    <h1>${esc(cv.prenom)} ${esc(cv.nom)}</h1>
    <p class="titre">${esc(cv.titre)}</p>
    <p class="fonction">${esc(cv.fonction)}</p>
    <div class="meta-row">
      <span class="meta-exp mono-label">${esc(cv.experience)}</span>
      ${cv.statut ? `<span class="chip mono-label">${esc(cv.statut)}</span>` : ''}
    </div>
  </header>

  <div class="corps">
    <aside>
      <span class="coin tl"></span><span class="coin br"></span>
      <div class="cartouche">
        <div class="cell">
          <h2 class="mono-label">Contact</h2>
          ${cv.contact.map(([k, v]) => `<div class="contact-row"><span class="k mono-label">${esc(k)}</span><span class="v">${esc(v)}</span></div>`).join('\n          ')}
        </div>
        <div class="cell">
          <h2 class="mono-label">Formation</h2>
          ${cv.formations.map((f) => `<div class="form-item"><span class="annee mono-label">${esc(f.annee)}</span><p class="t">${esc(f.titre)}</p>${f.lieu ? `<p class="l">${esc(f.lieu)}</p>` : ''}</div>`).join('\n          ')}
        </div>
        <div class="cell">
          <h2 class="mono-label">Logiciels</h2>
          <div class="chips">
            ${cv.logiciels.map((l) => `<span class="mono-label">${esc(l)}</span>`).join('\n            ')}
          </div>
        </div>
      </div>
    </aside>

    <main>
      <section>
        <h2><span class="h">Réalisations</span><span class="a mono-label">références récentes</span></h2>
        <ul class="timeline">
          ${cv.realisations.map((r) => `<li><span class="annee mono-label">${esc(r.annee)}</span><p class="rt">${esc(r.titre)}</p><p class="lieu">${esc(r.lieu)}</p><p class="detail">${esc(r.detail)}</p></li>`).join('\n          ')}
        </ul>
      </section>
      <section>
        <h2><span class="h">Expériences</span><span class="a mono-label">parcours</span></h2>
        <ul class="exp">
          ${cv.experiences.map((e) => `<li><span class="periode mono-label">${esc(e.periode)}</span><p class="poste">${esc(e.poste)}</p><p class="org">${esc(e.org)}</p><ul>${e.points.map((p) => `<li>${esc(p)}</li>`).join('')}</ul></li>`).join('\n          ')}
        </ul>
      </section>
    </main>
  </div>

  <footer>
    <span class="mono-label">ft2e — bureau d’études techniques · la rochelle</span>
    <span class="mono-label">édition août 2026</span>
  </footer>
</body>
</html>`;
}

for (const cv of cvs) {
  const file = resolve(outDir, `CV-FT2E-${cv.slug}.html`);
  writeFileSync(file, html(cv), 'utf8');
  console.log(`OK ${file}`);
}
