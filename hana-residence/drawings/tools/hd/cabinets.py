"""Joinery elevation sheets (CF series), modelled on AC.R3 'ELEVATION PLAN' sheets.

A cabinet is a run of columns; each column is a stack of parts (bottom -> top).
The generator draws: plan key, ELEVATION A, INNER CARCASS A, SECTION X-X,
1:5 details and a material legend, with blue dims, red notes and material tags.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional

from .core import Sheet, View, RED, BLUE, MAGENTA, GREEN, A3, MARGIN
from . import data as D

MAT = {m[0]: m for m in D.MATERIALS}


@dataclass
class Part:
    h: float
    kind: str = "door"      # door, pair, drawer, open, glass, appliance, niche, flap, panel, hang, gap, counter, void, liftup
    mat: str = "M01"
    label: str = ""
    shelves: int = 0        # adjustable shelves inside (door/open/glass)
    led: bool = False       # LED strip under shelf / in niche
    hinge: str = "L"        # L/R for single doors
    n: int = 1              # number of doors / drawers side by side (kind doors / drawers)


@dataclass
class Col:
    w: float
    parts: List[Part]


@dataclass
class Cabinet:
    code: str
    title: str              # e.g. "SHOE CABINET"
    room: str               # e.g. "ENTRANCE"
    depth: float
    cl: float               # ceiling level above FFL
    cols: List[Col]
    plinth: float = 100
    plinth_kind: str = "recess"   # recess | float (LED) | none
    top_gap: float = 20           # infill recess to ceiling
    worktop: Optional[tuple] = None   # (height_top, thickness, mat)
    wall_left: bool = True
    wall_right: bool = True
    notes: List[str] = field(default_factory=list)
    details: List[str] = field(default_factory=lambda: ["infill", "finger"])
    sheet_no: str = ""
    elev_title: str = ""
    free: bool = False            # freestanding (island): no walls / ceiling

    @property
    def W(self):
        return sum(c.w for c in self.cols)

    @property
    def top(self):
        return self.cl - self.top_gap if self.top_gap is not None else self.cl


WALL_T = 150  # wall thickness drawn in elevation / section
HATCH = "ANSI31"


def col_height(c: Col, cab: Cabinet):
    return cab.plinth + sum(p.h for p in c.parts)


# ======================================================================= drawing primitives
def wall_strip(v: View, x0, y0, x1, y1):
    v.rect(x0, y0, x1, y1, "A-WALL")
    v.pattern([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], HATCH, 1.6 * v.scale / 30, 0, "I-JOIN-HATCH")


def door_swing(v: View, x0, y0, x1, y1, hinge="L"):
    """AC.R3 draws the opening indication as a dashed 'V' from the hinge side."""
    if hinge == "L":
        v.poly([(x1, y0), (x0, (y0 + y1) / 2), (x1, y1)], "I-JOIN-HIDDEN")
    else:
        v.poly([(x0, y0), (x1, (y0 + y1) / 2), (x0, y1)], "I-JOIN-HIDDEN")


def finger_pull(v: View, x, y0, y1):
    """45 deg finger-pull groove shown as a thin double line on the door edge."""
    v.line((x, y0), (x, y1), "I-JOIN-THIN")


# ======================================================================= views
def draw_front(v: View, cab: Cabinet, inner=False):
    W, top = cab.W, cab.top
    yb = 0
    # walls / ceiling / floor
    if cab.free:
        v.line((-300, 0), (W + 300, 0), "A-WALL")
        v.level((W + 700, 0), "FFL 000")
    if cab.free:
        pass
    elif cab.wall_left:
        wall_strip(v, -WALL_T, -60, 0, cab.cl + 120)
    if cab.wall_right and not cab.free:
        wall_strip(v, W, -60, W + WALL_T, cab.cl + 120)
    if not cab.free:
        v.line((-WALL_T - 300, 0), (W + WALL_T + 300, 0), "A-WALL")
        v.line((-WALL_T - 300, cab.cl), (W + WALL_T + 300, cab.cl), "I-CEIL")
        v.level((W + WALL_T + 700, cab.cl), f"CL {int(cab.cl)}")
        v.level((W + WALL_T + 700, 0), "FFL 000")
    # plinth
    if cab.plinth > 0:
        if cab.plinth_kind == "float":
            v.line((0, cab.plinth), (W, cab.plinth), "I-JOIN-ELEV")
            v.line((40, 15), (W - 40, 15), "I-LITE", color=RED)
        else:
            v.rect(0, 0, W, cab.plinth, "I-JOIN-THIN")
    # top infill
    if cab.top_gap and cab.top_gap > 0 and cab.top < cab.cl and not cab.free:
        v.rect(0, cab.top, W, cab.cl, "I-JOIN-THIN")
    x = 0
    for c in cab.cols:
        y = cab.plinth
        for p in c.parts:
            draw_part(v, cab, x, y, c.w, p, inner)
            y += p.h
        x += c.w
    v.rect(0, cab.plinth, W, max(col_height(c, cab) for c in cab.cols), "I-JOIN-ELEV")
    if cab.worktop:
        hgt, t, m = cab.worktop
        v.rect(-10, hgt - t, W + 10, hgt, "I-JOIN-ELEV")


def draw_part(v: View, cab, x, y, w, p: Part, inner):
    x0, y0, x1, y1 = x, y, x + w, y + p.h
    L = "I-JOIN-ELEV"
    if p.kind == "gap":
        # backsplash / wall between base and wall cabinets
        v.pattern([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], "BRICK", 0.6 * v.scale / 30, 0, "I-JOIN-HATCH", color=8)
        if not inner and p.label:
            v.text(p.label, ((x0 + x1) / 2, (y0 + y1) / 2), 1.6, "I-TEXT")
        return
    if p.kind == "counter":
        v.rect(x0 - 10, y0, x1 + 10, y1, L)
        return
    v.rect(x0, y0, x1, y1, L)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if inner:
        if p.kind in ("doors", "drawers"):
            for k in range(1, p.n):
                v.line((x0 + w * k / p.n, y0), (x0 + w * k / p.n, y1), "I-JOIN-THIN")
        if p.kind == "drawers":
            v.text("DRAWER", (cx, cy), 1.4, "I-TEXT")
        if p.kind in ("door", "pair", "doors", "glass", "open", "niche", "liftup", "flap"):
            n = p.shelves
            for k in range(1, n + 1):
                yy = y0 + p.h * k / (n + 1)
                v.line((x0 + 16, yy), (x1 - 16, yy), "I-JOIN-THIN")
                v.text("ADJ", (x0 + 30, yy + 40), 1.5, "I-TEXT", "LEFT")
            v.line((x0 + 16, y0), (x0 + 16, y1), "I-JOIN-THIN")
            v.line((x1 - 16, y0), (x1 - 16, y1), "I-JOIN-THIN")
        if p.kind == "hang":
            v.line((x0 + 30, y1 - 120), (x1 - 30, y1 - 120), "I-JOIN-ELEV")
            v.text("HANGING ROD", (cx, y1 - 220), 1.4, "I-TEXT")
        if p.kind == "drawer":
            v.rect(x0 + 30, y0 + 30, x1 - 30, y1 - 30, "I-JOIN-THIN")
            v.text("DRAWER", (cx, cy), 1.5, "I-TEXT")
        if p.kind == "appliance":
            v.text(p.label or "APPLIANCE", (cx, cy), 1.5, "I-TEXT")
        return
    # ---------------- front (elevation) view
    if p.kind == "door":
        door_swing(v, x0, y0, x1, y1, p.hinge)
    elif p.kind == "pair":
        v.line((cx, y0), (cx, y1), L)
        door_swing(v, x0, y0, cx, y1, "L")
        door_swing(v, cx, y0, x1, y1, "R")
    elif p.kind == "doors":
        dw = w / p.n
        for k in range(p.n):
            a = x0 + k * dw
            if k:
                v.line((a, y0), (a, y1), L)
            door_swing(v, a, y0, a + dw, y1, "L" if k % 2 == 0 else "R")
    elif p.kind == "drawers":
        dw = w / p.n
        for k in range(p.n):
            a = x0 + k * dw
            if k:
                v.line((a, y0), (a, y1), L)
            v.line((a + 0.3 * dw, y1 - 35), (a + 0.7 * dw, y1 - 35), "I-JOIN-THIN")
        if p.h >= 180:
            v.text("DRAWER", (cx, cy), 1.4, "I-TEXT")
    elif p.kind == "liftup":
        v.poly([(x0, y0), (cx, y1), (x1, y0)], "I-JOIN-HIDDEN")
    elif p.kind == "flap":
        v.poly([(x0, y1), (cx, y0), (x1, y1)], "I-JOIN-HIDDEN")
    elif p.kind == "drawer":
        v.line((x0 + 0.25 * w, y1 - 40), (x1 - 0.25 * w, y1 - 40), "I-JOIN-THIN")
        v.text("DRAWER", (cx, cy), 1.5, "I-TEXT")
    elif p.kind == "glass":
        v.rect(x0 + 25, y0 + 25, x1 - 25, y1 - 25, L)
        for k in (0.25, 0.55):
            v.line((x0 + w * k, y0 + 60), (x0 + w * (k + 0.2), y0 + p.h * 0.45), "I-JOIN-THIN")
        door_swing(v, x0, y0, x1, y1, p.hinge)
    elif p.kind in ("open", "niche"):
        v.rect(x0 + 16, y0 + 16, x1 - 16, y1 - 16, "I-JOIN-THIN")
        for k in range(1, p.shelves + 1):
            yy = y0 + p.h * k / (p.shelves + 1)
            v.line((x0 + 16, yy), (x1 - 16, yy), L)
            if p.led:
                v.line((x0 + 40, yy - 15), (x1 - 40, yy - 15), "I-LITE", color=RED)
        if p.led and p.shelves == 0:
            v.line((x0 + 40, y1 - 40), (x1 - 40, y1 - 40), "I-LITE", color=RED)
        if p.kind == "niche":
            v.pattern([(x0 + 16, y0 + 16), (x1 - 16, y0 + 16), (x1 - 16, y1 - 16), (x0 + 16, y1 - 16)], "ANSI32",
                      0.9 * v.scale / 30, 90, "I-JOIN-HATCH", color=8)
    elif p.kind == "appliance":
        v.rect(x0 + 20, y0 + 20, x1 - 20, y1 - 20, "I-JOIN-THIN")
        v.text(p.label or "APPLIANCE", (cx, cy), 1.5, "I-TEXT")
        v.text("(BY OWNER)", (cx, cy - 120 * v.scale / 30), 1.2, "I-TEXT")
    elif p.kind == "hang":
        v.line((x0 + 30, y1 - 120), (x1 - 30, y1 - 120), L)
        v.text("OPEN HANGING", (cx, cy), 1.4, "I-TEXT")
    elif p.kind == "void":
        if p.label:
            v.text(p.label, (cx, cy), 2.0, "I-TEXT")
        v.line((x0, y0), (x1, y1), "I-JOIN-HIDDEN"); v.line((x0, y1), (x1, y0), "I-JOIN-HIDDEN")
    elif p.kind == "panel":
        pass
    if p.label and p.kind not in ("appliance", "void", "drawer"):
        v.text(p.label, (cx, y0 + 90), 1.3, "I-TEXT")


def draw_plan_key(v: View, cab: Cabinet):
    W, Dp = cab.W, cab.depth
    # wall behind (y = Dp .. Dp+150) and side walls
    if not cab.free:
        wall_strip(v, -WALL_T if cab.wall_left else 0, Dp, W + (WALL_T if cab.wall_right else 0), Dp + WALL_T)
        if cab.wall_left:
            wall_strip(v, -WALL_T, -150, 0, Dp)
        if cab.wall_right:
            wall_strip(v, W, -150, W + WALL_T, Dp)
    v.rect(0, 0, W, Dp, "I-JOIN")
    x = 0
    for c in cab.cols:
        v.line((x, 0), (x, Dp), "I-JOIN")
        x += c.w
    v.line((0, 18), (W, 18), "I-JOIN")
    # elevation & section markers
    v.elev_marker((W / 2, -420), "A", "N", r=2.6)
    sx, acc = cab.cols[0].w / 2, 0
    for c in cab.cols:
        if any(p.kind == "counter" for p in c.parts):
            sx = acc + c.w / 2
            break
        acc += c.w
    v.section_marker((sx, -250), (sx, Dp + 300), "X")
    v.dim((0, Dp + WALL_T), (W, Dp + WALL_T), 220, 1.8)
    xs = [0]
    for c in cab.cols:
        xs.append(xs[-1] + c.w)
    for a, b in zip(xs, xs[1:]):
        v.dim((a, 0), (b, 0), -170, 1.6)
    v.dim((W, 0), (W, Dp), -260 if not cab.wall_right else -360, 1.6)


def draw_section(v: View, cab: Cabinet, col: Col):
    """Side section X-X: wall at right (x = depth), front at x=0 (left)."""
    Dp = cab.depth
    v.line((-300, 0), (Dp + WALL_T + 150, 0), "A-WALL")
    v.level((Dp + WALL_T + 650, 0), "FFL 000")
    if not cab.free:
        wall_strip(v, Dp, -60, Dp + WALL_T, cab.cl + 120)
        v.line((-300, cab.cl), (Dp + WALL_T + 150, cab.cl), "I-CEIL")
        v.level((Dp + WALL_T + 650, cab.cl), f"CL {int(cab.cl)}")
    y = cab.plinth
    if cab.plinth > 0:
        v.rect(60 if cab.plinth_kind == "recess" else 120, 0, Dp - 18, cab.plinth, "I-JOIN-THIN")
        if cab.plinth_kind == "float":
            v.line((140, 15), (Dp - 60, 15), "I-LITE", color=RED)
    for p in col.parts:
        y0, y1 = y, y + p.h
        if p.kind == "gap":
            y = y1
            continue
        if p.kind == "counter":
            v.rect(-10, y0, Dp, y1, "I-JOIN-ELEV")
            y = y1
            continue
        d0 = 18 if p.kind not in ("open", "niche", "hang") else 0
        dp = Dp if p.kind not in ("liftup",) else min(Dp, 350)
        x0 = Dp - dp
        v.rect(x0 + d0, y0, Dp - 18, y1, "I-JOIN-ELEV")          # carcass
        v.rect(Dp - 18, y0, Dp, y1, "I-JOIN-THIN")               # back panel
        if d0:
            v.rect(x0, y0, x0 + 18, y1, "I-JOIN-ELEV")            # door
        for k in range(1, p.shelves + 1):
            yy = y0 + p.h * k / (p.shelves + 1)
            v.rect(x0 + d0 + 20, yy - 9, Dp - 18, yy + 9, "I-JOIN-THIN")
            if p.led:
                v.line((x0 + d0 + 40, yy - 20), (x0 + d0 + 120, yy - 20), "I-LITE", color=RED)
        if p.kind == "hang":
            v.circle((Dp / 2, y1 - 120), 15, "I-JOIN-ELEV")
        if p.kind == "drawer":
            v.rect(x0 + 18, y0 + 40, Dp - 60, y1 - 40, "I-JOIN-THIN")
        y = y1
    if cab.worktop:
        hgt, t, m = cab.worktop
        v.rect(-20, hgt - t, Dp, hgt, "I-JOIN-ELEV")
    if cab.top_gap and cab.top < cab.cl and not cab.free:
        v.rect(0, cab.top, Dp, cab.cl, "I-JOIN-THIN")
    v.dim((0, -60), (Dp, -60), -150, 1.8)


# ======================================================================= details (1:5, inside a circle)
def detail_circle(s: Sheet, c, r, num, title_lines):
    s.circle(c, r, "I-NOTE", color=RED)
    x, y = c
    s.circle((x - r + 3.2, y - r - 3.5), 3.2, "I-NOTE", color=RED)
    s.text(f"DETAIL {num}", (x - r + 8, y - r - 2.6), 2.6, "I-NOTE", "LEFT", color=RED)
    s.line((x - r + 6.4, y - r - 3.5), (x - r + 32, y - r - 3.5), "I-NOTE", color=RED)
    s.text("1:5", (x - r + 8, y - r - 6.6), 2.2, "I-NOTE", "LEFT", color=RED)
    for i, t in enumerate(title_lines):
        s.text(t, (x, y + r + 2.2 + (len(title_lines) - 1 - i) * 3.2), 2.3, "I-NOTE", "BOTTOM_CENTER", color=RED)


def detail_geom(s: Sheet, kind, c, r):
    """Draw the detail inside the circle at 1:5 (1 paper mm = 5 model mm)."""
    v = View(s, c, 5)
    L = "I-JOIN-ELEV"
    if kind == "infill":
        # ceiling slab, cabinet top, 20mm infill recess
        v.rect(-90, 40, 90, 70, "A-WALL"); v.pattern([(-90, 40), (90, 40), (90, 70), (-90, 70)], HATCH, 0.25, 0, "I-JOIN-HATCH")
        v.rect(-80, -90, 60, 20, L); v.rect(60, -90, 78, 20, L)          # carcass side + door
        v.rect(-80, 20, 78, 40, "I-JOIN-THIN")
        v.dim((78, 20), (78, 40), -18, 1.6, txt="20")
        v.leader((10, 30), (60, 95), ["INFILL RECESS 20MM"], 1.8, RED)
    elif kind == "finger":
        # plan of two doors meeting with 45 deg finger pull
        v.rect(-90, -10, -4, 8, L); v.rect(4, -10, 90, 8, L)
        v.poly([(-4, 8), (-4, -2), (-14, 8)], L, close=True)
        v.poly([(4, 8), (4, -2), (14, 8)], L, close=True)
        v.rect(-90, 8, 90, 70, "I-JOIN-THIN")
        v.text("45°", (0, -30), 2.2, "I-NOTE", color=RED)
        v.leader((-9, 5), (-60, -70), ["45° FINGER PULL", "DOOR PANEL"], 1.8, RED, "LEFT")
    elif kind == "led":
        v.rect(-90, -9, 90, 9, L)
        v.rect(-80, -20, -60, -9, "I-LITE", color=RED)
        v.circle((-70, -15), 3, "I-LITE", color=RED)
        v.leader((-70, -15), (-20, -70), ["LED STRIP LIGHT 3000K", "C/W ALU PROFILE"], 1.8, RED, "LEFT")
    elif kind == "plinth":
        v.rect(-90, -80, 90, -60, "A-WALL")
        v.rect(-30, -60, 70, 20, L)      # plinth recess
        v.rect(-60, 20, 90, 38, L)       # cabinet bottom
        v.line((-50, -55), (-35, -55), "I-LITE", color=RED)
        v.leader((-40, -50), (-80, 70), ["PLINTH RECESS 30MM", "C/W LED STRIP (FLOAT)"], 1.8, RED, "LEFT")
    elif kind == "handle":
        v.rect(-90, -10, 90, 8, L)
        v.poly([(-30, 8), (-30, 30), (30, 30), (30, 8)], L)
        v.leader((0, 30), (40, 75), ["J&C HANDLE", "BLACK (TBC)"], 1.8, RED, "LEFT")
    elif kind == "stone":
        v.rect(-90, 0, 70, 12, L)
        v.poly([(70, 0), (82, 12), (82, -40), (70, -52), (70, 0)], L)
        v.rect(-90, -60, 60, 0, "I-JOIN-THIN")
        v.text("45°", (90, 5), 2.0, "I-NOTE", "LEFT", color=RED)
        v.leader((76, -10), (10, -85), ["SINTERED STONE 45° CORNER", "MITRE (NO CAPPING)"], 1.7, RED, "LEFT")
    elif kind == "glass":
        v.rect(-90, -8, 90, 8, L)
        v.rect(-60, -3, 60, 3, "I-JOIN-THIN")
        v.leader((0, 3), (30, 70), ["20MM ALU FRAME BLACK", "C/W FLUTED GLASS"], 1.8, RED, "LEFT")
    elif kind == "hidden":
        v.rect(-90, -10, 90, 8, L)
        v.rect(-90, 8, -60, 80, "A-WALL")
        v.circle((-60, 0), 5, L)
        v.leader((-60, 0), (10, -70), ["CONCEALED HINGE", "FLUSH HIDDEN DOOR"], 1.8, RED, "LEFT")


DETAIL_TITLES = {
    "infill": ["INFILL RECESS 20MM"], "finger": ["45° FINGER PULL", "DOOR PANEL"], "led": ["LED STRIP LIGHT 3000K"],
    "plinth": ["PLINTH RECESS", "C/W LED"], "handle": ["J&C HANDLE BLACK"], "stone": ["SINTERED STONE", "45° CORNER"],
    "glass": ["SLIM FRAME", "GLASS DOOR"], "hidden": ["FLUSH HIDDEN DOOR"],
}


# ======================================================================= material notes
def material_lines(code):
    m = MAT.get(code)
    if not m:
        return [code]
    return [m[2], m[3], (m[4] if len(m[4]) < 22 else m[1], RED)]


def used_mats(cab):
    seen = []
    for c in cab.cols:
        for p in c.parts:
            if p.mat and p.mat not in seen and p.kind not in ("gap", "void", "appliance"):
                seen.append(p.mat)
    if cab.worktop and cab.worktop[2] not in seen:
        seen.append(cab.worktop[2])
    return seen


# ======================================================================= sheet builder
SCALES = [20, 25, 30, 35, 40, 50, 60, 75]


def build_sheet(cab: Cabinet):
    s = Sheet(cab.sheet_no, cab.title, drawing_title=f"{cab.room} {cab.title} ELEVATION")
    W, H, Dp = cab.W, cab.cl + 150, cab.depth
    top_area = 290 - 6
    elev_h_max = 112
    # choose scale: prefer elevation + inner carcass + section; else elevation + section
    def fits(sc, inner):
        ew = (W + 2 * WALL_T + 1400) / sc
        sw = (Dp + WALL_T + 1300) / sc
        total = (ew * 2 if inner else ew) + sw + 20
        return H / sc <= elev_h_max and total <= 400
    sc, with_inner = None, True
    for cand in SCALES:
        if cand <= 40 and fits(cand, True):
            sc = cand
            break
    if sc is None:
        with_inner = False
        sc = next((c for c in SCALES if fits(c, False)), SCALES[-1])
    base_y = s.draw_top + 44                       # FFL line on paper
    x_cursor = 14 + WALL_T / sc + 4
    # ---------------- elevation A
    ve = View(s, (x_cursor, base_y), sc)
    draw_front(ve, cab)
    # material tags + notes
    mats = used_mats(cab)
    tagged = set()
    xx = 0
    for c in cab.cols:
        yy = cab.plinth
        for p in c.parts:
            if p.mat and p.kind not in ("gap", "void", "appliance") and p.h > 150:
                ve.mat_tag((xx + c.w / 2, yy + p.h - 120 * sc / 30), p.mat, 1.5)
            yy += p.h
        xx += c.w
    # dims
    xs = [0]
    for c in cab.cols:
        xs.append(xs[-1] + c.w)
    for a, b in zip(xs, xs[1:]):
        ve.dim((a, 0), (b, 0), -260 * sc / 30, 1.9)
    ve.dim((0, cab.cl), (W, cab.cl), 230 * sc / 30, 1.9)
    c0 = cab.cols[-1]
    ys = [0, cab.plinth] if cab.plinth else [0]
    for p in c0.parts:
        ys.append(ys[-1] + p.h)
    if cab.top < cab.cl and ys[-1] < cab.cl:
        ys.append(cab.cl)
    for a, b in zip(ys, ys[1:]):
        if b - a > 1:
            ve.dim((W, a), (W, b), -(WALL_T + 220 * sc / 30), 1.8)
    ve.dim((0, 0), (0, max(ys)), WALL_T + 330 * sc / 30, 1.9)
    elev_right = x_cursor + (W + WALL_T + 900) / sc
    ex, _ = ve.P(0, 0)
    s.elev_label((ex - 2, base_y - 26), "ELEVATION A", f"1:{sc}")
    # notes column (right of elevation)
    note_x = (W + WALL_T + 450 * sc / 30)
    ny = cab.cl * 0.78
    for m in mats:
        # pick a part with this material for the leader tip
        tip = None
        xx = 0
        for c in cab.cols:
            yy = cab.plinth
            for p in c.parts:
                if p.mat == m and tip is None and p.kind not in ("gap",):
                    tip = (xx + c.w * 0.75, yy + p.h * 0.5)
                yy += p.h
            xx += c.w
        if tip is None and cab.worktop:
            tip = (W * 0.6, cab.worktop[0] - 10)
        if tip:
            ve.leader(tip, (note_x, ny), material_lines(m), 1.7, 7, "LEFT")
        ny -= 520 * sc / 30
    x_cursor = elev_right + 22
    # ---------------- inner carcass
    if with_inner:
        vi = View(s, (x_cursor + WALL_T / sc, base_y), sc)
        draw_front(vi, cab, inner=True)
        vi.leader((W * 0.5, cab.cl * 0.55), (W + WALL_T + 260, cab.cl * 0.62),
                  ["INNER CARCASS", "WHITE", ("MELAMINE", RED)], 1.7, 7, "LEFT")
        ix, _ = vi.P(0, 0)
        s.elev_label((ix - 2, base_y - 26), "INNER CARCASS A", f"1:{sc}")
        x_cursor = x_cursor + (W + 2 * WALL_T + 900) / sc + 18
    # ---------------- section X-X
    vs = View(s, (x_cursor, base_y), sc)
    sec_col = next((c for c in cab.cols if any(p.kind == "counter" for p in c.parts)), cab.cols[0])
    draw_section(vs, cab, sec_col)
    sx, _ = vs.P(0, 0)
    s.elev_label((sx - 2, base_y - 26), "SECTION X-X", f"1:{sc}")
    # ---------------- plan key (top-left)
    psc = max(sc, 30)
    if W / psc > 150:
        psc = int(math.ceil(W / 150 / 5) * 5)
    plan_y = 290 - 22 - (Dp + WALL_T) / psc
    vp = View(s, (14 + WALL_T / psc + 18, plan_y), psc)
    draw_plan_key(vp, cab)
    px, py = vp.P(0, 0)
    s.circle((14 + 8, py + 4), 7.5, "I-TEXT")
    s.text(cab.code, (14 + 8, py + 4), 3.0, "I-TEXT", "MIDDLE_CENTER")
    s.text(f"{cab.title} SET", (14 + 17, py + 5.2), 2.4, "I-TEXT", "LEFT")
    s.line((14 + 15.5, py + 4), (14 + 17 + len(cab.title) * 1.9 + 10, py + 4), "I-TEXT")
    s.text(f"1:{psc}", (14 + 17, py + 0.6), 2.2, "I-TEXT", "LEFT")
    # ---------------- details (top-right)
    plan_right = vp.P(cab.W + WALL_T + 400, 0)[0]
    r = 21
    n = len(cab.details)
    dx0 = max(plan_right + r + 6, 415 - n * (2 * r + 9) + r - 4)
    for i, k in enumerate(cab.details):
        cx = dx0 + i * (2 * r + 9)
        cy = 290 - 14 - r - 6
        if cx + r > 414:
            break
        detail_circle(s, (cx, cy), r, i + 1, DETAIL_TITLES[k])
        detail_geom(s, k, (cx, cy), r)
    # notes block
    if cab.notes:
        s.text("NOTES:", (262, 214), 2.2, "I-NOTE", "LEFT", color=RED)
        for i, t in enumerate(cab.notes):
            s.text(f"{i + 1}. {t}", (262, 210 - i * 3.4), 1.75, "I-NOTE", "LEFT", color=RED)
    s.sheet_tag(f"{cab.room} - {cab.title}", "ELEVATION PLAN", "ID", cab.sheet_no.split(".")[1] if "." in cab.sheet_no else "02")
    return s
