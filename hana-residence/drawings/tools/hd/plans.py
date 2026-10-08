"""Plan sheets (ID.01 series) for GF and FF."""
from __future__ import annotations

import math
import os
import pymupdf

from .core import Sheet, View, grid_bubble, RED, BLUE, MAGENTA, GREEN, A3, MARGIN
from .base import draw_base, _load
from . import data as D

SRC_PDF = "/root/.claude/uploads/9270a7da-af5d-57ee-8fc3-3260542e09a0/9ee71a27-HANA_RESIDENCEDWG__G1_FLOOR.pdf"
SCALE = 100
PLAN_BOX = (14, 36, 322, 286)        # paper area for the plan incl. grid bubbles
LEG_X = 326                          # legend column x


class Floor:
    def __init__(self, key):
        self.key = key
        if key == "GF":
            self.grid, self.clip, self.rooms, self.join, self.rects = D.GRID_GF, D.CLIP_GF, D.ROOMS_GF, D.JOIN_GF, D.RECT_GF
            self.base_ori, self.base_new, self.name = "gf_ori", "gf_new", "GROUND FLOOR"
        else:
            self.grid, self.clip, self.rooms, self.join, self.rects = D.GRID_FF, D.CLIP_FF, D.ROOMS_FF, D.JOIN_FF, D.RECT_FF
            self.base_ori, self.base_new, self.name = "ff_exist", "ff_new", "FIRST FLOOR"


def new_plan_sheet(fl: Floor, number, title, legend_needed=True):
    s = Sheet(number, title, fl.name, drawing_title=f"{title} ({fl.name})")
    x0, y0, x1, y1 = fl.clip
    bx0, by0, bx1, by1 = PLAN_BOX
    w = (x1 - x0) / SCALE
    h = (y1 - y0) / SCALE
    ox = bx0 + 14 + ((bx1 - bx0 - 14) - w) / 2
    oy = by0 + ((by1 - by0 - 18) - h) / 2
    v = View(s, (ox, oy), SCALE, (x0, y0))
    draw_grid(v, fl)
    s.view_label((12, 42), "01", f"{title} ({fl.name})".upper(), f"SCALE 1:{SCALE}", w=95)
    s.sheet_tag(title.upper(), fl.name, "ID", number.split(".")[-1])
    return s, v


def draw_grid(v: View, fl: Floor):
    x0, y0, x1, y1 = fl.clip
    xs = [p for p in fl.grid["x"] if x0 - 500 <= p[1] <= x1 + 500]
    ys = [p for p in fl.grid["y"] if y0 - 500 <= p[1] <= y1 + 500]
    ytop, xleft = y1 + 900, x0 - 900
    for lab, x in xs:
        v.line((x, y0 - 200), (x, ytop - 200), "A-GRID")
        px, py = v.P(x, ytop)
        grid_bubble(v.s, (px, py + 4.2), lab)
    for lab, y in ys:
        v.line((xleft + 200, y), (x1 + 200, y), "A-GRID")
        px, py = v.P(xleft, y)
        grid_bubble(v.s, (px - 4.2, py), lab)
    xv = [x for _, x in xs]
    yv = [y for _, y in ys]
    for a, b in zip(xv, xv[1:]):
        v.dim((a, ytop - 450), (b, ytop - 450), 0, 1.8, ext=False)
    for a, b in zip(yv, yv[1:]):
        v.dim((xleft + 450, a), (xleft + 450, b), 0, 1.8, ext=False)


# ------------------------------------------------------------------ labels
def ori_labels(v: View, fl: Floor):
    """Room names from the original DWG text, placed at their mm positions."""
    doc = pymupdf.open(SRC_PDF)
    if fl.key == "GF":
        page, ya, xr, s = doc[0], 169.8, 241.9, 36.1106
    else:
        page, ya, xr, s = doc[3], 270.0, 259.8, 28.234
    words = page.get_text("words")
    skip = set("ABCDEFG") | {str(i) for i in range(0, 11)} | {"01"}
    groups = {}
    for w in words:
        t = w[4]
        if t.isdigit() or t in skip or len(t) < 2 or t.startswith("/"):
            continue
        X = ((w[1] + w[3]) / 2 - ya) * s
        Y = ((w[0] + w[2]) / 2 - xr) * s
        x0, y0, x1, y1 = fl.clip
        if not (x0 < X < x1 and y0 < Y < y1):
            continue
        groups.setdefault((round(X / 900), round(Y / 2500)), []).append((Y, X, t))
    for key, items in groups.items():
        items.sort(key=lambda r: -r[0])
        X = sum(i[1] for i in items) / len(items)
        Y = sum(i[0] for i in items) / len(items)
        txt = " ".join(i[2] for i in items)
        if any(k in txt for k in ("TURFING", "measurements", "COPYRIGHT")):
            continue
        v.text(txt, (X, Y), 2.0, "I-ROOM")


def room_labels(v: View, fl: Floor, with_cl=False, with_finish=None):
    for name, (x, y), cl, fin, paint in fl.rooms:
        v.text(name, (x, y), 2.1, "I-ROOM")
        if with_cl and cl not in ("-",):
            tag_box(v, (x, y - 520), cl)
        if with_finish == "floor" and fin not in ("-",):
            v.mat_tag((x, y - 520), fin, 1.7)
        if with_finish == "wall" and paint not in ("-",):
            v.mat_tag((x, y - 520), paint, 1.7)


def tag_box(v: View, p, txt, color=RED):
    x, y = v.P(p)
    w = len(txt) * 1.25 + 2.4
    v.s.rect(x - w / 2, y - 1.6, x + w / 2, y + 1.6, "I-NOTE", color=color)
    v.s.text(txt, (x, y), 1.7, "I-NOTE", "MIDDLE_CENTER", color=color)


# ------------------------------------------------------------------ joinery & furniture
def draw_join(v: View, fl: Floor, label=True, codes=False, dims=False):
    for code, lab, (x0, y0, x1, y1), front, kind in fl.join:
        lay = "I-JOIN"
        if kind == "wall":
            v.rect(x0, y0, x1, y1, "I-JOIN-HIDDEN")
        else:
            v.rect(x0, y0, x1, y1, lay)
        # door line 20mm inside front face
        d = 20
        if kind in ("full", "base", "tall"):
            if front == "S":
                v.line((x0, y0 + d), (x1, y0 + d), lay)
            elif front == "N":
                v.line((x0, y1 - d), (x1, y1 - d), lay)
            elif front == "E":
                v.line((x1 - d, y0), (x1 - d, y1), lay)
            elif front == "W":
                v.line((x0 + d, y0), (x0 + d, y1), lay)
        if kind == "full":
            v.line((x0, y0), (x1, y1), "I-JOIN-HIDDEN")
        if kind == "island":
            v.rect(x0 + 30, y0 + 30, x1 - 30, y1 - 30, "I-JOIN-HIDDEN")
        w, h = x1 - x0, y1 - y0
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        rot = 90 if h > w * 1.6 else 0
        if label:
            span = (h if rot else w) / SCALE
            th = min(1.25, span * 0.85 / max(1, len(lab) * 0.62))
            if th >= 0.55:
                v.text(lab, (cx, cy), th, "I-JOIN", "MIDDLE_CENTER", rot)
        if codes:
            off = 450
            p = {"S": (cx, y0 - off), "N": (cx, y1 + off), "E": (x1 + off, cy), "W": (x0 - off, cy)}[front]
            v.elev_marker(p, "A", {"S": "N", "N": "S", "E": "W", "W": "E"}[front], r=2.0)
            v.text(code, (p[0], p[1] - 380 if front in "EW" else p[1] + (380 if front == "N" else -380)), 1.6,
                   "I-SYMB", "MIDDLE_CENTER", color=MAGENTA)
        if dims:
            if w >= h:
                side = -1 if front == "S" else 1
                yy = y0 if side < 0 else y1
                v.dim((x0, yy), (x1, yy), 260 * side, 1.5)
                v.dim((x1, y0), (x1, y1), -230, 1.4)
            else:
                side = 1 if front == "W" else -1
                xx = x0 if side > 0 else x1
                v.dim((xx, y0), (xx, y1), 260 * side, 1.5)
                v.dim((x0, y1), (x1, y1), 230, 1.4)


def furniture(v: View, fl: Floor):
    L = "I-FURN"
    if fl.key == "GF":
        # dining: round table + 8 chairs
        c = (4550, 18600)
        v.circle(c, 900, L); v.circle(c, 450, L)
        for i in range(8):
            a = math.radians(i * 45 + 22.5)
            p = (c[0] + 1250 * math.cos(a), c[1] + 1250 * math.sin(a))
            chair(v, p, i * 45 + 22.5)
        # stools at island
        for x in (6900, 7700):
            v.circle((x, 19200), 230, L)
        # sofa (L shape) + coffee table
        v.poly([(3800, 15900), (7400, 15900), (7400, 15050), (6600, 15050), (6600, 13500), (5800, 13500),
                (5800, 15050), (3800, 15050)], L, close=True)
        v.rect(4300, 13300, 5600, 14300, L)
        v.circle((4900, 13800), 300, L)
        # lounge armchairs + side table, piano
        for y in (9600, 10500):
            v.rect(3500, y, 4300, y + 750, L)
        v.rect(4750, 8800, 5800, 9350, L)
        v.text("PIANO", (5275, 9075), 1.1, L)
        v.circle((7800, 10200), 500, L)
        # parents bed (queen)
        bed(v, (4100, 23400), 1830, 2100, "E")
        # maid bed
        v.rect(9800, 22200, 10800, 24100, L)
        # wet kitchen hob
        for x in (12600, 12900):
            v.circle((x, 16250), 120, L)
        # washer & dryer
        for x in (12100, 12750):
            v.rect(x, 26480, x + 600, 27020, L); v.circle((x + 300, 26750), 210, L)
    else:
        bed(v, (330, 16900), 1830, 2050, "E", king=True)
        v.rect(2900, 15400, 3500, 16100, L); v.text("MASSAGE CHAIR", (3200, 15750), 0.9, L)
        # family area lounge chairs + piano
        v.rect(-600, 12200, 600, 12750, L); v.text("PIANO", (0, 12475), 1.0, L)
        for x in (1300, 2700):
            v.rect(x, 12500, x + 800, 13300, L)
        v.rect(1900, 12600, 2500, 13200, L)
        # son's bed + daughter's bed
        bed(v, (7200, 1300), 1520, 1950, "N")
        bed(v, (1900, 3500), 1520, 1950, "S")
        v.poly([(7300, 19900), (8900, 19900), (8900, 19100), (7300, 19100)], L, close=True)
        v.text("BATHTUB", (8100, 19500), 1.1, L)


def chair(v, p, ang):
    a = math.radians(ang)
    r = 260
    pts = []
    for dx, dy in ((-r, -r), (r, -r), (r, r), (-r, r)):
        pts.append((p[0] + dx * math.cos(a) - dy * math.sin(a), p[1] + dx * math.sin(a) + dy * math.cos(a)))
    v.poly(pts, "I-FURN", close=True)


def bed(v, p, w, l, head, king=False):
    """Bed with headboard on side `head` (E: head at x0, foot towards +x; N: head at top...)."""
    x, y = p
    L = "I-FURN"
    if head == "E":
        v.rect(x, y, x + l, y + w, L)
        v.rect(x + 50, y + 80, x + 450, y + w / 2 - 40, L)
        v.rect(x + 50, y + w / 2 + 40, x + 450, y + w - 80, L)
        v.line((x + 700, y), (x + 700, y + w), L)
    elif head == "N":
        v.rect(x, y, x + w, y + l, L)
        v.rect(x + 80, y + l - 450, x + w / 2 - 40, y + l - 50, L)
        v.rect(x + w / 2 + 40, y + l - 450, x + w - 80, y + l - 50, L)
        v.line((x, y + l - 700), (x + w, y + l - 700), L)
    else:  # S
        v.rect(x, y, x + w, y + l, L)
        v.rect(x + 80, y + 50, x + w / 2 - 40, y + 450, L)
        v.rect(x + w / 2 + 40, y + 50, x + w - 80, y + 450, L)
        v.line((x, y + 700), (x + w, y + 700), L)


# ------------------------------------------------------------------ legend helper
def legend(s: Sheet, title, rows, y_top=None, x=LEG_X, w=86, row_h=7.0, symbol_fn=None, count=True):
    """rows: list of (symbol_key, text, qty). symbol_fn(sheet, (cx,cy), key) draws symbol."""
    y = y_top or (A3[1] - MARGIN - 18)
    s.text(title, (x, y + 2.5), 2.6, "I-NOTE", "LEFT", color=RED)
    s.line((x, y + 1.6), (x + len(title) * 2.1, y + 1.6), "I-NOTE", color=RED)
    y -= 1
    for i, (key, txt, qty) in enumerate(rows):
        yy = y - i * row_h
        s.rect(x, yy - row_h, x + 14, yy, "I-TEXT")
        s.rect(x + 14, yy - row_h, x + w - (12 if count else 0), yy, "I-TEXT")
        if count:
            s.rect(x + w - 12, yy - row_h, x + w, yy, "I-TEXT")
            s.text(str(qty), (x + w - 6, yy - row_h / 2), 1.8, "I-TEXT", "MIDDLE_CENTER")
        lines = txt.split("\n")
        for j, ln in enumerate(lines):
            s.text(ln, (x + 16, yy - row_h / 2 + (len(lines) - 1) * 1.1 - j * 2.2), 1.7, "I-NOTE", "MIDDLE_LEFT", color=RED)
        if symbol_fn:
            symbol_fn(s, (x + 7, yy - row_h / 2), key)
    return y - len(rows) * row_h - 8
