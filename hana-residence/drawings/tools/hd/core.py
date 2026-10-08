"""Drafting core for the Hana Residence 2D working-drawing set.

Every sheet is its own DXF whose modelspace is the A3 sheet in paper millimetres
(420 x 297).  Drawings (plans, elevations) are placed through a View, which maps
model millimetres to paper millimetres at a given scale, so dimension text always
shows real model sizes.  The house layout follows the AC.R3 (Pallet Howse) set:
blue dims, red notes, magenta joinery in plan, tagged materials, title strip at
the bottom.
"""
from __future__ import annotations

import math
import ezdxf
from ezdxf.enums import TextEntityAlignment

A3 = (420.0, 297.0)
MARGIN = 5.0
TB_H = 30.0  # title strip height incl. notice line

# ---------------------------------------------------------------- project info
PROJECT = {
    "type": "DESIGN & BUILD",
    "project": "HANA RESIDENCE, TROPICANA AMAN",
    "client": "MS SHEON & MR TEE",
    "designer": "YANXIANG & YS",
    "sales": "RAYMOND",
    "checked": "RAYMOND",
    "status": [("1ST DRAFT (R0)", "09 OCT' 26"), ("AMENDMENT 01", ""), ("AMENDMENT 02", ""),
               ("AMENDMENT 03", ""), ("AMENDMENT 04", "")],
    "company": "GROO SPACE SDN BHD (1662567-V)",
    "address": ["LEVEL 3A, WISMA JAG, JALAN DESA UTAMA,", "TAMAN DESA, 58100 KUALA LUMPUR"],
    "contact": ["T: +6016-913 6785 / +6012-528 7212", "E: groospacemy@gmail.com  IG: @groospace.my"],
}

# ---------------------------------------------------------------- colours
BLUE, RED, MAGENTA, GREEN, CYAN, GREY, DGREY, BLACK = 5, 1, 6, 3, 4, 8, 250, 7

LAYERS = {
    # name: (aci, lineweight in 1/100 mm, linetype)
    "0-SHEET": (7, 50, "CONTINUOUS"),
    "0-TITLE": (7, 18, "CONTINUOUS"),
    "0-TITLE-TXT": (7, 13, "CONTINUOUS"),
    "A-WALL": (250, 35, "CONTINUOUS"),
    "A-WALL-FILL": (250, 0, "CONTINUOUS"),
    "A-WALL-NEW": (5, 35, "CONTINUOUS"),
    "A-WALL-DEMO": (1, 35, "DASHED"),
    "A-DOOR": (7, 18, "CONTINUOUS"),
    "A-WIND": (7, 13, "CONTINUOUS"),
    "A-STAIR": (7, 13, "CONTINUOUS"),
    "A-DETAIL": (7, 13, "CONTINUOUS"),
    "A-GRID": (8, 13, "DASHED"),
    "A-GRID-TAG": (7, 18, "CONTINUOUS"),
    "A-SITE": (8, 13, "CONTINUOUS"),
    "I-FURN": (7, 13, "CONTINUOUS"),
    "I-JOIN": (6, 25, "CONTINUOUS"),
    "I-JOIN-HIDDEN": (6, 13, "DASHED"),
    "I-JOIN-ELEV": (7, 25, "CONTINUOUS"),
    "I-JOIN-THIN": (7, 13, "CONTINUOUS"),
    "I-JOIN-HATCH": (8, 9, "CONTINUOUS"),
    "I-CEIL": (7, 18, "CONTINUOUS"),
    "I-CEIL-COVE": (1, 18, "DASHED"),
    "I-LITE": (1, 18, "CONTINUOUS"),
    "I-POWR": (1, 18, "CONTINUOUS"),
    "I-FLOR": (8, 9, "CONTINUOUS"),
    "I-CURT": (6, 25, "CONTINUOUS"),
    "I-FINISH": (6, 50, "CONTINUOUS"),
    "I-TAG": (5, 13, "CONTINUOUS"),
    "I-NOTE": (1, 13, "CONTINUOUS"),
    "I-DIM": (5, 13, "CONTINUOUS"),
    "I-TEXT": (7, 13, "CONTINUOUS"),
    "I-ROOM": (7, 13, "CONTINUOUS"),
    "I-SYMB": (6, 18, "CONTINUOUS"),
    "I-WATER": (5, 18, "CONTINUOUS"),
}


def new_doc():
    doc = ezdxf.new("R2018", setup=True)
    doc.units = ezdxf.units.MM
    for name, (col, lw, lt) in LAYERS.items():
        if name not in doc.layers:
            doc.layers.add(name, color=col, lineweight=lw, linetype=lt)
    st = doc.styles.get("Standard")
    st.dxf.font = "arial.ttf"
    if "ARIAL-N" not in doc.styles:
        doc.styles.add("ARIAL-N", font="arialn.ttf")
    doc.header["$LTSCALE"] = 1.0
    doc.header["$PSLTSCALE"] = 0
    doc.header["$LWDISPLAY"] = 1
    return doc


class Sheet:
    """One A3 landscape sheet."""

    def __init__(self, number: str, title: str, subtitle: str = "", drawing_title: str = ""):
        self.number = number            # e.g. "ID.01.03"
        self.title = title              # big label, e.g. "FURNITURE LAYOUT PLAN"
        self.subtitle = subtitle        # e.g. "GROUND FLOOR"
        self.drawing_title = drawing_title or (title + (" - " + subtitle if subtitle else ""))
        self.doc = new_doc()
        self.msp = self.doc.modelspace()
        self._frame()
        self._title_block()

    # --------------------------------------------------------- primitives (paper mm)
    def line(self, a, b, layer="0-TITLE", **kw):
        return self.msp.add_line(a, b, dxfattribs={"layer": layer, **kw})

    def poly(self, pts, layer="0-TITLE", close=False, **kw):
        return self.msp.add_lwpolyline(pts, close=close, dxfattribs={"layer": layer, **kw})

    def rect(self, x0, y0, x1, y1, layer="0-TITLE", **kw):
        return self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], layer, close=True, **kw)

    def text(self, s, p, h=2.0, layer="I-TEXT", align="LEFT", rot=0.0, color=None, style="Standard", width=None):
        at = {"layer": layer, "height": h, "rotation": rot, "style": style}
        if color is not None:
            at["color"] = color
        if width:
            at["width"] = width
        t = self.msp.add_text(str(s), dxfattribs=at)
        t.set_placement(p, align=getattr(TextEntityAlignment, align))
        return t

    def mtext(self, s, p, h=2.0, width=60, layer="I-TEXT", color=None, attach=7):
        at = {"layer": layer, "char_height": h, "width": width, "attachment_point": attach}
        if color is not None:
            at["color"] = color
        m = self.msp.add_mtext(s, dxfattribs=at)
        m.set_location(p)
        return m

    def circle(self, c, r, layer="I-TEXT", **kw):
        return self.msp.add_circle(c, r, dxfattribs={"layer": layer, **kw})

    def solid(self, pts, layer="A-WALL-FILL", color=None, rgb=None):
        h = self.msp.add_hatch(dxfattribs={"layer": layer, **({"color": color} if color is not None else {})})
        if rgb:
            h.set_solid_fill(rgb=rgb)
        elif color is not None:
            h.set_solid_fill(color=color)
        h.paths.add_polyline_path(pts, is_closed=True)
        return h

    def pattern(self, pts, name="ANSI31", scale=1.0, angle=0.0, layer="I-JOIN-HATCH", color=None):
        h = self.msp.add_hatch(dxfattribs={"layer": layer, **({"color": color} if color is not None else {})})
        h.set_pattern_fill(name, scale=scale, angle=angle)
        h.paths.add_polyline_path(pts, is_closed=True)
        return h

    # --------------------------------------------------------- frame & title block
    def _frame(self):
        W, H = A3
        self.rect(MARGIN, MARGIN, W - MARGIN, H - MARGIN, "0-SHEET")

    def _title_block(self):
        W, _ = A3
        x0, x1 = MARGIN, W - MARGIN
        y0 = MARGIN
        yn = y0 + 7.0           # notice line top
        yt = yn + 19.5          # title strip top
        L, T = "0-TITLE", "0-TITLE-TXT"
        self.line((x0, yt), (x1, yt), L)
        self.line((x0, yn), (x1, yn), L)
        P = PROJECT
        # column boundaries (proportions from AC.R3)
        c1, c2, c3, c4, c5 = x0 + 92, x0 + 214, x0 + 282, x0 + 340, x1
        for c in (c1, c2, c3, c4):
            self.line((c, yn), (c, yt), L)
        rh = (yt - yn) / 3
        for i in (1, 2):
            self.line((x0, yn + i * rh), (c2, yn + i * rh), L)
        # left block
        rows = [("PROJECT TYPE :", P["type"]), ("PROJECT :", P["project"]), ("CLIENT :", P["client"])]
        for i, (k, v) in enumerate(rows):
            yy = yt - (i + 0.5) * rh
            self.text(k, (x0 + 1.5, yy), 1.9, T, "MIDDLE_LEFT", style="Standard")
            self.text(v, (c1 - 1.5, yy), 1.9, T, "MIDDLE_RIGHT")
        # middle block
        mid = c1 + 61
        self.line((mid, yn + rh), (mid, yn + 2 * rh), L)
        self.text("DRAWING TITLE :", (c1 + 1.5, yt - 0.5 * rh), 1.9, T, "MIDDLE_LEFT")
        self.text(self.drawing_title.upper(), (c2 - 1.5, yt - 0.5 * rh), 1.9, T, "MIDDLE_RIGHT")
        self.text("INTERIOR DESIGNER :", (c1 + 1.5, yt - 1.5 * rh), 1.9, T, "MIDDLE_LEFT")
        self.text(P["designer"], (mid - 1.5, yt - 1.5 * rh), 1.9, T, "MIDDLE_RIGHT")
        self.text("SALE PERSON :", (mid + 1.5, yt - 1.5 * rh), 1.9, T, "MIDDLE_LEFT")
        self.text(P["sales"], (c2 - 1.5, yt - 1.5 * rh), 1.9, T, "MIDDLE_RIGHT")
        self.text("CHECK BY :", (c1 + 1.5, yt - 2.5 * rh), 1.9, T, "MIDDLE_LEFT")
        self.text(P["checked"], (mid - 1.5, yt - 2.5 * rh), 1.9, T, "MIDDLE_RIGHT")
        self.text(self.number, (c2 - 1.5, yt - 2.5 * rh), 1.9, T, "MIDDLE_RIGHT")
        # drawing status table
        self.text("DRAWING'S STATUS :", (c2 + 1.2, yt - 1.6), 1.8, T, "MIDDLE_LEFT")
        sh = (yt - 3.2 - yn) / 5
        self.line((c2, yt - 3.2), (c3, yt - 3.2), L)
        midc = c2 + 36
        self.line((midc, yn), (midc, yt - 3.2), L)
        for i, (k, v) in enumerate(P["status"]):
            yy = yt - 3.2 - (i + 0.5) * sh
            self.text(k, (c2 + 1.2, yy), 1.45, T, "MIDDLE_LEFT")
            self.text(v, (midc + 1.2, yy), 1.45, T, "MIDDLE_LEFT")
            if i:
                self.line((c2, yt - 3.2 - i * sh), (c3, yt - 3.2 - i * sh), L)
        # copyright + logo
        self.text("ALL DRAWINGS ARE COPY-RIGHT OF:", (c3 + 1.2, yt - 1.6), 1.4, T, "MIDDLE_LEFT")
        self.text("groo", (c3 + 2.0, yn + 6.0), 5.6, T, "LEFT")
        self.text("space", (c3 + 6.0, yn + 2.6), 1.8, T, "LEFT")
        tx = c3 + 22.5
        lines = [P["company"]] + P["address"] + P["contact"]
        for i, s in enumerate(lines):
            self.text(s, (tx, yt - 4.6 - i * 2.6), 1.12, T, "MIDDLE_LEFT")
        self.text("CLIENTS ACKNOWLEDGE & SIGN :", (c4 + 1.2, yt - 1.6), 1.8, T, "MIDDLE_LEFT")
        notice = ('"NOTICE TO CONTRACTOR: DO NOT SCALE DRAWINGS. All dimensions and site levels must be Verified In Field '
                  '(V.I.F.) before any fabrication or commencement of work.')
        notice2 = ('Any discrepancies between these drawings and actual site conditions must be reported to the Designer '
                   'immediately for clarification. Failure to do so will be at the Contractor\'s own risk."')
        self.text(notice, (x0 + 1.5, yn - 2.3), 1.55, T, "MIDDLE_LEFT")
        self.text(notice2, (x0 + 1.5, yn - 4.9), 1.55, T, "MIDDLE_LEFT")
        self.draw_top = yt  # drawable area is above this line

    # --------------------------------------------------------- labels
    def view_label(self, p, code, name, scale_txt, code_top="ID", w=70):
        """Circle tag + underlined view name, e.g.  (ID/01) LIGHTING PLAN  SCALE 1:100."""
        x, y = p
        r = 4.2
        self.circle((x + r, y), r, "I-TEXT")
        self.line((x, y), (x + 2 * r, y), "I-TEXT")
        self.text(code_top, (x + r, y + 1.9), 1.9, "I-TEXT", "MIDDLE_CENTER")
        self.text(code, (x + r, y - 1.9), 1.9, "I-TEXT", "MIDDLE_CENTER")
        self.text(name, (x + 2 * r + 1.5, y + 0.8), 3.4, "I-TEXT", "LEFT")
        self.line((x + 2 * r, y), (x + 2 * r + w, y), "I-TEXT")
        self.text(scale_txt, (x + 2 * r + 1.5, y - 3.2), 2.0, "I-TEXT", "LEFT")

    def elev_label(self, p, name, scale_txt, w=45):
        """Empty circle + name + scale, as used under each elevation in AC.R3."""
        x, y = p
        self.circle((x + 4.5, y), 4.5, "I-TEXT")
        self.text(name, (x + 11, y + 0.9), 2.8, "I-TEXT", "LEFT")
        self.line((x + 9, y), (x + 9 + w, y), "I-TEXT")
        self.text(scale_txt, (x + 11, y - 3.2), 2.4, "I-TEXT", "LEFT")

    def sheet_tag(self, title, sub, code="ID", num="01"):
        """Bottom-right sheet tag, e.g. 'ENTRANCE - SHOE CABINET / ELEVATION PLAN (ID 02)'."""
        x1 = A3[0] - MARGIN - 4
        y = self.draw_top + 7
        self.circle((x1 - 4.5, y), 4.5, "I-TEXT")
        self.line((x1 - 9, y), (x1, y), "I-TEXT")
        self.text(code, (x1 - 4.5, y + 2.0), 1.9, "I-TEXT", "MIDDLE_CENTER")
        self.text(num, (x1 - 4.5, y - 2.0), 1.9, "I-TEXT", "MIDDLE_CENTER")
        self.text(title, (x1 - 10, y + 1.0), 3.4, "I-TEXT", "BOTTOM_RIGHT")
        self.line((x1 - 10 - len(title) * 2.75, y), (x1 - 9, y), "I-TEXT")
        self.text(sub, (x1 - 10, y - 1.2), 2.2, "I-TEXT", "TOP_RIGHT")

    def save(self, path):
        self.doc.saveas(path)


class View:
    """Model (mm) -> paper (mm) mapping for one drawing on a sheet."""

    def __init__(self, sheet: Sheet, origin_paper, scale: float, origin_model=(0.0, 0.0)):
        self.s = sheet
        self.ox, self.oy = origin_paper
        self.mx, self.my = origin_model
        self.k = 1.0 / scale            # paper mm per model mm
        self.scale = scale

    def P(self, x, y=None):
        if y is None:
            x, y = x
        return (self.ox + (x - self.mx) * self.k, self.oy + (y - self.my) * self.k)

    def Ps(self, pts):
        return [self.P(p) for p in pts]

    # geometry in model mm
    def line(self, a, b, layer="I-JOIN-ELEV", **kw):
        return self.s.line(self.P(a), self.P(b), layer, **kw)

    def poly(self, pts, layer="I-JOIN-ELEV", close=False, **kw):
        return self.s.poly(self.Ps(pts), layer, close, **kw)

    def rect(self, x0, y0, x1, y1, layer="I-JOIN-ELEV", **kw):
        return self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], layer, True, **kw)

    def circle(self, c, r, layer="I-FURN", **kw):
        return self.s.circle(self.P(c), r * self.k, layer, **kw)

    def arc(self, c, r, a0, a1, layer="A-DOOR", **kw):
        return self.s.msp.add_arc(self.P(c), r * self.k, a0, a1, dxfattribs={"layer": layer, **kw})

    def solid(self, pts, layer="A-WALL-FILL", color=None, rgb=None):
        return self.s.solid(self.Ps(pts), layer, color, rgb)

    def pattern(self, pts, name="ANSI31", scale=1.0, angle=0.0, layer="I-JOIN-HATCH", color=None):
        return self.s.pattern(self.Ps(pts), name, scale, angle, layer, color)

    def text(self, s, p, h=2.0, layer="I-TEXT", align="MIDDLE_CENTER", rot=0.0, color=None):
        return self.s.text(s, self.P(p), h, layer, align, rot, color)

    def mtext(self, s, p, h=2.0, width=40, layer="I-TEXT", color=None, attach=5):
        return self.s.mtext(s, self.P(p), h, width, layer, color, attach)

    # ------------------------------------------------ dimensions (AC.R3 style, blue, ticks)
    def dim(self, a, b, off, h=2.0, txt=None, layer="I-DIM", ext=True, color=None):
        """Aligned dimension between model points a,b, offset `off` (model mm, + = left of a->b)."""
        ax, ay = a; bx, by = b
        L = math.hypot(bx - ax, by - ay)
        if L < 1:
            return
        ux, uy = (bx - ax) / L, (by - ay) / L
        nx, ny = -uy, ux
        da = (ax + nx * off, ay + ny * off)
        db = (bx + nx * off, by + ny * off)
        at = {"color": color} if color is not None else {}
        if ext:
            g = 1.2 / self.k  # gap 1.2 paper mm
            e = 1.5 / self.k  # extension past dim line
            sgn = 1 if off >= 0 else -1
            for p, q in ((a, da), (b, db)):
                self.line((p[0] + nx * g * sgn, p[1] + ny * g * sgn),
                          (q[0] + nx * e * sgn, q[1] + ny * e * sgn), layer, **at)
        ex = 1.5 / self.k
        self.line((da[0] - ux * ex, da[1] - uy * ex), (db[0] + ux * ex, db[1] + uy * ex), layer, **at)
        t = 1.1 / self.k
        for p in (da, db):  # architectural tick at 45 deg
            self.line((p[0] - (ux + nx) * t, p[1] - (uy + ny) * t), (p[0] + (ux + nx) * t, p[1] + (uy + ny) * t), layer, **at)
        ang = math.degrees(math.atan2(uy, ux))
        if ang > 90.5 or ang <= -89.5:
            ang += 180
        mid = ((da[0] + db[0]) / 2, (da[1] + db[1]) / 2)
        sgn = 1 if ang == math.degrees(math.atan2(uy, ux)) else -1
        tp = (mid[0] + nx * (0.9 / self.k) * sgn * (1 if off >= 0 else 1), mid[1] + ny * (0.9 / self.k) * sgn)
        self.s.text(txt if txt is not None else f"{round(L):d}", self.P(tp), h, layer, "BOTTOM_CENTER", ang, color)

    def dim_chain(self, pts, off, h=2.0, horizontal=True, layer="I-DIM"):
        """Chain of dims along X (horizontal=True) or Y through sorted coordinates.
        pts: list of coordinates; off: fixed other coordinate of the dim line."""
        for a, b in zip(pts, pts[1:]):
            if horizontal:
                self.dim((a, off), (b, off), 0, h, layer=layer, ext=False)
            else:
                self.dim((off, a), (off, b), 0, h, layer=layer, ext=False)

    # ------------------------------------------------ annotation symbols
    def leader(self, tip, text_pt, lines, h=2.0, color=RED, align="LEFT", layer="I-NOTE", dot=True):
        self.line(tip, text_pt, layer, color=color)
        if dot:
            self.s.msp.add_circle(self.P(tip), 0.45, dxfattribs={"layer": layer, "color": color})
        x, y = self.P(text_pt)
        step = h * 1.45
        al = "MIDDLE_LEFT" if align == "LEFT" else "MIDDLE_RIGHT"
        dx = 0.8 if align == "LEFT" else -0.8
        y0 = y + (len(lines) - 1) * step / 2
        for i, ln in enumerate(lines):
            col = color
            if isinstance(ln, tuple):
                ln, col = ln
            self.s.text(ln, (x + dx, y0 - i * step), h, layer, al, color=col)

    def mat_tag(self, p, code, h=1.6):
        """Oval material tag like (M01)."""
        x, y = self.P(p)
        w, hh = h * 2.6, h * 1.25
        # stadium shape
        pts = []
        for i in range(0, 181, 15):
            a = math.radians(90 + i)
            pts.append((x - w / 2 + hh * math.cos(a), y + hh * math.sin(a)))
        for i in range(0, 181, 15):
            a = math.radians(270 + i)
            pts.append((x + w / 2 + hh * math.cos(a), y + hh * math.sin(a)))
        self.s.poly(pts, "I-TAG", close=True)
        self.s.text(code, (x, y), h * 0.85, "I-TAG", "MIDDLE_CENTER")

    def level(self, p, label, h=1.6, right=True):
        """Level marker 'CL 2638 ▽' / 'FFL 000 ▽'."""
        x, y = self.P(p)
        t = 1.2
        self.s.poly([(x, y), (x - t, y + t * 1.4), (x + t, y + t * 1.4)], "I-NOTE", close=True, color=RED)
        self.s.text(label, (x - t - 0.8, y + 0.2), h, "I-TEXT", "BOTTOM_RIGHT")

    def elev_marker(self, p, letter, direction="S", r=2.6, color=MAGENTA):
        """Triangle elevation marker with letter (A/B/C) pointing to `direction` (N,S,E,W)."""
        x, y = self.P(p)
        ang = {"N": 90, "S": 270, "E": 0, "W": 180}[direction]
        a = math.radians(ang)
        self.s.msp.add_circle((x, y), r, dxfattribs={"layer": "I-SYMB", "color": color})
        tip = (x + math.cos(a) * r * 1.9, y + math.sin(a) * r * 1.9)
        l = (x + math.cos(a + 1.2) * r, y + math.sin(a + 1.2) * r)
        rr = (x + math.cos(a - 1.2) * r, y + math.sin(a - 1.2) * r)
        h = self.s.msp.add_hatch(dxfattribs={"layer": "I-SYMB", "color": color})
        h.set_solid_fill(color=color)
        h.paths.add_polyline_path([tip, l, rr], is_closed=True)
        self.s.text(letter, (x, y), r * 1.05, "I-SYMB", "MIDDLE_CENTER", color=color)

    def section_marker(self, a, b, letter="X", color=MAGENTA):
        """Section cut line with circled letters at both ends."""
        self.line(a, b, "I-SYMB", color=color)
        for p in (a, b):
            x, y = self.P(p)
            self.s.msp.add_circle((x, y), 2.2, dxfattribs={"layer": "I-SYMB", "color": color})
            self.s.text(letter, (x, y), 2.2, "I-SYMB", "MIDDLE_CENTER", color=color)

    def detail_bubble(self, c, r_model, label):
        """Red circle on drawing marking a detail, with 'DETAIL n' text."""
        self.circle(c, r_model, "I-NOTE", color=RED)
        x, y = self.P(c)
        self.s.text(label, (x + r_model * self.k * 0.75, y - r_model * self.k - 0.8), 2.0, "I-NOTE", "TOP_LEFT", color=RED)


def grid_bubble(sheet: Sheet, p, label, r=3.6):
    sheet.circle(p, r, "A-GRID-TAG")
    sheet.text(label, p, r * 1.15, "A-GRID-TAG", "MIDDLE_CENTER")
