#!/usr/bin/env python3
"""Groo quotation sheet audit (first-pass, mechanical checks).

Input: JSON {"formulas": [[...]], "values": [[...]]} dumped from Google Sheets
get_values on range A1:L600 (formulas = valueRenderOption FORMULA).
Columns: C no., D description, E/F/G W/D/H or unit, H qty, I rate, J amount, K section sum.
"""
import csv, json, re, sys
from pathlib import Path

COL = {c: i for i, c in enumerate("ABCDEFGHIJKL")}
HERE = Path(__file__).resolve().parent.parent
TOL = 0.15  # rate deviation tolerance vs rate card

CHECKLIST = {
    "protection": "site protection", "clean": "final cleaning", "debris": "debris disposal",
    "scaffold": "scaffolding (double volume)", "waterproof": "waterproofing",
    "wastage": "tile supply incl. wastage", "skirting": "skirting", "threshold": "threshold",
    "cap-off": "cap-off removed bathroom", "garden tap": "garden tap", "curtain motor": "curtain motor point",
    "access panel": "ceiling access panel", "riser": "staircase riser", "nosing": "staircase nosing",
    "accessor": "cabinetry accessories PS", "project management": "project management",
    "discount": "discount", "full name": "signature Full Name / IC", "exclusion": "exclusions",
}


def cell(rows, r, c):
    row = rows[r] if r < len(rows) else []
    i = COL[c]
    return row[i] if i < len(row) else ""


def num(v):
    if v in ("", None):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).replace(",", "").replace("RM", "").strip()
    neg = s.startswith("(") and s.endswith(")")
    s = s.strip("()")
    try:
        return -float(s) if neg else float(s)
    except ValueError:
        return None


def load_rates():
    with open(HERE / "references" / "rate-card.csv", newline="") as f:
        return [r for r in csv.DictReader(f) if r["sell"]]


def main(path):
    data = json.load(open(path))
    F, V = data["formulas"], data["values"]
    n = max(len(F), len(V))
    red, amber = [], []

    # section headers: K holds =SUM(Jx:Jy)
    heads = []
    for r in range(n):
        m = re.match(r"=\s*SUM\(\s*J(\d+)\s*:\s*J(\d+)\s*\)", str(cell(F, r, "K")), re.I)
        if m:
            heads.append((r, int(m.group(1)), int(m.group(2))))
    tail = next((r for r in range(n) if re.search(r"project management|sub\s*total",
                                                    str(cell(V, r, "D")) + str(cell(V, r, "C")), re.I)), n)
    print(f"Sections found: {len(heads)}\n")
    for k, (r, a, b) in enumerate(heads):
        end = heads[k + 1][0] if k + 1 < len(heads) else tail
        rows_with_j = [x + 1 for x in range(r + 1, end) if num(cell(V, x, "J")) not in (None, 0)]
        outside = [x for x in rows_with_j if not a <= x <= b]
        name = str(cell(V, r, "D"))[:40]
        print(f"  row {r+1:>4} {name:<40} K={cell(V, r, 'K')}  range J{a}:J{b}")
        if outside:
            red.append(f"row {r+1} '{name}': SUM J{a}:J{b} misses rows {outside}")

    rates = load_rates()
    star_total = 0.0
    text_all = " ".join(str(cell(V, r, "D")) for r in range(n)).lower()
    for r in range(n):
        d = str(cell(V, r, "D"))
        h, i, j = num(cell(V, r, "H")), num(cell(V, r, "I")), num(cell(V, r, "J"))
        if "⭐" in d:
            star_total += j or num(cell(V, r, "K")) or 0
        if re.search(r"discount", d, re.I):
            k = num(cell(V, r, "K")) or j
            if k and k > 0:
                red.append(f"row {r+1}: discount is positive ({k}) — must be negative")
        if r >= tail:
            continue
        if h and i is not None and j is not None and abs(h * i - j) > 0.05:
            red.append(f"row {r+1}: J {j} != H×I {h*i:.2f}")
        if h and i in (None, 0) and d:
            amber.append(f"row {r+1}: qty {h} but no rate — {d[:50]}")
        if i and not h and d and not str(cell(F, r, "K")).startswith("="):
            amber.append(f"row {r+1}: rate {i} but no qty — {d[:50]}")
        fi = str(cell(F, r, "I"))
        if i and not fi.startswith("=") and i >= 1000:
            amber.append(f"row {r+1}: rate {i} typed as a number (cost not traceable) — {d[:50]}")
        if i:
            dl = d.lower()
            for rc in rates:
                if rc["keyword"] in dl:
                    s = float(rc["sell"])
                    if abs(i - s) / s > TOL:
                        amber.append(f"row {r+1}: rate {i} vs card {s} ({rc['keyword']}, {rc['source']}) — {d[:45]}")
                    break

    missing = [label for kw, label in CHECKLIST.items() if kw not in text_all]

    print("\n🔴 Structure / errors")
    print("\n".join("  - " + x for x in red) or "  none")
    print("\n🟡 Check")
    print("\n".join("  - " + x for x in amber) or "  none")
    print("\n🟡 Checklist keywords not found (verify manually)")
    print("\n".join("  - " + x for x in missing) or "  none")
    print(f"\n⭐ starred total: RM{star_total:,.2f}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
