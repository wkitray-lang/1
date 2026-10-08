"""Import the mm-scaled source DXFs (converted from the AutoCAD PDF) into a View."""
from __future__ import annotations

import os
import ezdxf

SRC = os.path.join(os.path.dirname(__file__), "..", "..")

# source layer -> (target layer, mode)   mode: "fill" (solid hatch), "line"
MAP_GF_ORI = {
    "SRC-FILLSTROKE-000000": ("A-WALL", "fill"),
    "SRC-STROKE-000000": ("A-WALL", "line"),
    "SRC-FILLSTROKE-636466": ("A-WALL", "fill"),
    "SRC-STROKE-636466": ("A-WIND", "line"),
    "SRC-STROKE-767676": ("A-DOOR", "line"),
    "SRC-STROKE-808080": ("A-DOOR", "line"),
}
MAP_GF_NEW = {
    "SRC-FILLSTROKE-000000": ("A-WALL", "fill"),
    "SRC-STROKE-000000": ("A-WALL", "line"),
    "SRC-FILLSTROKE-636466": ("A-WALL", "fill"),
    "SRC-STROKE-636466": ("A-WIND", "line"),
    "SRC-STROKE-767676": ("A-DOOR", "line"),
    "SRC-STROKE-808080": ("A-DOOR", "line"),
    "SRC-FILLSTROKE-0000ff": ("A-WALL-NEW", "fill"),
}
MAP_FF_EXIST = {
    "SRC-FILLSTROKE-636466": ("A-WALL", "fill"),
    "SRC-FILLSTROKE-000000": ("A-WALL", "fill"),
    "SRC-STROKE-000000": ("A-WALL", "line"),
    "SRC-STROKE-636466": ("A-WIND", "line"),
}
MAP_FF_NEW = {
    "SRC-FILLSTROKE-636466": ("A-WALL", "fill"),
    "SRC-FILLSTROKE-000000": ("A-WALL", "fill"),
    "SRC-FILLSTROKE-4554a5": ("A-WALL-NEW", "fill"),
    "SRC-FILLSTROKE-727430": ("A-WALL-DEMO", "fill"),
    "SRC-STROKE-000000": ("A-WALL", "line"),
    "SRC-STROKE-636466": ("A-WIND", "line"),
}

FILES = {
    "gf_ori": ("src_gf_ori.dxf", MAP_GF_ORI),
    "gf_new": ("src_gf_new.dxf", MAP_GF_NEW),
    "ff_exist": ("src_ff_exist.dxf", MAP_FF_EXIST),
    "ff_new": ("src_ff_new.dxf", MAP_FF_NEW),
}

WALL_RGB = (77, 77, 77)
NEW_RGB = (69, 84, 165)
SEAL_RGB = (114, 116, 48)

_cache = {}


def _load(key):
    if key not in _cache:
        fn, _ = FILES[key]
        _cache[key] = ezdxf.readfile(os.path.join(SRC, fn))
    return _cache[key]


import math


def _dim_junk(doc):
    """Ids of source dimension lines / ticks / extension lines and long sheet-frame lines."""
    segs = []
    ticks = []
    junk = set()
    for e in doc.modelspace().query("LWPOLYLINE"):
        pts = [(x, y) for x, y in e.vertices()]
        if e.dxf.layer == "SRC-FILLSTROKE-000000" and 4 <= len(pts) <= 5:
            xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
            if max(xs) - min(xs) < 130 and max(ys) - min(ys) < 130:
                (ax, ay), (bx, by) = pts[0], pts[1]
                a = abs(math.degrees(math.atan2(by - ay, bx - ax))) % 90
                if 25 < a < 65:
                    ticks.append((sum(xs) / len(xs), sum(ys) / len(ys)))
                    junk.add(id(e))
            continue
        if e.dxf.layer != "SRC-STROKE-000000":
            continue
        if len(pts) == 2:
            segs.append((e, pts))
    for e, ((x0, y0), (x1, y1)) in segs:
        L = math.hypot(x1 - x0, y1 - y0)
        if 40 < L < 400:
            a = abs(math.degrees(math.atan2(y1 - y0, x1 - x0))) % 90
            if 30 < a < 60:
                ticks.append(((x0 + x1) / 2, (y0 + y1) / 2))
                junk.add(id(e))
    # SHX text glyphs exported as strokes: small shapes floating away from walls
    walls = []
    for e in doc.modelspace().query("LWPOLYLINE"):
        if e.dxf.layer.startswith("SRC-FILLSTROKE") and id(e) not in junk:
            xs = [p[0] for p in e.vertices()]; ys = [p[1] for p in e.vertices()]
            if max(xs) - min(xs) > 130 or max(ys) - min(ys) > 130:
                walls.append((min(xs), min(ys), max(xs), max(ys)))
    def far_from_walls(cx, cy, d=230):
        for x0, y0, x1, y1 in walls:
            if x0 - d < cx < x1 + d and y0 - d < cy < y1 + d:
                return False
        return True
    for e in doc.modelspace().query("LWPOLYLINE"):
        if e.dxf.layer not in ("SRC-STROKE-000000", "SRC-STROKE-636466"):
            continue
        xs = [p[0] for p in e.vertices()]; ys = [p[1] for p in e.vertices()]
        if max(xs) - min(xs) < 330 and max(ys) - min(ys) < 330:
            if far_from_walls((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2):
                junk.add(id(e))

    def near_tick(p, r=140):
        return any(abs(p[0] - t[0]) < r and abs(p[1] - t[1]) < r for t in ticks)
    for e, (a, b) in segs:
        if id(e) in junk:
            continue
        if near_tick(a) or near_tick(b):
            junk.add(id(e))
            continue
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if L > 16000:  # sheet / site frame
            junk.add(id(e))
    return junk


_junk = {}


def draw_base(view, key, clip=None, skip=lambda pts: False, wall_rgb=WALL_RGB):
    """Copy base geometry into view. clip=(x0,y0,x1,y1) model mm to keep."""
    doc = _load(key)
    _, mp = FILES[key]
    if key not in _junk:
        _junk[key] = _dim_junk(doc)
    junk = _junk[key]
    if clip is None:
        clip = (1100, 5400, 16800, 28800) if key.startswith("gf") else (-2400, -1600, 12800, 21800)
    for e in doc.modelspace().query("LWPOLYLINE"):
        if e.dxf.layer not in mp or id(e) in junk:
            continue
        lay, mode = mp[e.dxf.layer]
        pts = [(x, y) for x, y in e.vertices()]
        if clip and not all(clip[0] <= x <= clip[2] and clip[1] <= y <= clip[3] for x, y in pts):
            continue
        if skip(pts):
            continue
        if mode == "fill" and len(pts) >= 3:
            rgb = NEW_RGB if lay == "A-WALL-NEW" else SEAL_RGB if lay == "A-WALL-DEMO" else wall_rgb
            view.solid(pts, "A-WALL-FILL" if lay == "A-WALL" else lay, rgb=rgb)
        else:
            view.poly(pts, lay, close=e.closed)
