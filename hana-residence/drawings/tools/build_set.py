"""Build the complete Hana Residence 2D working-drawing set (R0).

Outputs (in hana-residence/drawings/):
  HANA_RESIDENCE_2D_WORKING_DRAWINGS_R0.pdf   combined A3 set
  dxf/<sheet>.dxf                              one AutoCAD-openable DXF per sheet (paper mm, 1:1)
  quantities_R0.json                           counts read off the drawings (lights, sockets, areas, curtains)

Usage: python3 build_set.py [--png]
"""
import json
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.dirname(__file__))

from hd.plans import Floor
from hd import plans2 as P2
from hd.cabinets import build_sheet
from hd.cf_data import CABINETS
from hd.covers import drawing_list, material_list
from hd.plot import plot, merge

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DXF_DIR = os.path.join(OUT, "dxf")
PNG = "--png" in sys.argv


def slug(t):
    return re.sub(r"[^A-Z0-9]+", "_", t.upper()).strip("_")


def main():
    os.makedirs(DXF_DIR, exist_ok=True)
    gf, ff = Floor("GF"), Floor("FF")
    qty = {"GF": {}, "FF": {}}
    plan_specs = [
        ("ORI. LAYOUT PLAN", lambda fl, n: P2.sheet_ori(fl, n), None),
        ("WET WORK & DEMOLISH PLAN", lambda fl, n: P2.sheet_demolish(fl, n), None),
        ("FURNITURE LAYOUT PLAN", lambda fl, n: P2.sheet_furniture(fl, n), None),
        ("FURNITURE LAYOUT PLAN - DIMENSION", lambda fl, n: P2.sheet_flp_dim(fl, n), None),
        ("REFLECTED CEILING PLAN", lambda fl, n: P2.sheet_rcp(fl, n), "cove_m"),
        ("M&E PLAN - SOCKET", lambda fl, n: P2.sheet_sockets(fl, n), "sockets"),
        ("LIGHTING PLAN", lambda fl, n: P2.sheet_lighting(fl, n), "lighting"),
        ("WALL FINISHES PLAN", lambda fl, n: P2.sheet_wall(fl, n), None),
        ("FLOOR FINISHES PLAN", lambda fl, n: P2.sheet_floor(fl, n), "floor_sqft"),
        ("CURTAIN PLAN", lambda fl, n: P2.sheet_curtain(fl, n), "curtain_ft"),
        ("ELEVATION CODE PLAN", lambda fl, n: P2.sheet_elev_code(fl, n), None),
    ]
    jobs = []   # (number, description, group, builder)
    k = 1
    for title, fn, qkey in plan_specs:
        for fl in (gf, ff):
            num = f"ID.01.{k:02d}"
            jobs.append((num, f"{title} ({fl.name})", "ID.01  KEY DRAWING - PLANS", fl, fn, qkey))
            k += 1
    for c in CABINETS:
        grp = "ID.02  JOINERY - GROUND FLOOR" if c.sheet_no.startswith("ID.02") else "ID.03  JOINERY - FIRST FLOOR"
        jobs.append((c.sheet_no, f"{c.code} - {c.room} {c.title} ELEVATION", grp, c, None, None))
    sheet_index = [("ID.00.01", "TENDER DRAWING LIST", "ID.00  COVER"), ("ID.00.02", "MATERIAL LIST", "ID.00  COVER")]
    sheet_index += [(j[0], j[1], j[2]) for j in jobs]

    tmp = tempfile.mkdtemp()
    pdfs = []

    def emit(sheet, num, desc):
        name = f"{num}_{slug(desc)}"
        sheet.save(os.path.join(DXF_DIR, name + ".dxf"))
        pdf = os.path.join(tmp, name + ".pdf")
        plot(sheet.doc, pdf_path=pdf, png_path=os.path.join(tmp, name + ".png") if PNG else None, dpi=110)
        pdfs.append(pdf)
        print("  ", num, desc)

    emit(drawing_list(sheet_index), "ID.00.01", "TENDER DRAWING LIST")
    emit(material_list(), "ID.00.02", "MATERIAL LIST")
    for num, desc, grp, obj, fn, qkey in jobs:
        if fn is None:
            emit(build_sheet(obj), num, desc)
            continue
        r = fn(obj, num)
        sheet = r[0] if isinstance(r, tuple) else r
        if qkey and isinstance(r, tuple):
            qty[obj.key][qkey] = r[1]
        emit(sheet, num, desc)
    out_pdf = os.path.join(OUT, "HANA_RESIDENCE_2D_WORKING_DRAWINGS_R0.pdf")
    merge(pdfs, out_pdf)
    with open(os.path.join(OUT, "quantities_R0.json"), "w") as f:
        json.dump(qty, f, indent=2, default=str)
    print("PDF:", out_pdf, "sheets:", len(pdfs))
    print("PNG previews in", tmp if PNG else "(skipped)")


if __name__ == "__main__":
    main()
