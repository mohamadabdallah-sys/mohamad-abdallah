const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa");
const gi = require("react-icons/gi");
const { applyTheme } = require("/root/.claude/skills/synced/3ca34b4b-c007-4210-8145-41afb9720412_ed11fd95-a5df-4aff-94b2-dbf012f463d6/pptx/scripts/apply_theme.js");

const P = {
  bg: "0B1026", card: "161E40", card2: "1E2852", line: "2C3768",
  text: "F8FAFC", muted: "A5B1CC", gold: "FBBF24",
  ke: "3B82F6", pe: "A78BFA", me: "2DD4BF", w: "FB7185", pw: "FB923C", g: "4ADE80",
};
const THEME = {
  name: "Energy Night", headFontFace: "Arial", bodyFontFace: "Arial",
  colors: { dk1: P.bg, lt1: "FFFFFF", dk2: P.card, lt2: P.muted,
    accent1: P.ke, accent2: P.pe, accent3: P.me, accent4: P.w, accent5: P.pw, accent6: P.g,
    hlink: P.gold, folHlink: P.pe },
};
const F = "Arial";

async function icon(Comp, color, size = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { color: "#" + color, size: String(size) }));
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}
async function bg(color, color2 = P.gold) {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">
  <defs>
   <radialGradient id="a" cx="0.02" cy="0.0" r="0.75"><stop offset="0" stop-color="#${color}" stop-opacity="0.38"/><stop offset="1" stop-color="#${color}" stop-opacity="0"/></radialGradient>
   <radialGradient id="b" cx="1" cy="1" r="0.6"><stop offset="0" stop-color="#${color2}" stop-opacity="0.12"/><stop offset="1" stop-color="#${color2}" stop-opacity="0"/></radialGradient>
   <pattern id="d" width="48" height="48" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.6" fill="#ffffff" fill-opacity="0.06"/></pattern>
  </defs>
  <rect width="1920" height="1080" fill="#${P.bg}"/><rect width="1920" height="1080" fill="url(#d)"/>
  <rect width="1920" height="1080" fill="url(#a)"/><rect width="1920" height="1080" fill="url(#b)"/></svg>`;
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// RTL Arabic text helper
function ar(slide, text, o) {
  slide.addText(text, Object.assign({ isTextBox: true, fontFace: F, rtlMode: true, align: "right", lang: "ar-SA", color: P.text, margin: 0, valign: "middle" }, o));
}
function ltr(slide, text, o) {
  slide.addText(text, Object.assign({ isTextBox: true, fontFace: F, color: P.text, margin: 0, valign: "middle" }, o));
}
function card(slide, x, y, w, h, fill = P.card, extra = {}) {
  slide.addShape("roundRect", Object.assign({ x, y, w, h, rectRadius: 0.14, fill: { color: fill }, line: { color: fill, width: 0 },
    shadow: { type: "outer", color: "000000", opacity: 0.35, blur: 10, offset: 3, angle: 90 } }, extra));
}
function circle(slide, x, y, d, color, extra = {}) {
  slide.addShape("ellipse", Object.assign({ x, y, w: d, h: d, fill: { color }, line: { color, width: 0 } }, extra));
}
function arrow(slide, x1, y1, x2, y2, color, width = 2, dash) {
  const o = { x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.max(Math.abs(x2 - x1), 0.001), h: Math.max(Math.abs(y2 - y1), 0.001),
    line: { color, width, endArrowType: "triangle" } };
  if (dash) o.line.dashType = dash;
  if (x2 < x1) o.flipH = true;
  if (y2 < y1) o.flipV = true;
  slide.addShape("line", o);
}
function iconCircle(slide, img, x, y, d, color, pad = 0.22) {
  circle(slide, x, y, d, color);
  slide.addImage({ data: img, x: x + d * pad, y: y + d * pad, w: d * (1 - 2 * pad), h: d * (1 - 2 * pad) });
}

const LESSONS = [
  { key: "ke", name: "الطاقة الحركية", color: P.ke, ic: fa.FaCarSide,
    def: "هي الطاقة التي يملكها الجسم لأنه يتحرك.",
    pts: ["كلما زادت السرعة أو الكتلة زادت الطاقة الحركية.", "الجسم الساكن طاقته الحركية صفر."],
    ex: "مثال: كتلة 2 كغ وسرعة 3 م/ث", sol: "KE = ½ × 2 × 3² = 9 J",
    f: "KE = ½ × m × v²", units: "الكتلة m بالكغ • السرعة v بالم/ث • الوحدة: جول",
    life: "السيارة السريعة تحتاج مسافة أطول لتتوقف، لذلك نلتزم بحدود السرعة.", lifeIc: fa.FaTachometerAlt, unit: "J جول" },
  { key: "pe", name: "الطاقة الكامنة", color: P.pe, ic: fa.FaMountain,
    def: "هي الطاقة المخزنة في الجسم بسبب ارتفاعه.",
    pts: ["كلما زاد الارتفاع زادت الطاقة الكامنة.", "عند سقوط الجسم تتحول إلى طاقة حركية."],
    ex: "مثال: كتلة 2 كغ وارتفاع 5 م", sol: "PE = 2 × 10 × 5 = 100 J",
    f: "PE = m × g × h", units: "g ≈ 10 • الارتفاع h بالمتر • الوحدة: جول",
    life: "الماء المحجوز خلف السدّ يملك طاقة كامنة تتحول إلى كهرباء.", lifeIc: gi.GiDam, unit: "J جول" },
  { key: "me", name: "الطاقة الميكانيكية", color: P.me, ic: fa.FaSync,
    def: "هي مجموع الطاقة الحركية والطاقة الكامنة.",
    pts: ["أثناء الحركة تتحول الطاقة من شكل إلى آخر.", "بدون احتكاك تبقى الطاقة الميكانيكية ثابتة."],
    ex: "مثال: حركية 30 جول وكامنة 20 جول", sol: "ME = 30 + 20 = 50 J",
    f: "ME = KE + PE", units: "الميكانيكية = الحركية + الكامنة",
    life: "الأفعوانية: طاقة كامنة كبيرة في القمة، وحركية كبيرة في القاع.", lifeIc: fa.FaRoute, unit: "J جول" },
  { key: "w", name: "الشغل", color: P.w, ic: gi.GiPush,
    def: "يُبذل شغل عندما تحرك قوة جسماً لمسافة.",
    pts: ["إذا لم يتحرك الجسم فلا يوجد شغل.", "كلما زادت القوة أو المسافة زاد الشغل."],
    ex: "مثال: قوة 10 نيوتن ومسافة 3 م", sol: "W = 10 × 3 = 30 J",
    f: "W = F × d", units: "القوة F بالنيوتن • المسافة d بالمتر • الوحدة: جول",
    life: "رفع صندوق أو دفع سيارة معطلة: قوة أكبر ومسافة أكبر = شغل أكبر.", lifeIc: fa.FaBox, unit: "J جول" },
  { key: "pw", name: "القدرة", color: P.pw, ic: fa.FaBolt,
    def: "هي سرعة إنجاز الشغل.",
    pts: ["القدرة الأكبر تنجز نفس الشغل في زمن أقل.", "1 واط = 1 جول في كل ثانية."],
    ex: "مثال: شغل 100 جول خلال 5 ث", sol: "P = 100 ÷ 5 = 20 W",
    f: "P = W ÷ t", units: "الشغل W بالجول • الزمن t بالثانية • الوحدة: واط",
    life: "مصباح 100 واط يستهلك الطاقة أسرع من مصباح LED بقدرة 10 واط.", lifeIc: fa.FaLightbulb, unit: "W واط" },
  { key: "g", name: "قوة الجاذبية", color: P.g, ic: fa.FaGlobeAfrica,
    def: "الجاذبية قوة تجذب الأجسام نحو الأرض.",
    pts: ["بسببها تسقط الأجسام ولا نطير في الهواء.", "وزن الجسم هو قوة جذب الأرض له."],
    ex: "مثال: كتلة جسم 5 كغ", sol: "W = 5 × 10 = 50 N",
    f: "W = m × g", units: "الوزن = الكتلة × g • الوحدة: نيوتن (g ≈ 10)",
    life: "الجاذبية تُسقط المظلّي نحو الأرض وتُبقي القمر يدور حول الأرض.", lifeIc: gi.GiParachute, unit: "N نيوتن" },
];

(async () => {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.rtlMode = true;
  pres.title = "الطاقة والشغل";
  pres.theme = { headFontFace: F, bodyFontFace: F };

  const IC = {};
  for (const L of LESSONS) {
    IC[L.key] = await icon(L.ic, P.bg);
    IC[L.key + "c"] = await icon(L.ic, L.color);
    IC[L.key + "life"] = await icon(L.lifeIc, P.bg);
    L.bg = await bg(L.color);
  }
  const iBolt = await icon(fa.FaBolt, P.gold), iBoltDark = await icon(fa.FaBolt, P.bg);
  const iCheck = await icon(fa.FaCheck, P.bg), iTimes = await icon(fa.FaTimes, P.bg);
  const iPencil = await icon(fa.FaPencilAlt, P.bg), iRecycle = await icon(fa.FaRecycle, P.gold);
  const iInfo = await icon(fa.FaInfoCircle, P.bg);
  IC.pwRun = await icon(fa.FaRunning, P.pw); IC.pwWalk = await icon(fa.FaWalking, P.muted);
  IC.gEarth = await icon(gi.GiEarthAfricaEurope, "60A5FA");
  const bgGold = await bg(P.gold, P.ke), bgTeal = await bg(P.me, P.pe);

  // ---------- 1. Cover ----------
  pres.addSection({ title: "المقدمة" });
  let s = pres.addSlide({ sectionTitle: "المقدمة" });
  s.background = { data: bgGold };
  // energy orb (left)
  circle(s, 0.55, 0.95, 3.7, P.gold, { fill: { color: P.gold, transparency: 92 }, line: { color: P.gold, width: 1, transparency: 60 } });
  circle(s, 0.95, 1.35, 2.9, P.gold, { fill: { color: P.gold, transparency: 85 }, line: { color: P.gold, width: 1, transparency: 40 } });
  circle(s, 1.4, 1.8, 2.0, P.gold);
  s.addImage({ data: iBoltDark, x: 1.85, y: 2.25, w: 1.1, h: 1.1 });
  // orbiting lesson dots
  const orb = [[0.62, 1.4], [3.7, 1.05], [4.15, 2.6], [3.65, 4.1], [0.75, 4.0], [0.35, 2.65]];
  LESSONS.forEach((L, i) => iconCircle(s, IC[L.key], orb[i][0], orb[i][1], 0.5, L.color));
  ar(s, "ملف الفيزياء • الصف الثامن", { x: 5.0, y: 0.75, w: 4.5, h: 0.35, fontSize: 14, bold: true, color: P.gold });
  ar(s, "الطاقة والشغل", { x: 4.75, y: 1.1, w: 4.8, h: 1.0, fontSize: 42, bold: true });
  ar(s, "افهم، احسب، وطبّق في حياتك اليومية", { x: 4.8, y: 2.15, w: 4.7, h: 0.45, fontSize: 18, color: P.muted });
  LESSONS.forEach((L, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = 7.3 - col * 2.4, y = 2.95 + row * 0.62;
    s.addShape("roundRect", { x, y, w: 2.25, h: 0.5, rectRadius: 0.25, fill: { color: P.card }, line: { color: L.color, width: 1.25 } });
    iconCircle(s, IC[L.key], x + 1.8, y + 0.07, 0.36, L.color);
    ar(s, L.name, { x: x + 0.08, y, w: 1.66, h: 0.5, fontSize: 13, bold: true });
  });
  s.addNotes("مقدمة: سنتعرف اليوم على ستة مفاهيم مترابطة: الطاقة الحركية، الكامنة، الميكانيكية، الشغل، القدرة، والجاذبية.");

  // ---------- 2. Concept map ----------
  s = pres.addSlide({ sectionTitle: "المقدمة" });
  s.background = { data: bgGold };
  ar(s, "خريطة المفاهيم", { x: 3.5, y: 0.3, w: 6.05, h: 0.6, fontSize: 32, bold: true });
  ar(s, "كيف ترتبط المفاهيم الستة ببعضها؟", { x: 3.5, y: 0.88, w: 6.05, h: 0.32, fontSize: 14, color: P.gold });
  const node = (L, x, y, f) => {
    card(s, x, y, 2.4, 0.82, P.card, { line: { color: L.color, width: 1.5 } });
    iconCircle(s, IC[L.key], x + 1.8, y + 0.15, 0.52, L.color);
    ar(s, L.name, { x: x + 0.08, y: y + 0.08, w: 1.65, h: 0.38, fontSize: 13, bold: true });
    ltr(s, f, { x: x + 0.08, y: y + 0.45, w: 1.65, h: 0.3, fontSize: 12, bold: true, color: L.color, align: "right" });
  };
  const [KE, PE, ME, W, PW, G] = LESSONS;
  node(W, 7.15, 2.55, W.f); node(PW, 7.15, 1.4, PW.f); node(G, 7.15, 3.95, G.f);
  node(KE, 3.8, 1.75, KE.f); node(PE, 3.8, 3.35, PE.f); node(ME, 0.45, 2.55, ME.f);
  arrow(s, 8.4, 2.55, 8.4, 2.25, P.muted, 1.75);
  arrow(s, 7.15, 2.85, 6.2, 2.2, P.muted, 1.75);
  arrow(s, 7.15, 3.1, 6.2, 3.7, P.muted, 1.75);
  arrow(s, 7.15, 4.35, 6.2, 3.95, P.muted, 1.75, "dash");
  arrow(s, 3.8, 2.2, 2.85, 2.85, P.muted, 1.75);
  arrow(s, 3.8, 3.75, 2.85, 3.1, P.muted, 1.75);
  ar(s, "يُنجز بسرعة", { x: 8.5, y: 2.25, w: 1.05, h: 0.3, fontSize: 10, color: P.muted });
  ar(s, "ينقل الطاقة", { x: 6.2, y: 2.82, w: 1.0, h: 0.3, fontSize: 10, color: P.muted, align: "center" });
  ar(s, "الوزن يرفع الكامنة", { x: 5.75, y: 4.42, w: 1.3, h: 0.3, fontSize: 10, color: P.muted, align: "center" });
  ar(s, "مجموعهما", { x: 2.8, y: 2.82, w: 1.05, h: 0.3, fontSize: 10, color: P.muted, align: "center" });
  ar(s, "تتحول الكامنة إلى حركية والعكس", { x: 3.6, y: 4.25, w: 2.4, h: 0.3, fontSize: 11, color: P.gold, align: "center" });
  s.addShape("line", { x: 4.25, y: 2.62, w: 0.001, h: 0.68, line: { color: P.gold, width: 1.5, beginArrowType: "triangle", endArrowType: "triangle" } });
  s.addNotes("الشغل هو طريقة نقل الطاقة إلى الجسم، فيكسب طاقة حركية أو كامنة، ومجموعهما هو الطاقة الميكانيكية. القدرة تقيس سرعة إنجاز الشغل، والجاذبية مسؤولة عن الوزن الذي يحدد الطاقة الكامنة.");

  // ---------- 3-8. Lessons ----------
  pres.addSection({ title: "الدروس" });
  LESSONS.forEach((L, i) => {
    const s = pres.addSlide({ sectionTitle: "الدروس" });
    s.background = { data: L.bg };
    // header
    circle(s, 8.95, 0.32, 0.62, L.color);
    ltr(s, String(i + 1), { x: 8.95, y: 0.32, w: 0.62, h: 0.62, fontSize: 24, bold: true, color: P.bg, align: "center" });
    ar(s, L.name, { x: 3.6, y: 0.27, w: 5.2, h: 0.5, fontSize: 30, bold: true });
    ar(s, `الدرس ${i + 1} من 6`, { x: 3.6, y: 0.77, w: 5.2, h: 0.25, fontSize: 12, color: L.color, bold: true });
    // progress dots (lesson 1 at right)
    LESSONS.forEach((M, j) => {
      const x = 2.45 - j * 0.32;
      if (j === i) s.addShape("roundRect", { x: x - 0.12, y: 0.52, w: 0.36, h: 0.14, rectRadius: 0.07, fill: { color: M.color }, line: { color: M.color, width: 0 } });
      else circle(s, x, 0.52, 0.14, M.color, { fill: { color: M.color, transparency: 60 }, line: { color: M.color, width: 0, transparency: 60 } });
    });

    // right column
    const RX = 4.95, RW = 4.6;
    card(s, RX, 1.25, RW, 1.0, P.card);
    ar(s, "التعريف", { x: RX + 0.2, y: 1.33, w: RW - 0.4, h: 0.26, fontSize: 11, bold: true, color: L.color });
    ar(s, L.def, { x: RX + 0.2, y: 1.58, w: RW - 0.4, h: 0.6, fontSize: 15, bold: true });
    L.pts.forEach((p, k) => {
      const y = 2.35 + k * 0.42;
      circle(s, RX + RW - 0.3, y + 0.1, 0.18, L.color);
      ar(s, p, { x: RX + 0.05, y, w: RW - 0.45, h: 0.38, fontSize: 14, color: "E2E8F0" });
    });
    card(s, RX, 3.2, RW, 0.82, P.card2);
    iconCircle(s, iPencil, RX + RW - 0.62, 3.36, 0.5, L.color, 0.26);
    ar(s, L.ex, { x: RX + 0.2, y: 3.27, w: RW - 0.95, h: 0.3, fontSize: 12, color: P.muted });
    ltr(s, L.sol, { x: RX + 0.2, y: 3.56, w: RW - 0.95, h: 0.4, fontSize: 20, bold: true, color: L.color, align: "right" });

    // left column: illustration card + formula
    const LX = 0.45, LW = 4.3;
    card(s, LX, 1.25, LW, 1.8, P.card);
    drawIllustration(s, L, LX, 1.25, LW, 1.8, IC);
    card(s, LX, 3.2, LW, 0.82, L.color);
    ltr(s, L.f, { x: LX, y: 3.24, w: LW, h: 0.5, fontSize: 26, bold: true, color: P.bg, align: "center" });
    ar(s, L.units, { x: LX + 0.15, y: 3.72, w: LW - 0.3, h: 0.25, fontSize: 10, color: P.bg, align: "center" });

    // life strip
    card(s, 0.45, 4.22, 9.1, 0.85, P.card, { line: { color: L.color, width: 1, transparency: 50 } });
    iconCircle(s, IC[L.key + "life"], 8.88, 4.37, 0.55, L.color);
    ar(s, "من الحياة", { x: 7.5, y: 4.22, w: 1.25, h: 0.85, fontSize: 14, bold: true, color: L.color });
    ar(s, L.life, { x: 0.7, y: 4.22, w: 6.7, h: 0.85, fontSize: 14 });
    s.addNotes(`${L.name}: ${L.def} القانون: ${L.f}. ${L.ex} ← ${L.sol}.`);
  });

  function drawIllustration(s, L, x, y, w, h, IC) {
    const c = L.color, m = P.muted;
    if (L.key === "ke") {
      s.addImage({ data: IC.kec, x: x + 1.15, y: y + 0.35, w: 1.5, h: 1.1 });
      [0.6, 0.8, 1.0].forEach((dy, k) => s.addShape("line", { x: x + 0.35 + k * 0.1, y: y + dy, w: 0.6 - k * 0.1, h: 0.001, line: { color: m, width: 2, transparency: 30 } }));
      arrow(s, x + 2.85, y + 0.85, x + 3.95, y + 0.85, P.gold, 2.5);
      ltr(s, "v", { x: x + 3.2, y: y + 0.48, w: 0.4, h: 0.32, fontSize: 18, bold: true, italic: true, color: P.gold, align: "center" });
      s.addShape("line", { x: x + 0.3, y: y + 1.5, w: w - 0.6, h: 0.001, line: { color: P.line, width: 2.5 } });
      ar(s, "كتلة m تتحرك بسرعة v", { x: x + 0.3, y: y + 1.52, w: w - 0.6, h: 0.25, fontSize: 10, color: m, align: "center" });
    } else if (L.key === "pe") {
      s.addShape("line", { x: x + 0.4, y: y + 1.5, w: w - 0.8, h: 0.001, line: { color: P.line, width: 2.5 } });
      circle(s, x + 1.4, y + 0.18, 0.5, c);
      ltr(s, "m", { x: x + 1.4, y: y + 0.18, w: 0.5, h: 0.5, fontSize: 16, bold: true, color: P.bg, align: "center" });
      circle(s, x + 1.4, y + 1.0, 0.5, c, { fill: { color: c, transparency: 75 }, line: { color: c, width: 1, dashType: "dash" } });
      arrow(s, x + 1.65, y + 0.72, x + 1.65, y + 0.96, c, 1.5);
      s.addShape("line", { x: x + 2.4, y: y + 0.22, w: 0.001, h: 1.24, line: { color: P.gold, width: 2, dashType: "dash", beginArrowType: "triangle", endArrowType: "triangle" } });
      ltr(s, "h", { x: x + 2.5, y: y + 0.65, w: 0.4, h: 0.36, fontSize: 20, bold: true, italic: true, color: P.gold });
      ar(s, "كلما ارتفع زادت طاقته المخزنة", { x: x + 2.9, y: y + 0.55, w: 1.4, h: 0.6, fontSize: 10, color: m });
    } else if (L.key === "me") {
      s.addChart(pres.charts.BAR, [
        { name: "PE كامنة", labels: ["أعلى", "منتصف", "أسفل"], values: [50, 25, 0] },
        { name: "KE حركية", labels: ["أعلى", "منتصف", "أسفل"], values: [0, 25, 50] },
      ], { x: x + 0.15, y: y + 0.08, w: w - 0.3, h: h - 0.16, barDir: "col", barGrouping: "stacked", barGapWidthPct: 70,
        chartColors: [P.pe, P.ke], showLegend: true, legendPos: "r", legendColor: "E2E8F0", legendFontSize: 10, legendFontFace: "+mn-lt",
        showValue: false, catAxisLabelColor: "E2E8F0", catAxisLabelFontSize: 10, catAxisLabelFontFace: "+mn-lt",
        valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" }, catAxisLineShow: false,
        valAxisMaxVal: 55, showTitle: false });
    } else if (L.key === "w") {
      s.addShape("line", { x: x + 0.3, y: y + 1.2, w: w - 0.6, h: 0.001, line: { color: P.line, width: 2.5 } });
      s.addShape("roundRect", { x: x + 0.5, y: y + 0.5, w: 0.8, h: 0.7, rectRadius: 0.06, fill: { color: c }, line: { color: c, width: 0 } });
      s.addShape("roundRect", { x: x + 3.0, y: y + 0.5, w: 0.8, h: 0.7, rectRadius: 0.06, fill: { color: c, transparency: 80 }, line: { color: c, width: 1, dashType: "dash" } });
      arrow(s, x + 1.35, y + 0.85, x + 2.5, y + 0.85, P.gold, 3);
      ltr(s, "F", { x: x + 1.7, y: y + 0.45, w: 0.4, h: 0.35, fontSize: 18, bold: true, italic: true, color: P.gold, align: "center" });
      s.addShape("line", { x: x + 0.9, y: y + 1.45, w: 2.5, h: 0.001, line: { color: m, width: 1.5, beginArrowType: "triangle", endArrowType: "triangle" } });
      ltr(s, "d", { x: x + 1.95, y: y + 1.47, w: 0.4, h: 0.3, fontSize: 16, bold: true, italic: true, color: m, align: "center" });
    } else if (L.key === "pw") {
      ar(s, "نفس الشغل W", { x: x + 0.2, y: y + 0.08, w: w - 0.4, h: 0.3, fontSize: 12, bold: true, align: "center" });
      const rows = [[fa.FaWalking, "10 ث", 2.4, "قدرة صغيرة", 0.48], [fa.FaRunning, "5 ث", 1.5, "قدرة كبيرة", 1.1]];
      rows.forEach(([ic, t, bw, lbl, dy], k) => {
        s.addImage({ data: k ? IC.pwRun : IC.pwWalk, x: x + w - 0.68, y: y + dy, w: 0.45, h: 0.45 });
        s.addShape("roundRect", { x: x + w - 0.8 - bw, y: y + dy + 0.06, w: bw, h: 0.33, rectRadius: 0.08, fill: { color: k ? c : P.line }, line: { color: k ? c : P.line, width: 0 } });
        ar(s, t, { x: x + w - 0.8 - bw, y: y + dy + 0.06, w: bw - 0.1, h: 0.33, fontSize: 12, bold: true, color: k ? P.bg : P.text });
        ar(s, lbl, { x: x + 0.15, y: y + dy + 0.06, w: w - 1.05 - bw, h: 0.33, fontSize: 11, color: k ? c : m, bold: !!k });
      });
    } else if (L.key === "g") {
      s.addImage({ data: IC.gEarth, x: x + 0.5, y: y + 0.18, w: 1.2, h: 1.2 });
      circle(s, x + 3.3, y + 0.2, 0.42, P.w);
      ltr(s, "m", { x: x + 3.3, y: y + 0.2, w: 0.42, h: 0.42, fontSize: 14, bold: true, color: P.bg, align: "center" });
      arrow(s, x + 3.2, y + 0.6, x + 2.0, y + 1.05, P.gold, 2.5);
      ar(s, "جذب الأرض = الوزن", { x: x + 2.15, y: y + 1.15, w: 2.1, h: 0.3, fontSize: 11, bold: true, color: P.gold, align: "center" });
      ar(s, "الأرض", { x: x + 0.45, y: y + 1.45, w: 1.3, h: 0.25, fontSize: 10, color: m, align: "center" });
    }
  }

  // ---------- 9. Formula card ----------
  pres.addSection({ title: "المراجعة" });
  s = pres.addSlide({ sectionTitle: "المراجعة" });
  s.background = { data: bgGold };
  ar(s, "بطاقة القوانين", { x: 3.5, y: 0.3, w: 6.05, h: 0.6, fontSize: 32, bold: true });
  ar(s, "كل ما تحتاجه في صفحة واحدة (g ≈ 10)", { x: 3.5, y: 0.88, w: 6.05, h: 0.32, fontSize: 14, color: P.gold });
  LESSONS.forEach((L, i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const cw = 2.9, ch = 1.75, x = 9.55 - cw - col * (cw + 0.2), y = 1.4 + row * (ch + 0.2);
    card(s, x, y, cw, ch, P.card);
    iconCircle(s, IC[L.key], x + cw - 0.7, y + 0.18, 0.52, L.color);
    ar(s, L.name, { x: x + 0.2, y: y + 0.2, w: cw - 1.0, h: 0.45, fontSize: 15, bold: true });
    ltr(s, L.f, { x: x + 0.2, y: y + 0.78, w: cw - 0.4, h: 0.45, fontSize: 21, bold: true, color: L.color, align: "right" });
    s.addShape("roundRect", { x: x + 0.2, y: y + 1.3, w: 1.1, h: 0.3, rectRadius: 0.15, fill: { color: L.color, transparency: 80 }, line: { color: L.color, width: 0.75 } });
    ar(s, L.unit, { x: x + 0.2, y: y + 1.3, w: 1.1, h: 0.3, fontSize: 11, bold: true, color: L.color, align: "center" });
  });

  // ---------- 10. True / False ----------
  s = pres.addSlide({ sectionTitle: "المراجعة" });
  s.background = { data: bgTeal };
  ar(s, "صح أم خطأ؟", { x: 3.5, y: 0.3, w: 6.05, h: 0.6, fontSize: 32, bold: true });
  ar(s, "فكّر قبل أن تنظر إلى الإجابة", { x: 3.5, y: 0.88, w: 6.05, h: 0.32, fontSize: 14, color: P.me });
  const tf = [
    ["الجسم الساكن طاقته الحركية صفر.", true, "لأن سرعته صفر", P.ke],
    ["إذا دفعت جداراً ولم يتحرك فقد بذلت شغلاً.", false, "لا شغل بدون مسافة d", P.w],
    ["وحدة قياس القدرة هي الجول.", false, "وحدة القدرة هي الواط", P.pw],
    ["عند سقوط الجسم تتحول طاقته الكامنة إلى حركية.", true, "يقل الارتفاع وتزداد السرعة", P.pe],
  ];
  tf.forEach(([q, ok, why, c], k) => {
    const y = 1.4 + k * 0.92;
    card(s, 0.45, y, 9.1, 0.78, P.card);
    circle(s, 9.0, y + 0.2, 0.38, c);
    ltr(s, String(k + 1), { x: 9.0, y: y + 0.2, w: 0.38, h: 0.38, fontSize: 14, bold: true, color: P.bg, align: "center" });
    ar(s, q, { x: 3.6, y, w: 5.25, h: 0.78, fontSize: 15, bold: true });
    const bc = ok ? P.g : P.w;
    s.addShape("roundRect", { x: 2.25, y: y + 0.19, w: 1.15, h: 0.4, rectRadius: 0.2, fill: { color: bc }, line: { color: bc, width: 0 } });
    s.addImage({ data: ok ? iCheck : iTimes, x: 3.06, y: y + 0.28, w: 0.22, h: 0.22 });
    ar(s, ok ? "صح" : "خطأ", { x: 2.3, y: y + 0.19, w: 0.7, h: 0.4, fontSize: 14, bold: true, color: P.bg, align: "center" });
    ar(s, why, { x: 0.6, y, w: 1.55, h: 0.78, fontSize: 11, color: P.muted });
  });

  // ---------- 11. Practice ----------
  s = pres.addSlide({ sectionTitle: "المراجعة" });
  s.background = { data: bgGold };
  ar(s, "تمرّن بنفسك", { x: 3.5, y: 0.3, w: 6.05, h: 0.6, fontSize: 32, bold: true });
  ar(s, "احسب ثم قارن مع الجواب (g = 10)", { x: 3.5, y: 0.88, w: 6.05, h: 0.32, fontSize: 14, color: P.gold });
  const qs = [
    [KE, "كتلة 4\u00A0كغ وسرعة 5\u00A0م/ث. احسب الطاقة الحركية.", "50\u00A0جول"],
    [PE, "جسم 3\u00A0كغ على ارتفاع 4\u00A0م. احسب الطاقة الكامنة.", "120\u00A0جول"],
    [ME, "حركية 40\u00A0جول وكامنة 60\u00A0جول. احسب الميكانيكية.", "100\u00A0جول"],
    [W, "قوة 20\u00A0نيوتن حرّكت جسماً 5\u00A0م. احسب الشغل.", "100\u00A0جول"],
    [PW, "شغل 300\u00A0جول خلال 10\u00A0ث. احسب القدرة.", "30 واط"],
    [{ ...G, name: "الوزن" }, "جسم كتلته 8\u00A0كغ. احسب وزنه.", "80\u00A0نيوتن"],
  ];
  qs.forEach(([L, q, a], i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const cw = 2.9, ch = 1.75, x = 9.55 - cw - col * (cw + 0.2), y = 1.4 + row * (ch + 0.2);
    card(s, x, y, cw, ch, P.card);
    iconCircle(s, IC[L.key], x + cw - 0.6, y + 0.15, 0.42, L.color);
    ar(s, L.name, { x: x + 0.2, y: y + 0.15, w: cw - 0.9, h: 0.42, fontSize: 14, bold: true, color: L.color });
    ar(s, q, { x: x + 0.2, y: y + 0.62, w: cw - 0.4, h: 0.6, fontSize: 14, valign: "top" });
    s.addShape("roundRect", { x: x + 0.2, y: y + 1.27, w: cw - 0.4, h: 0.34, rectRadius: 0.17, fill: { color: L.color, transparency: 82 }, line: { color: L.color, width: 0.75, dashType: "dash" } });
    ar(s, `الجواب: ${a}`, { x: x + 0.2, y: y + 1.27, w: cw - 0.4, h: 0.34, fontSize: 12, bold: true, color: L.color, align: "center" });
  });
  s.addNotes("اطلب من الطلاب الحل أولاً قبل عرض الأجوبة.");

  // ---------- 12. Closing ----------
  pres.addSection({ title: "الخاتمة" });
  s = pres.addSlide({ sectionTitle: "الخاتمة" });
  s.background = { data: bgGold };
  circle(s, 4.25, 0.55, 1.5, P.gold, { fill: { color: P.gold, transparency: 88 }, line: { color: P.gold, width: 1, transparency: 50 } });
  s.addImage({ data: iRecycle, x: 4.6, y: 0.9, w: 0.8, h: 0.8 });
  ar(s, "الطاقة لا تختفي… بل تتحول من شكل إلى آخر", { x: 0.6, y: 2.15, w: 8.8, h: 0.7, fontSize: 26, bold: true, align: "center" });
  ar(s, "الشغل ينقلها، والقدرة تقيس سرعتها، والجاذبية تخزّنها في الارتفاع", { x: 0.8, y: 2.95, w: 8.4, h: 0.45, fontSize: 16, color: P.muted, align: "center" });
  LESSONS.forEach((L, i) => iconCircle(s, IC[L.key], 6.55 - i * 0.7, 3.85, 0.5, L.color));
  ar(s, "أحسنت! شكراً لكم", { x: 0.8, y: 4.6, w: 8.4, h: 0.45, fontSize: 18, bold: true, color: P.gold, align: "center" });

  await pres.writeFile({ fileName: "/tmp/pp/new.pptx" });
  await applyTheme("/tmp/pp/new.pptx", THEME);
  console.log("ok");
})();
