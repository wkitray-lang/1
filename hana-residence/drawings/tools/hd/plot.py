"""Plot sheet DXFs to A3 PDF pages (vector) and merge them into one set."""
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.config import (Configuration, BackgroundPolicy, ColorPolicy,
                                          LineweightPolicy, HatchPolicy)
from ezdxf.fonts import fonts

from .core import A3

# Arial is not installed here; Liberation Sans is metric-identical, so plot with it.
try:
    fonts.font_manager.add_synonyms({"arial.ttf": "LiberationSans-Regular.ttf",
                                     "arialn.ttf": "LiberationSansNarrow-Regular.ttf"}, reverse=False)
except Exception:  # older/newer ezdxf without add_synonyms
    pass

CFG = Configuration(
    background_policy=BackgroundPolicy.WHITE,
    color_policy=ColorPolicy.COLOR,
    lineweight_policy=LineweightPolicy.ABSOLUTE,
    lineweight_scaling=1.0,
    min_lineweight=0.12,
    hatch_policy=HatchPolicy.NORMAL,
)


def _swap_fonts(doc):
    """Plot with Liberation Sans (metric clone of Arial); restore names after."""
    saved = {}
    for st in doc.styles:
        f = (st.dxf.font or "").lower()
        if f in ("arial.ttf", "arialn.ttf"):
            saved[st.dxf.name] = st.dxf.font
            st.dxf.font = "LiberationSans-Regular.ttf" if f == "arial.ttf" else "LiberationSansNarrow-Regular.ttf"
    return saved


def plot(doc, pdf_path=None, png_path=None, dpi=150):
    saved = _swap_fonts(doc)
    W, H = A3
    fig = plt.figure(figsize=(W / 25.4, H / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ctx = RenderContext(doc)
    Frontend(ctx, MatplotlibBackend(ax), config=CFG).draw_layout(doc.modelspace(), finalize=False)
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_aspect("equal")
    ax.axis("off")
    if pdf_path:
        fig.savefig(pdf_path, format="pdf")
    if png_path:
        fig.savefig(png_path, dpi=dpi)
    plt.close(fig)
    for name, f in saved.items():
        doc.styles.get(name).dxf.font = f


def merge(pdfs, out):
    import pymupdf
    res = pymupdf.open()
    for p in pdfs:
        with pymupdf.open(p) as d:
            res.insert_pdf(d)
    res.save(out, deflate=True)
