"""Build the Lecture 01 deck (ASE principles module) with python-pptx.

Inputs, beside this script: assets/lecture-01-base.pptx (the lean skeleton: one master,
its eleven layouts, the title and motivation slides) and assets/stakeholders-icon.png.
Output: lecture-01-intent-specifications-realizations-and-judgments.pptx in this directory.

    uv run --with python-pptx --with pillow python build-lecture-01.py

The slide content follows ../lecture-notes/lecture-01-intent-specifications-realizations-and-judgments.md.
"""
from pathlib import Path
HERE = Path(__file__).resolve().parent
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.dml import MSO_LINE
from pptx.oxml.ns import qn
import copy

PURPLE = RGBColor(0x6E, 0x1E, 0xC6); DPURPLE = RGBColor(0x99, 0x00, 0x99)
GOLD = RGBColor(0xFF, 0xCF, 0x01); PALEGOLD = RGBColor(0xFF, 0xF3, 0xB0)
LAV = RGBColor(0xD9, 0xD2, 0xEC); LAV2 = RGBColor(0xF3, 0xF0, 0xF9)
BLACK = RGBColor(0, 0, 0); WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GRAY = RGBColor(0x59, 0x59, 0x59); LGRAY = RGBColor(0xF2, 0xF2, 0xF2); MGRAY = RGBColor(0xBF, 0xBF, 0xBF)
RED = RGBColor(0xC0, 0x00, 0x00); GREEN = RGBColor(0x2E, 0x7D, 0x32); PALEGREEN = RGBColor(0xDD, 0xF2, 0xDD); PALERED = RGBColor(0xF8, 0xD7, 0xD7)
ICON = str(HERE / "assets" / "stakeholders-icon.png")
FOOTER = "Agentic Software Engineering — ASE Principles Module, Lecture 01"

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

def para(tf, text, size=14, bold=False, italic=False, color=None, level=0, bullet=False, first=False,
         after=4, before=0, align=None, font=None, char="•"):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.space_after = Pt(after)
    if before: p.space_before = Pt(before)
    if align is not None: p.alignment = align
    if bullet:
        pPr = p._p.get_or_add_pPr()
        pPr.set("marL", str(int(Inches(0.2 + 0.28 * level)))); pPr.set("indent", str(int(-Inches(0.2))))
        pPr.append(pPr.makeelement(qn("a:buChar"), {"char": char if level == 0 else "–"}))
    runs_of(p, text, size, bold, italic, color, font)
    return p

def textbox(slide, x, y, w, h, lines=None, size=14, fill=None, line=None, margin=0.05, anchor=None, wrap=True, shadow=False):
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

def bullets(slide, x, y, w, h, items, size=14, after=5, title=None, title_size=None):
    """items: str | (str, level) | dict(text=..., level=, bold=, ...)"""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.05); tf.margin_top = tf.margin_bottom = Inches(0.03)
    first = True
    if title:
        para(tf, title, size=title_size or size + 1, bold=True, first=True, after=6, color=DPURPLE); first = False
    for it in items:
        if isinstance(it, dict):
            kw = dict(it); txt = kw.pop("text"); lvl = kw.pop("level", 0)
            para(tf, txt, size=kw.pop("size", size - (1 if lvl else 0)), level=lvl, bullet=kw.pop("bullet", True), first=first, after=kw.pop("after", after), **kw)
        elif isinstance(it, tuple):
            txt, lvl = it; para(tf, txt, size=size - (1 if lvl else 0), level=lvl, bullet=True, first=first, after=after)
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

def box(slide, x, y, w, h, text=None, size=14, fill=LAV, line=BLACK, lw=1.0, bold=False, shape=MSO_SHAPE.RECTANGLE,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, color=BLACK, shadow=False, margin=0.05, italic=False):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None: s.fill.background()
    else: s.fill.solid(); s.fill.fore_color.rgb = fill
    if line is None: s.line.fill.background()
    else: s.line.color.rgb = line; s.line.width = Pt(lw)
    if shadow: add_shadow(s)
    tf = s.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(margin); tf.margin_top = tf.margin_bottom = Inches(0.03)
    if text is not None:
        first = True
        for ln in (text if isinstance(text, list) else [text]):
            kw = dict(size=size, bold=bold, color=color, align=align, italic=italic, after=2)
            if isinstance(ln, dict): kw.update({k: v for k, v in ln.items() if k != "text"}); ln = ln["text"]
            para(tf, ln, first=first, **kw); first = False
    return s

def callout(slide, x, y, w, h, lines, size=12, title=None, fill=GOLD):
    s = box(slide, x, y, w, h, fill=fill, line=BLACK, lw=0.75, shadow=True, anchor=MSO_ANCHOR.TOP, align=PP_ALIGN.LEFT, margin=0.08)
    tf = s.text_frame; first = True
    if title:
        para(tf, title, size=size + 1, bold=True, first=True, after=3, align=PP_ALIGN.LEFT, color=BLACK); first = False
    for ln in lines:
        if isinstance(ln, dict):
            kw = dict(ln); txt = kw.pop("text"); lvl = kw.pop("level", 0); kw.setdefault("color", BLACK)
            para(tf, txt, size=kw.pop("size", size), level=lvl, bullet=kw.pop("bullet", True), first=first, after=kw.pop("after", 2), align=PP_ALIGN.LEFT, **kw)
        elif isinstance(ln, tuple):
            para(tf, ln[0], size=size - 1, level=ln[1], bullet=True, first=first, after=2, align=PP_ALIGN.LEFT, color=BLACK)
        else:
            para(tf, ln, size=size, bullet=True, first=first, after=2, align=PP_ALIGN.LEFT, color=BLACK)
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

def keybar(slide, text, y=1.3, x=0.85, w=12.0, h=0.5, size=15):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.gradient(); s.fill.gradient_angle = 0
    st = s.fill.gradient_stops; st[0].color.rgb = GOLD; st[0].position = 0.0; st[1].color.rgb = WHITE; st[1].position = 1.0
    s.line.fill.background()
    tf = s.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.12); tf.margin_top = tf.margin_bottom = Inches(0.02)
    para(tf, text, size=size, first=True, after=0, align=PP_ALIGN.LEFT, color=BLACK)
    return s

def code(slide, x, y, w, h, text, size=10.5):
    tb = textbox(slide, x, y, w, h, fill=LGRAY, line=MGRAY, margin=0.1, wrap=True)
    tf = tb.text_frame; first = True
    for ln in text.rstrip("\n").split("\n"):
        kw = {}
        para(tf, [(ln if ln else " ", {"font": "Courier New"})], size=size, first=first, after=0); first = False
    return tb

def table(slide, x, y, w, rows, col_w, size=12, header=True, row_h=0.32, hdr_fill=PURPLE):
    gf = slide.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y), Inches(w), Inches(row_h * len(rows)))
    tbl = gf.table
    for i, cw in enumerate(col_w): tbl.columns[i].width = Inches(cw)
    for r, row in enumerate(rows):
        tbl.rows[r].height = Inches(row_h)
        for c, val in enumerate(row):
            cell = tbl.cell(r, c)
            cell.margin_left = cell.margin_right = Inches(0.06); cell.margin_top = cell.margin_bottom = Inches(0.03)
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
    textbox(s, 0.85, 7.02, 7.5, 0.3, [{"text": FOOTER, "size": 10, "color": GRAY}], margin=0.02)
    textbox(s, 12.1, 7.02, 0.8, 0.3, [{"text": str(slide_no[0]), "size": 10, "color": GRAY, "align": PP_ALIGN.RIGHT}], margin=0.02)
    if notes: s.notes_slide.notes_text_frame.text = notes
    return s

def section(title, sub, notes=None):
    s = prs.slides.add_slide(layouts["Section Header"]); slide_no[0] += 1
    for ph in s.placeholders:
        if ph.placeholder_format.type is not None and "TITLE" in str(ph.placeholder_format.type):
            tf = ph.text_frame; tf.text = ""; para(tf, title, size=34, bold=True, first=True)
        else:
            tf = ph.text_frame; tf.text = ""; para(tf, sub, size=18, first=True, color=GRAY)
    if notes: s.notes_slide.notes_text_frame.text = notes
    return s

# ---------- the diagram ----------
def diagram(slide, hl=None, dx=0.0, dy=0.0, labels=True, small=False):
    """Entities and judgments. hl in {intent, specs, real, val, conf, sq, rq, tr}."""
    H = lambda k: hl == k
    def X(v): return v + dx
    def Y(v): return v + dy
    # intent
    slide.shapes.add_picture(ICON, Inches(X(4.12)), Inches(Y(1.38)), width=Inches(0.95))
    textbox(slide, X(3.25), Y(2.3), 2.7, 0.62,
            [{"text": "Intent", "size": 16, "bold": True, "align": PP_ALIGN.CENTER, "after": 0},
             {"text": "the stakeholders; no artifact", "size": 11, "align": PP_ALIGN.CENTER, "color": GRAY}],
            fill=GOLD if H("intent") else None, line=BLACK if H("intent") else None)
    # boxes
    box(slide, X(3.55), Y(3.35), 2.1, 0.85, "Specifications", size=16, fill=GOLD if H("specs") else LAV, lw=2.0 if H("specs") else 1.0, bold=H("specs"))
    box(slide, X(3.55), Y(5.35), 2.1, 0.85, "Realization", size=16, fill=GOLD if H("real") else LAV, lw=2.0 if H("real") else 1.0, bold=H("real"))
    # VAL arrow: intent -> specifications
    line_(slide, X(4.6), Y(2.95), X(4.6), Y(3.35), color=PURPLE if H("val") else BLACK, width=3 if H("val") else 1.5, tail=True)
    # CONF double arrow
    line_(slide, X(4.95), Y(4.2), X(4.95), Y(5.35), color=PURPLE if H("conf") else BLACK, width=3 if H("conf") else 1.5, head=True, tail=True)
    # TR dashed
    line_(slide, X(3.9), Y(4.2), X(3.9), Y(5.35), color=PURPLE if H("tr") else GRAY, width=2.5 if H("tr") else 1.25, dash=MSO_LINE.DASH, head=True, tail=True)
    # SQ / RQ loops
    for key, yy in (("sq", 3.42), ("rq", 5.42)):
        u = slide.shapes.add_shape(MSO_SHAPE.U_TURN_ARROW, Inches(X(5.78)), Inches(Y(yy)), Inches(0.62), Inches(0.7))
        u.rotation = 270
        u.fill.solid(); u.fill.fore_color.rgb = PURPLE if H(key) else BLACK; u.line.fill.background()
    if labels:
        def lab(key, x, y, w, h, big, small_t, align=PP_ALIGN.LEFT):
            textbox(slide, X(x), Y(y), w, h,
                    [{"text": big, "size": 13, "bold": True, "after": 0, "align": align, "color": PURPLE if H(key) else BLACK},
                     {"text": small_t, "size": 10.5, "color": GRAY, "align": align}],
                    fill=PALEGOLD if H(key) else None, line=BLACK if H(key) else None)
        lab("val", 4.75, 2.78, 1.9, 0.5, "VAL", "validation")
        lab("conf", 5.1, 4.5, 2.2, 0.5, "CONF", "conformance, by verification")
        lab("tr", 2.0, 4.5, 1.8, 0.5, "TR", "traceability", align=PP_ALIGN.RIGHT)
        lab("sq", 6.5, 3.45, 2.1, 0.5, "SQ", "specification quality")
        lab("rq", 6.5, 5.45, 2.1, 0.5, "RQ", "realization quality")

def ledger_table(slide, x, y, w, statuses=None, size=11, row_h=0.3, short=False):
    st = statuses or {}
    def cell(k):
        v = st.get(k, "established")
        if v == "established": return {"text": "established", "fill": PALEGREEN, "color": GREEN, "bold": True}
        if v == "stale": return {"text": "stale", "fill": PALERED, "color": RED, "bold": True}
        return {"text": v, "fill": PALEGOLD, "color": BLACK, "bold": True}
    if short:
        rows = [["Judgment", "Status", "Evidence"],
                ["SQ  specification quality", cell("SQ"), "read together"],
                ["RQ  realization quality", cell("RQ"), "ruff; collects"],
                ["CONF  conformance", cell("CONF"), "tests; two coverages; walked"],
                ["VAL  validated", cell("VAL"), "sign-off"],
                ["TR  traceable", cell("TR"), "links resolve"]]
        return table(slide, x, y, w, rows, [1.75, 1.0, w - 2.75], size=size, row_h=row_h)
    rows = [["Judgment", "Status", "Evidence"],
            ["SQ  specification quality", cell("SQ"), "the two specifications read together; 7 clauses, no gap"],
            ["RQ  realization quality", cell("RQ"), "ruff exit 0; suite collects (10 tests)"],
            ["CONF  conformance", cell("CONF"), "10 passed; 4 of 4 test clauses cited; 100% branches; 3 stories walked"],
            ["VAL  validated", cell("VAL"), "sign-off by both user categories on conops.md A0"],
            ["TR  traceable", cell("TR"), "every marker and every \"derived from\" resolves"]]
    return table(slide, x, y, w, rows, [1.75, 1.25, w - 3.0], size=size, row_h=row_h)

# ---------- slide 1 and 2: fix the skeleton's text ----------
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
        runs_of(p0, [("The question this lecture begins to answer:", {"bold": True})], 14)
        para(tf, "", size=14, after=0)
        para(tf, "What basic principles can guide us in engineering the development and assurance context?", size=14, after=0)
    elif "Human effort will shift" in t:
        tf = sh.text_frame
        for p in list(tf.paragraphs)[1:]: p._p.getparent().remove(p._p)
        p0 = tf.paragraphs[0]
        for r in list(p0.runs): r._r.getparent().remove(r._r)
        runs_of(p0, [("Human effort will shift", {})], 16)
        for a, b in [("…from ", "engineering the code"), ("…to ", "engineering and managing the development and assurance context"),
                     ("…to ", "engineering layered, composable abstractions"), ("…that ", "provide direction to agents but also explainability to humans")]:
            para(tf, [(a, {}), (b, {"bold": True})], size=16, after=0)
s2.notes_slide.notes_text_frame.text = (s2.notes_slide.notes_text_frame.text + "\n\nLecture 01 framing: the three stages of the effort shift are the structure of the purpose section in the notes.")

# ---------- 3 purpose ----------
s = new_slide("Purpose of this lecture", notes="Name the three entities and the five judgments, define a managed process, and name the records. Everything later is an instance of this slide.")
keybar(s, "A development process is managed when the truth of five judgments can be stated at any commit, with evidence, by someone who did not write the code.", h=0.62, size=14)
bullets(s, 0.85, 2.1, 5.6, 3.9, [
    {"text": [("Intent", {"bold": True}), (" — what the stakeholders want. Lives in their minds; no file.", {})]},
    {"text": [("Specifications", {"bold": True}), (" — what the system must do, as identified clauses.", {})]},
    {"text": [("Realization", {"bold": True}), (" — the code and the tests built to satisfy them.", {})]},
], size=14, title="Three entities", title_size=16)
bullets(s, 6.7, 2.1, 6.2, 3.9, [
    {"text": [("SQ", {"bold": True}), ("  are the specifications well-formed, unambiguous, consistent, complete for their level?", {})]},
    {"text": [("RQ", {"bold": True}), ("  does the realization lint, collect, and follow the test discipline?", {})]},
    {"text": [("CONF", {"bold": True}), ("  does the realization satisfy every clause of every specification?", {})]},
    {"text": [("VAL", {"bold": True}), ("  do the specifications describe what the stakeholders intend?", {})]},
    {"text": [("TR", {"bold": True}), ("  does every clause carry an identifier, and does every link resolve?", {})]},
], size=14, title="Five judgments, each a claim tracked commit by commit", title_size=16)
bullets(s, 0.85, 5.3, 12.0, 1.5, [
    {"text": [("Records that make the state visible: ", {"bold": True}), ("the ledger (which judgments hold, on what evidence), the development log (what each task did), and the reports each judgment produces.", {})], "bullet": False},
    {"text": [("Independent of the kind of system. ", {"bold": True}), ("What varies between domains is the forms of specification and the verification methods; later lectures give the details and guidelines.", {})], "bullet": False},
], size=13, after=6)

# ---------- 4 effort ----------
s = new_slide("Where human effort goes when agents write the code", notes="Three stages of the shift. The layers serve two readers: direction for agents at the layer they work in; explanation for people, trustworthy because conformance between layers is checked.")
xs = [0.85, 4.95, 9.05]
heads = ["from engineering the code", "to engineering and managing the development and assurance context", "to engineering layered, composable abstractions"]
bodies = ["An agent writes the code quickly and in volume. The person cannot read all of it; their effort must go where an agent cannot replace it.",
          "What the agent reads and what the person reads back: specifications, rules, verification methods, evidence, records of state. Engineered artifacts with their own quality criteria.",
          "Each layer summarizes the one below; rules say how each layer is checked against the next. Direction for agents; explainability for people."]
for i in range(3):
    box(s, xs[i], 1.45, 3.4, 0.75, heads[i], size=13, fill=PURPLE if i == 2 else LAV, color=WHITE if i == 2 else BLACK, bold=True)
    textbox(s, xs[i], 2.3, 3.4, 1.5, [{"text": bodies[i], "size": 12}])
    if i < 2: line_(s, xs[i] + 3.45, 1.82, xs[i + 1] - 0.05, 1.82, width=2, tail=True)
# layer stack
ly = 4.05
layers = [("Concept of operations", "purpose, scope, user categories, stories"), ("Requirements", "identified clauses with a method"),
          ("Contracts and tests", "executable claims about clauses"), ("Code", "the realization")]
for i, (a, b) in enumerate(layers):
    box(s, 3.3, ly + i * 0.62, 4.6, 0.52, [{"text": a, "bold": True, "size": 12, "after": 0}, {"text": b, "size": 10, "color": GRAY}], fill=LAV if i < 3 else LGRAY)
box(s, 8.2, ly, 2.2, 2.38, [{"text": "Rules", "bold": True, "size": 12, "after": 2}, {"text": "how each layer is checked against the next; who decides; what evidence", "size": 10.5}], fill=PALEGOLD)
line_(s, 2.9, ly + 0.1, 2.9, ly + 2.3, width=2, tail=True); textbox(s, 0.85, ly + 0.6, 2.0, 1.0, [{"text": "direction to agents", "size": 11, "align": PP_ALIGN.RIGHT, "color": PURPLE, "bold": True}, {"text": "each layer is the standard its work is judged against", "size": 10, "align": PP_ALIGN.RIGHT, "color": GRAY}])
line_(s, 10.75, ly + 2.3, 10.75, ly + 0.1, width=2, tail=True); textbox(s, 10.9, ly + 0.6, 2.0, 1.2, [{"text": "explainability to humans", "size": 11, "color": PURPLE, "bold": True}, {"text": "read at the layer you need; trust the summary because conformance between layers is checked", "size": 10, "color": GRAY}])

# ---------- 5 objectives ----------
s = new_slide("Learning objectives", notes="Ten objectives; each is something a student can do on A0.")
obj = ["Name the three entities and the five judgments, define each as the glossary does, and point at the A0 artifact that holds or evidences each.",
       "Explain why intent has no artifact, what the purpose statement is instead, and what follows for which judgments an agent can establish alone.",
       "Describe the clause as the unit of a specification (identifier, method, derivation); distinguish mechanical from judgment clauses and say why it matters when an agent writes code and tests.",
       "State the five specification-quality properties and check a small specification against them by reading.",
       "Explain why a passing test suite is not by itself a verification, and name the four conditions of conformance in A0 with the evidence for each.",
       "Say what validation asks, who can answer it, and construct a case in which every other judgment holds and validation fails.",
       "Read a ledger row as a claim with evidence, provenance, and a stale-when condition, and say which rows a given change makes stale.",
       "Explain what a gate is and why an algorithmic gate before each commit matters when an agent is the one committing.",
       "Read a development rule in the template form and identify its decider, its evidence, and what happens on failure.",
       "Identify which elements of A0 can be set up directly in your own project and which need adaptation."]
bullets(s, 0.85, 1.4, 6.0, 5.5, [{"text": o, "char": f"{i+1}."} for i, o in enumerate(obj[:5])], size=12.5, after=7)
bullets(s, 7.05, 1.4, 5.85, 5.5, [{"text": o, "char": f"{i+6}."} for i, o in enumerate(obj[5:])], size=12.5, after=7)

# ---------- Part 1 ----------
section("Part 1 · Entities and judgments", "The picture, then one judgment at a time", notes="Part 1 is the abstract picture. Part 2 shows every element on A0.")

s = new_slide("Three entities, five judgments, one ledger", notes="Diagram 1. Intent has no artifact. VAL compares intent and specifications; CONF compares specifications and realization; SQ and RQ are loops on one artifact; TR is the dashed links. The ledger records the five; the gate decides the mechanical parts before a commit.")
diagram(s)
ledger_table(s, 8.75, 1.45, 4.15, size=10.5, row_h=0.36, short=True)
textbox(s, 8.75, 3.85, 4.15, 0.6, [{"text": "The ledger: at a named commit, which judgments hold, on what evidence, and which are stale. Every row carries its provenance.", "size": 10.5, "color": GRAY}])
box(s, 8.75, 4.85, 1.1, 0.6, "work", size=12, fill=LGRAY)
line_(s, 9.9, 5.15, 10.3, 5.15, width=2, tail=True)
box(s, 10.35, 4.7, 1.5, 0.9, [{"text": "gate", "bold": True, "size": 12, "after": 0}, {"text": "a program's exit code", "size": 9.5, "color": GRAY}], fill=PALEGOLD)
line_(s, 11.9, 5.15, 12.3, 5.15, width=2, tail=True)
box(s, 12.35, 4.85, 0.55, 0.6, "commit", size=9, fill=LGRAY, margin=0.02)
textbox(s, 8.75, 5.75, 4.15, 0.8, [{"text": "The gate: the mechanical parts of the judgments are decided before every commit; an approval gate is a recorded human decision.", "size": 10.5, "color": GRAY}])

s = new_slide("Intent", notes="Intent lives with the stakeholders; a person cannot enumerate it; the purpose statement is the nearest written thing and is an engineering artifact. An agent reaches intent only through a person, which is why VAL is reserved to a person. Elicitation is the next lecture.")
diagram(s, hl="intent")
callout(s, 8.75, 1.45, 4.15, 1.75, ["Lives in the stakeholders' minds; never fully written down.", "A person cannot enumerate everything they want, and recognizes some of it only when it is missing.", "Consulted only by asking a person: \"is this what you want?\""], title="What it is")
callout(s, 8.75, 3.4, 4.15, 1.75, ["No file called intent.", "The purpose statement that opens the concept of operations is the nearest written thing.", "An engineering artifact, agreed and audited; not a transcript of what anyone said."], title="In the repository")
callout(s, 8.75, 5.35, 4.15, 1.5, ["An agent has no access to intent except through a person.", "So one judgment, validation, is reserved to a person; and intent stays out of the set of artifacts."], title="Consequence")
leader(s, 8.75, 2.2, 5.95, 2.6)

s = new_slide("Specifications", notes="The forms A0 uses, the role a specification plays, and the clause as the unit with its three fields.")
diagram(s, hl="specs")
callout(s, 8.75, 1.45, 4.15, 2.25, ["Concept of operations: purpose, scope and terms, user categories, user stories", "Requirements: identified clauses, each with a method", ("Later: glossary, architecture, data format, contracts, state machines, sequence charts", 0)], title="Forms in A0")
callout(s, 8.75, 3.9, 4.15, 1.6, ["Captures intent (should conform to it)", "Directs the work: what the agent is told to build", "Summarizes the system; an abstraction of the realization"], title="Role")
callout(s, 8.75, 5.7, 4.15, 1.15, [{"text": [("identifier · verification method · derived from", {"bold": True})], "bullet": False}], title="The unit is the clause")
leader(s, 8.75, 2.5, 5.7, 3.6)

s = new_slide("Specification quality (SQ)", notes="Five properties, each one sentence; A0 establishes SQ by a person reading. The audit as a procedure, with seeded gaps, is the A1 lecture.")
diagram(s, hl="sq")
callout(s, 8.75, 1.45, 4.15, 3.1, [
    {"text": [("Well-formed", {"bold": True}), (" — every clause has an identifier and a method, in a form a program can read", {})]},
    {"text": [("Unambiguous", {"bold": True}), (" — one reading, so a verifier reaches yes or no", {})]},
    {"text": [("Internally consistent", {"bold": True}), (" — no two clauses contradict", {})]},
    {"text": [("Externally consistent", {"bold": True}), (" — the documents of the family agree; the same terms in the same sense", {})]},
    {"text": [("Complete for its level", {"bold": True}), (" — nothing missing at the chosen abstraction", {})]}], title="The question SQ asks", size=11.5)
callout(s, 8.75, 4.75, 4.15, 2.1, ["Traceability is tracked as its own judgment, TR", "In A0: a person reads the seven clauses together and records it (rule SQ-1)", "Next lecture: the audit as a procedure, by a person, then an agent, then a skill, on gaps placed on purpose"], title="And", size=11.5)
leader(s, 8.75, 3.2, 6.45, 3.75)

s = new_slide("Realization, and realization quality (RQ)", notes="Code and tests are both realization. RQ asks whether the realization is in a state where it can be checked: lint, collect, test discipline. Kept separate from CONF so that a conformance result is about runnable code and a suite that ran.")
diagram(s, hl="real")
callout(s, 8.75, 1.45, 4.15, 2.0, ["An artifact built to satisfy a specification; code, tests, a document, a configuration", "The code and the test suite are both realization", "One specification, many realizations: another language, another design, the same clauses"], title="Realization")
callout(s, 8.75, 3.65, 4.15, 3.2, ["Lints: ruff finds a class of mistakes more cheaply than any test", "Collects: every test file imports; every marker is declared", "Test discipline: a test can fail; asserts no looser than its clause; sets up by construction", "Structure judged appropriate (reviewed; later versions)", {"text": "Kept separate from CONF: a suite that does not collect gives no conformance evidence at all", "bold": True}], title="RQ: can the realization be checked at all?")

s = new_slide("Conformance (CONF), by verification", notes="Conformance is a relationship on the pair; verification is the attempt, so a result is evidence with a scope. In A0 CONF is four conditions because a suite written by the same agent that wrote the code can mislead in three ways.")
diagram(s, hl="conf")
callout(s, 8.75, 1.45, 4.15, 1.3, ["Conformance: R satisfies every property S states; yes or no, on the pair", "Verification: trying to confirm it; the result is evidence with a scope"], title="Does the realization conform?")
callout(s, 8.75, 2.95, 4.15, 2.2, ["Every test passes", "Requirements coverage: every test clause has a passing test", "Structural coverage: every branch exercised", "Every judgment clause has been walked"], title="Four conditions in A0", size=12)
callout(s, 8.75, 5.35, 4.15, 1.5, ["Decided by programs (pytest, the report plugin, pytest-cov) and by a person", "Three kinds of verifier: human, agent, algorithmic", "A verifier can be wrong; the ledger records which one made each claim"], title="Who decides", size=11)
leader(s, 8.75, 3.9, 7.3, 4.75)

s = new_slide("Validation (VAL)", notes="Validation compares an artifact with what is in a person's mind; only a person can decide; recorded as a sign-off. It can fail while every other judgment holds, which is the sabotage in Part 2.")
diagram(s, hl="val")
callout(s, 8.75, 1.45, 4.15, 1.6, ["Verification compares two artifacts, both in the repository", "Validation compares an artifact with what is in a person's mind, which is not"], title="Do the specifications describe what is intended?")
callout(s, 8.75, 3.25, 4.15, 1.6, ["Only a person can decide it", "Recorded as a sign-off: who, in which role, when, on which version", "Usually by reading the stories or walking the operations"], title="How it is decided")
callout(s, 8.75, 5.05, 4.15, 1.8, ["It can fail while SQ, RQ, CONF, and TR all hold: a wrong specification, realized correctly", "It goes stale when a stakeholder changes their mind, even if no file changed"], title="Why it is a separate row")
leader(s, 8.75, 2.3, 6.65, 3.1)

s = new_slide("Traceability (TR)", notes="Every clause has an identifier and every link resolves both ways. Its own row because a program decides it cheaply and the other rows depend on it clause by clause. Identifiers are the shared vocabulary of person, agent, and program.")
diagram(s, hl="tr")
callout(s, 8.75, 1.45, 4.15, 2.1, ["Every clause carries an identifier", "Every link resolves, in both directions:", {"text": "story → requirement → test → report row → ledger row", "level": 1}], title="What TR asks")
callout(s, 8.75, 3.75, 4.15, 1.45, ["The markers: a program lists any it cannot resolve", "The \"derived from\" fields: a person, with SQ"], title="Decided by")
callout(s, 8.75, 5.4, 4.15, 1.45, ["Cheap to keep established; the other four rows depend on it clause by clause", "Identifiers are the vocabulary a person, an agent, and a program share: REQ-1 means one sentence"], title="Why its own row")

# ---------- Part 2 ----------
section("Part 2 · The judgments on a real system", "Message guard, version A0", notes="Every element of Part 1 pointed at in a file.")

s = new_slide("The example: a message guard", notes="Small, realistic shape, and it grows. Version A0 is one stage, filter. The Python sibling of the HAMR Simple Network Guard.")
bullets(s, 0.85, 1.45, 5.9, 5.4, [
    "A protected enclave produces messages of differing sensitivity; some must reach a less trusted network outside",
    "The guard sits on the boundary and decides, one message at a time, whether a message may leave",
    {"text": [("A message: ", {"bold": True}), ("a security level (Public, Restricted, Critical) and an integer payload", {})]},
    {"text": [("Version A0: ", {"bold": True}), ("one stage, ", {}), ("filter", {"font": "Courier New"}), (". A Critical message is dropped; any other message passes unchanged", {})]},
    "Chosen because it is small (the working file is ten lines), its shape is realistic (a boundary, a responsible stakeholder, a wrong outcome that matters), and it grows: a second stage, a record of what was stopped, a policy change, sessions, a message format",
    {"text": "Python counterpart of the HAMR Simple Network Guard for seL4", "color": GRAY, "size": 12}], size=13, after=7)
# flow picture
box(s, 7.2, 2.2, 1.5, 0.8, "sender\n(enclave)", size=12, fill=LGRAY)
line_(s, 8.75, 2.6, 9.45, 2.6, width=2, tail=True)
textbox(s, 8.55, 1.7, 1.6, 0.45, [{"text": "Message(level, payload)", "size": 9.5, "color": GRAY, "font": "Courier New"}])
box(s, 9.5, 2.05, 1.9, 1.1, [{"text": "guard", "bold": True, "size": 13, "after": 0}, {"text": "filter", "size": 12, "font": "Courier New"}], fill=LAV)
line_(s, 11.45, 2.35, 12.15, 2.35, width=2, tail=True); textbox(s, 12.2, 2.15, 0.7, 0.4, [{"text": "pass", "size": 12, "bold": True, "color": GREEN}])
line_(s, 11.45, 2.85, 12.15, 2.85, width=2, tail=True); textbox(s, 12.2, 2.65, 0.7, 0.4, [{"text": "drop", "size": 12, "bold": True, "color": RED}])
table(s, 7.2, 3.7, 5.7, [["Level", "A0 behavior", "HAMR requirement"], ["Public", "passes unchanged", "Req_P"], ["Restricted", "passes unchanged", "Req_R_1"], ["Critical", "dropped: no output", "Req_C"]], [1.5, 2.3, 1.9], size=12)

s = new_slide("The question the code cannot answer", notes="Twelve-line file. Is it right? It cannot say what was asked, what was promised, or whether the promise was checked. With an agent writing the code, the person reads three other things instead.")
code(s, 0.85, 1.45, 7.6, 2.2, '''"""The filter stage: pass or drop a message by its security level (REQ-1 to REQ-3)."""

from guard.message import Message, SecurityLevel


def filter_message(message: Message) -> Message | None:
    """Return the message unchanged if it may leave the enclave, or None if it is dropped."""
    if message.level is SecurityLevel.CRITICAL:
        return None  # REQ-1
    return message  # REQ-2, REQ-3''', size=10)
textbox(s, 0.85, 3.7, 7.6, 0.3, [{"text": "guard/filter.py, the whole file", "size": 10, "color": GRAY, "font": "Courier New"}])
callout(s, 8.75, 1.45, 4.15, 2.55, [{"text": [("What was asked for", {"bold": True}), (" — which levels were meant to be stopped", {})]},
                                   {"text": [("What was promised", {"bold": True}), (" — a statement someone responsible agreed to", {})]},
                                   {"text": [("Whether the promise was checked", {"bold": True}), (" — by what, and when", {})]},
                                   {"text": "The code would look exactly like this if Restricted messages were meant to be stopped too.", "bullet": False, "italic": True, "size": 11}], title="Three things the code does not say")
keybar(s, "With an agent writing the code, the person reads the specification, the evidence of conformance, and the record of whether that evidence is current. An agent's description of its own work is not evidence about the work.", y=4.35, h=0.85, size=13)
bullets(s, 0.85, 5.4, 12.0, 1.2, ["When those three exist and can be trusted, a person can direct the work, review it, and take responsibility for code they have not read line by line."], size=13)

s = new_slide("Version A0, by category", notes="The directory tree, by the categories the diagram uses. Support files are not realizations of any clause.")
table(s, 0.85, 1.45, 12.05, [["Category", "Files", "Role"],
    ["Intent", "none", "lives with the stakeholders; consulted through a person"],
    ["Specifications", "specs/conops.md · specs/requirements.md", "what the system must do, as identified clauses"],
    ["Realization", "guard/ (the code) · tests/ (the suite)", "what was built, and the executable claims about it"],
    ["Development rules", "process/rules.md", "how each judgment is established and when it must hold"],
    ["Reports", "reports/ledger.md · dev-log.md · walkthrough.md · conformance.md (generated)", "the development state, readable without reading the code"],
    ["Technology", "pyproject.toml · uv.lock", "Python 3.12+; pytest, pytest-cov, ruff; managed by uv"],
    ["Support", "tools/gate.sh · tools/walk.py", "the gate command; a helper for walking a scenario; neither realizes a clause"]],
    [2.0, 5.0, 5.05], size=12, row_h=0.5)
keybar(s, "Every entity and every judgment in Part 1 is now a file or a row that can be opened.", y=5.75, size=14)

s = new_slide("Intent in A0: the purpose statement", notes="The nearest written thing to intent. Agreed by the stakeholders, audited, derived from; not a transcript. How it was obtained is the next lecture.")
box(s, 0.85, 1.45, 7.9, 1.7, [{"text": "An organization keeps a protected enclave whose systems produce messages of differing sensitivity, and it needs some of those messages to reach a less trusted network outside the enclave. The message guard sits on that boundary and decides, one message at a time, whether a message may leave. Nothing leaves the enclave except through the guard.", "size": 13, "italic": True, "align": PP_ALIGN.LEFT}], fill=PALEGOLD, line=BLACK, lw=0.75, anchor=MSO_ANCHOR.TOP, margin=0.15, shadow=True)
textbox(s, 0.85, 3.2, 7.9, 0.3, [{"text": "specs/conops.md, section 1, first paragraph", "size": 10, "color": GRAY, "font": "Courier New"}])
bullets(s, 9.0, 1.45, 3.9, 5.4, ["A short text the stakeholders revised until they agreed", "An engineering artifact: a clause others derive from, checked for consistency with the rest", "Not a transcript; a transcript is reference material and is not checked", "No file called intent anywhere in v0", "The sign-off that validates it is in reports/walkthrough.md"], size=12.5, after=8, title="What it is and is not")
bullets(s, 0.85, 3.7, 7.9, 2.2, [{"text": [("How it was obtained ", {"bold": True}), ("from the stakeholders, and how the stories were, is the next lecture: elicitation on version A1. In A0 they are given as already agreed.", {})], "bullet": False}], size=13)

s = new_slide("The specifications in A0: a family of two", notes="conops.md has five sections; requirements.md has four clauses. Two kinds of document that govern one system and must agree.")
bullets(s, 0.85, 1.45, 6.0, 5.3, [
    {"text": [("1  Purpose", {"bold": True}), (" — the agreed purpose statement", {})]},
    {"text": [("2  Scope and system boundary", {"bold": True}), (" — a library function: one message in, that message or nothing out; outside: transport, authentication, how levels are assigned, any record of drops; ", {}), ("Terms", {"bold": True}), (": message, security level, payload, pass, drop, filter", {})]},
    {"text": [("3  User categories", {"bold": True}), (" — message sender; security officer", {})]},
    {"text": [("4  User stories", {"bold": True}), (" — US-1, US-2, US-3, each with an example message, each marked ", {}), ("walkthrough (human)", {"italic": True})]},
    {"text": [("5  Sign-off", {"bold": True}), (" — a pointer to the record", {})]}], size=12.5, after=7, title="specs/conops.md — the concept of operations", title_size=14)
bullets(s, 7.1, 1.45, 5.8, 5.3, [
    {"text": [("REQ-0", {"bold": True}), ("  a message is a level, one of three, and an integer payload; it does not change after creation", {})]},
    {"text": [("REQ-1", {"bold": True}), ("  the filter drops every Critical message: no output", {})]},
    {"text": [("REQ-2", {"bold": True}), ("  the filter passes every Restricted message unchanged", {})]},
    {"text": [("REQ-3", {"bold": True}), ("  the filter passes every Public message unchanged", {})]},
    {"text": "each marked test; each names the story or term it derives from", "bullet": False, "italic": True, "color": GRAY, "size": 12}], size=12.5, after=7, title="specs/requirements.md — the requirements", title_size=14)
keybar(s, "A family: two documents of different kinds that govern one system and must agree with each other.", y=5.95, size=14)

s = new_slide("The clause is the unit", notes="Two clauses verbatim. Three fields, each with a job: the identifier is what a report cites; the method says who verifies; derived-from makes the family.")
code(s, 0.85, 1.45, 7.5, 1.9, '''**US-1** · Method: walkthrough (human) · User category: message sender

As a message sender, when I send a Public message, I expect it to
arrive outside the enclave unchanged.

Example: the guard is given (Public, 42); it outputs (Public, 42).''', size=10.5)
code(s, 0.85, 3.5, 7.5, 1.25, '''**REQ-1** · Method: test · Derived from: US-3

The filter drops every message whose security level is Critical:
for such a message it produces no output.''', size=10.5)
callout(s, 8.75, 1.45, 4.15, 1.5, ["What a report cites. A person, an agent, and a program all say REQ-1 and mean the same sentence, so their reports compare."], title="Identifier", size=11.5)
callout(s, 8.75, 3.15, 4.15, 1.9, ["How the clause is verified, so who can verify it. test: a program decides. walkthrough: a person exercises the system and judges.", "Recorded on the clause, not in the verifier's head."], title="Verification method", size=11.5)
callout(s, 8.75, 5.25, 4.15, 1.6, ["Links a requirement to the story or term it refines. Every requirement traces back to something a stakeholder wanted; every story forward to what makes it precise."], title="Derived from", size=11.5)
textbox(s, 0.85, 4.9, 7.5, 1.9, [{"text": "What the specifications leave open on purpose: how a message reaches the guard, how its level was assigned, what happens to a dropped message. Outside the boundary; the realization is free there.", "size": 12, "color": GRAY}])

s = new_slide("Mechanical clauses and judgment clauses", notes="A mechanical clause can be checked at every commit by a program nobody has to remember to run; a judgment clause costs a person's attention every time. With an agent writing the code, make as many clauses mechanical as possible and record the choice on the clause.")
table(s, 0.85, 1.45, 12.05, [["Method", "Who decides", "In A0", "Can stand in a gate"],
    ["test", "a program: a test cites the clause and passes or fails", "REQ-0 to REQ-3", "yes"],
    ["walkthrough", "a person exercises the system along the scenario and judges", "US-1 to US-3", "no"],
    ["analysis (later)", "a program, by examining the artifact rather than running it: type checker, import rule, schema validator", "version A2", "yes"],
    ["review (later)", "a reader, from the text: a person or an agent", "version A2", "no"]], [2.0, 5.4, 2.4, 2.25], size=12, row_h=0.55)
keybar(s, "Mechanical: a program can decide it. Judgment: it needs a reader. A clause that cannot be made mechanical is marked as such, never silently left unchecked.", y=4.5, h=0.7, size=13)
bullets(s, 0.85, 5.4, 12.0, 1.4, ["A mechanical clause is checked at every commit by a program nobody has to remember to run; a judgment clause costs a person's attention each time", "When an agent writes the code and the tests, push clauses toward mechanical, and keep the pressure visible on the clause itself"], size=13, after=6)

s = new_slide("Specification quality on A0", notes="Each property with the place in A0 where it can be checked. The REQ-2 question is planted to show that a reading is a judgment. SQ-1 and the SQ row.")
table(s, 0.85, 1.45, 12.05, [["Property", "Means", "Where to look in A0"],
    ["Well-formed", "every clause has an identifier and a method, in a form a program can read", "the header line **REQ-1** · Method: test; the report plugin parses exactly that"],
    ["Unambiguous", "one reading, so a verifier reaches yes or no", "REQ-1 says what drop means in the same sentence. REQ-2 says \"unchanged\": is equality of level and payload the only reading?"],
    ["Internally consistent", "no two clauses contradict", "REQ-1 to REQ-3 give each level one outcome; \"every message is passed\" would contradict REQ-1"],
    ["Externally consistent", "the family agrees; same terms, same sense", "every REQ derives from a story or a term; Public, Restricted, Critical, pass, drop mean the same in both files"],
    ["Complete for its level", "nothing missing at the chosen abstraction", "three levels, three requirements; transport is outside the boundary, not a gap"]],
    [2.0, 4.0, 6.05], size=11.5, row_h=0.62)
bullets(s, 0.85, 5.35, 12.0, 1.5, [{"text": [("Established in A0 by rule SQ-1: ", {"bold": True}), ("a person read the seven clauses together and recorded who, when, and which clauses in the ledger's SQ row.", {})]},
                                   {"text": [("Next lecture: ", {"bold": True}), ("the audit as a procedure, on a specification with gaps placed in it on purpose; the form in which gaps are reported and ruled on.", {})]}], size=12.5, after=5)

s = new_slide("The realization", notes="message.py makes REQ-0 concrete: three levels, a frozen dataclass, rejection of wrong types. filter.py is the working file. One specification, many realizations.")
code(s, 0.85, 1.45, 6.6, 3.5, '''class SecurityLevel(Enum):
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
            raise TypeError(...)''', size=10.5)
textbox(s, 0.85, 5.0, 6.6, 0.3, [{"text": "guard/message.py (abridged): REQ-0 made concrete", "size": 10, "color": GRAY, "font": "Courier New"}])
code(s, 7.75, 1.45, 5.15, 1.5, '''def filter_message(message: Message) -> Message | None:
    if message.level is SecurityLevel.CRITICAL:
        return None  # REQ-1
    return message  # REQ-2, REQ-3''', size=10)
textbox(s, 7.75, 3.0, 5.15, 0.3, [{"text": "guard/filter.py: REQ-1 to REQ-3", "size": 10, "color": GRAY, "font": "Courier New"}])
bullets(s, 7.75, 3.5, 5.15, 3.3, ["The code and the test suite are both realization: both are built to satisfy the specifications", "One specification, many realizations: a different program in a different language that drops Critical and passes the rest realizes the same clauses", "Under thirty lines of code; the specifications, rules, and reports are over three hundred"], size=12.5, after=8)

s = new_slide("Tests as executable specification", notes="Each test is a claim about one clause and cites it. The marker serves three readers. A test that cites nothing is not allowed in A0.")
code(s, 0.85, 1.45, 7.3, 3.65, '''@pytest.mark.req("REQ-1")
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
    assert filter_message(message) == message''', size=10.5)
textbox(s, 0.85, 5.15, 7.3, 0.3, [{"text": "tests/test_filter.py", "size": 10, "color": GRAY, "font": "Courier New"}])
callout(s, 8.45, 1.45, 4.45, 2.9, [{"text": [("A program", {"bold": True}), (" computes which clauses have tests and which do not", {})]},
                                   {"text": [("A person", {"bold": True}), (" who sees the test fail knows which clause is in question without reading the body", {})]},
                                   {"text": [("An agent", {"bold": True}), (" writing a test must say which clause it is evidence for; a test that exercises code and claims nothing is ruled out", {})]}], title="The marker serves three readers", size=12)
callout(s, 8.45, 4.55, 4.45, 1.0, [{"text": "A test that cites no clause is not allowed in the suite (CONF-1, TR-1).", "bullet": False}], size=12, fill=PALEGOLD)
leader(s, 8.45, 2.2, 3.3, 1.65)

s = new_slide("Realization quality (RQ) in A0", notes="Two programs decide RQ; the test discipline is reviewed. RQ is separate from CONF so a conformance result is about runnable code and a suite that ran.")
bullets(s, 0.85, 1.45, 6.3, 5.3, [
    {"text": [("ruff check", {"font": "Courier New", "bold": True}), ("  unused and undefined names, syntax that will not run: cheaper than any test", {})]},
    {"text": [("pytest --collect-only -q --no-cov", {"font": "Courier New", "bold": True}), ("  every test file imports; every marker is declared", {})]},
    {"text": [("Test discipline", {"bold": True}), (" (reviewed): a test can fail; asserts no more loosely than its clause; sets up inputs by construction, not by reaching into internals", {})]},
    {"text": [("Structure judged appropriate", {"bold": True}), (": reviewed in later versions", {})]}], size=13, after=9, title="What RQ asks of A0", title_size=15)
table(s, 7.4, 1.45, 5.5, [["RQ-1", ""], ["Style", "obligation"], ["Maintains", "RQ"], ["When", "at every commit; guard/, tests/, tools/"], ["Statement", "The realization MUST pass ruff check, and the suite MUST collect without error."], ["Decided by", "analysis: the two commands; a non-zero exit code fails it"], ["Evidence", "exit codes, in the dev-log entry of the task"], ["On failure", "fixed before the commit (WF-1)"]], [1.3, 4.2], size=11, row_h=0.42, hdr_fill=DPURPLE)
keybar(s, "Why a separate row: a suite that does not collect produces no conformance evidence at all; a module with an undefined name passes every test that does not reach it.", y=5.6, h=0.7, size=13)

s = new_slide("Conformance is four conditions", notes="A passing suite establishes only that its own claims hold. With the same agent writing code and tests a green suite misleads in three ways, so CONF is the conjunction of four conditions, each with its own evidence.")
keybar(s, "A passing test suite, on its own, establishes only that the suite's own claims hold.", size=15)
conds = [("1  Every test passes", "the run itself", "pytest", "program"),
         ("2  Requirements coverage", "every test clause is cited by a passing test", "reports/conformance.md", "program: the plugin"),
         ("3  Structural coverage", "every branch of guard/ exercised", "the coverage table", "program: pytest-cov"),
         ("4  Judgment clauses walked", "each story exercised by a person in its role", "reports/walkthrough.md", "a person")]
for i, (a, b, c, d) in enumerate(conds):
    x = 0.85 + i * 3.05
    box(s, x, 2.1, 2.85, 0.65, a, size=13, bold=True, fill=LAV)
    textbox(s, x, 2.85, 2.85, 1.1, [{"text": b, "size": 12}])
    textbox(s, x, 3.95, 2.85, 0.5, [{"text": c, "size": 10.5, "font": "Courier New", "color": GRAY}])
    box(s, x, 4.5, 2.85, 0.5, [{"text": [("decided by ", {"color": GRAY}), (d, {"bold": True})], "size": 11}], fill=PALEGOLD, line=None)
bullets(s, 0.85, 5.3, 12.0, 1.5, ["The suite may contain no test for a clause: green, and the clause is unverified (condition 2)", "The tests may exercise only part of the code: the rest may do anything (condition 3)", "The clauses no test can decide may simply be skipped (condition 4)"], size=12.5, after=4, title="Three ways a green suite misleads", title_size=13)

s = new_slide("The evidence: the conformance report and the coverage table", notes="The plugin reads the clause identifiers from the specifications and the markers from the suite; one row per clause. A clause with no citing test would show no evidence and fail the run. Branch coverage is weak but finds the places where code can do anything unnoticed.")
table(s, 0.85, 1.45, 7.3, [["Clause", "Method", "Tests citing it", "Status"],
    ["US-1", "walkthrough", "—", "see walkthrough.md"], ["US-2", "walkthrough", "—", "see walkthrough.md"], ["US-3", "walkthrough", "—", "see walkthrough.md"],
    ["REQ-0", "test", "five tests in test_message.py", {"text": "pass", "color": GREEN, "bold": True}],
    ["REQ-1", "test", "test_critical_is_dropped[0], [100], [-5]", {"text": "pass", "color": GREEN, "bold": True}],
    ["REQ-2", "test", "test_restricted_passes_unchanged", {"text": "pass", "color": GREEN, "bold": True}],
    ["REQ-3", "test", "test_public_passes_unchanged", {"text": "pass", "color": GREEN, "bold": True}]], [0.9, 1.3, 3.5, 1.6], size=11, row_h=0.36)
textbox(s, 0.85, 4.4, 7.3, 0.5, [{"text": "reports/conformance.md — Requirements coverage: 4 of 4 test clauses have passing evidence. Unknown identifiers: none.", "size": 10.5, "color": GRAY}])
code(s, 8.4, 1.45, 4.5, 1.5, '''Name              Stmts Miss Branch BrPart Cover
guard/__init__.py     3    0      0      0  100%
guard/filter.py       5    0      2      0  100%
guard/message.py     13    0      4      0  100%
TOTAL                21    0      6      0  100%''', size=9.5)
textbox(s, 8.4, 3.0, 4.5, 0.5, [{"text": "pytest-cov: branch coverage; the run fails below 100 percent", "size": 10.5, "color": GRAY}])
bullets(s, 0.85, 5.0, 12.0, 1.9, ["Requirements coverage is a coverage measure over the specification, as branch coverage is one over the code", "Branch coverage is not strong: every branch was taken by some test, not that the test checked anything useful there; but a branch no test took is a place where the code can do anything unnoticed"], size=12.5, after=5)

s = new_slide("Who decided: the walkthroughs, and three kinds of verifier", notes="Condition 4 was decided by a person in the story's role. Three kinds of verifier; A0 uses human and algorithmic; the agent verifier enters in A1.")
table(s, 0.85, 1.45, 12.05, [["Clause", "Role", "Command", "Observed", "Finding"],
    ["US-1", "message sender", "tools/walk.py Public 42", "pass: Public 42", "as the story expects"],
    ["US-2", "message sender", "tools/walk.py Restricted 7", "pass: Restricted 7", "as the story expects"],
    ["US-3", "security officer", "tools/walk.py Critical 100, then Critical 0", "drop, both times", "as the story expects"]], [0.9, 1.7, 4.2, 2.3, 2.95], size=11.5, row_h=0.36)
textbox(s, 0.85, 2.95, 12.0, 0.3, [{"text": "reports/walkthrough.md — walked by the instructor, in each role, on 2026-10-20, against v0", "size": 10.5, "color": GRAY}])
table(s, 0.85, 3.45, 12.05, [["", "Human", "Agent", "Algorithmic"],
    ["Cost per check", "minutes of attention", "tokens", "milliseconds"],
    ["Same result on repeat", "not guaranteed", "not guaranteed", "yes"],
    ["Decides judgment clauses", "yes", "yes", "no"],
    ["Can stand in a gate", "no", "with effort", "yes, via the exit code"],
    ["In A0", "the walkthroughs; SQ; the sign-off", "not yet (enters in A1, as the auditor)", "pytest, the report plugin, pytest-cov, ruff"]], [2.6, 3.0, 3.2, 3.25], size=11.5, row_h=0.4)
textbox(s, 0.85, 6.0, 12.0, 0.8, [{"text": "A verifier is itself a realization of the specification it checks: a test can assert the wrong thing, a plugin can misread a marker. \"Who verifies the verifier\" is answered separately, and the ledger records which verifier made each claim so that a wrong one can be traced. That is as far as this lecture takes it.", "size": 11.5, "color": GRAY}])

s = new_slide("Validation in A0: the sign-off", notes="The sign-off names who, in which role, when, on which version. The walkthrough does double duty: one activity, two questions. Keep them apart in thought.")
box(s, 0.85, 1.45, 7.6, 1.75, [{"text": "\"The concept of operations, version A0, describes the guard I intend: a Critical message never leaves, and anything else leaves as it arrived.\"", "size": 13, "italic": True, "align": PP_ALIGN.LEFT, "after": 8},
    {"text": "Security officer: role played by the instructor, 2026-10-20, on specs/conops.md version A0.", "size": 11.5, "align": PP_ALIGN.LEFT, "after": 2},
    {"text": "Message sender: role played by the instructor, 2026-10-20, on specs/conops.md version A0.", "size": 11.5, "align": PP_ALIGN.LEFT}], fill=PALEGOLD, line=BLACK, lw=0.75, anchor=MSO_ANCHOR.TOP, margin=0.15, shadow=True)
textbox(s, 0.85, 3.25, 7.6, 0.3, [{"text": "reports/walkthrough.md, section Sign-off (rule VAL-1: one from each user category)", "size": 10, "color": GRAY, "font": "Courier New"}])
bullets(s, 8.75, 1.45, 4.15, 5.4, ["Verification compares two artifacts in the repository; validation compares an artifact with what is in a person's mind", "So only a person can decide it, and the decision is recorded: who, role, when, version", {"text": [("One activity, two questions. ", {"bold": True}), ("When the officer walks US-3 and sees drop: does the system behave as the story says (conformance of a judgment clause), and is the story what the officer wants (validation)?", {})]}, "A different officer could answer the first yes and the second no"], size=12, after=8)
keybar(s, "An agent given a specification will realize it, and a well-run process will certify that. The sign-off is the one place the process asks a person whether the certified system is the one they wanted.", y=3.7, h=0.85, size=12.5)
bullets(s, 0.85, 4.75, 7.6, 1.3, ["The VAL row can go stale when no file has changed: a stakeholder changes their mind and says so. Version A3 records that as a change request."], size=12)

s = new_slide("Breaking it: a wrong system with a green ledger", notes="Suppose the officer meant Restricted must be stopped too and the author of the ConOps did not understand. Every artifact was derived from the same misunderstanding; nothing in the repository can detect it. Only the officer walking US-2 or declining to sign catches it.")
keybar(s, "Suppose the security officer meant that Restricted messages must be stopped as well, and the person who wrote the concept of operations did not understand this.", h=0.7, size=13)
ledger_table(s, 0.85, 2.25, 7.3, statuses={"VAL": "signed without reading?"}, size=11, row_h=0.42)
bullets(s, 8.45, 2.25, 4.45, 4.6, ["US-2 and REQ-2 agree with each other: consistent", "Every requirement has a passing test; branch coverage is complete; every identifier resolves", "Four rows on sound evidence; the fifth too, if the officer signs without reading", {"text": [("Nothing in the repository can detect it: ", {"bold": True}), ("every artifact was derived from the same misunderstanding", {})]}, {"text": [("What catches it: ", {"bold": True}), ("the officer walking US-2, seeing pass: Restricted 7, and saying this is not what they want; or reading the concept of operations and declining to sign", {})]}], size=12, after=7)
textbox(s, 0.85, 5.2, 7.3, 1.6, [{"text": "This is why validation is a separate judgment with a separate row, and why the row's evidence is a person's recorded decision rather than a tool's output. There is no command to run for this sabotage; that is its point.", "size": 12.5}])

s = new_slide("Traceability in A0", notes="The chain of links; TR-1; what the program decides and what a person reads. Identifiers are the vocabulary shared by person, agent, and program.")
chain = [("US-3", "story", "conops.md"), ("REQ-1", "requirement", "derived from US-3"), ("test_critical_is_dropped", "test", "@pytest.mark.req(\"REQ-1\")"), ("REQ-1 row", "conformance report", "pass"), ("CONF row", "ledger", "cites the report")]
for i, (a, b, c) in enumerate(chain):
    x = 0.85 + i * 2.45
    box(s, x, 1.55, 2.2, 1.1, [{"text": a, "bold": True, "size": 10 if i == 2 else 12, "font": "Courier New" if i == 2 else None, "after": 0}, {"text": b, "size": 10.5, "color": GRAY, "after": 0}, {"text": c, "size": 9.5, "color": GRAY}], fill=LAV if i < 3 else PALEGOLD)
    if i < 4: line_(s, x + 2.22, 2.1, x + 2.43, 2.1, width=2, tail=True)
textbox(s, 0.85, 2.75, 12.0, 0.4, [{"text": "Every link resolves in both directions; a reader can go from any claim to its evidence, and from any change to its consequences.", "size": 12}])
table(s, 0.85, 3.35, 7.3, [["TR-1", ""], ["Statement", "Every req marker MUST name a clause the specifications define; every \"derived from\" MUST name a clause that exists."], ["Decided by", "analysis: the report plugin lists unknown identifiers and fails the run; --strict-markers rejects an undeclared marker. The derived-from part: a person, with SQ-1."], ["Evidence", "the Unknown identifiers section of reports/conformance.md"], ["On failure", "the marker or the reference is corrected"]], [1.3, 6.0], size=11, row_h=0.5, hdr_fill=DPURPLE)
bullets(s, 8.45, 3.35, 4.45, 3.5, ["Its own row because a program decides it cheaply, and the other four rows depend on it clause by clause", "A conformance report is readable only if its identifiers resolve; an audit finding is actionable only if it names a clause", {"text": [("The identifiers are the vocabulary ", {"bold": True}), ("that the person, the agent, and the programs share: when all three say REQ-1 they mean the same sentence", {})]}], size=12, after=7, title="Why TR is a row", title_size=13)

s = new_slide("The ledger at v0", notes="Five rows. Each is a claim with status, evidence, provenance, and a stale-when. Provenance distinguishes evidence from a description of evidence: an exit code at a named commit can be rerun; an agent's 'all tests pass' cannot.")
table(s, 0.85, 1.45, 12.05, [["Judgment", "Status", "Evidence", "Provenance", "Goes stale when"],
    ["SQ", {"text": "established", "color": GREEN, "bold": True}, "two specifications read together; 7 clauses; no contradiction, no clause with two readings", "review (human): the instructor, 2026-10-20, specifications at v0, US-1–3, REQ-0–3", "any specification changes"],
    ["RQ", {"text": "established", "color": GREEN, "bold": True}, "ruff exit 0; collect exit 0, 10 tests", "analysis: ruff 0.17.1, pytest 9.1.1, Python 3.14.7; realization at v0", "the code or the tests change"],
    ["CONF", {"text": "established", "color": GREEN, "bold": True}, "10 passed; 4 of 4 test clauses; 100% branches; US-1–3 walked", "analysis: pytest 9.1.1 + pytest-cov 7.1.0 + the plugin, at v0, REQ-0–3; walkthrough (human): the instructor, 2026-10-20, US-1–3", "a specification or the code changes"],
    ["VAL", {"text": "established", "color": GREEN, "bold": True}, "sign-off by both user categories", "review (human): sign-off dated 2026-10-20 on conops.md A0", "a declared change of mind; conops or a requirement changes"],
    ["TR", {"text": "established", "color": GREEN, "bold": True}, "every marker resolves; every derived-from resolves", "analysis: the plugin at v0 over 10 markers; review (human) for derived-from", "any artifact changes"]],
    [0.9, 1.1, 3.4, 4.3, 2.35], size=10.5, row_h=0.62)
callout(s, 0.85, 5.3, 12.05, 1.5, [{"text": [("Status", {"bold": True}), (" established or stale.  ", {}), ("Evidence", {"bold": True}), (" what was produced, named precisely enough to be found.  ", {}), ("Provenance", {"bold": True}), (" who or what, against which versions, over which clauses: the three scope lines of a verification result, moved onto the row.  ", {}), ("Stale when", {"bold": True}), (" what change would require re-establishing it.", {})], "bullet": False, "size": 11.5},
    {"text": "A row is a claim made by a verifier, not a fact about the system. \"pytest 9.1.1 exited 0 at v0\" can be rerun; \"all tests pass\" in an agent's completion message cannot.", "bullet": False, "size": 11.5, "italic": True}], title="A row has four parts", size=11.5, fill=PALEGOLD)

s = new_slide("The gate", notes="WF-1: tools/gate.sh must exit 0 before a commit. An algorithmic gate decides RQ and the three mechanical conditions of CONF. Approval gates are recorded human decisions; the first one in front of a commit arrives with the build plan in A2. A gate makes the checks a property of every commit.")
box(s, 0.85, 1.6, 1.6, 0.9, "work on a task", size=12, fill=LGRAY)
line_(s, 2.5, 2.05, 3.0, 2.05, width=2, tail=True)
box(s, 3.05, 1.45, 4.3, 1.2, [{"text": "tools/gate.sh", "bold": True, "size": 13, "font": "Courier New", "after": 2}, {"text": "uv run ruff check .     →  RQ", "size": 11, "font": "Courier New", "after": 0}, {"text": "uv run pytest           →  CONF 1–3, TR", "size": 11, "font": "Courier New"}], fill=PALEGOLD)
line_(s, 7.4, 2.05, 7.9, 2.05, width=2, tail=True)
box(s, 7.95, 1.6, 1.3, 0.9, "exit 0", size=13, bold=True, fill=PALEGREEN, color=GREEN)
line_(s, 9.3, 2.05, 9.8, 2.05, width=2, tail=True)
box(s, 9.85, 1.6, 1.3, 0.9, "commit", size=12, fill=LGRAY)
box(s, 7.95, 2.7, 1.3, 0.7, "exit 1", size=13, bold=True, fill=PALERED, color=RED)
line_(s, 9.3, 3.05, 9.8, 3.05, width=2, tail=True)
textbox(s, 9.85, 2.8, 3.0, 0.5, [{"text": "the work is returned to the task; no commit", "size": 11.5}])
bullets(s, 0.85, 3.7, 6.0, 3.2, [{"text": [("A gate ", {"bold": True}), ("is a condition placed in front of a step so the step cannot complete unless it holds", {})]},
    {"text": [("Algorithmic gate: ", {"bold": True}), ("a program decides; the decision is an exit code. This one decides RQ and the first three conditions of CONF in one command (rule WF-1)", {})]},
    {"text": [("Approval gate: ", {"bold": True}), ("a recorded human decision. A0's sign-off is one but does not stand in front of a commit; the first that does arrives with the build plan in A2", {})]}], size=12.5, after=8)
callout(s, 7.2, 3.7, 5.7, 2.2, ["An agent commits often, and a rule that depends on someone remembering to run the checks will be skipped", "A gate makes the checks a property of every commit: an invariant of the history"], title="Why a gate rather than a rule that says to run the checks", size=12)

s = new_slide("Breaking it: a wrong realization", notes="Change the condition to RESTRICTED. Four tests fail; REQ-1 and REQ-2 show FAIL; coverage still 100 percent; only CONF turns red; the suite caught it. A failed check is a fact about the pair; which side moves is a recorded decision.")
code(s, 0.85, 1.45, 5.6, 1.1, '''-    if message.level is SecurityLevel.CRITICAL:
+    if message.level is SecurityLevel.RESTRICTED:''', size=10.5)
textbox(s, 0.85, 2.6, 5.6, 0.3, [{"text": "guard/filter.py: Critical now passes; Restricted is dropped", "size": 10, "color": GRAY, "font": "Courier New"}])
code(s, 0.85, 3.05, 5.6, 1.6, '''conformance: REQ-1: FAIL
conformance: REQ-2: FAIL
conformance: FAIL, see reports/conformance.md
TOTAL   21  0  6  0  100%
4 failed, 6 passed in 0.05s''', size=10.5)
textbox(s, 0.85, 4.7, 5.6, 0.3, [{"text": "tools/gate.sh, exit 1", "size": 10, "color": GRAY, "font": "Courier New"}])
ledger_table(s, 6.75, 1.45, 6.15, statuses={"CONF": "stale"}, size=10.5, row_h=0.4)
bullets(s, 6.75, 4.1, 6.15, 2.8, ["Four tests fail: three cases of REQ-1 and the one for REQ-2; the report shows those two clauses as FAIL", {"text": [("Branch coverage is still 100 percent: ", {"bold": True}), ("coverage says which code ran, not whether it was right", {})]}, "Only CONF turned red; the verifier that caught it is the test suite. SQ, VAL, TR are untouched: no specification changed, every link resolves"], size=12, after=6)
keybar(s, "A failed check reports a fact about the pair: S and R do not agree. Which side moves is an engineering decision made by a person and recorded; here the code moves back (dev log). Amendments and change requests arrive in A3.", y=5.2, x=0.85, w=5.6, h=1.3, size=11.5)

s = new_slide("The development rules: eight, in one form", notes="One rule per judgment plus workflow and reports, CONF having two. Each has the same fields. Decided-by makes a rule checkable; on-failure gives a red result a next step. Two styles in A0.")
bullets(s, 0.85, 1.45, 4.6, 5.4, [
    {"text": [("SQ-1", {"bold": True}), ("  the specifications are well-formed and consistent", {})]},
    {"text": [("RQ-1", {"bold": True}), ("  the realization lints and the suite collects", {})]},
    {"text": [("CONF-1", {"bold": True}), ("  every mechanical clause has passing evidence, and the code is exercised", {})]},
    {"text": [("CONF-2", {"bold": True}), ("  every judgment clause has a walkthrough record", {})]},
    {"text": [("VAL-1", {"bold": True}), ("  the concept of operations carries a sign-off", {})]},
    {"text": [("TR-1", {"bold": True}), ("  every reference resolves", {})]},
    {"text": [("WF-1", {"bold": True}), ("  the gate stands before every commit", {})]},
    {"text": [("RPT-1", {"bold": True}), ("  the dev log and the ledger are kept", {})]},
    {"text": "Two styles: an obligation (every X MUST have property P) and a gate (WHEN step S would complete, condition C MUST hold).", "bullet": False, "size": 11.5, "color": GRAY, "after": 0}], size=12, after=5, title="process/rules.md", title_size=14)
table(s, 5.7, 1.45, 7.2, [["CONF-1", "Every mechanical clause has passing evidence, and the code is exercised"],
    ["Style", "obligation"], ["Maintains", "CONF"], ["When", "at every commit; every clause whose method is test"],
    ["Statement", "Every clause with method test MUST be cited, by marker, by at least one test; every citing test MUST pass; and the suite MUST reach 100 percent branch coverage of guard/."],
    ["Decided by", "analysis: uv run pytest. The plugin fails the run on a clause with no evidence or a failing citation; pytest-cov fails it below 100 percent."],
    ["Evidence", "reports/conformance.md; the coverage table, recorded in the dev log"],
    ["On failure", "a test is added or fixed, or the code is fixed; a clause is never weakened to make the run pass"],
    ["Example", "REQ-1 is cited by test_filter.py::test_critical_is_dropped"]], [1.3, 5.9], size=10.5, row_h=0.45, hdr_fill=DPURPLE)
keybar(s, "Decided by names the verifier, so a rule can actually be checked. On failure says what happens, so a red result has a next step.", y=6.1, x=5.7, w=7.2, h=0.7, size=11.5)

s = new_slide("Why the rules are a file, and where the effort goes", notes="The agent reads the file; person and agent follow the same written process; a habit cannot be followed by an agent and a prompt cannot be audited by a person. The dev log. Effort: under thirty lines of code against more than three hundred of specifications, rules, reports. Optional demo: ask an agent what the system does and how it knows; watch where it looks.")
bullets(s, 0.85, 1.45, 6.0, 5.4, ["An agent started in this directory is told to read process/rules.md; from then on the person and the agent follow the same written process", "It cites a clause in each test because CONF-1 says so; it records the gate result because RPT-1 says so", "A process that lives in a person's habits cannot be followed by an agent; one that lives in the agent's prompt cannot be audited by a person; a file can be both followed and audited", {"text": [("reports/dev-log.md", {"font": "Courier New", "bold": True}), (": the append-only record of what each task did, the judgments it touched, and the gate result. The ledger says where things stand; the log says what happened", {})]}], size=12.5, after=8, title="The rules are a file because the agent reads it", title_size=14)
box(s, 7.3, 1.45, 2.6, 1.5, [{"text": "< 30", "size": 34, "bold": True, "color": PURPLE, "after": 0}, {"text": "lines of code in guard/", "size": 11}], fill=LAV2, line=None)
box(s, 10.2, 1.45, 2.7, 1.5, [{"text": "> 300", "size": 34, "bold": True, "color": PURPLE, "after": 0}, {"text": "lines of specifications, rules, and reports", "size": 11}], fill=LAV2, line=None)
textbox(s, 7.3, 3.1, 5.6, 1.4, [{"text": "Not a property of the small example. When an agent writes the code, the person's effort goes into saying what is wanted, deciding how it will be checked, and reading the evidence: the parts an agent cannot do alone and the parts that make its output something a person can stand behind.", "size": 12}])
callout(s, 7.3, 4.7, 5.6, 2.1, ["Start an agent in v0/ and ask what the system does and how it is known that the code does it", "Watch where it looks. An answer drawn from specs/, the conformance report, and the ledger is one a person could check; an answer drawn from reading filter.py is the agent's opinion of the code"], title="In class: one demonstration", size=12)

s = new_slide("What is not here yet", notes="A1 keeps the system and improves the specifications; A2 adds the second stage and the first specifications of structure.")
bullets(s, 0.85, 1.45, 5.9, 5.4, ["Elicitation: how the purpose statement and the stories are obtained from stakeholders", "A glossary of the domain's terms as a specification of its own", "Requirements rewritten in a structured natural-language form (EARS)", "Fixtures derived from the stories, so a story can be checked by a test as well as walked", "The audit replaces the reading: a procedure on a specification with gaps placed on purpose, by a person, then an agent, then a packaged skill", "The agent as a verifier; the trace matrix as a tool"], size=12.5, after=7, title="Version A1 — the same system, better specifications (next two lectures)", title_size=13.5)
bullets(s, 7.05, 1.45, 5.85, 5.4, [{"text": [("A2: ", {"bold": True}), ("the second stage, sanitize, and the first specifications of structure: an architecture with two stages in a fixed order, the message format, contracts between the stages; a build plan with tasks and waves; analysis and review as methods; the ledger generated by a tool", {})]},
    {"text": [("A3: ", {"bold": True}), ("a change of policy: change requests, staleness in action, impact analysis", {})]},
    {"text": [("A4, A5: ", {"bold": True}), ("sessions with an ordering protocol (a state machine, a sequence chart, a verification plan); a standard message format (a schema and generated code)", {})]}], size=12.5, after=9, title="Later versions", title_size=13.5)

s = new_slide("Applying this to your own project", notes="What carries over directly on day one, and what needs adaptation. One skill underlies the adapted parts: phrasing your own criteria with a named decider, named evidence, and a stated consequence of failure.")
bullets(s, 0.85, 1.45, 5.95, 5.4, [{"text": [("The entities and judgments. ", {"bold": True}), ("Start a ledger on day one, by hand; \"not established\" is information", {})]},
    {"text": [("A concept of operations ", {"bold": True}), ("with the four elements, written with your team and an agent, agreed before code", {})]},
    {"text": [("A requirements document ", {"bold": True}), ("whose clauses carry an identifier, a method, and a derivation", {})]},
    {"text": [("A statement of the technology: ", {"bold": True}), ("language, tools, versions, the gate command", {})]},
    {"text": [("Tests that cite clauses, and the two coverages. ", {"bold": True}), ("Ask whether the suite supports a verification, not only whether it passes", {})]},
    {"text": [("A rules file ", {"bold": True}), ("with the template fields; one gate and the ledger first; add a rule the second time you check something by hand", {})]},
    {"text": [("A sign-off, and provenance ", {"bold": True}), ("on every claim", {})]}], size=12, after=6, title="Carries over directly", title_size=14)
bullets(s, 7.05, 1.45, 5.85, 4.2, [{"text": [("The forms of specification: ", {"bold": True}), ("architecture, data format, state machine, contracts, as your system needs them (specification-kinds.md)", {})]},
    {"text": [("The verification methods: ", {"bold": True}), ("analysis and review, with their tools and evidence", {})]},
    {"text": [("The tooling: ", {"bold": True}), ("the idea of citation-derived coverage carries; the plugin does not", {})]},
    {"text": [("The thresholds, the people, the records: ", {"bold": True}), ("a justified coverage level; real stakeholders found early; a generated ledger when hand-writing stops scaling", {})]}], size=12, after=6, title="Needs adaptation", title_size=14)
keybar(s, "The skill the next lectures build: phrasing your own criteria for specification quality, realization quality, and verification with a named decider, named evidence, and a stated consequence of failure.", y=5.75, x=7.05, w=5.85, h=1.1, size=11.5)

s = new_slide("Exercise 1, and before next meeting", notes="Exercise 1 forces an amendment, a stale VAL row, and a re-sign before the test and the gate.")
callout(s, 0.85, 1.45, 6.3, 4.1, ["Add a requirement: a message whose payload is negative is dropped, whatever its level", "Before writing code, read it with REQ-0 to REQ-3: do the five quality properties still hold? At least one does not; the resolution amends existing clauses", "Record which ledger rows the amendment makes stale, and why", "Carry it through: the clause (identifier, method, derivation), a test that cites it, the gate, the ledger, a dev-log entry; if a story is affected, what must the sign-off now say?", {"text": [("Deliverable: ", {"bold": True}), ("the diff; the ledger after; half a page on which rows went stale, which verifier re-established each, and which needed a person", {})]}], title="Exercise 1", size=12, fill=PALEGOLD)
bullets(s, 7.4, 1.45, 5.5, 2.6, ["Run A0: uv sync; tools/gate.sh; the two sabotages, restoring the file after the first; check one ledger row's evidence against the file it names", "Read the glossary entries for the terms introduced today", "Read specs/conops.md again and ask how its author could have found out what the security officer wanted. The next lecture is about that"], size=12, after=6, title="Before next meeting", title_size=14)
bullets(s, 7.4, 4.2, 5.5, 2.7, ["A reading of \"unchanged\" in REQ-2 under which the test is too weak, and which artifact you would change", "A change to filter.py under which every test passes and every requirement has evidence, yet the gate is red", "For each ledger row: program or person? What would have to be written down before a program could take it over, and is anything lost?"], size=11.5, after=5, title="Questions to think about", title_size=14)

OUT = HERE / "lecture-01-intent-specifications-realizations-and-judgments.pptx"
prs.save(str(OUT))
print("saved", len(prs.slides), "slides to", OUT.name)
