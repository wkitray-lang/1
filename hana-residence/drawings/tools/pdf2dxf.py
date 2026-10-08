"""Convert one page of the AutoCAD-exported HANA PDF into a mm-scaled DXF.

Usage: python3 pdf2dxf.py <pdf> <page> <out.dxf> <gridA_y> <grid_ref_x> <x_ref_mm> <scale> <bbox x0,x1,y0,y1>
Coordinates: PDF unrotated (x,y) -> CAD X=(y-gridA_y)*s, Y=(x-grid_ref_x)*s + x_ref_mm
"""
import sys, pymupdf, ezdxf, json

pdf, pno, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
ya, xr, xref_mm, s = map(float, sys.argv[4:8])
bx0, bx1, by0, by1 = map(float, sys.argv[8].split(","))

def T(p):
    return ((p.y - ya) * s, (p.x - xr) * s + xref_mm)

def inbox(p):
    return bx0 <= p.x <= bx1 and by0 <= p.y <= by1

def layer_for(path):
    c = path.get("color"); f = path.get("fill")
    key = lambda v: "%02x%02x%02x" % tuple(int(round(x * 255)) for x in v) if v else "none"
    if f and not c:
        return "SRC-FILL-" + key(f)
    if f:
        return "SRC-FILLSTROKE-" + key(f)
    return "SRC-STROKE-" + key(c)

doc = ezdxf.new("R2018", setup=True)
doc.units = ezdxf.units.MM
msp = doc.modelspace()
page = pymupdf.open(pdf)[pno - 1]
stats = {}
for path in page.get_drawings():
    pts_all = []
    for it in path["items"]:
        if it[0] == "l": pts_all += [it[1], it[2]]
        elif it[0] == "c": pts_all += [it[1], it[4]]
        elif it[0] == "re": r = it[1]; pts_all += [r.tl, r.br]
        elif it[0] == "qu": q = it[1]; pts_all += [q.ul, q.lr]
    if not pts_all or not all(inbox(p) for p in pts_all):
        continue
    lay = layer_for(path)
    if lay not in doc.layers:
        rgb = path.get("fill") or path.get("color") or (0, 0, 0)
        L = doc.layers.add(lay)
        L.rgb = tuple(int(round(v * 255)) for v in rgb)
    stats[lay] = stats.get(lay, 0) + 1
    filled = path.get("fill") is not None
    # build polyline(s)
    poly = []
    def flush():
        global poly
        if len(poly) >= 2:
            if filled and len(poly) >= 3:
                h = msp.add_hatch(dxfattribs={"layer": lay})
                h.set_solid_fill(rgb=tuple(int(round(v * 255)) for v in path["fill"]))
                h.paths.add_polyline_path(poly, is_closed=True)
            if path.get("color") is not None or not filled:
                msp.add_lwpolyline(poly, dxfattribs={"layer": lay}, close=bool(path.get("closePath")))
        poly = []
    last = None
    for it in path["items"]:
        if it[0] == "l":
            a, b = T(it[1]), T(it[2])
            if last is None or abs(last[0]-a[0]) > 1 or abs(last[1]-a[1]) > 1:
                flush(); poly = [a]
            poly.append(b); last = b
        elif it[0] == "c":
            # flatten bezier
            p0, p1, p2, p3 = it[1], it[2], it[3], it[4]
            a = T(p0)
            if last is None or abs(last[0]-a[0]) > 1 or abs(last[1]-a[1]) > 1:
                flush(); poly = [a]
            for k in range(1, 9):
                t = k / 8
                x = (1-t)**3*p0.x + 3*(1-t)**2*t*p1.x + 3*(1-t)*t*t*p2.x + t**3*p3.x
                y = (1-t)**3*p0.y + 3*(1-t)**2*t*p1.y + 3*(1-t)*t*t*p2.y + t**3*p3.y
                poly.append(T(pymupdf.Point(x, y)))
            last = poly[-1]
        elif it[0] == "re":
            flush(); r = it[1]
            poly = [T(r.tl), T(r.tr), T(r.br), T(r.bl), T(r.tl)]; flush(); last = None
        elif it[0] == "qu":
            flush(); q = it[1]
            poly = [T(q.ul), T(q.ur), T(q.lr), T(q.ll), T(q.ul)]; flush(); last = None
    flush()
doc.saveas(out)
print(json.dumps(stats, indent=0))
