// Génère les CV DOCX au design system « Ingénierie de l'invisible ».
// Usage : node scripts/cv-rebrand/generate-docx.mjs
// Nota : les polices Archivo et IBM Plex Mono doivent être installées sur le poste
// du lecteur pour un rendu fidèle ; à défaut, Word substitue des polices proches.
import { writeFileSync, mkdirSync } from 'node:fs';
import { resolve } from 'node:path';
import {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, BorderStyle, ShadingType, AlignmentType, TabStopType, LevelFormat,
} from 'docx';
import { cvs } from './data.mjs';

const C = {
  encre: '08131F', marine: '16324F', coolWhite: 'EDF0F2', paper: 'F7F9FA',
  slate: '4A6076', mist: '8FA2B4', copper: 'C46A38', brightCopper: 'E08A50',
  copperText: 'A04E20', line: '9AA9B8',
};
const ARCHIVO = 'Archivo';
const MONO = 'IBM Plex Mono';

const PAGE_W = 11906;                       // A4 en twips
const MARGIN = { top: 340, right: 500, bottom: 300, left: 500 };
const USABLE = PAGE_W - MARGIN.left - MARGIN.right; // 10906
const SIDEBAR_W = 3400;
const MAIN_W = USABLE - SIDEBAR_W;

// Profils très chargés : espacements et corps réduits pour tenir la page A4.
const isDense = (cv) =>
  cv.realisations.length + cv.experiences.reduce((n, e) => n + e.points.length, 0) > 18;

const noBorder = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };
const lineBorder = { style: BorderStyle.SINGLE, size: 6, color: C.slate };

// Runs -----------------------------------------------------------------------
const monoLabel = (text, { color = C.slate, size = 13, bold = true } = {}) =>
  new TextRun({ text: text.toUpperCase(), font: MONO, size, color, bold, characterSpacing: 20 });
const monoText = (text, { color = C.slate, size = 15 } = {}) =>
  new TextRun({ text, font: MONO, size, color });

// Paragraphes ----------------------------------------------------------------
const spacer = (after = 60) => new Paragraph({ children: [], spacing: { after } });

function headerCell(cv) {
  const children = [
    new Paragraph({
      tabStops: [{ type: TabStopType.RIGHT, position: USABLE - 500 }],
      spacing: { after: 60 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: C.mist } },
      children: [
        monoLabel('FT2E', { color: C.coolWhite, size: 17 }),
        new TextRun({ text: '\t' }),
        monoLabel('ingénierie fluide · thermique · énergie · électricité', { color: C.mist, size: 12, bold: false }),
      ],
    }),
    new Paragraph({
      spacing: { before: 140, after: 100 },
      children: [monoLabel('curriculum vitæ — équipe ft2e, la rochelle', { color: C.copper, size: 13 })],
    }),
    new Paragraph({
      spacing: { after: 40 },
      children: [new TextRun({
        text: `${cv.prenom} ${cv.nom}`.toUpperCase(),
        font: ARCHIVO, bold: true, size: 50, color: C.coolWhite, characterSpacing: -6,
      })],
    }),
    new Paragraph({
      spacing: { after: 60 },
      children: [new TextRun({ text: cv.titre.toUpperCase(), font: ARCHIVO, bold: true, size: 21, color: C.coolWhite })],
    }),
    new Paragraph({
      spacing: { after: 90 },
      children: [monoText(cv.fonction, { color: C.mist, size: 15 })],
    }),
    new Paragraph({
      children: [
        monoLabel(cv.experience, { color: C.mist, size: 13, bold: false }),
        ...(cv.statut ? [
          new TextRun({ text: '   ' }),
          monoLabel(`[ ${cv.statut} ]`, { color: C.brightCopper, size: 13 }),
        ] : []),
      ],
    }),
  ];

  return new Table({
    width: { size: USABLE, type: WidthType.DXA },
    columnWidths: [USABLE],
    borders: {
      ...noBorders,
      top: { style: BorderStyle.SINGLE, size: 24, color: C.copper },
      insideHorizontal: noBorder, insideVertical: noBorder,
    },
    rows: [new TableRow({
      children: [new TableCell({
        width: { size: USABLE, type: WidthType.DXA },
        shading: { type: ShadingType.CLEAR, fill: C.encre },
        margins: { top: 220, bottom: 260, left: 320, right: 320 },
        children,
      })],
    })],
  });
}

function sideTitle(text) {
  return new Paragraph({
    spacing: { before: 60, after: 90 },
    children: [
      new TextRun({ text: '■ ', color: C.copper, size: 13, font: MONO }),
      monoLabel(text, { color: C.slate, size: 13 }),
    ],
  });
}

function sidebarChildren(cv) {
  const out = [sideTitle('Contact')];
  for (const [k, v] of cv.contact) {
    out.push(new Paragraph({ spacing: { after: 10 }, children: [monoLabel(k, { color: C.slate, size: 11, bold: false })] }));
    out.push(new Paragraph({ spacing: { after: 70 }, children: [monoText(v, { color: C.marine, size: 16 })] }));
  }
  out.push(new Paragraph({
    spacing: { before: 60, after: 0 },
    border: { top: { style: BorderStyle.SINGLE, size: 4, color: C.line } },
    children: [],
  }));
  out.push(sideTitle('Formation'));
  for (const f of cv.formations) {
    out.push(new Paragraph({ spacing: { after: 14 }, children: [monoLabel(f.annee, { color: C.copperText, size: 13 })] }));
    out.push(new Paragraph({
      spacing: { after: f.lieu ? 14 : 80 },
      children: [new TextRun({ text: f.titre, font: ARCHIVO, size: 16, color: C.marine })],
    }));
    if (f.lieu) {
      out.push(new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: f.lieu, font: ARCHIVO, size: 14, color: C.slate })] }));
    }
  }
  out.push(new Paragraph({
    spacing: { before: 40, after: 0 },
    border: { top: { style: BorderStyle.SINGLE, size: 4, color: C.line } },
    children: [],
  }));
  out.push(sideTitle('Logiciels'));
  out.push(new Paragraph({
    spacing: { after: 0 },
    children: cv.logiciels.flatMap((l, i) => [
      ...(i ? [new TextRun({ text: '  ·  ', color: C.copper, size: 13, font: MONO })] : []),
      monoLabel(l, { color: C.slate, size: 12, bold: false }),
    ]),
  }));
  return out;
}

function sectionTitle(titre, annotation, dense = false) {
  return new Paragraph({
    spacing: { before: dense ? 60 : 120, after: dense ? 70 : 120 },
    border: { top: { style: BorderStyle.SINGLE, size: 8, color: C.copper } },
    children: [
      new TextRun({ text: titre.toUpperCase(), font: ARCHIVO, bold: true, size: 24, color: C.marine }),
      new TextRun({ text: '   ' }),
      monoLabel(annotation, { color: C.slate, size: 12, bold: false }),
    ],
  });
}

function mainChildren(cv) {
  const dense = isDense(cv);
  const titreSize = dense ? 17 : 18;
  const corpsSize = dense ? 15 : 16;
  const out = [sectionTitle('Réalisations', 'références récentes', dense)];
  for (const r of cv.realisations) {
    out.push(new Paragraph({
      spacing: { after: dense ? 4 : 8 },
      children: [
        new TextRun({ text: '■ ', color: C.copper, size: 13, font: MONO }),
        monoLabel(r.annee, { color: C.copperText, size: 13 }),
      ],
    }));
    out.push(new Paragraph({
      indent: { left: 200 },
      spacing: { after: dense ? 3 : 6 },
      children: [new TextRun({ text: r.titre.toUpperCase(), font: ARCHIVO, bold: true, size: titreSize, color: C.marine })],
    }));
    out.push(new Paragraph({
      indent: { left: 200 },
      spacing: { after: dense ? 3 : 6 },
      children: [monoText(r.lieu, { color: C.slate, size: 13 })],
    }));
    out.push(new Paragraph({
      indent: { left: 200 },
      spacing: { after: dense ? 45 : 90 },
      children: [new TextRun({ text: r.detail, font: ARCHIVO, size: corpsSize, color: C.slate })],
    }));
  }

  out.push(sectionTitle('Expériences', 'parcours', dense));
  for (const e of cv.experiences) {
    out.push(new Paragraph({ spacing: { after: dense ? 4 : 8 }, children: [monoLabel(e.periode, { color: C.copperText, size: 13 })] }));
    out.push(new Paragraph({
      spacing: { after: dense ? 3 : 6 },
      children: [new TextRun({ text: e.poste.toUpperCase(), font: ARCHIVO, bold: true, size: titreSize, color: C.marine })],
    }));
    out.push(new Paragraph({ spacing: { after: dense ? 16 : 30 }, children: [monoText(e.org, { color: C.slate, size: 13 })] }));
    for (const p of e.points) {
      out.push(new Paragraph({
        numbering: { reference: 'puces', level: 0 },
        spacing: { after: dense ? 8 : 16 },
        children: [new TextRun({ text: p, font: ARCHIVO, size: corpsSize, color: C.slate })],
      }));
    }
    out.push(spacer(dense ? 35 : 70));
  }
  return out;
}

function corps(cv) {
  return new Table({
    width: { size: USABLE, type: WidthType.DXA },
    columnWidths: [SIDEBAR_W, MAIN_W],
    borders: { ...noBorders, insideHorizontal: noBorder, insideVertical: noBorder },
    rows: [new TableRow({
      children: [
        new TableCell({
          width: { size: SIDEBAR_W, type: WidthType.DXA },
          shading: { type: ShadingType.CLEAR, fill: C.paper },
          borders: { top: lineBorder, bottom: lineBorder, left: lineBorder, right: lineBorder },
          margins: { top: 180, bottom: 200, left: 200, right: 200 },
          children: sidebarChildren(cv),
        }),
        new TableCell({
          width: { size: MAIN_W, type: WidthType.DXA },
          margins: { top: 0, bottom: 0, left: 260, right: 0 },
          children: mainChildren(cv),
        }),
      ],
    })],
  });
}

function footer() {
  return new Paragraph({
    spacing: { before: 160 },
    border: { top: { style: BorderStyle.SINGLE, size: 4, color: C.line } },
    tabStops: [{ type: TabStopType.RIGHT, position: USABLE }],
    children: [
      monoLabel('ft2e — bureau d’études techniques · la rochelle', { color: C.slate, size: 11, bold: false }),
      new TextRun({ text: '\t' }),
      monoLabel('édition août 2026', { color: C.slate, size: 11, bold: false }),
    ],
  });
}

async function build(cv) {
  const doc = new Document({
    numbering: {
      config: [{
        reference: 'puces',
        levels: [{
          level: 0,
          format: LevelFormat.BULLET,
          text: '–',
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 260, hanging: 160 } }, run: { color: C.copperText, font: MONO } },
        }],
      }],
    },
    styles: { default: { document: { run: { font: ARCHIVO, size: 16, color: C.slate } } } },
    sections: [{
      properties: { page: { size: { width: PAGE_W, height: 16838 }, margin: MARGIN } },
      children: [headerCell(cv), spacer(120), corps(cv), footer()],
    }],
  });
  return Packer.toBuffer(doc);
}

const outDir = resolve('livrables/cv-ft2e');
mkdirSync(outDir, { recursive: true });
for (const cv of cvs) {
  const buf = await build(cv);
  const file = resolve(outDir, `CV-FT2E-${cv.slug}.docx`);
  writeFileSync(file, buf);
  console.log(`OK ${file}`);
}
