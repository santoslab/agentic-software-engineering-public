"""Build the Lecture 01 deck (ASE principles module) with python-pptx.

Inputs, beside this script: assets/lecture-01-base.pptx (the lean skeleton: one master,
its eleven layouts, the title and motivation slides) and assets/stakeholders-icon.png.
Output: lecture-01-intent-specifications-realizations-and-judgments.pptx in this directory.

    uv run --with python-pptx --with pillow python build-lecture-01.py

Typography: body text 18 pt; tables and diagram sub-labels 16 pt; code 16 pt bold in a
dark color on a light panel; captions under code 14 pt. The slide content follows
../lecture-notes/lecture-01-intent-specifications-realizations-and-judgments.md.
"""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.dml import MSO_LINE
from pptx.oxml.ns import qn

HERE = Path(__file__).resolve().parent
PURPLE = RGBColor(0x6E, 0x1E, 0xC6); DPURPLE = RGBColor(0x99, 0x00, 0x99)
GOLD = RGBColor(0xFF, 0xCF, 0x01); PALEGOLD = RGBColor(0xFF, 0xF3, 0xB0)
LAV = RGBColor(0xD9, 0xD2, 0xEC); LAV2 = RGBColor(0xF3, 0xF0, 0xF9)
BLACK = RGBColor(0, 0, 0); WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GRAY = RGBColor(0x59, 0x59, 0x59); LGRAY = RGBColor(0xF2, 0xF2, 0xF2); MGRAY = RGBColor(0xBF, 0xBF, 0xBF)
RED = RGBColor(0xC0, 0x00, 0x00); GREEN = RGBColor(0x2E, 0x7D, 0x32)
PALEGREEN = RGBColor(0xDD, 0xF2, 0xDD); PALERED = RGBColor(0xF8, 0xD7, 0xD7)
CODE = RGBColor(0x10, 0x10, 0x40)
ICON = str(HERE / "assets" / "stakeholders-icon.png")
FOOTER = "Agentic Software Engineering — ASE Principles Module, Lecture 01"
BODY, TBL, CODESZ, CAP = 18, 16, 16, 14

prs = Presentation(str(HERE / "assets" / "lecture-01-base.pptx"))
layouts = {l.name: l for l in prs.slide_layouts}
slide_no = [2]

# ---------- helpers ----------
def runs_of(p, text, size, bold=False, italic=False, color=None, font=None):
    items = text if isinstance(text, list) else [(text, {})]
    for s, o in items:
        r = p.add_run(); r.text = s
        r.font.size = Pt(o.get("size", size)); r.font.bold = o.get("bold", bold); r.font.italic = o.get("italic", italic)
        c = o.get("color", color)
        if c is not None: r.font.color.rgb = c
        f = o.get("font", font)
        if f: r.font.name = f

def para(tf, text, size=BODY, bold=False, italic=False, color=None, level=0, bullet=False, first=False,
         after=4, before=0, align=None, font=None, char="•"):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.space_after = Pt(after)
    if before: p.space_before = Pt(before)
    if align is not None: p.alignment = align
    if bullet:
        pPr = p._p.get_or_add_pPr()
        pPr.set("marL", str(int(Inches(0.28 + 0.3 * level)))); pPr.set("indent", str(int(-Inches(0.28))))
        pPr.append(pPr.makeelement(qn("a:buChar"), {"char": char if level == 0 else "–"}))
    runs_of(p, text, size, bold, italic, color, font)
    return p

def textbox(slide, x, y, w, h, lines=None, size=BODY, fill=None, line=None, margin=0.05, anchor=None, wrap=True, shadow=False):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = wrap
    tf.margin_left = tf.margin_right = Inches(margin); tf.margin_top = tf.margin_bottom = Inches(margin)
    if anchor is not None: tf.vertical_anchor = anchor
    if fill is not None: tb.fill.solid(); tb.fill.fore_color.rgb = fill
    if line is not None: tb.line.color.rgb = line; tb.line.width = Pt(1)
    if shadow: add_shadow(tb)
    first = True
    for ln in (lines or []):
        kw = dict(size=size)
        if isinstance(ln, dict): kw.update({k: v for k, v in ln.items() if k != "text"}); txt = ln["text"]
        else: txt = ln
        para(tf, txt, first=first, **kw); first = False
    return tb

def bullets(slide, x, y, w, h, items, size=BODY, after=8, title=None, title_size=None):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.05); tf.margin_top = tf.margin_bottom = Inches(0.03)
    first = True
    if title:
        para(tf, title, size=title_size or size + 2, bold=True, first=True, after=8, color=DPURPLE); first = False
    for it in items:
        if isinstance(it, dict):
            kw = dict(it); txt = kw.pop("text"); lvl = kw.pop("level", 0)
            para(tf, txt, size=kw.pop("size", size - (2 if lvl else 0)), level=lvl, bullet=kw.pop("bullet", True), first=first, after=kw.pop("after", after), **kw)
        elif isinstance(it, tuple):
            txt, lvl = it; para(tf, txt, size=size - (2 if lvl else 0), level=lvl, bullet=True, first=first, after=after)
        else:
            para(tf, it, size=size, bullet=True, first=first, after=after)
        first = False
    return tb

def add_shadow(shape):
    spPr = shape._element.spPr
    eff = spPr.makeelement(qn("a:effectLst"), {})
    sh = eff.makeelement(qn("a:outerShdw"), {"blurRad": "38100", "dist": "38100", "dir": "2700000", "algn": "tl", "rotWithShape": "0"})
    clr = sh.makeelement(qn("a:srgbClr"), {"val": "000000"}); clr.append(clr.makeelement(qn("a:alpha"), {"val": "40000"}))
    sh.append(clr); eff.append(sh); spPr.append(eff)

def box(slide, x, y, w, h, text=None, size=BODY, fill=LAV, line=BLACK, lw=1.0, bold=False, shape=MSO_SHAPE.RECTANGLE,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, color=BLACK, shadow=False, margin=0.06, italic=False):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None: s.fill.background()
    else: s.fill.solid(); s.fill.fore_color.rgb = fill
    if line is None: s.line.fill.background()
    else: s.line.color.rgb = line; s.line.width = Pt(lw)
    if shadow: add_shadow(s)
    tf = s.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(margin); tf.margin_top = tf.margin_bottom = Inches(0.04)
    if text is not None:
        first = True
        for ln in (text if isinstance(text, list) else [text]):
            kw = dict(size=size, bold=bold, color=color, align=align, italic=italic, after=2)
            if isinstance(ln, dict): kw.update({k: v for k, v in ln.items() if k != "text"}); ln = ln["text"]
            para(tf, ln, first=first, **kw); first = False
    return s

def callout(slide, x, y, w, h, lines, size=BODY, title=None, fill=GOLD):
    s = box(slide, x, y, w, h, fill=fill, line=BLACK, lw=0.75, shadow=True, anchor=MSO_ANCHOR.TOP, align=PP_ALIGN.LEFT, margin=0.1)
    tf = s.text_frame; first = True
    if title:
        para(tf, title, size=size, bold=True, first=True, after=4, align=PP_ALIGN.LEFT, color=BLACK); first = False
    for ln in lines:
        if isinstance(ln, dict):
            kw = dict(ln); txt = kw.pop("text"); lvl = kw.pop("level", 0); kw.setdefault("color", BLACK)
            para(tf, txt, size=kw.pop("size", size), level=lvl, bullet=kw.pop("bullet", True), first=first, after=kw.pop("after", 4), align=PP_ALIGN.LEFT, **kw)
        elif isinstance(ln, tuple):
            para(tf, ln[0], size=size - 2, level=ln[1], bullet=True, first=first, after=4, align=PP_ALIGN.LEFT, color=BLACK)
        else:
            para(tf, ln, size=size, bullet=True, first=first, after=4, align=PP_ALIGN.LEFT, color=BLACK)
        first = False
    return s

def line_(slide, x1, y1, x2, y2, color=BLACK, width=1.5, dash=None, head=False, tail=False):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = color; c.line.width = Pt(width)
    if dash: c.line.dash_style = dash
    ln = c.line._get_or_add_ln()
    if head: ln.append(ln.makeelement(qn("a:headEnd"), {"type": "triangle", "w": "med", "len": "med"}))
    if tail: ln.append(ln.makeelement(qn("a:tailEnd"), {"type": "triangle", "w": "med", "len": "med"}))
    return c

def leader(slide, x1, y1, x2, y2):
    return line_(slide, x1, y1, x2, y2, color=RED, width=1.5, dash=MSO_LINE.DASH)

def keybar(slide, text, y=1.3, x=0.85, w=12.05, h=0.6, size=BODY):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.gradient(); s.fill.gradient_angle = 0
    st = s.fill.gradient_stops; st[0].color.rgb = GOLD; st[0].position = 0.0; st[1].color.rgb = WHITE; st[1].position = 1.0
    s.line.fill.background()
    tf = s.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.12); tf.margin_top = tf.margin_bottom = Inches(0.03)
    para(tf, text, size=size, first=True, after=0, align=PP_ALIGN.LEFT, color=BLACK)
    return s

def code(slide, x, y, w, h, text, size=CODESZ, caption=None):
    tb = textbox(slide, x, y, w, h, fill=LGRAY, line=MGRAY, margin=0.12, wrap=True)
    tf = tb.text_frame; first = True
    for ln in text.rstrip("\n").split("\n"):
        para(tf, [(ln if ln else " ", {"font": "Courier New", "bold": True, "color": CODE})], size=size, first=first, after=0); first = False
    if caption:
        textbox(slide, x, y + h + 0.05, w, 0.35, [{"text": caption, "size": CAP, "color": GRAY, "font": "Courier New"}])
    return tb

def table(slide, x, y, w, rows, col_w, size=TBL, header=True, row_h=0.4, hdr_fill=PURPLE):
    gf = slide.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y), Inches(w), Inches(row_h * len(rows)))
    tbl = gf.table
    for i, cw in enumerate(col_w): tbl.columns[i].width = Inches(cw)
    for r, row in enumerate(rows):
        tbl.rows[r].height = Inches(row_h)
        for c, val in enumerate(row):
            cell = tbl.cell(r, c)
            cell.margin_left = cell.margin_right = Inches(0.08); cell.margin_top = cell.margin_bottom = Inches(0.04)
            fill_c, color, bold = None, BLACK, False
            if isinstance(val, dict):
                fill_c = val.get("fill"); color = val.get("color", BLACK); bold = val.get("bold", False); val = val["text"]
            tf = cell.text_frame; tf.word_wrap = True
            p = tf.paragraphs[0]; p.space_after = Pt(0)
            runs_of(p, val, size, bold=bold or (r == 0 and header), color=WHITE if (r == 0 and header) else color)
            cell.fill.solid()
            cell.fill.fore_color.rgb = hdr_fill if (r == 0 and header) else (fill_c or (LAV2 if r % 2 == 0 else WHITE))
    return gf

def new_slide(title, layout="Title Only", notes=None, size=30):
    s = prs.slides.add_slide(layouts[layout])
    if s.shapes.title is not None:
        tf = s.shapes.title.text_frame; tf.text = ""
        para(tf, title, size=size, first=True, after=0)
    slide_no[0] += 1
    textbox(s, 0.85, 7.0, 8.0, 0.35, [{"text": FOOTER, "size": 12, "color": GRAY}], margin=0.02)
    textbox(s, 11.9, 7.0, 1.0, 0.35, [{"text": str(slide_no[0]), "size": 12, "color": GRAY, "align": PP_ALIGN.RIGHT}], margin=0.02)
    if notes: s.notes_slide.notes_text_frame.text = notes
    return s

def section(title, sub, notes=None):
    s = prs.slides.add_slide(layouts["Section Header"]); slide_no[0] += 1
    for ph in s.placeholders:
        if ph.placeholder_format.type is not None and "TITLE" in str(ph.placeholder_format.type):
            tf = ph.text_frame; tf.text = ""; para(tf, title, size=34, bold=True, first=True)
        else:
            tf = ph.text_frame; tf.text = ""; para(tf, sub, size=20, first=True, color=GRAY)
    if notes: s.notes_slide.notes_text_frame.text = notes
    return s

# ---------- the diagram (spans x 0.9 .. 7.5; callouts go at x 7.8, w 5.1) ----------
CX, CW = 7.8, 5.1
def diagram(slide, hl=None, dx=-1.1, dy=0.0):
    H = lambda k: hl == k
    X = lambda v: v + dx; Y = lambda v: v + dy
    slide.shapes.add_picture(ICON, Inches(X(4.12)), Inches(Y(1.25)), width=Inches(0.95))
    textbox(slide, X(3.2), Y(2.12), 2.8, 0.66,
            [{"text": "Intent", "size": 20, "bold": True, "align": PP_ALIGN.CENTER, "after": 0},
             {"text": "the stakeholders; no artifact", "size": 14, "align": PP_ALIGN.CENTER, "color": GRAY}],
            fill=GOLD if H("intent") else None, line=BLACK if H("intent") else None)
    box(slide, X(3.55), Y(3.4), 2.1, 0.85, "Specifications", size=20, fill=GOLD if H("specs") else LAV, lw=2.0 if H("specs") else 1.0, bold=H("specs"))
    box(slide, X(3.55), Y(5.4), 2.1, 0.85, "Realization", size=20, fill=GOLD if H("real") else LAV, lw=2.0 if H("real") else 1.0, bold=H("real"))
    line_(slide, X(4.6), Y(2.82), X(4.6), Y(3.4), color=PURPLE if H("val") else BLACK, width=3 if H("val") else 1.5, tail=True)
    line_(slide, X(4.95), Y(4.25), X(4.95), Y(5.4), color=PURPLE if H("conf") else BLACK, width=3 if H("conf") else 1.5, head=True, tail=True)
    line_(slide, X(3.9), Y(4.25), X(3.9), Y(5.4), color=PURPLE if H("tr") else GRAY, width=2.5 if H("tr") else 1.25, dash=MSO_LINE.DASH, head=True, tail=True)
    for key, yy in (("sq", 3.47), ("rq", 5.47)):
        u = slide.shapes.add_shape(MSO_SHAPE.U_TURN_ARROW, Inches(X(5.78)), Inches(Y(yy)), Inches(0.62), Inches(0.7))
        u.rotation = 270
        u.fill.solid(); u.fill.fore_color.rgb = PURPLE if H(key) else BLACK; u.line.fill.background()
    def lab(key, x, y, w, h, big, small_t, align=PP_ALIGN.LEFT):
        textbox(slide, X(x), Y(y), w, h,
                [{"text": big, "size": 18, "bold": True, "after": 0, "align": align, "color": PURPLE if H(key) else BLACK},
                 {"text": small_t, "size": 14, "color": GRAY, "align": align}],
                fill=PALEGOLD if H(key) else None, line=BLACK if H(key) else None)
    lab("val", 4.75, 2.8, 2.0, 0.6, "VAL", "validation")
    lab("conf", 5.1, 4.5, 2.85, 0.62, "CONF", "conformance, by verification")
    lab("tr", 1.95, 4.5, 1.85, 0.6, "TR", "traceability", align=PP_ALIGN.RIGHT)
    lab("sq", 6.5, 3.5, 2.1, 0.6, "SQ", "specification quality")
    lab("rq", 6.5, 5.5, 2.1, 0.6, "RQ", "realization quality")

def ledger_table(slide, x, y, w, statuses=None, size=TBL, row_h=0.42, short=False):
    """The summary table of the assurance report (the name is historical)."""
    st = statuses or {}
    def cell(k):
        v = st.get(k, "holds")
        if v == "holds": return {"text": "holds", "fill": PALEGREEN, "color": GREEN, "bold": True}
        if v == "does not hold": return {"text": "does not hold", "fill": PALERED, "color": RED, "bold": True}
        return {"text": v, "fill": PALEGOLD, "color": BLACK, "bold": True}
    if short:
        rows = [["Judgment", "Holds?", "Rests on"],
                ["SQ", cell("SQ"), "a review record"], ["RQ", cell("RQ"), "ruff; collects"],
                ["CONF", cell("CONF"), "tests; two coverages; walked"], ["VAL", cell("VAL"), "the sign-off"], ["TR", cell("TR"), "links resolve"]]
        return table(slide, x, y, w, rows, [1.5, 1.8, w - 3.3], size=size, row_h=row_h)
    rows = [["Judgment", "Holds?", "Rests on"],
            ["SQ", cell("SQ"), "ConOps-SQ-1, Reqs-SQ-1, Specs-SQ-1: the review record; the header parts run now"],
            ["RQ", cell("RQ"), "Code-RQ-1: ruff exit 0; suite collects (10 tests), run now"],
            ["CONF", cell("CONF"), "Reqs-CONF-1: 10 passed; 4 of 4; 100% branches, run now · ConOps-CONF-1: 3 stories walked (record)"],
            ["VAL", cell("VAL"), "ConOps-VAL-1: sign-off by both user categories on conops.md A0 (record)"],
            ["TR", cell("TR"), "Specs-TR-1: every marker resolves, run now; every derived-from read (record)"]]
    return table(slide, x, y, w, rows, [1.5, 1.8, w - 3.3], size=size, row_h=row_h)

# ---------- slides 1 and 2: the skeleton's, with text fixed and enlarged ----------
s1, s2 = prs.slides[0], prs.slides[1]
for sh in s1.shapes:
    if sh.has_text_frame and "SE Module" in sh.text_frame.text:
        for p in sh.text_frame.paragraphs:
            for r in p.runs: r.text = ("ASE Principles Module · Lecture 01" if "SE Module" in r.text else "")
for sh in s2.shapes:
    if not sh.has_text_frame: continue
    t = sh.text_frame.text
    if "RASE for seL4" in t:
        for p in sh.text_frame.paragraphs:
            for r in p.runs: r.text = "ASE Principles Module · Lecture 01" if "RASE" in r.text else ""
    elif "The question this lecture" in t:
        tf = sh.text_frame
        for p in list(tf.paragraphs)[1:]: p._p.getparent().remove(p._p)
        p0 = tf.paragraphs[0]
        for r in list(p0.runs): r._r.getparent().remove(r._r)
        runs_of(p0, [("The question this lecture begins to answer:", {"bold": True})], BODY)
        para(tf, "What basic principles can guide us in engineering the development and assurance context?", size=BODY, after=0, before=6)
    elif "Human effort will shift" in t:
        tf = sh.text_frame
        for p in list(tf.paragraphs)[1:]: p._p.getparent().remove(p._p)
        p0 = tf.paragraphs[0]
        for r in list(p0.runs): r._r.getparent().remove(r._r)
        runs_of(p0, [("Human effort will shift", {})], BODY)
        for a, b in [("…from ", "engineering the code"), ("…to ", "engineering and managing the development and assurance context"),
                     ("…to ", "engineering layered, composable abstractions"), ("…that ", "provide direction to agents but also explainability to humans")]:
            para(tf, [(a, {}), (b, {"bold": True})], size=BODY, after=0)
    elif "As we move into the future" in t:
        for p in sh.text_frame.paragraphs:
            for r in p.runs: r.font.size = Pt(BODY)
        sh.top = Inches(4.03)
for sh in s2.shapes:
    if sh.has_text_frame and "Human effort will shift" in sh.text_frame.text:
        sh.top = Inches(4.4); sh.width = Inches(5.7); sh.height = Inches(2.3)
    elif sh.shape_type is not None and "PICTURE" in str(sh.shape_type):
        sh.height = Inches(2.45); sh.width = Inches(5.79)  # the photo ended at 4.27 in; keep the aspect ratio
s2.notes_slide.notes_text_frame.text = (s2.notes_slide.notes_text_frame.text + "\n\nLecture 01 framing: the three stages of the effort shift are the structure of the purpose section in the notes.")

# ---------- purpose ----------
s = new_slide("Purpose of this lecture", notes="Name the three entities, define a managed process, and name the records. The five judgments are the next slide.")
keybar(s, "A development process is managed when the truth of five judgments can be stated at any commit, with evidence, by someone who did not write the code.", h=0.95)
bullets(s, 0.85, 2.5, 12.05, 2.6, [
    {"text": [("Intent", {"bold": True}), (" — what the stakeholders want. It lives in their minds; there is no file.", {})]},
    {"text": [("Specifications", {"bold": True}), (" — what the system must do, as identified clauses.", {})]},
    {"text": [("Realization", {"bold": True}), (" — the code and the tests built to satisfy the specifications.", {})]},
], title="Three entities", title_size=20)
bullets(s, 0.85, 5.3, 12.05, 1.5, [
    {"text": [("The records that make the state visible: ", {"bold": True}), ("the assurance report (which judgments hold, on what evidence), the records (what people decided and did), and the development log (what each task did).", {})], "bullet": False},
], after=0)

s = new_slide("Five judgments, each a claim tracked commit by commit", notes="Each judgment fails independently; knowing which failed says what to do. Domain-independent; what varies is the forms and the methods.")
bullets(s, 0.85, 1.45, 12.05, 4.3, [
    {"text": [("SQ", {"bold": True}), ("  are the specifications well-formed, unambiguous, consistent, and complete for their level?", {})]},
    {"text": [("RQ", {"bold": True}), ("  does the realization lint, collect, and follow the test discipline?", {})]},
    {"text": [("CONF", {"bold": True}), ("  does the realization satisfy every clause of every specification?", {})]},
    {"text": [("VAL", {"bold": True}), ("  do the specifications describe what the stakeholders intend?", {})]},
    {"text": [("TR", {"bold": True}), ("  does every clause carry an identifier, and does every link resolve?", {})]},
])
keybar(s, "The same five questions apply to a web service, a controller, a data pipeline, or a document set. What varies is the forms of specification and the verification methods.", y=5.75, h=0.95)

# ---------- effort ----------
s = new_slide("Where human effort goes when agents write the code", notes="Three stages of the shift.")
xs = [0.85, 4.95, 9.05]
heads = ["from engineering the code", "to engineering and managing the development and assurance context", "to engineering layered, composable abstractions"]
bodies = ["An agent writes the code quickly and in volume. The person cannot read all of it.",
          "What the agent reads, and what the person reads back: specifications, judgments, verification methods, evidence, records and reports of state.",
          "Each layer summarizes the one below; judgment clauses say how each layer is checked against the next."]
for i in range(3):
    box(s, xs[i], 1.5, 3.4, 1.15, heads[i], size=BODY, fill=PURPLE if i == 2 else LAV, color=WHITE if i == 2 else BLACK, bold=True)
    textbox(s, xs[i], 2.85, 3.4, 2.6, [{"text": bodies[i], "size": BODY}])
    if i < 2: line_(s, xs[i] + 3.45, 2.07, xs[i + 1] - 0.05, 2.07, width=2.5, tail=True)
keybar(s, "The effort goes where an agent cannot replace it: saying what is wanted, deciding how it is checked, reading the evidence.", y=5.9, h=0.8)

s = new_slide("Layered abstractions: direction for agents, explanation for people", notes="The layers serve two readers at once. Direction for agents at the layer they work in; explanation for people, trustworthy because conformance between layers is checked.")
ly = 1.55
layers = [("Concept of operations", "purpose, scope, user categories, stories"), ("Requirements", "identified clauses, each with a method"),
          ("Contracts and tests", "executable claims about clauses"), ("Code", "the realization")]
for i, (a, b) in enumerate(layers):
    box(s, 3.6, ly + i * 1.05, 4.6, 0.9, [{"text": a, "bold": True, "size": BODY, "after": 0}, {"text": b, "size": 14, "color": GRAY}], fill=LAV if i < 3 else LGRAY)
box(s, 8.5, ly, 2.1, 4.05, [{"text": "Judgments", "bold": True, "size": BODY, "after": 4}, {"text": "how each layer is checked against the next; what evaluates it; what evidence", "size": 16}], fill=PALEGOLD)
line_(s, 3.2, ly + 0.1, 3.2, ly + 3.95, width=2.5, tail=True)
textbox(s, 0.85, ly + 1.0, 2.25, 2.0, [{"text": "direction to agents", "size": BODY, "align": PP_ALIGN.RIGHT, "color": PURPLE, "bold": True}, {"text": "the layer above is the standard its work is judged against", "size": 14, "align": PP_ALIGN.RIGHT, "color": GRAY}])
line_(s, 10.95, ly + 3.95, 10.95, ly + 0.1, width=2.5, tail=True)
textbox(s, 11.1, ly + 0.9, 1.85, 2.5, [{"text": "explanation to humans", "size": BODY, "color": PURPLE, "bold": True}, {"text": "read at the layer you need", "size": 14, "color": GRAY}])
keybar(s, "The summary can be trusted because conformance between layers is checked rather than assumed.", y=5.95, h=0.7)

# ---------- objectives ----------
obj = ["Name the three entities and the five judgments, define each as the glossary does, and point at the A0 artifact that holds or evidences each.",
       "Explain why intent has no artifact, what the purpose statement is instead, and which judgments an agent can establish alone.",
       "Describe the clause as the unit of a specification (identifier, method, derivation); distinguish mechanical from judgment clauses.",
       "State the five specification-quality properties and check a small specification against them by reading.",
       "Explain why a passing test suite is not by itself a verification, and name the four conditions of conformance in A0.",
       "Say what validation asks, who can answer it, and construct a case in which every other judgment holds and validation fails.",
       "Read a row of the assurance report as a claim with evidence and provenance, and say why a change can make the evidence insufficient.",
       "Say what A0 leaves out, when a claim must hold, and why keeping that apart from what a claim is and how it is evaluated is deliberate.",
       "Read a judgment clause in its four fields: what holds, how it is evaluated, what evidence results, how it is bound to the project.",
       "Identify which elements of A0 can be set up directly in your own project and which need adaptation."]
s = new_slide("Learning objectives (1 of 2)", notes="Ten objectives; each is something a student can do on A0.")
bullets(s, 0.85, 1.45, 12.05, 5.4, [{"text": o, "char": f"{i+1}."} for i, o in enumerate(obj[:5])], after=10)
s = new_slide("Learning objectives (2 of 2)")
bullets(s, 0.85, 1.45, 12.05, 5.4, [{"text": o, "char": f"{i+6}."} for i, o in enumerate(obj[5:])], after=10)

# ---------- Part 1 ----------
section("Part 1 · Entities and judgments", "The picture, then one judgment at a time", notes="Part 1 is the abstract picture. Part 2 shows every element on A0.")

s = new_slide("Three entities, five judgments, one report", notes="Diagram 1. Intent has no artifact. VAL compares intent and specifications; CONF compares specifications and realization; SQ and RQ are loops on one artifact; TR is the dashed links. The assurance report states the five, compiled on request; nothing gates a commit in A0.")
diagram(s)
ledger_table(s, CX, 1.45, CW, short=True, row_h=0.42)
textbox(s, CX, 4.5, CW, 0.7, [{"text": "The assurance report: which judgments hold for a named state, on what evidence.", "size": 16, "color": GRAY}])
box(s, CX, 5.45, 1.2, 0.7, "ask", size=16, fill=LGRAY)
line_(s, CX + 1.25, 5.8, CX + 1.7, 5.8, width=2, tail=True)
box(s, CX + 1.75, 5.3, 1.9, 1.0, [{"text": "evaluate; read", "bold": True, "size": 16, "after": 0}, {"text": "runs now; records", "size": 14, "color": GRAY}], fill=PALEGOLD)
line_(s, CX + 3.7, 5.8, CX + 4.15, 5.8, width=2, tail=True)
box(s, CX + 4.2, 5.45, 0.9, 0.7, "report", size=14, fill=LGRAY, margin=0.02)
textbox(s, CX, 6.4, CW, 0.55, [{"text": "Compiled on request. Nothing in A0 says when a claim must hold.", "size": 16, "color": GRAY}])

s = new_slide("Intent", notes="Intent lives with the stakeholders; a person cannot enumerate it; the purpose statement is the nearest written thing. An agent reaches intent only through a person, which is why VAL is reserved to a person. Elicitation is the next lecture.")
diagram(s, hl="intent")
callout(s, CX, 1.45, CW, 2.35, ["Lives in the stakeholders' minds; never fully written down", "Consulted only by asking a person: \"is this what you want?\""], title="What it is")
callout(s, CX, 4.0, CW, 2.2, ["No file called intent", "The purpose statement that opens the concept of operations is the nearest written thing: agreed and audited, not a transcript"], title="In the repository")
keybar(s, "An agent reaches intent only through a person, so validation is reserved to a person.", y=6.35, h=0.55)
leader(s, CX, 2.3, 4.9, 2.45)

s = new_slide("Specifications", notes="The forms A0 uses, the role a specification plays, and the clause as the unit with its three fields.")
diagram(s, hl="specs")
callout(s, CX, 1.45, CW, 2.35, ["Concept of operations: purpose, scope and terms, user categories, user stories", "Requirements: identified clauses, each with a method", {"text": "Later: glossary, architecture, data format, contracts, state machines", "size": 16}], title="Forms in A0")
callout(s, CX, 4.0, CW, 2.2, ["Captures intent (should conform to it)", "Directs the work: what the agent is told to build", "Summarizes the system: an abstraction of the realization"], title="Role")
keybar(s, "The unit is the clause: identifier · verification method · derived from", y=6.35, h=0.55)
leader(s, CX, 2.6, 4.6, 3.6)

s = new_slide("Specification quality (SQ)", notes="Five properties, each one phrase; A0 establishes SQ by a person reading. The audit as a procedure, with seeded gaps, is the A1 lecture.")
diagram(s, hl="sq")
callout(s, CX, 1.45, CW, 3.6, [
    {"text": [("Well-formed", {"bold": True}), (" — identifier and method on every clause", {})]},
    {"text": [("Unambiguous", {"bold": True}), (" — one reading", {})]},
    {"text": [("Internally consistent", {"bold": True}), (" — no two clauses contradict", {})]},
    {"text": [("Externally consistent", {"bold": True}), (" — the family agrees", {})]},
    {"text": [("Complete for its level", {"bold": True}), (" — nothing missing at the chosen abstraction", {})]}], title="The question SQ asks")
callout(s, CX, 5.2, CW, 1.0, [{"text": "In A0: a person read the seven clauses together (ConOps-SQ-1, Reqs-SQ-1, Specs-SQ-1)", "bullet": False}])
keybar(s, "Traceability is its own judgment, TR. The audit as a procedure, on gaps placed on purpose: next lecture.", y=6.35, h=0.55)
leader(s, CX, 3.3, 5.4, 3.8)

s = new_slide("Realization, and realization quality (RQ)", notes="Code and tests are both realization. RQ asks whether the realization is in a state where it can be checked: lint, collect, test discipline.")
diagram(s, hl="real")
callout(s, CX, 1.45, CW, 2.35, ["Built to satisfy a specification; the code and the test suite both", "One specification, many realizations"], title="Realization")
callout(s, CX, 4.0, CW, 2.2, ["Lints (ruff); the suite collects", "Test discipline: a test can fail; asserts no looser than its clause", "Structure judged appropriate (later)"], title="RQ: can it be checked at all?")
keybar(s, "Separate from CONF: a suite that does not collect gives no conformance evidence at all.", y=6.35, h=0.55)

s = new_slide("Conformance (CONF), by verification", notes="Conformance is a relationship on the pair; verification is the attempt, so a result is evidence with a scope. In A0 CONF is four conditions because a suite written by the same agent that wrote the code can mislead in three ways.")
diagram(s, hl="conf")
callout(s, CX, 1.45, CW, 2.75, ["Every test passes", "Requirements coverage: every test clause has a passing test", "Structural coverage: every branch exercised", "Every judgment clause has been walked"], title="Four conditions in A0")
callout(s, CX, 4.4, CW, 1.8, ["Programs for the first three; a person for the fourth", "Three kinds of verifier: human, agent, algorithmic"], title="Who decides")
keybar(s, "Conformance: R satisfies every property S states. Verification: trying to confirm it; evidence with a scope.", y=6.35, h=0.55, size=16)
leader(s, CX, 3.6, 6.3, 4.8)

s = new_slide("Validation (VAL)", notes="Validation compares an artifact with what is in a person's mind; only a person can decide; recorded as a sign-off. It can fail while every other judgment holds.")
diagram(s, hl="val")
callout(s, CX, 1.45, CW, 2.35, ["Verification compares two artifacts, both in the repository", "Validation compares an artifact with what is in a person's mind"], title="Do the specifications describe what is intended?")
callout(s, CX, 4.0, CW, 2.2, ["Only a person can decide it", "Recorded as a sign-off: who, in which role, when, on which version"], title="How it is decided")
keybar(s, "It can fail while SQ, RQ, CONF, and TR all hold; it goes stale when a stakeholder changes their mind.", y=6.35, h=0.55, size=16)
leader(s, CX, 2.4, 5.65, 3.1)

s = new_slide("Traceability (TR)", notes="Every clause has an identifier and every link resolves both ways. Its own row because a program decides it cheaply and the other rows depend on it clause by clause.")
diagram(s, hl="tr")
callout(s, CX, 1.45, CW, 2.5, ["Every clause carries an identifier", "Every link resolves, both ways: story → requirement → test → conformance-report row → assurance-report row"], title="What TR asks")
callout(s, CX, 4.15, CW, 2.05, ["The markers: a program lists any it cannot resolve", "The \"derived from\" fields: a person, with SQ"], title="Decided by")
keybar(s, "Identifiers are the vocabulary a person, an agent, and a program share: REQ-1 means one sentence.", y=6.35, h=0.55, size=16)

# ---------- Part 2 ----------
section("Part 2 · The judgments on a real system", "Message guard, version A0", notes="Every element of Part 1 pointed at in a file.")

s = new_slide("The example: a message guard", notes="Small, realistic shape, and it grows. Version A0 is one stage, filter. The Python sibling of the HAMR Simple Network Guard.")
bullets(s, 0.85, 1.45, 6.2, 5.4, [
    "A protected enclave produces messages; some must reach a less trusted network outside",
    "The guard decides, one message at a time, whether a message may leave",
    {"text": [("A message: ", {"bold": True}), ("a security level (Public, Restricted, Critical) and an integer payload", {})]},
    {"text": [("Version A0: ", {"bold": True}), ("one stage, ", {}), ("filter", {"font": "Courier New", "bold": True, "color": CODE}), (". Critical is dropped; anything else passes unchanged", {})]}])
box(s, 7.3, 2.0, 1.5, 0.9, "sender", size=BODY, fill=LGRAY)
line_(s, 8.85, 2.45, 9.45, 2.45, width=2.5, tail=True)
box(s, 9.5, 1.75, 1.9, 1.4, [{"text": "guard", "bold": True, "size": BODY, "after": 0}, {"text": "filter", "size": 16, "font": "Courier New", "bold": True, "color": CODE}], fill=LAV)
line_(s, 11.45, 2.15, 12.05, 2.15, width=2.5, tail=True); textbox(s, 12.1, 1.9, 0.8, 0.5, [{"text": "pass", "size": BODY, "bold": True, "color": GREEN}])
line_(s, 11.45, 2.75, 12.05, 2.75, width=2.5, tail=True); textbox(s, 12.1, 2.5, 0.8, 0.5, [{"text": "drop", "size": BODY, "bold": True, "color": RED}])
table(s, 7.3, 3.7, 5.6, [["Level", "A0 behavior", "HAMR"], ["Public", "passes unchanged", "Req_P"], ["Restricted", "passes unchanged", "Req_R_1"], ["Critical", "dropped: no output", "Req_C"]], [1.6, 2.6, 1.4], row_h=0.45)

s = new_slide("The question the code cannot answer", notes="The whole file, ten lines. Is it right? The code cannot say what was asked, what was promised, or whether the promise was checked.")
code(s, 0.85, 1.45, 12.05, 4.0, '''"""The filter stage: pass or drop a message by its security level
(REQ-1 to REQ-3)."""

from guard.message import Message, SecurityLevel


def filter_message(message: Message) -> Message | None:
    """Return the message unchanged if it may leave the enclave,
    or None if it is dropped."""
    if message.level is SecurityLevel.CRITICAL:
        return None  # REQ-1
    return message  # REQ-2, REQ-3''', caption="guard/filter.py, the whole file (two docstrings wrapped to fit)")
keybar(s, "Is this code right?", y=6.35, h=0.55)

s = new_slide("Three things the code does not say", notes="With an agent writing the code, the person reads three other things instead. An agent's description of its own work is not evidence about the work.")
bullets(s, 0.85, 1.45, 12.05, 2.9, [
    {"text": [("What was asked for", {"bold": True}), (" — which levels were meant to be stopped", {})]},
    {"text": [("What was promised", {"bold": True}), (" — a statement someone responsible agreed to", {})]},
    {"text": [("Whether the promise was checked", {"bold": True}), (" — by what, and when", {})]},
    {"text": "The code would look exactly like this if Restricted messages were meant to be stopped too.", "bullet": False, "italic": True}])
keybar(s, "With an agent writing the code, the person reads the specification, the evidence of conformance, and the record of whether that evidence is current.", y=4.5, h=0.95)
textbox(s, 0.85, 5.65, 12.05, 1.2, [{"text": "An agent's description of its own work is not evidence about the work. When the three things exist and can be trusted, a person can direct the work, review it, and take responsibility for code they have not read line by line.", "size": BODY}])

s = new_slide("Version A0, by category", notes="The directory tree, by the categories the diagram uses.")
table(s, 0.85, 1.45, 12.05, [["Category", "Files", "Role"],
    ["Intent", "none", "lives with the stakeholders"],
    ["Specifications", "specs/conops.md · specs/requirements.md", "what the system must do, as clauses"],
    ["Realization", "guard/ · tests/", "the code, and the executable claims about it"],
    ["Judgments", "process/judgments.md · templates/assurance-report.md", "what each claim says, per form; how it is evaluated"],
    ["Records", "records/reviews.md · walkthrough.md · dev-log.md", "what people decided and did"],
    ["Reports", "reports/assurance-report.md · conformance.md", "the development state, without reading the code"],
    ["Technology", "pyproject.toml · uv.lock", "Python 3.12+; pytest, pytest-cov, ruff; uv"],
    ["Support", "tools/evaluate.sh · tools/walk.py · CLAUDE.md", "every mechanical evaluation; the walkthrough helper; what an agent reads first"]],
    [2.3, 5.0, 4.75], row_h=0.52)
keybar(s, "Every entity and every judgment in Part 1 is now a file or a row that can be opened.", y=6.35, h=0.55)

s = new_slide("Intent in A0: the purpose statement", notes="The nearest written thing to intent. Agreed by the stakeholders, audited, derived from; not a transcript. How it was obtained is the next lecture.")
box(s, 0.85, 1.45, 12.05, 1.75, [{"text": "An organization keeps a protected enclave whose systems produce messages of differing sensitivity, and it needs some of those messages to reach a less trusted network outside the enclave. The message guard sits on that boundary and decides, one message at a time, whether a message may leave. Nothing leaves the enclave except through the guard.", "size": BODY, "italic": True, "align": PP_ALIGN.LEFT}], fill=PALEGOLD, line=BLACK, lw=0.75, anchor=MSO_ANCHOR.TOP, margin=0.15, shadow=True)
textbox(s, 0.85, 3.25, 12.05, 0.35, [{"text": "specs/conops.md, section 1, first paragraph", "size": CAP, "color": GRAY, "font": "Courier New"}])
bullets(s, 0.85, 3.75, 12.05, 2.2, ["A short text the stakeholders revised until they agreed; audited like any clause", "Not a transcript; a transcript is reference material and is not checked", "No file called intent anywhere in a0"], after=6)
keybar(s, "How it was obtained from the stakeholders is the next lecture: elicitation, on version A1.", y=6.25, h=0.6)

s = new_slide("The specifications in A0: a family of two", notes="conops.md has five sections; requirements.md has four clauses. Two kinds of document that govern one system and must agree.")
bullets(s, 0.85, 1.45, 6.0, 4.7, [
    {"text": [("1  Purpose", {"bold": True}), (" — the agreed purpose statement", {})]},
    {"text": [("2  Scope", {"bold": True}), (" — the boundary, and the terms", {})]},
    {"text": [("3  User categories", {"bold": True}), (" — message sender; security officer", {})]},
    {"text": [("4  User stories", {"bold": True}), (" — US-1 to US-3, each with an example, marked walkthrough", {})]},
    {"text": [("5  Sign-off", {"bold": True}), (" — a pointer to the record", {})]}], after=6, title="specs/conops.md", title_size=18)
bullets(s, 7.1, 1.45, 5.8, 4.7, [
    {"text": [("REQ-0", {"bold": True}), ("  a message is a level, one of three, and an integer payload", {})]},
    {"text": [("REQ-1", {"bold": True}), ("  drops every Critical message", {})]},
    {"text": [("REQ-2", {"bold": True}), ("  passes every Restricted message unchanged", {})]},
    {"text": [("REQ-3", {"bold": True}), ("  passes every Public message unchanged", {})]},
    {"text": "each marked test; each names what it derives from", "bullet": False, "italic": True, "color": GRAY, "size": 16}], after=6, title="specs/requirements.md", title_size=18)
keybar(s, "A family: two documents of different kinds that govern one system and must agree with each other.", y=6.35, h=0.55)

s = new_slide("The clause is the unit", notes="Two clauses verbatim.")
code(s, 0.85, 1.45, 12.05, 2.2, '''**US-1** · Method: walkthrough (human) · User category: message sender

As a message sender, when I send a Public message, I expect it to
arrive outside the enclave unchanged.

Example: the guard is given (Public, 42); it outputs (Public, 42).''', caption="specs/conops.md")
code(s, 0.85, 4.2, 12.05, 1.65, '''**REQ-1** · Method: test · Derived from: US-3

The filter drops every message whose security level is Critical:
for such a message it produces no output.''', caption="specs/requirements.md")
keybar(s, "Every clause: an identifier, a verification method, and what it derives from.", y=6.35, h=0.55)

s = new_slide("The three fields of a clause", notes="The identifier is what a report cites; the method says who verifies; derived-from makes the family.")
callout(s, 0.85, 1.45, 3.85, 2.7, ["What a report cites", "A person, an agent, and a program all say REQ-1 and mean the same sentence"], title="Identifier")
callout(s, 4.95, 1.45, 3.85, 2.7, ["How the clause is verified, so who can verify it", "test: a program decides; walkthrough: a person judges", "Recorded on the clause"], title="Verification method")
callout(s, 9.05, 1.45, 3.85, 2.7, ["Links a requirement to the story or term it refines", "Every requirement traces back to something a stakeholder wanted"], title="Derived from")
keybar(s, "What the specifications leave open on purpose: transport, how the level was assigned, what happens to a dropped message. Outside the boundary.", y=4.5, h=0.95, size=16)

s = new_slide("Mechanical clauses and judgment clauses", notes="A mechanical clause can be checked at every commit by a program nobody has to remember to run; a judgment clause costs a person's attention every time.")
table(s, 0.85, 1.45, 12.05, [["Method", "Who decides", "In A0", "Behind a gate (A2)?"],
    ["test", "a program: a test cites the clause and passes or fails", "REQ-0 to REQ-3", "yes"],
    ["walkthrough", "a person exercises the system and judges", "US-1 to US-3", "no"],
    ["analysis (later)", "a program, by examining the artifact: type checker, import rule", "A2", "yes"],
    ["review (later)", "a reader, from the text: a person or an agent", "A2", "no"]], [2.4, 5.6, 2.3, 1.75], row_h=0.6)
keybar(s, "Mechanical: a program can decide it. Judgment: it needs a reader. Push clauses toward mechanical, and record the choice on the clause.", y=5.3, h=0.95)

s = new_slide("Specification quality on A0", notes="Each property with the place in A0 where it can be checked. The REQ-2 question is planted to show that a reading is a judgment.")
table(s, 0.85, 1.45, 12.05, [["Property", "Where to look in A0"],
    ["Well-formed", "the header line **REQ-1** · Method: test; the report plugin parses it"],
    ["Unambiguous", "REQ-1 says what drop means. REQ-2 says \"unchanged\": is equality the only reading?"],
    ["Internally consistent", "REQ-1 to REQ-3 give each level one outcome"],
    ["Externally consistent", "every REQ derives from a story or a term; the same words in both files"],
    ["Complete for its level", "three levels, three requirements; transport is outside the boundary"]], [3.0, 9.05], row_h=0.62)
keybar(s, "Evaluated in A0 under ConOps-SQ-1, Reqs-SQ-1, and Specs-SQ-1: a person read the seven clauses together and recorded who, when, and which clauses in records/reviews.md.", y=5.5, h=0.95, size=16)

s = new_slide("The realization", notes="message.py makes REQ-0 concrete: three levels, a frozen dataclass, rejection of wrong types. One specification, many realizations.")
code(s, 0.85, 1.45, 7.2, 4.5, '''class SecurityLevel(Enum):
    PUBLIC = "Public"
    RESTRICTED = "Restricted"
    CRITICAL = "Critical"


@dataclass(frozen=True)
class Message:
    level: SecurityLevel
    payload: int

    def __post_init__(self) -> None:
        if not isinstance(self.level, SecurityLevel):
            raise TypeError(...)
        if not isinstance(self.payload, int):
            raise TypeError(...)''', size=15, caption="guard/message.py (abridged): REQ-0 made concrete")
bullets(s, 8.3, 1.45, 4.6, 5.3, ["The code and the test suite are both realization", "One specification, many realizations: another language, another design, the same clauses", {"text": "Under thirty lines of code; over three hundred of specifications, rules, and reports", "size": 16}], after=10)

s = new_slide("Tests as executable specification", notes="Each test is a claim about one clause and cites it by marker.")
code(s, 0.85, 1.45, 12.05, 4.5, '''@pytest.mark.req("REQ-1")
@pytest.mark.parametrize("payload", [0, 100, -5])
def test_critical_is_dropped(payload):
    assert filter_message(Message(SecurityLevel.CRITICAL, payload)) is None


@pytest.mark.req("REQ-2")
def test_restricted_passes_unchanged():
    message = Message(SecurityLevel.RESTRICTED, 7)
    assert filter_message(message) == message


@pytest.mark.req("REQ-3")
def test_public_passes_unchanged():
    message = Message(SecurityLevel.PUBLIC, 42)
    assert filter_message(message) == message''', size=15, caption="tests/test_filter.py")

s = new_slide("The marker serves three readers", notes="A test may cite nothing; a test clause with no citing test fails the run.")
callout(s, 0.85, 1.45, 12.05, 2.3, [{"text": [("A program", {"bold": True}), (" computes which clauses have tests and which do not", {})]},
                                    {"text": [("A person", {"bold": True}), (" who sees the test fail knows which clause is in question", {})]},
                                    {"text": [("An agent", {"bold": True}), (" writing a test must say which clause it is evidence for", {})]}], title="@pytest.mark.req(\"REQ-1\")")
keybar(s, "A test may omit a citation. A test clause with no citing test is a gap (Reqs-CONF-1); a citation that names no clause fails the run (Specs-TR-1).", y=4.1, h=0.8, size=16)

s = new_slide("Realization quality (RQ) in A0", notes="Two programs decide RQ; the test discipline is reviewed. RQ is separate from CONF so a conformance result is about runnable code and a suite that ran.")
bullets(s, 0.85, 1.45, 6.0, 5.3, [
    {"text": [("ruff check", {"font": "Courier New", "bold": True, "color": CODE}), ("  unused and undefined names, syntax that will not run", {})]},
    {"text": [("pytest --collect-only", {"font": "Courier New", "bold": True, "color": CODE}), ("  every test file imports; every marker is declared", {})]},
    {"text": [("Test discipline", {"bold": True}), (" (reviewed): a test can fail; asserts no more loosely than its clause", {})]}], after=10)
table(s, 7.1, 1.45, 5.8, [["Code-RQ-1", ""], ["Holds when", "The realization passes the project's linter, and its test suite collects without error."], ["Evaluated by", "analysis: the two commands"], ["Evidence", "the exit codes, quoted in the report"], ["In this project", "guard/, tests/, tools/; uv run ruff check .; uv run pytest --collect-only"]], [1.7, 4.1], row_h=0.6, hdr_fill=DPURPLE)
keybar(s, "Why a separate row: a suite that does not collect produces no conformance evidence at all.", y=6.1, h=0.7)

s = new_slide("Conformance is four conditions", notes="A passing suite establishes only that its own claims hold. With the same agent writing code and tests a green suite misleads in three ways.")
keybar(s, "A passing test suite, on its own, establishes only that the suite's own claims hold.", h=0.6)
conds = [("1  Every test passes", "the run itself", "program"),
         ("2  Requirements coverage", "every test clause is cited by a passing test", "program"),
         ("3  Structural coverage", "every branch of guard/ exercised", "program"),
         ("4  Judgment clauses walked", "each story exercised by a person in its role", "a person")]
for i, (a, b, d) in enumerate(conds):
    x = 0.85 + i * 3.05
    box(s, x, 2.15, 2.85, 1.0, a, size=BODY, bold=True, fill=LAV)
    textbox(s, x, 3.25, 2.85, 1.7, [{"text": b, "size": BODY}])
    box(s, x, 5.0, 2.85, 0.6, [{"text": [("decided by ", {"color": GRAY}), (d, {"bold": True})], "size": 16}], fill=PALEGOLD, line=None)
keybar(s, "Three ways a green suite misleads: no test for a clause; code never exercised; stories silently skipped.", y=5.95, h=0.8)

s = new_slide("The evidence: the conformance report", notes="The plugin reads the clause identifiers from the specifications and the markers from the suite; one row per clause.")
table(s, 0.85, 1.45, 12.05, [["Clause", "Method", "Tests citing it", "Status"],
    ["US-1 to US-3", "walkthrough", "—", "see records/walkthrough.md"],
    ["REQ-0", "test", "five tests in test_message.py", {"text": "pass", "color": GREEN, "bold": True}],
    ["REQ-1", "test", "test_critical_is_dropped [0], [100], [-5]", {"text": "pass", "color": GREEN, "bold": True}],
    ["REQ-2", "test", "test_restricted_passes_unchanged", {"text": "pass", "color": GREEN, "bold": True}],
    ["REQ-3", "test", "test_public_passes_unchanged", {"text": "pass", "color": GREEN, "bold": True}]], [2.2, 2.0, 5.3, 2.55], row_h=0.5)
textbox(s, 0.85, 4.6, 12.05, 0.4, [{"text": "reports/conformance.md", "size": CAP, "color": GRAY, "font": "Courier New"}])
keybar(s, "Requirements coverage: 4 of 4 test clauses have passing evidence. Unknown identifiers: none. A clause with no citing test would show \"no evidence\" and fail the run.", y=5.2, h=0.95, size=16)

s = new_slide("The evidence: the coverage table", notes="Branch coverage is weak but finds the places where code can do anything unnoticed.")
code(s, 0.85, 1.45, 12.05, 2.1, '''Name                Stmts   Miss Branch BrPart  Cover
guard/__init__.py       3      0      0      0   100%
guard/filter.py         5      0      2      0   100%
guard/message.py       13      0      4      0   100%
TOTAL                  21      0      6      0   100%''', caption="pytest-cov: branch coverage of guard/; the run fails below 100 percent")
bullets(s, 0.85, 4.1, 12.05, 2.7, ["Requirements coverage is a coverage measure over the specification, as branch coverage is one over the code", "Branch coverage is not strong: a branch was taken, not that the test checked anything useful there. But a branch no test took is a place where the code can do anything unnoticed"], after=10)

s = new_slide("Who decided: the walkthroughs", notes="Condition 4 was decided by a person in the story's role.")
table(s, 0.85, 1.45, 12.05, [["Clause", "Role", "Command", "Observed"],
    ["US-1", "message sender", "tools/walk.py Public 42", "pass: Public 42"],
    ["US-2", "message sender", "tools/walk.py Restricted 7", "pass: Restricted 7"],
    ["US-3", "security officer", "tools/walk.py Critical 100, then 0", "drop, both times"]], [1.3, 2.6, 4.9, 3.25], row_h=0.5)
textbox(s, 0.85, 3.6, 12.05, 0.4, [{"text": "records/walkthrough.md — walked by the instructor, in each role, on 2026-10-20, against the A0 snapshot", "size": CAP, "color": GRAY}])
keybar(s, "Each story is a judgment clause: a person, in the role the story names, exercises the guard and judges what they observe.", y=4.3, h=0.95)

s = new_slide("Three kinds of verifier", notes="A0 uses human and algorithmic; the agent verifier enters in A1. A verifier is itself a realization of the specification it checks.")
table(s, 0.85, 1.45, 12.05, [["", "Human", "Agent", "Algorithmic"],
    ["Cost per check", "minutes of attention", "tokens", "milliseconds"],
    ["Same result on repeat", "not guaranteed", "not guaranteed", "yes"],
    ["Decides judgment clauses", "yes", "yes", "no"],
    ["Can be put behind a gate (A2)", "no", "with effort", "yes, via the exit code"],
    ["In A0", "walkthroughs; SQ; sign-off", "not yet (A1: the auditor)", "pytest, the plugin, pytest-cov, ruff"]], [3.0, 2.9, 2.9, 3.25], row_h=0.55)
keybar(s, "A verifier can be wrong: a test can assert the wrong thing. The report records which verifier made each claim, so a wrong one can be traced. More later.", y=5.3, h=0.95, size=16)

s = new_slide("Validation in A0: the sign-off", notes="The sign-off names who, in which role, when, on which version.")
box(s, 0.85, 1.45, 12.05, 1.95, [{"text": "\"The concept of operations, version A0, describes the guard I intend: a Critical message never leaves, and anything else leaves as it arrived.\"", "size": BODY, "italic": True, "align": PP_ALIGN.LEFT, "after": 10},
    {"text": "Security officer: role played by the instructor, 2026-10-20, on specs/conops.md version A0.", "size": 16, "align": PP_ALIGN.LEFT, "after": 2},
    {"text": "Message sender: role played by the instructor, 2026-10-20, on specs/conops.md version A0.", "size": 16, "align": PP_ALIGN.LEFT}], fill=PALEGOLD, line=BLACK, lw=0.75, anchor=MSO_ANCHOR.TOP, margin=0.15, shadow=True)
textbox(s, 0.85, 3.45, 12.05, 0.35, [{"text": "records/walkthrough.md, section Sign-off (ConOps-VAL-1: one from each user category)", "size": CAP, "color": GRAY, "font": "Courier New"}])
bullets(s, 0.85, 3.95, 12.05, 1.8, ["Validation compares an artifact with what is in a person's mind, so only a person can decide it", "The decision is recorded: who, in which role, when, on which version"], after=6)
keybar(s, "The VAL row can stop holding when no file has changed: a stakeholder changes their mind and says so (A3).", y=6.25, h=0.6, size=16)

s = new_slide("One activity, two questions", notes="Keep the two duties of the walkthrough apart in thought.")
bullets(s, 0.85, 1.45, 12.05, 3.0, [{"text": [("When the officer walks US-3 and sees ", {}), ("drop", {"font": "Courier New", "bold": True, "color": CODE}), (", two questions are answered at once:", {})], "bullet": False},
    "Does the system behave as the story says? (conformance of a judgment clause)",
    "Is the story what the officer wants? (validation)",
    {"text": "A different officer could answer the first yes and the second no.", "bullet": False, "italic": True}], after=8)
keybar(s, "An agent given a specification will realize it, and a well-run process will certify that. The sign-off is the one place the process asks a person whether the certified system is the one they wanted.", y=4.8, h=1.3)

s = new_slide("Breaking it: a wrong system with a green report", notes="Suppose the officer meant Restricted must be stopped too. Every artifact was derived from the same misunderstanding; nothing in the repository can detect it.")
keybar(s, "Suppose the security officer meant that Restricted messages must be stopped as well, and the author of the concept of operations did not understand this.", h=0.95)
ledger_table(s, 0.85, 2.6, 6.6, statuses={"VAL": "signed, unread?"}, short=True, row_h=0.45)
bullets(s, 7.7, 2.6, 5.2, 4.2, ["US-2 and REQ-2 agree: consistent", "Every requirement has a passing test; coverage is complete; every identifier resolves", {"text": [("Nothing in the repository can detect it", {"bold": True})]}], after=8)
keybar(s, "What catches it: the officer walking US-2, seeing pass: Restricted 7, and saying this is not what they want. There is no command for this; that is its point.", y=5.9, h=0.95, size=16)

s = new_slide("Traceability in A0: the chain", notes="The chain of links. Identifiers are the vocabulary shared by person, agent, and program.")
chain = [("US-3", "story"), ("REQ-1", "requirement"), ("test_critical_\nis_dropped", "test"), ("REQ-1 row", "conformance report"), ("CONF row", "assurance report")]
for i, (a, b) in enumerate(chain):
    x = 0.85 + i * 2.45
    box(s, x, 1.65, 2.2, 1.4, [{"text": a, "bold": True, "size": 16 if i == 2 else BODY, "font": "Courier New" if i == 2 else None, "color": CODE if i == 2 else BLACK, "after": 0}, {"text": b, "size": 14, "color": GRAY}], fill=LAV if i < 3 else PALEGOLD)
    if i < 4: line_(s, x + 2.22, 2.35, x + 2.43, 2.35, width=2.5, tail=True)
bullets(s, 0.85, 3.4, 12.05, 2.5, ["Every link resolves in both directions: from any claim to its evidence, and from any change to its consequences", "The markers are decided by a program (unknown identifiers fail the run); the \"derived from\" fields by a person"], after=8)
keybar(s, "Its own row: a program decides it cheaply, and the other four rows depend on it clause by clause.", y=6.1, h=0.7)

s = new_slide("The assurance report at a0", notes="The summary table; below it, one section per judgment with a row per clause: holds, evidence, provenance. Compiled by an agent on request; the last section lists what was run and read.")
ledger_table(s, 0.85, 1.45, 12.05, row_h=0.55)
table(s, 0.85, 4.9, 12.05, [["Status words", ""], ["holds (run now)", "the evaluation was run against this tree while compiling the report, and passed"], ["holds (record)", "a record exists, names this state, and records a positive decision"], ["record names another state · does not hold · not evaluated", "the decision is reported, its currency is a person's call · a run failed or a record is negative · no run, no record"]], [3.6, 8.45], row_h=0.45, hdr_fill=DPURPLE)

s = new_slide("A row has four parts", notes="Provenance distinguishes evidence from a description of evidence.")
bullets(s, 0.85, 1.45, 12.05, 3.6, [
    {"text": [("Holds?", {"bold": True}), (" — run now, by record, record names another state, does not hold, not evaluated", {})]},
    {"text": [("Evidence", {"bold": True}), (" — what was produced, named precisely enough to be found", {})]},
    {"text": [("Provenance", {"bold": True}), (" — which verifier and version, which artifacts at which state, which clauses", {})]},
    {"text": [("What was run and read", {"bold": True}), (" — the report's last section, so that a reader can check the compiler", {})]}], after=8)
code(s, 0.85, 4.55, 12.05, 0.85, "test: pytest 9.1.1 with pytest-cov 7.1.0 and the plugin, 2026-10-24, at the A0 snapshot, REQ-0 to REQ-3", size=15, caption="the Reqs-CONF-1 row's provenance")
keybar(s, "A row is a claim made by a verifier, not a fact. \"pytest 9.1.1 exited 0 at a0\" can be rerun; \"all tests pass\" in an agent's message cannot.", y=5.95, h=0.9, size=16)

s = new_slide("No gate yet: one command, every mechanical evaluation", notes="tools/evaluate.sh runs every mechanical evaluation and exits at the first failure; nothing runs it unasked. The gate, the same command behind a hook, is A2's.")
box(s, 0.85, 1.55, 1.9, 1.1, "ask for the report", size=BODY, fill=LGRAY)
line_(s, 2.8, 2.1, 3.3, 2.1, width=2.5, tail=True)
box(s, 3.35, 1.45, 4.5, 1.3, [{"text": "tools/evaluate.sh", "bold": True, "size": BODY, "font": "Courier New", "color": CODE, "after": 2}, {"text": "ruff, then pytest with coverage and the plugin; a header saying what was checked", "size": 15}], fill=PALEGOLD)
line_(s, 7.9, 2.1, 8.4, 2.1, width=2.5, tail=True)
box(s, 8.45, 1.55, 1.5, 1.1, "exit 0", size=BODY, bold=True, fill=PALEGREEN, color=GREEN)
line_(s, 10.0, 2.1, 10.5, 2.1, width=2.5, tail=True)
box(s, 10.55, 1.55, 2.3, 1.1, "the row holds (run now)", size=16, fill=LGRAY)
box(s, 8.45, 2.95, 1.5, 0.9, "exit 1", size=BODY, bold=True, fill=PALERED, color=RED)
line_(s, 10.0, 3.4, 10.5, 3.4, width=2.5, tail=True)
textbox(s, 10.55, 3.05, 2.35, 0.8, [{"text": "the row does not hold", "size": 16}])
bullets(s, 0.85, 4.2, 12.05, 2.0, [{"text": [("It evaluates; it does not gate. ", {"bold": True}), ("Nothing runs it unasked, nothing waits for its result; a failing run is a row that does not hold, and that is all", {})]},
    {"text": [("A gate (A2): ", {"bold": True}), ("the same command behind a pre-commit hook, so a commit cannot complete unless it exits 0; an approval gate: a recorded human decision before a wave is accepted", {})]}], after=8)
keybar(s, "What a claim is, how it is evaluated, how its state is shown, and when it must hold are four questions. A0 answers three on purpose.", y=6.1, h=0.8, size=16)

s = new_slide("Breaking it: a wrong realization", notes="Change the condition to RESTRICTED. Four tests fail; REQ-1 and REQ-2 show FAIL; coverage still 100 percent; only CONF turns red.")
code(s, 0.85, 1.45, 6.6, 0.95, '''- if message.level is SecurityLevel.CRITICAL:
+ if message.level is SecurityLevel.RESTRICTED:''', size=15, caption="guard/filter.py, changed")
code(s, 0.85, 3.0, 6.6, 2.0, '''conformance: REQ-1: FAIL
conformance: REQ-2: FAIL
TOTAL   21  0  6  0  100%
4 failed, 6 passed in 0.05s''', size=15, caption="tools/evaluate.sh, exit 1")
ledger_table(s, 7.7, 1.45, 5.2, statuses={"CONF": "does not hold"}, short=True, row_h=0.5)
bullets(s, 7.7, 4.6, 5.2, 2.3, [{"text": [("Coverage is still 100 percent: ", {"bold": True}), ("coverage says which code ran, not whether it was right", {})]}], after=6)
keybar(s, "Only CONF turned red; the verifier that caught it is the test suite. SQ, VAL, and TR are untouched.", y=5.6, h=0.75, x=0.85, w=6.6, size=16)

s = new_slide("A failed check is a fact about the pair", notes="Which side moves is a recorded decision.")
bullets(s, 0.85, 1.45, 12.05, 3.4, ["The specification and the realization do not agree; the check does not say which side is wrong", "Here the specification is right and the code moved back", "In other cases the realization is what the stakeholders want and the specification is amended"], after=10)
keybar(s, "Which side moves is an engineering decision, made by a person and recorded: in A0, the dev log. Amendments and change requests arrive in version A3.", y=5.0, h=0.95)

s = new_slide("The judgments file: five definitions, eight clauses, by form", notes="Each judgment stated once, then as clauses per form. No rule says when a claim must hold.")
bullets(s, 0.85, 1.45, 6.0, 5.4, [
    {"text": [("ConOps-SQ-1", {"bold": True}), ("  the concept of operations is well-formed", {})]},
    {"text": [("ConOps-CONF-1", {"bold": True}), ("  every story has been walked on the realization", {})]},
    {"text": [("ConOps-VAL-1", {"bold": True}), ("  the stakeholders have confirmed the concept of operations", {})]},
    {"text": [("Reqs-SQ-1", {"bold": True}), ("  the requirements are well-formed and cover the scope", {})]}], after=8)
bullets(s, 7.1, 1.45, 5.8, 5.4, [
    {"text": [("Reqs-CONF-1", {"bold": True}), ("  every requirement assigned test has passing evidence; the code is exercised", {})]},
    {"text": [("Specs-SQ-1", {"bold": True}), ("  the specifications agree with one another", {})]},
    {"text": [("Specs-TR-1", {"bold": True}), ("  every reference resolves", {})]},
    {"text": [("Code-RQ-1", {"bold": True}), ("  the realization lints and the suite collects", {})]}], after=8)
keybar(s, "Four fields per clause: holds when, evaluated by, evidence, in this project. No when and no on-failure: nothing in A0 says when a claim must hold.", y=5.5, h=0.95, size=16)

s = new_slide("One clause in four fields", notes="The first three fields depend only on the form; the fourth binds the clause to this project. Evaluated-by makes a clause checkable.")
table(s, 0.85, 1.45, 12.05, [["Reqs-CONF-1", "Every requirement assigned test has passing test evidence, and the realization is exercised"],
    ["Holds when", "Every requirement whose method is test is cited by at least one test; every citing test passes; the suite meets the project's structural-coverage objective"],
    ["Evaluated by", "test: the test runner, with a plugin that computes requirements coverage from the citations and the outcomes, and a coverage tool"],
    ["Evidence", "the generated conformance report; the coverage table of the run"],
    ["In this project", "the REQ clauses of specs/requirements.md; guard/; 100 percent branch coverage; uv run pytest with tests/conftest.py and pytest-cov. Instance: REQ-1 is cited by test_critical_is_dropped"]], [2.6, 9.45], row_h=0.78, hdr_fill=DPURPLE)
keybar(s, "The first three fields would read the same in any project with a requirements document; the fourth is what you write for yours.", y=5.9, h=0.85, size=16)

s = new_slide("Why the judgments are a file: the agent's three roles", notes="The agent reads the file; person and agent work to the same written definitions. CLAUDE.md gives it three roles.")
bullets(s, 0.85, 1.45, 12.05, 4.4, ["An agent started in this directory is told, by CLAUDE.md, to read process/judgments.md; from then on the person and the agent work to the same written definitions",
    {"text": [("Author: ", {"bold": True}), ("its work is held to the clauses; it cites a clause in a test because Reqs-CONF-1 says what evidence looks like", {})]},
    {"text": [("Assessor, when asked: ", {"bold": True}), ("it compiles the report by running the evaluations now and reading the records, and lists what it ran and read", {})]},
    {"text": [("Never a decider of a human judgment: ", {"bold": True}), ("it does not sign, walk a story for a stakeholder, or record what a person did not do", {})]},
    "A habit cannot be followed by an agent; a prompt cannot be audited by a person; a file can be both"], after=8)
keybar(s, "records/dev-log.md records what each task did; the report records where things stand.", y=6.1, h=0.7)

s = new_slide("Where the effort goes", notes="Under thirty lines of code against several hundred of specifications, judgments, records, reports. Optional demo: ask an agent what the system does and how it knows.")
box(s, 0.85, 1.45, 5.8, 2.0, [{"text": "< 30", "size": 44, "bold": True, "color": PURPLE, "after": 0}, {"text": "lines of code in guard/", "size": BODY}], fill=LAV2, line=None)
box(s, 7.1, 1.45, 5.8, 2.0, [{"text": "> 300", "size": 44, "bold": True, "color": PURPLE, "after": 0}, {"text": "lines of specifications, judgments, records, and reports", "size": BODY}], fill=LAV2, line=None)
textbox(s, 0.85, 3.7, 12.05, 1.6, [{"text": "Not a property of the small example. When an agent writes the code, the person's effort goes into saying what is wanted, deciding how it will be checked, and reading the evidence.", "size": BODY}])
callout(s, 0.85, 5.35, 12.05, 1.5, [{"text": "Ask an agent in a0/ what the system does and how it is known that the code does it. Watch where it looks: the specifications and the report, or the code.", "bullet": False, "size": 16}], title="In class, optional", size=16)

s = new_slide("What is not here yet: version A1", notes="A1 keeps the system and improves the specifications.")
bullets(s, 0.85, 1.45, 12.05, 5.4, ["Elicitation: how the purpose statement and the stories are obtained from stakeholders", "A glossary of the domain's terms; requirements in a structured form (EARS)", "Fixtures derived from the stories, so a story can be checked by a test as well as walked", "The audit replaces the reading: a procedure on gaps placed on purpose, by a person, then an agent, then a skill"], after=10)

s = new_slide("What is not here yet: later versions", notes="A2 adds the second stage and the first specifications of structure.")
bullets(s, 0.85, 1.45, 12.05, 5.4, [{"text": [("A2: ", {"bold": True}), ("the second stage, sanitize; architecture, the message format, contracts; a build plan with tasks and waves; analysis and review as methods; the first process rules, and the ledger as the report kept", {})]},
    {"text": [("A3: ", {"bold": True}), ("a change of policy: change requests, staleness in action", {})]},
    {"text": [("A4, A5: ", {"bold": True}), ("sessions with a protocol (state machine, sequence chart, verification plan); a standard message format", {})]}], after=10)

s = new_slide("Applying this: what carries over directly", notes="On day one, in any project.")
bullets(s, 0.85, 1.45, 6.0, 5.4, [{"text": [("The judgments. ", {"bold": True}), ("Start the judgments file and the report on day one", {})]},
    {"text": [("A concept of operations ", {"bold": True}), ("with the four elements, agreed before code", {})]},
    {"text": [("Requirements ", {"bold": True}), ("whose clauses carry an identifier, a method, and a derivation", {})]},
    {"text": [("A statement of the technology ", {"bold": True}), ("and the evaluation command", {})]}], after=8)
bullets(s, 7.1, 1.45, 5.8, 5.4, [{"text": [("Tests that cite clauses, ", {"bold": True}), ("and the two coverages: does the suite support a verification?", {})]},
    {"text": [("A judgments file: ", {"bold": True}), ("four fields per clause; the first three copied from the form, the fourth yours", {})]},
    {"text": [("A sign-off, ", {"bold": True}), ("and provenance on every claim", {})]}], after=8)

s = new_slide("Applying this: what needs adaptation", notes="One skill underlies the adapted parts.")
bullets(s, 0.85, 1.45, 12.05, 3.8, [{"text": [("The forms of specification: ", {"bold": True}), ("architecture, data format, state machine, contracts (specification-kinds.md)", {})]},
    {"text": [("The verification methods: ", {"bold": True}), ("analysis and review, with their tools", {})]},
    {"text": [("The tooling: ", {"bold": True}), ("citation-derived coverage carries; the plugin does not", {})]},
    {"text": [("The thresholds, the people, the records", {"bold": True})]}], after=8)
keybar(s, "The skill the next lectures build: phrasing your own criteria as clauses with a named evaluation and named evidence, and, when your process needs it, a trigger and a consequence of failure.", y=5.5, h=0.95, size=16)

s = new_slide("Exercise 1", notes="Forces an amendment, a VAL row that stops holding, and a re-sign before the test and the report.")
callout(s, 0.85, 1.45, 12.05, 2.9, ["Add a requirement: a message whose payload is negative is dropped, whatever its level", "Before writing code: do the five quality properties still hold with REQ-0 to REQ-3? Amend what must be amended", "Record which clauses of the report the amendment affects, and why", "Carry it through: clause, test, evaluations, report, dev-log entry; what must the sign-off now say?"], fill=PALEGOLD)
keybar(s, "Deliverable: the diff; the report after; half a page on which rows the change affected and which evaluation re-established each.", y=4.6, h=0.85, size=16)

s = new_slide("Before next meeting", notes="Run A0; read the glossary; reread the ConOps with the elicitation question in mind.")
bullets(s, 0.85, 1.45, 12.05, 3.2, ["Run A0: uv sync; tools/evaluate.sh; the two sabotages, restoring the file after the first", "Read the glossary entries for the terms introduced today", "Reread specs/conops.md and ask how its author could have found out what the security officer wanted"], after=10)
keybar(s, "Question to think about: a reading of \"unchanged\" in REQ-2 under which the test is too weak, and which artifact you would change.", y=5.0, h=0.95, size=16)

OUT = HERE / "lecture-01-intent-specifications-realizations-and-judgments.pptx"
prs.save(str(OUT))
print("saved", len(prs.slides), "slides to", OUT.name)
