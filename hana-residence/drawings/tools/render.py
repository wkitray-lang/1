"""Render a DXF modelspace (or layout) to PNG/PDF for preview. Usage: render.py in.dxf out.png [dpi] [layout]"""
import sys, ezdxf, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.config import Configuration, BackgroundPolicy, ColorPolicy
doc = ezdxf.readfile(sys.argv[1])
dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 150
fig = plt.figure(figsize=(16, 16)); ax = fig.add_axes([0, 0, 1, 1])
ctx = RenderContext(doc)
cfg = Configuration(background_policy=BackgroundPolicy.WHITE, color_policy=ColorPolicy.COLOR, lineweight_scaling=0.5)
lay = doc.layouts.get(sys.argv[4]) if len(sys.argv) > 4 else doc.modelspace()
Frontend(ctx, MatplotlibBackend(ax), config=cfg).draw_layout(lay, finalize=True)
fig.savefig(sys.argv[2], dpi=dpi)
