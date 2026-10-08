"""Cover sheets: tender drawing list and material list (AC.R3 style tables)."""
from __future__ import annotations

from .core import Sheet, RED, A3, MARGIN, PROJECT
from . import data as D

SWATCH = {  # approximate colour of each material for the list
    "M01": (198, 160, 120), "M02": (238, 234, 224), "M03": (30, 30, 30), "M04": (245, 245, 245), "M05": (70, 55, 45),
    "L01": (190, 150, 110), "L02": (35, 35, 35), "L03": (240, 232, 214),
    "T01": (236, 232, 226), "T02": (226, 222, 214), "T03": (220, 210, 196), "T04": (214, 196, 170), "T05": (222, 210, 190),
    "W01": (160, 110, 70), "S01": (232, 228, 222), "P01": (246, 242, 234), "P02": (226, 214, 196), "P03": (170, 166, 160),
}


def table(s, x, y, widths, rows, header=None, row_h=4.6, h=1.75, fills=None):
    """Simple ruled table; returns bottom y."""
    if header:
        s.solid([(x, y - row_h), (x + sum(widths), y - row_h), (x + sum(widths), y), (x, y)], "0-TITLE", rgb=(200, 200, 200))
        cx = x
        for w, t in zip(widths, header):
            s.text(t, (cx + w / 2, y - row_h / 2), h, "0-TITLE-TXT", "MIDDLE_CENTER")
            cx += w
        y -= row_h
    for r in rows:
        if r is None:
            y -= row_h * 0.5
            continue
        if isinstance(r, str):  # section header
            s.solid([(x, y - row_h), (x + sum(widths), y - row_h), (x + sum(widths), y), (x, y)], "0-TITLE", rgb=(225, 225, 225))
            s.text(r, (x + 1.5, y - row_h / 2), h, "0-TITLE-TXT", "MIDDLE_LEFT")
            s.rect(x, y - row_h, x + sum(widths), y, "0-TITLE")
            y -= row_h
            continue
        cx = x
        for w, t in zip(widths, r):
            s.rect(cx, y - row_h, cx + w, y, "0-TITLE")
            s.text(str(t), (cx + 1.5, y - row_h / 2), h, "0-TITLE-TXT", "MIDDLE_LEFT")
            cx += w
        y -= row_h
    return y


def drawing_list(sheets):
    """sheets: list of (number, description, group)."""
    s = Sheet("ID.00.01", "TENDER DRAWING LIST", drawing_title="TENDER DRAWING LIST")
    W = A3[0]
    x0, ytop = 14, 286
    s.solid([(x0, ytop - 7), (x0 + 190, ytop - 7), (x0 + 190, ytop), (x0, ytop)], "0-TITLE", rgb=(170, 170, 170))
    s.text("TENDER DRAWING LIST", (x0 + 95, ytop - 3.5), 3.2, "0-TITLE-TXT", "MIDDLE_CENTER")
    info = [("PROJECT NAME", PROJECT["project"]), ("CLIENT NAME", PROJECT["client"]), ("PROJECT CODE", "GS26-HANA"),
            ("INTERIOR DESIGNER", PROJECT["designer"]), ("SALES PERSON", PROJECT["sales"]), ("REVISION", "R0 - 1ST DRAFT 09 OCT 2026")]
    y = ytop - 10
    for k, v in info:
        s.text(k, (x0 + 1, y), 1.9, "0-TITLE-TXT", "LEFT")
        s.text(": " + v, (x0 + 38, y), 1.9, "0-TITLE-TXT", "LEFT")
        y -= 4
    groups = []
    for num, desc, grp in sheets:
        if not groups or groups[-1][0] != grp:
            groups.append((grp, []))
        groups[-1][1].append((num, desc))
    rows_all = []
    for grp, items in groups:
        rows_all.append(grp)
        for num, desc in items:
            rows_all.append((num, desc, "R0", ""))
        rows_all.append(None)
    widths = [26, 120, 18, 26]
    half = (len(rows_all) + 1) // 2
    # split into two columns without breaking right after a header
    while half < len(rows_all) and isinstance(rows_all[half - 1], str):
        half += 1
    table(s, x0, y - 2, widths, rows_all[:half], header=["DRAWING NO.", "DESCRIPTION", "REV.", "REMARK"])
    table(s, x0 + 200, ytop, widths, rows_all[half:], header=["DRAWING NO.", "DESCRIPTION", "REV.", "REMARK"])
    s.sheet_tag("TENDER DRAWING LIST", "COVER", "ID", "00")
    return s


def material_list():
    s = Sheet("ID.00.02", "MATERIAL LIST", drawing_title="MATERIAL LIST")
    x0, ytop = 14, 286
    s.solid([(x0, ytop - 7), (x0 + 392, ytop - 7), (x0 + 392, ytop), (x0, ytop)], "0-TITLE", rgb=(170, 170, 170))
    s.text("HANA RESIDENCE MATERIAL LIST (SUPPLY & INSTALL BY GROO SPACE)", (x0 + 196, ytop - 3.5), 3.0, "0-TITLE-TXT",
           "MIDDLE_CENTER")
    groups = {}
    for m in D.MATERIALS:
        groups.setdefault(m[1], []).append(m)
    order = ["MELAMINE", "LAMINATE", "TILES", "STONE", "FLOORING", "PAINT"]
    colx = [x0, x0 + 198]
    ys = [ytop - 10, ytop - 10]
    widths = [14, 26, 18, 62, 76]
    for i, g in enumerate(order):
        c = 0 if ys[0] >= ys[1] else 1
        x, y = colx[c], ys[c]
        s.solid([(x, y - 5), (x + sum(widths), y - 5), (x + sum(widths), y), (x, y)], "0-TITLE", rgb=(180, 180, 180))
        s.text(g, (x + sum(widths) / 2, y - 2.5), 2.2, "0-TITLE-TXT", "MIDDLE_CENTER")
        y -= 5
        y = table(s, x, y, widths, [], header=["CODE", "BRAND", "REF", "DESCRIPTION", "AREA"], row_h=4.6)
        for m in groups.get(g, []):
            rh = 11
            cx = x
            for w in widths:
                s.rect(cx, y - rh, cx + w, y, "0-TITLE"); cx += w
            s.text(m[0], (x + 7, y - rh / 2), 2.2, "0-TITLE-TXT", "MIDDLE_CENTER")
            s.text(m[2], (x + 14 + 13, y - rh / 2), 1.7, "0-TITLE-TXT", "MIDDLE_CENTER")
            rgb = SWATCH.get(m[0], (200, 200, 200))
            sx = x + 14 + 26
            s.solid([(sx + 2, y - rh + 1.5), (sx + 16, y - rh + 1.5), (sx + 16, y - 1.5), (sx + 2, y - 1.5)], "0-TITLE", rgb=rgb)
            s.rect(sx + 2, y - rh + 1.5, sx + 16, y - 1.5, "0-TITLE")
            s.text(m[3], (sx + 18 + 31, y - rh / 2 + 1.4), 1.7, "0-TITLE-TXT", "MIDDLE_CENTER")
            s.text(m[4], (sx + 18 + 31, y - rh / 2 - 1.6), 1.5, "0-TITLE-TXT", "MIDDLE_CENTER", color=RED)
            s.text(m[5], (sx + 18 + 62 + 38, y - rh / 2), 1.45, "0-TITLE-TXT", "MIDDLE_CENTER")
            y -= rh
        ys[c] = y - 5
    s.text("ALL MATERIAL CODES TBC UPON CLIENT CONFIRMATION OF PHYSICAL SAMPLES.", (x0, s.draw_top + 4), 2.0, "I-NOTE",
           "LEFT", color=RED)
    s.sheet_tag("MATERIAL LIST", "COVER", "ID", "00")
    return s
