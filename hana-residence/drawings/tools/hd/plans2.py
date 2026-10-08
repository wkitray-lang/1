"""The ID.01 plan sheet builders (one function per sheet type)."""
from __future__ import annotations

import math

from .core import RED, BLUE, MAGENTA, GREEN, CYAN, A3, MARGIN
from .base import draw_base, _load
from .plans import (Floor, new_plan_sheet, room_labels, ori_labels, draw_join, furniture, legend, tag_box,
                    LEG_X, SCALE)
from . import data as D

# ======================================================================= design points
WINDOWS = {
    "GF": [("W", 3060, 9000, 11800, "LOUNGE"), ("W", 3060, 12700, 13600, "LIVING"),
           ("W", 3060, 16700, 18300, "DINING"), ("W", 3060, 19800, 20800, "DINING"),
           ("E", 15070, 9300, 11850, "FOYER"), ("E", 14220, 17400, 20900, "WET KITCHEN"),
           ("N", 26300, 4300, 7250, "PARENT'S ROOM"), ("N", 27120, 12800, 13900, "LAUNDRY AREA"),
           ("S", 8285, 7400, 8500, "LOUNGE")],
    "FF": [("N", 20520, 300, 3900, "MASTER BEDROOM"), ("N", 20520, 5100, 6600, "MASTER BEDROOM"),
           ("W", -925, 12700, 14000, "FAMILY AREA"), ("W", -925, 4000, 5600, "DAUGHTER'S ROOM"),
           ("S", -25, 2000, 3500, "DAUGHTER'S ROOM"), ("E", 11020, 4000, 6000, "SON'S ROOM"),
           ("E", 10220, 13000, 14100, "WALK IN CLOSET"), ("E", 11020, 17200, 19200, "MASTER BATH")],
}

CURTAIN_TYPE = {  # room -> (legend key, label)
    "LOUNGE": "SHEER", "LIVING": "SHEER", "DINING": "SHEER", "FOYER": "SHOJI",
    "WET KITCHEN": "ROLLER", "PARENT'S ROOM": "DOUBLE", "LAUNDRY AREA": "ROLLER",
    "MASTER BEDROOM": "DOUBLE", "FAMILY AREA": "SHEER", "DAUGHTER'S ROOM": "DOUBLE",
    "SON'S ROOM": "DOUBLE", "WALK IN CLOSET": "ROMAN", "MASTER BATH": "ROMAN",
}

COVE_ROOMS = {
    "GF": ["LOUNGE", "FOYER", "DINING", "DRY KITCHEN", "PARENT'S ROOM", "ENTRANCE"],
    "FF": ["MASTER BEDROOM", "WALK IN CLOSET", "FAMILY AREA", "DAUGHTER'S ROOM", "SON'S ROOM"],
}
COFFERS = {"GF": [((4550, 18600), 1200, "DINING"), ((12300, 10150), 1200, "FOYER"), ((7300, 19950), 900, "DRY KITCHEN")],
           "FF": [((7900, 13700), 1200, "WALK IN CLOSET"), ((4650, 9000), 600, "CORRIDOR")]}
AC_GRILLES = {"GF": [(4600, 21000, 0), (7600, 21000, 0), (6300, 16400, 0), (13000, 11600, 0), (6000, 25900, 0)],
              "FF": [(2000, 20100, 0), (1600, 14600, 0), (8200, 6450, 0), (1000, 6450, 0)]}
PENDANTS = {"GF": [(4550, 18600), (7300, 19950), (12300, 10150), (6000, 14500), (11950, 18500), (5800, 24300)],
            "FF": [(7900, 13700), (7300, 13700), (1000, 13300), (2200, 17400)]}
FANS = {"GF": [(5600, 14200), (11950, 19600), (5400, 24700), (5600, 10200)],
        "FF": [(2600, 18000), (8300, 4300), (1500, 4800), (1800, 13300)]}
WALL_LIGHTS = {"GF": [(9580, 13500, "E"), (3150, 19200, "E"), (3150, 15000, "E"), (11450, 7500, "E"), (13940, 7500, "W"),
                      (9760, 15000, "E")],
               "FF": [(330, 15900, "E"), (330, 20000, "E"), (-840, 13300, "E"), (5700, 2700, "E"), (2400, 6750, "S")]}
TRACKS = {"GF": [((5800, 20700), (8800, 20700))], "FF": [((6000, 15700), (9300, 15700))]}
SWITCHES = {
    "GF": [(10500, 8400, 3), (14900, 11700, 2), (3200, 11800, 3), (9450, 16000, 3), (9800, 16100, 2),
           (3200, 21300, 2), (9800, 14600, 1), (13000, 12700, 2), (11800, 21600, 2), (9800, 21600, 1),
           (9800, 25200, 1), (4100, 22300, 3), (7900, 23900, 1), (11500, 7000, 1)],
    "FF": [(3700, 15000, 3), (5600, 15200, 2), (5700, 10100, 2), (3900, 6900, 2), (5700, 6300, 2),
           (3600, 3900, 1), (3900, 3600, 1), (7050, 17500, 1), (3600, 6700, 2), (5600, 11500, 2)],
}

# sockets: (x, y, kind, note)  kinds: 13A, 13A2, 15A, 20A, 32A, AC, TV, DATA, CM (curtain motor), FLOOR
SOCKETS = {
    "GF": [
        (3300, 12450, "TV", "FFL 450MM TV"), (3600, 12450, "13A2", "FFL 450MM"), (4000, 12450, "DATA", "FFL 450MM"),
        (8900, 12450, "13A2", "FFL 450MM"), (3200, 9000, "13A", "FFL 300MM"), (5200, 8800, "13A", "FFL 300MM PIANO"),
        (10000, 8800, "13A", "FFL 1000MM KEY CONSOLE"), (12700, 12000, "13A2", "FFL 1050MM ALTAR"),
        (11000, 7100, "13A", "FFL 300MM SHOE CAB."), (14400, 8000, "13A", "FFL 300MM"),
        (7300, 19950, "FLOOR", "ISLAND POP-UP"), (5600, 21500, "13A2", "FFL 1050MM"), (7000, 21500, "13A2", "FFL 1050MM COFFEE"),
        (8200, 21500, "15A", "FFL 300MM WINE CHILLER"), (3200, 17000, "13A", "FFL 300MM"), (3200, 20500, "13A", "FFL 300MM"),
        (10100, 20700, "20A", "FFL 600MM OVEN"), (10700, 20700, "15A", "FFL 900MM MICROWAVE"), (11500, 20700, "13A", "FFL 300MM FRIDGE"),
        (12700, 16000, "32A", "FFL 600MM INDUCTION HOB"), (13700, 16000, "13A2", "FFL 1050MM"), (14100, 18700, "15A", "FFL 300MM DISHWASHER"),
        (14100, 19700, "13A2", "FFL 1050MM"), (14100, 17000, "13A", "FFL 2200MM HOOD"), (12000, 18500, "FLOOR", "ISLAND POP-UP"),
        (12200, 26500, "15A", "FFL 600MM WASHER"), (12850, 26500, "15A", "FFL 600MM DRYER"), (14100, 24000, "13A", "FFL 1050MM"),
        (7650, 24300, "13A2", "FFL 650MM BEDSIDE"), (4100, 24900, "13A2", "FFL 650MM BEDSIDE"), (4100, 22900, "13A2", "FFL 650MM BEDSIDE"),
        (9800, 23800, "13A", "FFL 650MM"), (9100, 26800, "15A", "FFL 2000MM WATER HEATER"),
        (10500, 14600, "13A", "FFL 1050MM"), (6000, 26150, "AC", "FFL 2200MM ISOLATOR"), (9700, 24800, "AC", "FFL 2200MM ISOLATOR"),
        (3200, 10500, "CM", "FFL 2820MM CURTAIN"), (3200, 17500, "CM", "FFL 2820MM CURTAIN"), (5800, 26150, "CM", "FFL 2820MM CURTAIN"),
    ],
    "FF": [
        (330, 16000, "13A2", "FFL 650MM BEDSIDE"), (330, 20100, "13A2", "FFL 650MM BEDSIDE"), (4590, 17900, "TV", "FFL 1200MM TV"),
        (4590, 17400, "13A2", "FFL 450MM FIREPLACE"), (4590, 18400, "DATA", "FFL 1200MM"), (3000, 15150, "13A", "FFL 300MM MASSAGE CHAIR"),
        (5500, 17500, "13A", "FFL 1050MM MINI BAR"), (2000, 20400, "CM", "FFL 2820MM CURTAIN"), (100, 17000, "AC", "FFL 2200MM ISOLATOR"),
        (10850, 18500, "13A2", "FFL 1050MM VANITY"), (10850, 19500, "15A", "FFL 2000MM WATER HEATER"),
        (6400, 10100, "13A2", "FFL 850MM DRESSING"), (8000, 13350, "13A", "FLOOR / ISLAND"), (-800, 12300, "13A", "FFL 300MM PIANO"),
        (-800, 14300, "13A2", "FFL 300MM"), (2500, 14900, "DATA", "FFL 300MM"), (-800, 13200, "CM", "FFL 2820MM CURTAIN"),
        (6300, 4300, "13A2", "FFL 750MM STUDY"), (6300, 4800, "DATA", "FFL 750MM"), (7100, 3200, "13A2", "FFL 650MM BEDSIDE"),
        (8900, 3200, "13A2", "FFL 650MM BEDSIDE"), (10900, 5000, "CM", "FFL 2820MM CURTAIN"), (10800, 2800, "AC", "FFL 2200MM ISOLATOR"),
        (1800, 3500, "13A2", "FFL 650MM BEDSIDE"), (3500, 3500, "13A2", "FFL 650MM BEDSIDE"), (3100, 4250, "13A2", "FFL 850MM DRESSING"),
        (-800, 4800, "CM", "FFL 2820MM CURTAIN"), (2400, 6100, "AC", "FFL 2200MM ISOLATOR"),
        (-800, 2900, "15A", "FFL 2000MM WATER HEATER"), (4300, 2900, "15A", "FFL 2000MM WATER HEATER"),
        (4650, 6900, "13A", "FFL 300MM CORRIDOR"),
    ],
}
SOCKET_LEGEND = [("13A", "NEW 13AMP SINGLE POWER POINT"), ("13A2", "NEW 13AMP TWIN POWER POINT"),
                 ("15A", "NEW 15AMP POWER POINT"), ("20A", "NEW 20AMP POWER POINT (OVEN)"),
                 ("32A", "NEW 32AMP POWER POINT (INDUCTION HOB)"), ("AC", "AIR-COND ISOLATOR POINT"),
                 ("TV", "TV POINT"), ("DATA", "DATA / CAT6 POINT"), ("CM", "SMART CURTAIN MOTOR POINT"),
                 ("FLOOR", "FLOOR / POP-UP SOCKET")]


# ======================================================================= helpers
def rects_of(fl, name):
    return fl.rects.get(name, [])


def all_room_rects(fl):
    for name, rs in fl.rects.items():
        for r in rs:
            yield name, r


def inside_join(fl, x, y, pad=150):
    for _, _, (x0, y0, x1, y1), _, _ in fl.join:
        if x0 - pad < x < x1 + pad and y0 - pad < y < y1 + pad:
            return True
    return False


def downlights(fl):
    """Auto layout of recessed downlights on a ~1.35 m grid, skipping joinery / void."""
    pts = []
    skip = {"VOID", "STAIRCASE", "MAID BATH"}
    for name, (x0, y0, x1, y1) in all_room_rects(fl):
        if name in skip:
            continue
        w, h = x1 - x0, y1 - y0
        nx = max(1, round((w - 600) / 1450))
        ny = max(1, round((h - 600) / 1450))
        for i in range(nx + 1 if nx > 1 else 1):
            for j in range(ny + 1 if ny > 1 else 1):
                x = x0 + 600 + (w - 1200) * (i / nx if nx > 1 else 0.5) if nx > 1 else (x0 + x1) / 2
                y = y0 + 600 + (h - 1200) * (j / ny if ny > 1 else 0.5) if ny > 1 else (y0 + y1) / 2
                if not inside_join(fl, x, y):
                    pts.append((x, y, name))
    return pts


# ======================================================================= symbols (paper coords)
def sym_downlight(s, c, r=1.1):
    x, y = c
    s.circle(c, r, "I-LITE", color=RED)
    s.line((x - r * 1.5, y), (x + r * 1.5, y), "I-LITE", color=RED)
    s.line((x, y - r * 1.5), (x, y + r * 1.5), "I-LITE", color=RED)


def sym_pendant(s, c):
    x, y = c
    s.circle(c, 1.6, "I-LITE", color=RED)
    s.circle(c, 0.7, "I-LITE", color=RED)
    s.text("PD", (x + 2.0, y), 1.4, "I-LITE", "MIDDLE_LEFT", color=RED)


def sym_fan(s, c, r=3.2):
    x, y = c
    s.circle(c, r, "I-LITE", color=RED)
    for a0 in (45, 225):
        pts = [(x, y)] + [(x + r * math.cos(math.radians(a)), y + r * math.sin(math.radians(a))) for a in range(a0 - 45, a0 + 46, 9)]
        s.solid(pts, "I-LITE", color=RED)


def sym_walllight(s, c):
    x, y = c
    s.rect(x - 1.3, y - 0.8, x + 1.3, y + 0.8, "I-LITE", color=RED)
    s.circle(c, 0.55, "I-LITE", color=RED)


def sym_ledstrip(s, c):
    x, y = c
    s.line((x - 4, y), (x + 4, y), "I-LITE", color=RED, lineweight=50)


def sym_track(s, c):
    x, y = c
    s.line((x - 4, y + 0.5), (x + 4, y + 0.5), "I-LITE", color=RED)
    s.line((x - 4, y - 0.5), (x + 4, y - 0.5), "I-LITE", color=RED)


def sym_switch(s, c, gang=1):
    x, y = c
    s.solid([(x + 0.8 * math.cos(math.radians(a)), y + 0.8 * math.sin(math.radians(a))) for a in range(0, 360, 30)],
            "I-LITE", color=RED)
    s.line((x, y), (x + 2.0, y + 1.6), "I-LITE", color=RED)
    for g in range(gang):
        s.line((x + 1.4 + g * 0.45, y + 1.1 + g * 0.36), (x + 1.85 + g * 0.45, y + 0.55 + g * 0.36), "I-LITE", color=RED)


def sym_socket(s, c, kind):
    x, y = c
    col = {"15A": BLUE, "20A": BLUE, "32A": BLUE, "AC": GREEN, "TV": MAGENTA, "DATA": MAGENTA, "CM": CYAN}.get(kind, RED)
    if kind in ("13A", "13A2", "15A", "20A", "32A", "FLOOR"):
        s.circle(c, 1.2, "I-POWR", color=col)
        s.line((x - 1.2, y), (x + 1.2, y), "I-POWR", color=col)
        if kind == "13A2":
            s.line((x - 0.6, y + 1.0), (x - 0.6, y + 2.0), "I-POWR", color=col)
            s.line((x + 0.6, y + 1.0), (x + 0.6, y + 2.0), "I-POWR", color=col)
        elif kind != "FLOOR":
            s.line((x, y + 1.2), (x, y + 2.1), "I-POWR", color=col)
        else:
            s.rect(x - 1.7, y - 1.7, x + 1.7, y + 1.7, "I-POWR", color=col)
        if kind in ("15A", "20A", "32A"):
            s.text(kind[:-1], (x, y - 2.2), 1.1, "I-POWR", "MIDDLE_CENTER", color=col)
    elif kind == "AC":
        s.rect(x - 1.4, y - 1.0, x + 1.4, y + 1.0, "I-POWR", color=col)
        s.text("AC", (x, y), 1.0, "I-POWR", "MIDDLE_CENTER", color=col)
    elif kind == "TV":
        s.rect(x - 1.4, y - 1.0, x + 1.4, y + 1.0, "I-POWR", color=col)
        s.text("TV", (x, y), 1.0, "I-POWR", "MIDDLE_CENTER", color=col)
    elif kind == "DATA":
        s.poly([(x - 1.3, y - 1.0), (x + 1.3, y - 1.0), (x, y + 1.2)], "I-POWR", close=True, color=col)
        s.text("D", (x, y - 0.25), 0.9, "I-POWR", "MIDDLE_CENTER", color=col)
    elif kind == "CM":
        s.circle(c, 1.2, "I-POWR", color=col)
        s.text("M", (x, y), 1.1, "I-POWR", "MIDDLE_CENTER", color=col)


# ======================================================================= sheets
def sheet_ori(fl, number):
    s, v = new_plan_sheet(fl, number, "ORI. LAYOUT PLAN")
    draw_base(v, fl.base_ori)
    ori_labels(v, fl)
    return s


def _wall_boxes(key):
    out = []
    for e in _load(key).modelspace().query("LWPOLYLINE"):
        if not e.dxf.layer.startswith("SRC-FILLSTROKE"):
            continue
        xs = [p[0] for p in e.vertices()]; ys = [p[1] for p in e.vertices()]
        bb = (min(xs), min(ys), max(xs), max(ys))
        if bb[2] - bb[0] > 130 or bb[3] - bb[1] > 130:
            out.append((e.dxf.layer, bb, [(x, y) for x, y in e.vertices()]))
    return out


def _covered(bb, boxes, tol=80):
    x0, y0, x1, y1 = bb
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    for _, (a0, b0, a1, b1), _ in boxes:
        if a0 - tol <= cx <= a1 + tol and b0 - tol <= cy <= b1 + tol:
            return True
    return False


def sheet_demolish(fl, number):
    s, v = new_plan_sheet(fl, number, "WET WORK & DEMOLISH PLAN")
    draw_base(v, fl.base_ori)
    ori_labels(v, fl)
    old = _wall_boxes(fl.base_ori)
    new = _wall_boxes(fl.base_new)
    n_hack = n_new = 0
    for lay, bb, pts in old:
        if not _covered(bb, new) and lay != "SRC-FILLSTROKE-4554a5":
            v.solid(pts, "A-WALL-DEMO", color=RED)
            n_hack += 1
    for lay, bb, pts in new:
        if not _covered(bb, old) or lay in ("SRC-FILLSTROKE-0000ff", "SRC-FILLSTROKE-4554a5"):
            v.solid(pts, "A-WALL-NEW", color=BLUE)
            n_new += 1
    # floor hacking hatch to all renovated rooms
    for name, (x0, y0, x1, y1) in all_room_rects(fl):
        if name in ("VOID", "MAID BATH"):
            continue
        v.pattern([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], "ANSI37", 3.0, 0, "I-NOTE", color=RED)
    notes = {
        "GF": [((6500, 23000), (2600, 27800), ["REMOVE EXISTING FLOOR TILES & SKIRTING", "- SELF LEVELING FOR ENGINEERED WOOD"]),
               ((6300, 17500), (300, 16200), ["REMOVE EXISTING FLOOR TILES & SKIRTING", "- SELF LEVELING", "NEW TILES: DONG PENG LING HUA BAI 900x1800"]),
               ((12000, 19000), (16500, 21500), ["REMOVE EXISTING FLOOR & WALL TILES", "WALL: DONG PENG LIMESTONE JH12352GZ", "600x1200 STRUCTURED"]),
               ((11200, 15200), (16500, 15200), ["POWDER ROOM: HACK FLOOR & WALL TILES", "WATERPROOFING + 72HR PONDING TEST", "NEW: AMAZON TRAVERTINE 600x1200 MATT"]),
               ((12000, 10000), (16500, 9800), ["REMOVE EXISTING FLOOR TILES & SKIRTING", "NEW: BELLEZZA X-OLIVETTI X01 BLANCO", "600x1200"]),
               ((12300, 13500), (16500, 13000), ["STAIRCASE: HACK EXISTING FINISH", "NEW TREAD / RISER (REFER DETAIL)"]),
               ((8700, 25300), (16500, 27500), ["PARENT'S BATH: HACK FLOOR & WALL TILES", "WATERPROOFING + 72HR PONDING TEST"])],
        "FF": [((2600, 18000), (-2000, 21800), ["EXISTING FLOORING TO BE HACKED", "- SELF LEVELING FOR ENGINEERED WOOD"]),
               ((9000, 18500), (12000, 21800), ["MASTER BATH: HACK FLOOR & WALL TILES", "WATERPROOFING + 72HR PONDING TEST"]),
               ((7900, 13500), (12000, 12200), ["EX BEDROOM 3 + BATH 3 -> WALK IN CLOSET", "HACK BATH 3 TILES, SEAL FLOOR TRAP"]),
               ((430, 1700), (-2400, -900), ["DAUGHTER'S BATH: HACK FLOOR & WALL TILES (TBC)"]),
               ((4650, 1300), (5200, -900), ["SON'S BATH: HACK FLOOR & WALL TILES (TBC)"])],
    }[fl.key]
    for tip, tp, lines in notes:
        v.leader(tip, tp, lines, 1.6, RED, "LEFT")
    rows = [("wall", "EXISTING WALL", ""), ("hack", "WALL TO BE HACKED", ""), ("new", "NEW WALL (BRICK / BOARD)", ""),
            ("floor", "EXISTING FLOOR TILES TO BE\nHACKED / REMOVED", "")]

    def sym(sh, c, k):
        x, y = c
        if k == "wall":
            sh.solid([(x - 5, y - 1), (x + 5, y - 1), (x + 5, y + 1), (x - 5, y + 1)], "A-WALL-FILL", rgb=(77, 77, 77))
        elif k == "hack":
            sh.solid([(x - 5, y - 1), (x + 5, y - 1), (x + 5, y + 1), (x - 5, y + 1)], "A-WALL-DEMO", color=RED)
        elif k == "new":
            sh.solid([(x - 5, y - 1), (x + 5, y - 1), (x + 5, y + 1), (x - 5, y + 1)], "A-WALL-NEW", color=BLUE)
        else:
            sh.pattern([(x - 5, y - 2.5), (x + 5, y - 2.5), (x + 5, y + 2.5), (x - 5, y + 2.5)], "ANSI37", 0.06, 0, "I-NOTE", color=RED)
    legend(s, "LEGEND (DEMOLISH):", rows, symbol_fn=sym, count=False)
    return s


def sheet_furniture(fl, number):
    s, v = new_plan_sheet(fl, number, "FURNITURE LAYOUT PLAN")
    draw_base(v, fl.base_new)
    draw_join(v, fl)
    furniture(v, fl)
    room_labels(v, fl)
    return s


def sheet_flp_dim(fl, number):
    s, v = new_plan_sheet(fl, number, "FURNITURE LAYOUT PLAN - DIMENSION")
    draw_base(v, fl.base_new)
    draw_join(v, fl, label=True, dims=True)
    room_labels(v, fl)
    for name, (x0, y0, x1, y1) in all_room_rects(fl):
        if name in ("VOID", "STAIRCASE") or (x1 - x0) < 1500:
            continue
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        v.dim((x0, cy - 700), (x1, cy - 700), 0, 1.5, ext=False, color=BLUE)
        v.dim((cx + 900, y0), (cx + 900, y1), 0, 1.5, ext=False, color=BLUE)
    s.mtext("ROOM CLEAR DIMENSIONS ARE FROM WALL FINISH TO WALL FINISH.\\PJOINERY SIZES TO BE V.I.F. AFTER PLASTERING & TILING.",
            (LEG_X, 285), 1.8, 86, "I-NOTE", color=RED)
    return s


def sheet_rcp(fl, number):
    s, v = new_plan_sheet(fl, number, "REFLECTED CEILING PLAN")
    draw_base(v, fl.base_new)
    for name, (x, y), cl, _, _ in fl.rooms:
        v.text(name, (x, y + 380), 1.9, "I-ROOM")
        if cl != "-":
            tag_box(v, (x, y - 250), cl)
    n_cove = 0.0
    for name in COVE_ROOMS[fl.key]:
        for (x0, y0, x1, y1) in rects_of(fl, name):
            o = 300
            pts = [(x0 + o, y0 + o), (x1 - o, y0 + o), (x1 - o, y1 - o), (x0 + o, y1 - o)]
            v.poly(pts, "I-CEIL", close=True)
            v.poly([(x0 + o + 60, y0 + o + 60), (x1 - o - 60, y0 + o + 60), (x1 - o - 60, y1 - o - 60), (x0 + o + 60, y1 - o - 60)],
                   "I-CEIL-COVE", close=True, color=RED)
            n_cove += 2 * ((x1 - x0 - 2 * o) + (y1 - y0 - 2 * o)) / 1000
    for c, r, room in COFFERS[fl.key]:
        v.circle(c, r, "I-CEIL")
        v.circle(c, r - 80, "I-CEIL-COVE", color=RED)
        v.text(f"Ø{2 * r} COFFER", (c[0], c[1] - r - 250), 1.5, "I-NOTE", color=RED)
    if fl.key == "GF":
        # curved bulkhead along the void edge over living
        v.poly([(3150, 16550), (8800, 16550)], "I-CEIL")
        v.arc((8800, 16050), 500, 0, 90, "I-CEIL")
        v.leader((6000, 16550), (6000, 17300), ["CURVED BULKHEAD AT VOID EDGE", "C/W CONCEALED LED COVE"], 1.6, RED)
        for x in (10500, 11700, 12900):  # existing skylight boxing at wet kitchen
            v.rect(x, 20100, x + 900, 20900, "I-CEIL")
            v.line((x, 20100), (x + 900, 20900), "I-CEIL")
        v.text("EXISTING SKYLIGHT - BOXING", (11950, 21050), 1.4, "I-NOTE", color=RED)
    else:
        v.pattern([(-840, 6950), (3780, 6950), (3780, 11700), (-840, 11700)], "ANSI31", 4.0, 45, "I-CEIL", color=8)
        v.text("OPEN TO BELOW", (1470, 9300), 2.0, "I-NOTE", color=RED)
    for x, y, rot in AC_GRILLES[fl.key]:
        v.rect(x - 600, y - 80, x + 600, y + 80, "I-CEIL", color=GREEN)
        for k in range(1, 6):
            v.line((x - 600 + k * 200, y - 80), (x - 600 + k * 200, y + 80), "I-CEIL", color=GREEN)
    for c in FANS[fl.key]:
        v.circle(c, 120, "I-CEIL"); v.text("FAN HOOK", (c[0], c[1] - 260), 1.2, "I-NOTE", color=RED)
    rows = [("pl", "9MM PLASTER CEILING C/W\nSKIM COAT & PAINT", ""), ("cove", "L-BOX / COVE C/W LED STRIP\n(3000K)", ""),
            ("cof", "CIRCULAR COFFER CEILING", ""), ("ac", "LINEAR AIR-COND GRILLE\n(BY AC VENDOR)", ""),
            ("cl", "CEILING LEVEL FROM FFL", "")]

    def sym(sh, c, k):
        x, y = c
        if k == "pl":
            sh.rect(x - 5, y - 2.5, x + 5, y + 2.5, "I-CEIL")
        elif k == "cove":
            sh.line((x - 5, y), (x + 5, y), "I-CEIL-COVE", color=RED)
        elif k == "cof":
            sh.circle(c, 2.6, "I-CEIL"); sh.circle(c, 2.0, "I-CEIL-COVE", color=RED)
        elif k == "ac":
            sh.rect(x - 5, y - 1, x + 5, y + 1, "I-CEIL", color=GREEN)
        else:
            sh.rect(x - 5, y - 1.5, x + 5, y + 1.5, "I-NOTE", color=RED); sh.text("CL", c, 1.4, "I-NOTE", "MIDDLE_CENTER", color=RED)
    legend(s, "LEGEND (CEILING):", rows, symbol_fn=sym, count=False)
    s.mtext("ALL CEILING LEVELS ARE DESIGN LEVELS (TBC).\\PSITE SOFFIT HEIGHTS PER SITE MEASURE: "
            + ("FOYER S3814, LIVING SH4207, BREAKFAST SH4273, DINING SH8118 (VOID), WET KITCHEN CH3539, ENTRANCE CH3334."
               if fl.key == "GF" else "MASTER CH3614, FAMILY CH3627, STAIR CH4620."),
            (LEG_X, 160), 1.7, 86, "I-NOTE", color=RED)
    return s, round(n_cove, 1)


def sheet_lighting(fl, number):
    s, v = new_plan_sheet(fl, number, "LIGHTING PLAN")
    draw_base(v, fl.base_new)
    draw_join(v, fl, label=False)
    room_labels(v, fl)
    dls = downlights(fl)
    for x, y, _ in dls:
        sym_downlight(s, v.P(x, y))
    for c in PENDANTS[fl.key]:
        sym_pendant(s, v.P(c))
    for c in FANS[fl.key]:
        sym_fan(s, v.P(c))
    for x, y, d in WALL_LIGHTS[fl.key]:
        sym_walllight(s, v.P(x, y))
    led = 0.0
    for name in COVE_ROOMS[fl.key]:
        for (x0, y0, x1, y1) in rects_of(fl, name):
            o = 360
            v.poly([(x0 + o, y0 + o), (x1 - o, y0 + o), (x1 - o, y1 - o), (x0 + o, y1 - o)], "I-LITE", close=True, color=RED)
            led += 2 * ((x1 - x0 - 2 * o) + (y1 - y0 - 2 * o)) / 1000
    for a, b in TRACKS[fl.key]:
        v.line((a[0], a[1] + 40), (b[0], b[1] + 40), "I-LITE", color=RED)
        v.line((a[0], a[1] - 40), (b[0], b[1] - 40), "I-LITE", color=RED)
    # joinery LED (shelves / plinth)
    jled = 0.0
    for code, lab, (x0, y0, x1, y1), front, kind in fl.join:
        if kind in ("full", "base", "island"):
            jled += max(x1 - x0, y1 - y0) / 1000
    nsw = {1: 0, 2: 0, 3: 0}
    for x, y, g in SWITCHES[fl.key]:
        sym_switch(s, v.P(x, y), g)
        nsw[g] += 1
    tr = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in TRACKS[fl.key]) / 1000
    rows = [("dl", "RECESSED LED DOWNLIGHT\n(CRI98, 3000K, 24°/36°)", len(dls)),
            ("pd", "PENDANT LIGHT (BY OWNER)", len(PENDANTS[fl.key])),
            ("wl", "WALL LIGHT (BY OWNER)", len(WALL_LIGHTS[fl.key])),
            ("led", "LED STRIP AT COVE / L-BOX\n3000K (M RUN)", f"{led:.1f}M"),
            ("led", "LED STRIP IN JOINERY\n(SHELF / PLINTH) (M RUN, EST.)", f"{jled:.1f}M"),
            ("tr", "MAGNETIC TRACK LIGHT (M RUN)", f"{tr:.1f}M"),
            ("fan", "CEILING FAN (BY OWNER)", len(FANS[fl.key]))]

    def sym(sh, c, k):
        {"dl": sym_downlight, "pd": sym_pendant, "wl": sym_walllight, "led": sym_ledstrip, "tr": sym_track,
         "fan": lambda a, b: sym_fan(a, b, 2.6)}[k](sh, c)
    y = legend(s, "LEGEND (LIGHTING):", rows, symbol_fn=sym)
    legend(s, "LEGEND (SWITCHES):", [(1, "1 GANG LIGHT SWITCH", nsw[1]), (2, "2 GANG LIGHT SWITCH", nsw[2]),
                                     (3, "3 GANG LIGHT SWITCH", nsw[3])],
           y_top=y, symbol_fn=lambda sh, c, k: sym_switch(sh, (c[0] - 1, c[1] - 0.8), k))
    s.mtext("SMART LIGHTING (SCENE / DIMMING) BY M VIDA (AETHO).\\PFINAL SWITCH POSITIONS & GANGING TO SMART-HOME LAYOUT.",
            (LEG_X, 60), 1.7, 86, "I-NOTE", color=RED)
    return s, {"downlight": len(dls), "pendant": len(PENDANTS[fl.key]), "wall": len(WALL_LIGHTS[fl.key]),
               "led_cove_m": round(led, 1), "led_join_m": round(jled, 1), "fan": len(FANS[fl.key]), "switch": nsw}


def sheet_sockets(fl, number):
    s, v = new_plan_sheet(fl, number, "M&E PLAN - SOCKET")
    draw_base(v, fl.base_new)
    draw_join(v, fl, label=False)
    furniture(v, fl)
    room_labels(v, fl)
    cnt = {k: 0 for k, _ in SOCKET_LEGEND}
    for x, y, kind, note in SOCKETS[fl.key]:
        p = v.P(x, y)
        sym_socket(s, p, kind)
        s.text(note, (p[0] + 2.2, p[1] + 1.4), 1.05, "I-NOTE", "LEFT", color=RED)
        cnt[kind] += 1
    rows = [(k, t, cnt[k]) for k, t in SOCKET_LEGEND]
    legend(s, "LEGEND (SOCKET):", rows, symbol_fn=lambda sh, c, k: sym_socket(sh, c, k))
    s.mtext("ALL HEIGHTS FFL TO CENTRE OF FACEPLATE.\\PDB UPGRADE / NEW SUB-DB TO BE CONFIRMED AFTER LOAD CHECK.",
            (LEG_X, 112), 1.7, 86, "I-NOTE", color=RED)
    return s, cnt


TILE = {"T01": (900, 1800), "T02": (600, 1200), "T03": (750, 1500), "T04": (600, 1200)}
FLOOR_COLOR = {"T01": 5, "T02": 6, "T03": 4, "T04": 30, "W01": 3}


def sheet_floor(fl, number):
    s, v = new_plan_sheet(fl, number, "FLOOR FINISHES PLAN")
    draw_base(v, fl.base_new)
    areas = {}
    for name, rs in fl.rects.items():
        fin = next((r[3] for r in fl.rooms if r[0] == name), None)
        if fin in (None, "-", "EXIST"):
            continue
        for (x0, y0, x1, y1) in rs:
            areas[fin] = areas.get(fin, 0) + (x1 - x0) * (y1 - y0) / 1e6
            col = FLOOR_COLOR.get(fin, 8)
            if fin in TILE:
                tw, tl = TILE[fin]
                x = x0
                while x < x1:
                    v.line((x, y0), (x, y1), "I-FLOR", color=col); x += tw
                y = y0
                while y < y1:
                    v.line((x0, y), (x1, y), "I-FLOR", color=col); y += tl
            else:  # engineered wood planks
                y = y0
                k = 0
                while y < y1:
                    v.line((x0, y), (x1, y), "I-FLOR", color=col)
                    x = x0 + (k % 3) * 600
                    while x < x1:
                        v.line((x, y), (x, min(y + 190, y1)), "I-FLOR", color=col); x += 1800
                    y += 190; k += 1
            v.rect(x0, y0, x1, y1, "I-FLOR", color=col)
    room_labels(v, fl, with_finish="floor")
    names = {m[0]: m for m in D.MATERIALS}
    rows = []
    for fin in sorted(areas):
        m = names.get(fin)
        rows.append((fin, f"{m[2]} {m[3]}\n{m[4]}" if m else fin, f"{areas[fin] * 10.764:.0f} SF"))

    def sym(sh, c, k):
        x, y = c
        col = FLOOR_COLOR.get(k, 8)
        sh.rect(x - 5, y - 2.8, x + 5, y + 2.8, "I-FLOR", color=col)
        for i in (-2.5, 0, 2.5):
            sh.line((x + i, y - 2.8), (x + i, y + 2.8), "I-FLOR", color=col)
        sh.line((x - 5, y), (x + 5, y), "I-FLOR", color=col)
    legend(s, "LEGEND (FLOORING):", rows, symbol_fn=sym, row_h=8.0)
    s.mtext("FLOORING INTERFACE (TILES TO ENGINEERED WOOD):\\P- 100% FLUSH, ZERO DROP.\\P- FLEXIBLE L-SHAPE S/STEEL EDGE TRIM ALONG TILE BORDER INCL. CURVES."
            "\\P- 3MM EXPANSION GAP SEALED W/ ANTI-FUNGUS SILICONE MATCHING FLOOR COLOUR.\\PAREAS ARE ROUGH TAKE-OFF (EXCL. WASTAGE) - V.I.F.",
            (LEG_X, 150), 1.7, 86, "I-NOTE", color=RED)
    return s, {k: round(a * 10.764) for k, a in areas.items()}


FEATURE_WALLS = {
    "GF": [((3140, 17000), (3140, 21400), "P02"), ((12030, 12500), (13960, 12500), "L01"),
           ((9740, 21330), (14150, 21330), "T05"), ((14150, 16540), (14150, 21330), "T05"), ((9740, 15940), (14150, 15940), "T05"),
           ((11870, 27040), (14150, 27040), "T05"), ((14150, 22300), (14150, 27040), "T05")],
    "FF": [((80, 15100), (80, 20440), "P02"), ((-840, 3450), (-840, 6800), "P02"), ((10940, 1000), (10940, 6800), "P03")],
}


def sheet_wall(fl, number):
    s, v = new_plan_sheet(fl, number, "WALL FINISHES PLAN")
    draw_base(v, fl.base_new)
    draw_join(v, fl, label=False)
    room_labels(v, fl, with_finish="wall")
    for a, b, code in FEATURE_WALLS[fl.key]:
        col = {"P02": MAGENTA, "P03": CYAN, "T05": RED, "L01": GREEN}[code]
        v.line(a, b, "I-FINISH", color=col, lineweight=70)
        mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        v.mat_tag((mid[0] + (350 if a[0] == b[0] else 0), mid[1] + (0 if a[0] == b[0] else 300)), code, 1.6)
    rows = [("P01", "JOTUN EMULSION (TBC) - WHOLE UNIT\nINCL. EXISTING DOOR & FRAME", ""),
            ("P02", "SUZUKA LIMEWASH / TEXTURE (TBC)\nFEATURE WALL", ""),
            ("P03", "JOTUN WARM GREY (TBC)", ""),
            ("T05", "LIMESTONE JH12352GZ WALL TILE\n600x1200 STRUCTURED", ""),
            ("L01", "PL0242 BW OAK BACK PANEL (ALTAR)", "")]

    def sym(sh, c, k):
        x, y = c
        col = {"P01": 7, "P02": MAGENTA, "P03": CYAN, "T05": RED, "L01": GREEN}[k]
        sh.line((x - 5, y), (x + 5, y), "I-FINISH", color=col, lineweight=70)
    legend(s, "PAINT / WALL FINISH CODE LEGEND", rows, symbol_fn=sym, count=False, row_h=8.0)
    return s


def sheet_curtain(fl, number):
    s, v = new_plan_sheet(fl, number, "CURTAIN PLAN")
    draw_base(v, fl.base_new)
    draw_join(v, fl, label=False)
    furniture(v, fl)
    room_labels(v, fl)
    tot = {}
    for side, c, a, b, room in WINDOWS[fl.key]:
        typ = CURTAIN_TYPE.get(room, "SHEER")
        off = {"N": -150, "S": 150, "E": -150, "W": 150}[side]
        col = {"SHEER": MAGENTA, "DOUBLE": GREEN, "ROLLER": BLUE, "ROMAN": CYAN, "SHOJI": RED}[typ]
        if side in "NS":
            pts = [(x, c + off + (40 if i % 2 else -40)) for i, x in enumerate(range(int(a), int(b) + 1, 120))]
        else:
            pts = [(c + off + (40 if i % 2 else -40), y) for i, y in enumerate(range(int(a), int(b) + 1, 120))]
        v.poly(pts, "I-CURT", color=col)
        if typ == "DOUBLE":
            pts2 = [(p[0] + (off * 0.6 if side in "EW" else 0), p[1] + (off * 0.6 if side in "NS" else 0)) for p in pts]
            v.poly(pts2, "I-CURT", color=MAGENTA)
        tot[typ] = tot.get(typ, 0) + (b - a + 300) / 304.8
    rows = [("SHEER", "SHEER CURTAIN (MOTORISED)\nRIPPLE FOLD", f"{tot.get('SHEER', 0):.0f} FT"),
            ("DOUBLE", "DAY + NIGHT CURTAIN\n(MOTORISED, SINGAPORE PLEAT)", f"{tot.get('DOUBLE', 0):.0f} FT"),
            ("ROLLER", "ROLLER BLIND", f"{tot.get('ROLLER', 0):.0f} FT"),
            ("ROMAN", "ROMAN BLIND", f"{tot.get('ROMAN', 0):.0f} FT"),
            ("SHOJI", "SHOJI-STYLE PANEL / BLIND", f"{tot.get('SHOJI', 0):.0f} FT")]

    def sym(sh, c, k):
        x, y = c
        col = {"SHEER": MAGENTA, "DOUBLE": GREEN, "ROLLER": BLUE, "ROMAN": CYAN, "SHOJI": RED}[k]
        sh.poly([(x - 5 + i * 1.25, y + (0.6 if i % 2 else -0.6)) for i in range(9)], "I-CURT", color=col)
    legend(s, "LEGEND (CURTAIN / BLIND):", rows, symbol_fn=sym, row_h=8.0)
    s.mtext("WIDTHS INCLUDE 150MM OVERLAP EACH SIDE. HEIGHTS FROM CEILING / PELMET TO FFL+10MM. WINDOW SIZES V.I.F.",
            (LEG_X, 190), 1.7, 86, "I-NOTE", color=RED)
    return s, {k: round(t) for k, t in tot.items()}


def sheet_elev_code(fl, number):
    s, v = new_plan_sheet(fl, number, "ELEVATION CODE PLAN")
    draw_base(v, fl.base_new)
    draw_join(v, fl, label=True, codes=True)
    room_labels(v, fl)
    codes = []
    for code, lab, *_ in fl.join:
        if code not in [c for c, _ in codes]:
            codes.append((code, lab))
    rows = [(c, f"{c} - {lab}", "") for c, lab in codes]

    def sym(sh, c, k):
        sh.text(k, c, 2.0, "I-SYMB", "MIDDLE_CENTER", color=MAGENTA)
    legend(s, "ELEVATION CODE:", rows, symbol_fn=sym, count=False, row_h=5.6)
    return s
