// build/word.json (+ cover images) -> ثرائد-التقوى.docx : Word edition with real footnotes at the foot of each page
const fs = require("fs"), path = require("path");
let D;
try { D = require("docx"); } catch { D = require("/opt/node22/lib/node_modules/docx"); }
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Footer, PageNumber, AlignmentType, HeadingLevel, TableOfContents,
  FootnoteReferenceRun, HorizontalPositionRelativeFrom, VerticalPositionRelativeFrom, TextWrappingType, NumberFormat, NoteNumberRestart, CharacterSet, BorderStyle, TabStopType, PageBreak,
} = D;

const HERE = __dirname;
const OUT = path.join(HERE, "ثرائد-التقوى.docx");
const data = JSON.parse(fs.readFileSync(path.join(HERE, "build", "word.json"), "utf8"));
const mm = v => Math.round(v * 56.6929);            // mm -> twips
const TEAL = "0C5D63", GOLD = "A9812F", INK = "1D1A16";
const BODY = "Amiri", QURAN = "Amiri Quran";

const footnotes = {};
let fnCount = 0;
const AR = s => String(s).replace(/[0-9]/g, d => "٠١٢٣٤٥٦٧٨٩"[d]);

function tr(text, o = {}) {
  return new TextRun({
    text, font: o.font || BODY, size: o.size || 26, color: o.color || INK,
    bold: !!o.bold, boldComplexScript: !!o.bold, rightToLeft: true, language: { value: "ar-SA", bidirectional: "ar-SA" },
  });
}

function inline(runs, base = {}) {
  const out = [];
  for (const r of runs) {
    if (r.fn !== undefined) {
      fnCount += 1;
      footnotes[fnCount] = { children: [new Paragraph({ bidirectional: true, children: [tr(r.fn, { size: 19, color: "3B342C" })] })] };
      out.push(new FootnoteReferenceRun(fnCount));
      continue;
    }
    if (!r.t) continue;
    if (r.k === "a") out.push(tr(r.t, { font: QURAN, size: 24, color: "111111" }));
    else if (r.k === "b") out.push(tr(r.t, { ...base, bold: true, color: TEAL }));
    else out.push(tr(r.t, base));
  }
  return out;
}

const children = [];
const para = (runs, o = {}) => new Paragraph({
  bidirectional: true, alignment: o.align || AlignmentType.BOTH, children: runs,
  spacing: { before: o.before || 0, after: o.after === undefined ? 100 : o.after, line: o.line || 400 },
  indent: o.indent, keepNext: !!o.keepNext, pageBreakBefore: !!o.pageBreak, heading: o.heading, border: o.border,
  outlineLevel: o.outline,
});

// ------------------------------------------------------------------ covers
function coverSection(file, blankFooter) {
  const img = fs.readFileSync(path.join(HERE, file));
  return {
    properties: { page: { size: { width: mm(170), height: mm(240) }, margin: { top: 0, bottom: 0, left: 0, right: 0, header: 0, footer: 0 } } },
    footers: blankFooter ? { default: new Footer({ children: [new Paragraph({})] }) } : undefined,
    children: [new Paragraph({ spacing: { after: 0, line: 240 }, children: [new ImageRun({
      type: "png", data: img, transformation: { width: 642, height: 907 },
      floating: {
        horizontalPosition: { relative: HorizontalPositionRelativeFrom.PAGE, offset: 0 },
        verticalPosition: { relative: VerticalPositionRelativeFrom.PAGE, offset: 0 },
        behindDocument: true, allowOverlap: true, wrap: { type: TextWrappingType.NONE },
      } })] })],
  };
}

// ------------------------------------------------------------------ front pages
children.push(new Paragraph({ bidirectional: true, alignment: AlignmentType.CENTER, spacing: { before: 2600, after: 600 }, children: [tr("۞", { size: 60, color: GOLD })] }));
children.push(para([tr("ثرائد التقوى", { font: BODY, size: 96, bold: true, color: TEAL })], { align: AlignmentType.CENTER, after: 300 }));
children.push(para([tr("تأليف", { size: 26, color: "6B5F50" })], { align: AlignmentType.CENTER, after: 80 }));
children.push(para([tr("محمّد عبدالله", { size: 52, bold: true, color: INK })], { align: AlignmentType.CENTER, after: 0 }));
children.push(para([tr("بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ", { font: QURAN, size: 60, color: TEAL })], { align: AlignmentType.CENTER, after: 500, pageBreak: true, before: 2600 }));
for (const l of ["الحمد لله ربّ العالمين", "والصّلاة والسّلام على المبعوث رحمةً للعالمين", "محمّدٍ وآله الطّيّبين الطّاهرين"])
  children.push(para([tr(l, { size: 30 })], { align: AlignmentType.CENTER, after: 120 }));

// ------------------------------------------------------------------ chapters
for (const ch of data) {
  children.push(new Paragraph({
    heading: HeadingLevel.HEADING_1, bidirectional: true, alignment: AlignmentType.CENTER, pageBreakBefore: true, keepNext: true,
    spacing: { before: 0, after: 220 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: GOLD, space: 6 } },
    children: [tr(ch.title, { size: 38, bold: true, color: TEAL })],
  }));
  for (const b of ch.blocks) {
    const R = b.runs;
    switch (b.type) {
      case "h3":
        children.push(para(inline(R, { size: 27, bold: true, color: TEAL }).map(x => x), { align: AlignmentType.START, keepNext: true, after: 80, indent: { start: 0 } }));
        break;
      case "li":
        children.push(para([tr("۞ ", { font: QURAN, size: 20, color: GOLD }), ...inline(R)], { indent: { start: 340, hanging: 340 }, after: 80 }));
        break;
      case "verse":
        children.push(para(inline(R), { align: AlignmentType.CENTER, after: 120 }));
        break;
      case "quote":
        children.push(para(inline(R), { indent: { start: 280, end: 280 } }));
        break;
      case "ded":
        children.push(para(inline(R), { align: AlignmentType.CENTER, after: 0, line: 380 }));
        break;
      case "bib":
        children.push(para(inline(R), { align: AlignmentType.START, indent: { start: 340, hanging: 340 }, after: 60, line: 340 }));
        break;
      case "end":
        children.push(para(inline(R, { bold: true, color: TEAL }), { align: AlignmentType.CENTER, after: 0 }));
        break;
      default:
        children.push(para(inline(R), { indent: { firstLine: 340 } }));
    }
  }
}

// ------------------------------------------------------------------ table of contents (at the end)
children.push(new Paragraph({
  bidirectional: true, alignment: AlignmentType.CENTER, pageBreakBefore: true, spacing: { after: 220 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: GOLD, space: 6 } },
  children: [tr("الفهرس", { size: 38, bold: true, color: TEAL })],
}));
children.push(new TableOfContents("الفهرس", { hyperlink: true, headingStyleRange: "1-1" }));

const footer = new Footer({
  children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], font: BODY, size: 22, color: TEAL, rightToLeft: true })] })],
});

const bodySection = {
  properties: {
    page: {
      size: { width: mm(170), height: mm(240) },
      margin: { top: mm(23), bottom: mm(24), left: mm(19), right: mm(19), header: mm(10), footer: mm(10) },
      pageNumbers: { start: 1, formatType: NumberFormat.HINDI_NUMBERS },
    },
    footnotePr: { numberFormat: NumberFormat.HINDI_NUMBERS, numberRestart: NoteNumberRestart.EACH_PAGE },
    bidi: true,
  },
  footers: { default: footer },
  children,
};

const doc = new Document({
  creator: "محمد عبدالله", title: "ثرائد التقوى", description: "ثرائد التقوى — محمد عبدالله",
  features: { updateFields: true },
  fonts: [
    { name: "Amiri", data: fs.readFileSync(path.join(HERE, "build", "ttf", "Amiri-Regular.ttf")), characterSet: CharacterSet.ARABIC },
    { name: "Amiri Quran", data: fs.readFileSync(path.join(HERE, "build", "ttf", "AmiriQuran-Regular.ttf")), characterSet: CharacterSet.ARABIC },
  ],
  styles: {
    default: {
      document: { run: { font: BODY, size: 26, color: INK, rightToLeft: true }, paragraph: { spacing: { line: 400 } } },
      heading1: { run: { font: BODY, size: 38, bold: true, color: TEAL }, paragraph: { spacing: { before: 0, after: 220 } } },
    },
    paragraphStyles: [
      { id: "FootnoteText", name: "footnote text", basedOn: "Normal", run: { size: 19, color: "3B342C" }, paragraph: { spacing: { line: 300, after: 20 } } },
      { id: "TOC1", name: "toc 1", basedOn: "Normal", next: "Normal", run: { size: 24 }, paragraph: { spacing: { line: 340, after: 40 } } },
    ],
  },
  footnotes,
  sections: [coverSection("غلاف-أمامي.png"), bodySection, coverSection("غلاف-خلفي.png", true)],
});

const JSZip = require("jszip");
Packer.toBuffer(doc).then(async buf => {
  // the footnote numbering (Arabic-Indic digits, restarting on every page) and the right-to-left section live in the section properties
  const zip = await JSZip.loadAsync(buf);
  let xml = await zip.file("word/document.xml").async("string");
  xml = xml.replace(/(<w:sectPr>(?:(?!<\/w:sectPr>).)*?<w:footerReference [^>]*\/>)/s,
    '$1<w:footnotePr><w:numFmt w:val="hindiNumbers"/><w:numRestart w:val="eachPage"/></w:footnotePr>');
  xml = xml.replace(/(<w:sectPr><w:footerReference(?:(?!<\/w:sectPr>).)*?)(<w:docGrid)/s, '$1<w:bidi/>$2');
  zip.file("word/document.xml", xml);
  const out = await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" });
  fs.writeFileSync(OUT, out);
  console.log("docx:", OUT, Math.round(out.length / 1024), "KB", "footnotes:", fnCount, "patched:", xml.includes('w:numRestart'), xml.includes('<w:bidi/>'));
});
