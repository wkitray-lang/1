"""Hana Residence quotation audit workbook (R2, after supplier prices). Run: python3 build_audit_r2.py <out.xlsx>"""
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

OUT = sys.argv[1]
CURRENT_TOTAL = 990075.16

HDR = PatternFill("solid", fgColor="3B3A36")
HFONT = Font(bold=True, color="FFFFFF")
RED = PatternFill("solid", fgColor="F8D7D3")
AMB = PatternFill("solid", fgColor="FCEBC7")
GRN = PatternFill("solid", fgColor="DDEFD9")
THIN = Side(style="thin", color="BBBBBB")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
PRIO_FILL = {"A": RED, "B": AMB, "C": GRN}

wb = Workbook()


def sheet(title, headers, widths):
    ws = wb.create_sheet(title)
    ws.append(headers)
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
        c = ws.cell(row=1, column=i)
        c.fill, c.font = HDR, HFONT
        c.alignment = Alignment(wrap_text=True, vertical="center")
    ws.freeze_panes = "A2"
    return ws


def finish(ws, money_cols=(), prio_col=None):
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
            c.border = BOX
            if c.column in money_cols and isinstance(c.value, (int, float)):
                c.number_format = '#,##0.00'
        if prio_col:
            p = row[prio_col - 1].value
            if p in PRIO_FILL:
                row[prio_col - 1].fill = PRIO_FILL[p]


# ---------------------------------------------------------------- 1. Missing / add items
# (section, item, qty, unit, rate, basis / where seen, priority)
# Priority A = clearly in 3D/drawings and not in quote; B = very likely, confirm; C = optional / provisional
ADD = [
    ("Wet Works", "PC Sum – tile MATERIAL for bathrooms x4 + powder, foyer, laundry floor/wall, wet kitchen wall (approx. 3,600 sqft incl. 10% wastage @ PC RM12/sqft, adjust upon final selection)", 3600, "sqft", 12.00,
     "Quote says 'TBC upon final selection' = currently RM0. Only Ling Hua Bai 900x1800 material is priced. Without a PC sum the client reads it as included.", "A"),
    ("Wet Works", "Laundry wall tiles – Dong Peng Limestone JH12352GZ 600x1200 structured (labour, prime coat, C2TE-S1, grout)", 180, "sqft", 35.00,
     "New Layout GF legend: red wall-tile lines along laundry walls (4310 + 2290). 3D laundry shows full-height wall tile. Not in quote.", "A"),
    ("Wet Works", "Wet kitchen wall tile – quantity top-up (take-off ~330 sqft vs 250 quoted)", 80, "sqft", 35.00,
     "Red wall lines 4670 + 5050 + 2118 mm x ~3.0 m height less openings.", "B"),
    ("Wet Works", "Parents Bath – hack, Mapei 223 waterproofing + 72h ponding test, floor & wall tiling 750x1500", 280, "sqft", 35.00,
     "3D p.42 Parent's Bath fully redone. Quote has no Parents Bath. CHECK: if the 'First Floor Bathroom' line was meant to be Parents Bath, rename it instead of adding.", "A"),
    ("Wet Works", "Parents Bath – 6\" floor trap", 2, "nos", 137.14, "As other bathrooms.", "A"),
    ("Wet Works", "Staircase risers & nosing (Porter quote covers treads only) – PC sum", 1, "L/S", 3500.00,
     "Porter staircase RM13,000 + install RM3,000 = steps only. Risers / nosing / LED step light groove still open.", "A"),
    ("Wet Works", "Terrace 1, 2 & 3 – new floor finish after removal of existing wood decking (approx. 315 sqft)", 315, "sqft", 28.00,
     "Demolition line says 'remove ... wood decking' but no reinstatement. Confirm finish with client (outdoor tile / composite decking).", "B"),
    ("Ceiling", "Ceiling quantity top-up: FF corridor & stair, powder, utility, maid room, + under-measured rooms (master, WIC, son, daughter)", 1000, "sqft", 6.00,
     "Quote ceiling total 2,799 sqft. Rough take-off: Master ~410 (quoted 300), WIC ~320 (190), Son ~310 (180), Daughter ~280 (130), Corridor ~215 (0). If partial ceiling intended, write 'partial' in description.", "B"),
    ("Ceiling", "Moisture-resistant ceiling – Parents, Son's & Daughter's bathrooms, powder room", 140, "sqft", 7.00,
     "Only Master Bath has ceiling. 3D shows LED pelmet ceilings in all bathrooms.", "A"),
    ("Ceiling", "Air-cond linear grille cut-out / access panel 600x600", 10, "nos", 150.00,
     "3D shows linear diffusers (living, dining, family area, master) – ducted AC needs openings & access panels even if AC is by owner's vendor.", "B"),
    ("Ceiling", "Curved arch / curved wall-to-ceiling transition at staircase & corridor", 2, "nos", 1200.00,
     "3D p.4-7, p.37 curved arch openings.", "B"),
    ("Preliminaries", "Scaffolding for double-volume void (ceiling, painting, curtain track & pendant installation)", 1, "L/S", 3500.00,
     "Living/dining void approx. 6-7 m height. Ceiling and painting rates assume normal height.", "A"),
    ("Preliminaries", "Final chemical cleaning, approx. 5,700 sqft built-up", 1, "L/S", 3800.00,
     "Not in quote. QS matrix: post-reno cleaning RM600-1,200 for condo → landed 5,700 sqft scale up.", "A"),
    ("Preliminaries", "Contractor All-Risk insurance (approx. 0.25% of contract)", 1, "L/S", 2500.00,
     "Optional but recommended for RM1M job.", "C"),
    ("Joinery", "Foyer / Living divider – full-height framed screen c/w indoor planter box, pebbles & concealed lighting", 1, "nos", 8500.00,
     "3D p.8-12 & plan label 'DIVIDER'. Not in quote.", "A"),
    ("Joinery", "Second hidden door (flush with wall panelling, concealed hinges & push latch) @ Utility / Powder", 1, "nos", 4500.00,
     "3D plan labels 'HIDDEN DOOR' x2. Quote only covers the Dry Kitchen one.", "A"),
    ("Joinery", "Maid room tatami platform c/w storage", 1, "nos", 2800.00,
     "Plan label 'TATAMI W/ STORAGE' at maid room. Quote has wardrobe + headboard only.", "B"),
    ("Joinery", "Parents Bath – floating vanity cabinet", 1, "nos", 2800.00, "3D p.43.", "A"),
    ("Joinery", "Parents Bath – tall storage cabinet (dark fluted door)", 1, "nos", 3200.00, "3D p.43 right side.", "A"),
    ("Joinery", "Son's & Daughter's Bath – floating vanity cabinet", 2, "nos", 2600.00, "3D p.73, p.78.", "A"),
    ("Joinery", "Parents, Son's & Daughter's Bath – mirror cabinet c/w LED", 3, "nos", 1200.00, "3D shows mirror cabinets in all three.", "A"),
    ("Joinery", "Powder room – vanity / stone pedestal basin base & mirror", 1, "L/S", 3000.00, "3D p.44.", "B"),
    ("Joinery", "Staircase side wall – full-height V-groove feature panelling", 1, "L/S", 8500.00, "3D p.37-38. Confirm extent with YS.", "B"),
    ("Joinery", "Master Bath – open-shelf tall storage unit", 1, "nos", 3500.00, "3D master bath (right side timber shelving).", "C"),
    ("Table Top", "Dry Kitchen island – top-up for 900mm depth + waterfall ends (≈44 sqft sintered @ RM140/sqft vs 10ft x RM280 quoted)", 1, "L/S", 3400.00,
     "Per-ft rate assumes 600mm depth. Island is 2800x900 with thick waterfall/curved end in 3D.", "A"),
    ("Table Top", "Vanity tops – Parents, Son's, Daughter's bath (sintered / quartz)", 12, "ft", 280.00, "3 vanities x ~4 ft.", "A"),
    ("Table Top", "Open hole – additional basins", 3, "nos", 150.00, "", "A"),
    ("Doors & Windows", "10mm tempered glass shower screen – Parents, Son's & Daughter's bath", 3, "nos", 1800.00,
     "Only Master Bath screen quoted. 3D shows glass screens in all.", "A"),
    ("Doors & Windows", "Existing doors – refurbish / laminate to match new palette c/w new black lever handles (approx. 10 leaves)", 10, "nos", 650.00,
     "3D shows flush doors with black handles everywhere. No door painting/refurb in Painting either. Confirm door schedule.", "B"),
    ("Doors & Windows", "Glass balustrade (12mm laminated tempered) c/w timber handrail @ staircase & void edge – IF replacing existing", 46, "ft", 450.00,
     "3D p.38-42 frameless glass + timber rail. Confirm whether existing balustrade stays.", "B"),
    ("Electrical", "32A dedicated point for induction hob (from DB)", 1, "nos", 650.00, "Induction hob cannot run on 15A.", "A"),
    ("Electrical", "Additional 15A points – water heaters x4, dishwasher, wine chiller (quote has only 6 nos)", 6, "nos", 350.00,
     "4 bathrooms with rain showers + oven + dryer + dishwasher + wine chiller = ~12 heavy points.", "A"),
    ("Electrical", "PROVISIONAL – DB upgrade / new sub-DB for smart home & added load (replace 'TBC')", 1, "L/S", 4500.00,
     "KNX + 18 curtain motors + cinema + heavy appliances. 'TBC' = RM0 today.", "B"),
    ("Electrical", "LED step-light points @ staircase", 10, "nos", 160.00, "3D p.38.", "B"),
    ("Electrical", "Exhaust fan points – powder room & bathrooms", 4, "nos", 200.00, "", "C"),
    ("Plumbing", "Water heater installation labour (unit by owner)", 4, "nos", 180.00, "", "A"),
    ("Plumbing", "PROVISIONAL – concealed piping re-route for new vanity positions @ Parents, Son's, Daughter's bath", 3, "nos", 1200.00,
     "Quote assumes 'reinstall' only. 3D vanity/shower positions differ from existing.", "B"),
    ("Curtains", "Family Area – full-height sheer + night curtain (over-height)", 14, "ft", 160.00, "3D p.41-44 sheer curtains. Not in quote.", "A"),
]

ws = sheet("1 Missing Items", ["#", "Section", "Item to add", "Qty", "Unit", "Suggested sell rate (RM)", "Amount (RM)", "Why / where seen", "Priority"],
           [4, 14, 60, 8, 7, 12, 13, 60, 8])
for i, (sec, item, q, u, r, why, p) in enumerate(ADD, 1):
    ws.append([i, sec, item, q, u, r, round(q * r, 2), why, p])
n = len(ADD) + 1
ws.append([])
ws.append(["", "", "TOTAL – Priority A", "", "", "", f'=SUMIF(I2:I{n},"A",G2:G{n})'])
ws.append(["", "", "TOTAL – Priority B", "", "", "", f'=SUMIF(I2:I{n},"B",G2:G{n})'])
ws.append(["", "", "TOTAL – Priority C", "", "", "", f'=SUMIF(I2:I{n},"C",G2:G{n})'])
ws.append(["", "", "TOTAL – all", "", "", "", f"=SUM(G2:G{n})"])
for r in range(n + 2, n + 6):
    ws.cell(row=r, column=3).font = Font(bold=True)
    ws.cell(row=r, column=7).font = Font(bold=True)
    ws.cell(row=r, column=7).number_format = '#,##0.00'
finish(ws, money_cols=(6, 7), prio_col=9)

add_A = sum(q * r for _, _, q, _, r, _, p in ADD if p == "A")
add_B = sum(q * r for _, _, q, _, r, _, p in ADD if p == "B")
add_C = sum(q * r for _, _, q, _, r, _, p in ADD if p == "C")

# ---------------------------------------------------------------- 2. Quantity check
QTY = [
    ("Wet Works", "Ling Hua Bai labour (FIXED in R2)", 1313, 1303, "sqft", 37.14,
     "Now = Dong Peng take-off 122 sqm. Drawing R0: T01 1,094 + Foyer 209 = 1,303 sqft. OK."),
    ("Wet Works", "Ling Hua Bai material (FIXED in R2)", 91, 91, "pcs", 330.00,
     "Dong Peng: 91 pcs @ RM250 incl. 20% wastage. Sell RM330 -> ~20% margin after est. logistics/unloading."),
    ("Wet Works", "Foyer finish – Bellezza line reduced to Entrance 45 sqft", 45, 45, "sqft", 35.00,
     "R2 follows Dong Peng (Foyer = Ling Hua Bai). DWG 02/10 legend says Foyer = Bellezza -> CONFIRM with YS/client before PO."),
    ("Wet Works", "Wet kitchen wall tile", 250, 330, "sqft", 35.00, "Still under – see Missing Items."),
    ("Wet Works", "'First Floor Bathroom' tiling (331 sqft + traps + mitre)", 331, 0, "sqft", 35.00,
     "Still open: FF has only Master, Son's & Daughter's bath. Probably Parents Bath (GF) – rename, don't double count."),
    ("Flooring", "Engineering wood (FIXED in R2 to Porter area)", 1647, 1880, "sqft", 39.00,
     "Porter area 1,647 sqft vs drawing R0 ~1,880 (FF 1,809 incl. walls + Parents 215). Ask Porter for room breakdown."),
    ("Wet Works", "Levelling screed (FIXED in R2)", 1647, 1647, "sqft", 5.00, "Matches wood area."),
    ("Ceiling", "Total plaster ceiling", 2799, 3800, "sqft", 6.00, "Still under – see Missing Items."),
    ("Preliminaries", "Rorobin 6 trips", 6, 0, "trip", 350.00,
     "Demolition L/S already says 'incl. Rorobin disposal'. Reword as additional trips or remove."),
    ("Wet Works", "45° mitre corner – unit shown as 'inch'", 251, 251, "inch→ft?", 37.14, "Change unit label to 'ft'."),
]
ws = sheet("2 Qty Check", ["Section", "Item", "Quoted qty", "My take-off", "Unit", "Rate", "Diff (RM)", "Note"],
           [14, 40, 11, 11, 9, 9, 12, 70])
for sec, item, q, t, u, r, note in QTY:
    diff = round((t - q) * r, 2) if isinstance(t, (int, float)) and "inch" not in u else 0
    ws.append([sec, item, q, t, u, r, diff, note])
finish(ws, money_cols=(6, 7))

# ---------------------------------------------------------------- 3. Rate / margin check
RATE = [
    ("Flooring", "Porter Art Deco E30 S&I RM39/sqft", "39.00", "36.59 (51,200+9,059)/1,647", "6% + 10% Porter commission", "25% (guide)",
     "Thin but low risk (supplier supplies & installs). Margin mostly from Porter's 10% commission (~RM5.8-6.4k, off-quote). Negotiate install to RM4.5 for +RM1.6k.", "B"),
    ("Flooring", "Staircase steps S&I RM18,000", "18,000", "16,000 (13,000+3,000)", "11% + commission", "25%", "Risers & nosing not included – see Missing Items.", "B"),
    ("Wet Works", "Ling Hua Bai material RM330/pc", "330.00", "250 + est. RM14 logistics/unloading", "~20%", "15-25% on material", "OK. Dong Peng logistics TBC; unloading excluded (45kg/pc).", "C"),
    ("Smart Home", "AETHO / M Vida package", "142,588.80", "142,588.80", "0%", "15-20%",
     "Passed through at vendor price – zero margin on 14.5% of contract, while Groo carries coordination, 3-month lead time, KNX programming risk. Add 15% (≈+RM21.4k) or let client contract AETHO directly + charge 8-10% coordination.", "A"),
    ("Project Management", "PM fee RM1.80/sqft", "9,900", "-", "~1% of contract", "5-8% (guide)",
     "RM9,900 on a RM1M, 6-month, 2-storey job with 10+ trades is thin. Suggest min 3% (~RM29k).", "A"),
    ("Ceiling", "9mm plaster ceiling RM6/sqft", "6.00", "3.60-5.00", "17-40%", "45%",
     "Matrix selling RM10. Move to RM7.50-8.00 (+RM4-6k).", "B"),
    ("Ceiling", "L-box LED RM28/ft", "28.00", "18-25", "11-36%", "45%", "Matrix selling RM50. Move to RM40.", "B"),
    ("Curtains", "Double-layer curtain RM135/ft", "135.00", "86-120", "11-36%", "25-35%",
     "Night 55-75 + day 28-42 + track 3. Move to RM150-160.", "B"),
    ("Joinery", "WIC wardrobe w/ black-frame glass doors RM991/ft", "991/ft", "750-900/ft?", "9-24%", "33%",
     "Alu-frame glass doors + LED cost more than melamine doors. Get carpenter price before sending.", "B"),
    ("Flooring", "Engineering wood RM22/sqft", "22.00", "14-20 (est.)", "10-35%", "25%",
     "Porter Rosewood 15-20mm – confirm supplier price incl. underlay & wastage.", "B"),
    ("Wet Works", "Rates like 37.14 / 53,064.29 / 12,285.71 / 137.14", "-", "-", "30% (cost/0.7)", "-",
     "Decimals show the client you priced cost ÷ 0.7. Round to 38.00, 53,100, 12,300, 140.00.", "B"),
    ("Joinery", "Kitchen wall cabinet with lift-up doors RM537/ft", "537/ft", "170-260 + lift-up fittings", "~30%", "33%",
     "Blum Aventos ~RM400-600 each. OK if hardware counted, else thin.", "C"),
]
ws = sheet("3 Rate & Margin", ["Section", "Item", "Quoted rate", "Subcon cost (QS matrix)", "Est. margin", "Target", "Comment", "Priority"],
           [14, 34, 12, 18, 14, 12, 70, 8])
for row in RATE:
    ws.append(list(row))
finish(ws, prio_col=8)

# ---------------------------------------------------------------- 4. Margin estimate by section
# (section, sell, est. cost) – cost estimated from QS matrix subcon ranges & the cost/0.7 pattern in the sheet
MARGIN = [
    ("Preliminaries", 4600, 3000), ("1.0 Ceiling", 37201, 26000), ("2.0 Painting", 24599, 17000),
    ("3.0 Demolition & Masonry / Wet Works", 258063.36, 183623), ("4.0 Plumbing", 9350, 6500),
    ("5.0 Electrical", 37470, 25000), ("6.0 Light Fittings & Fans", 2100, 1500), ("7.0 Doors & Windows", 12900, 9500),
    ("8.0 Joinery", 331650, 210000), ("9.0 Table Top", 21140, 15000), ("10.0 Flooring (Porter, incl. staircase)", 82233, 76259),
    ("11.0 Curtains & Blinds", 16280, 12000), ("12.0 Smart Home", 142588.80, 142588.80), ("Project Management", 9900, 5000),
]
ws = sheet("4 Margin Estimate", ["Section", "Quoted (RM)", "Est. cost (RM)", "Gross profit (RM)", "GP %"], [36, 15, 15, 16, 9])
for i, (s, sell, cost) in enumerate(MARGIN, 2):
    ws.append([s, sell, cost, f"=B{i}-C{i}", f"=IF(B{i}=0,0,D{i}/B{i})"])
last = len(MARGIN) + 1
ws.append(["TOTAL", f"=SUM(B2:B{last})", f"=SUM(C2:C{last})", f"=B{last+1}-C{last+1}", f"=D{last+1}/B{last+1}"])
ws.append(["TOTAL excl. Smart Home", f"=B{last+1}-B14", f"=C{last+1}-C14", f"=B{last+2}-C{last+2}", f"=D{last+2}/B{last+2}"])
for r in range(2, last + 3):
    for c in (2, 3, 4):
        ws.cell(row=r, column=c).number_format = '#,##0'
    ws.cell(row=r, column=5).number_format = '0.0%'
for r in (last + 1, last + 2):
    for c in range(1, 6):
        ws.cell(row=r, column=c).font = Font(bold=True)
ws.append([])
ws.append(["Est. cost = my estimate from the QS Pricing Matrix subcon ranges, not actual supplier quotes. Replace with real subcon quotes as they come in."])
finish(ws)

# ---------------------------------------------------------------- 5. Drawing issues + missing sheets
DWG = [
    ("Title block", "GF sheets (ORI / DEMOLISHED / NEW LAYOUT PLAN-G) copyright says 'property of seb design studio'.", "Fix before sending – it's another firm's name. FF sheets are already correct.", "A"),
    ("Title block", "All 3 GF sheets titled 'FURNITURE LAYOUT PLAN (GROUND FLOOR)' regardless of content; Drawing No. blank on all 6 sheets; every sheet labelled 'ID 01'.", "Number them e.g. HR-ID-01…, title per content.", "A"),
    ("Title block", "'PROJECT TITILE' typo; dates 02/10 (GF) vs 1/10 (FF); drawn by YANXIANG vs YS.", "Align.", "C"),
    ("Plot", "GF Demolished Layout Plan is rotated 90° and clipped – Breakfast/Dining left side and Parents Room are cut off the sheet.", "Re-plot to fit A3.", "A"),
    ("Scale", "Every sheet 'NOT TO SCALE'.", "Plot at 1:100 on A3 so contractors (and we) can measure off the PDF.", "B"),
    ("Content", "GF New Layout has no wall legend (new wall / wall to hack / hidden doors / divider).", "Add as per FF legend; the kitchen–dining wall is hacked in the demolition plan.", "A"),
    ("Content", "FF Demolition Plan doesn't mark Son's (Bath 2) & Daughter's (Bath 1) bathrooms for hacking, but the 3D and the quote redo them.", "Decide scope: if redoing, add hatch; if not, remove from quote (≈RM29.7k tiling + plumbing).", "A"),
    ("Content", "Wet Kitchen Option 1 (curved island + glass sliding doors) vs Option 2 – quote only prices Option 1.", "Show Option 2 as an alternative / deduction line so client sees the choice.", "B"),
    ("Content", "Master Bedroom Opt 2 (twin columns) – quote merges into TV divider.", "Confirm which option.", "C"),
    ("Missing sheet", "Reflected Ceiling Plan GF & FF (levels, coves, Ø coffers, pelmets, AC grilles, access panels).", "Drives Ceiling qty (≈RM37-50k).", "A"),
    ("Missing sheet", "Lighting layout (coordinate AETHO: 118 downlights, tracks, linear, 246 m strip, pendants, wall lights).", "Drives electrical points + smart home scope.", "A"),
    ("Missing sheet", "Power & data point layout (13A, 15A, 32A, data, TV, AC isolator, fireplace, curtain motors).", "Drives Electrical qty.", "A"),
    ("Missing sheet", "Plumbing layout (inlet/outlet, floor trap, heater, island sink, laundry).", "", "B"),
    ("Missing sheet", "Floor finishes plan with area schedule (sqft per finish).", "Locks flooring & tile quantities.", "A"),
    ("Missing sheet", "Wall finishes plan + bathroom / wet kitchen tile elevations.", "Locks wall tile quantities.", "B"),
    ("Missing sheet", "Cabinetry elevations & sections per item (W x D x H, materials, hardware).", "Basis for the W/D/H columns in quote and for carpenter pricing.", "A"),
    ("Missing sheet", "Door & window schedule (new / hidden / refurbish / sealed).", "", "B"),
    ("Missing sheet", "Staircase & balustrade detail.", "", "B"),
    ("Missing sheet", "Curtain & blind schedule (location, type, width, height, motorised).", "", "C"),
]
ws = sheet("5 Drawing Issues", ["Type", "Issue", "Action", "Priority"], [14, 80, 55, 8])
for row in DWG:
    ws.append(list(row))
finish(ws, prio_col=4)

# ---------------------------------------------------------------- 6. Questions to confirm
QS = [
    ("Client", "Son's & Daughter's bathrooms – full redo (as 3D) or keep existing tiles?"),
    ("Client", "Maid Bath – any works? (Not in 3D, not in quote.)"),
    ("Client", "Terraces – what finish after decking removal?"),
    ("Client", "Existing glass balustrade at void/stair – keep or replace?"),
    ("Client", "Wet Kitchen Option 1 or 2? Master Bedroom option 1 or 2?"),
    ("Client", "Who supplies kitchen sinks/taps, hood/hob/oven, water heaters, fireplace unit?"),
    ("Client", "Smart home – contract through Groo (with markup) or directly with AETHO?"),
    ("Internal", "Unit size: quote uses 5,500 sqft, fee proposal says 5,745 sqft – which is correct?"),
    ("Internal", "Company address: quote header '143 Jln Desa Utama, Taman Danau Desa' vs fee proposal 'Level 3A, Wisma JAG, Taman Desa'."),
    ("Internal", "Quote date shows '10/8/2026' – print as '08 Oct 2026' to avoid being read as 10 Aug."),
    ("Internal", "Is the design fee (Fee Proposal 261026) billed separately? Quote has no design fee line."),
    ("Internal", "Payment terms: AETHO likely needs ~50% upfront for imported items – add a separate smart-home deposit so Groo isn't funding it."),
    ("Internal", "Add an explicit EXCLUSIONS block: aircond, loose furniture, appliances, sanitary ware, decorative lights, fireplace, artwork/plants, landscape/turfing, gate, permits & JMB deposits."),
]
ws = sheet("6 Questions", ["For", "Question"], [10, 110])
for row in QS:
    ws.append(list(row))
finish(ws)

# ---------------------------------------------------------------- 7. Supplier quotes
SUP = [
    ("Dong Peng (DP Ceramic)", "09/10/2026", "Ling Hua Bai 900x1800x9 honed, 91 pcs @ RM250", 22750, "30,030 (91 @ RM330)",
     "Logistics TBC, unloading excl., 50% non-refundable deposit, 12-wk production (7-9 wk back-to-back), valid to 08/11/2026"),
    ("Porter Rosewood", "09/10/2026", "Art Deco E30 straight plank 1,647 sqft (incl. skirting, quarter round, adhesive, protection)", 51200,
     "64,233 incl. install (1,647 @ RM39)", "Includes 10% designer commission. Area breakdown TBC."),
    ("Porter Rosewood (installer est.)", "10/10/2026", "Glue-down install 1,647 sqft @ RM5.5", 9059, "(in RM39/sqft)", "Market rate RM5+; negotiable"),
    ("Porter Rosewood", "09/10/2026", "Staircase steps 1.2mm top layer, GF-1F", 13000, "18,000 incl. install", "Steps only"),
    ("Porter Rosewood (installer est.)", "10/10/2026", "Staircase install", 3000, "(in 18,000)", "RM2-3k+ per set"),
    ("M Vida (AETHO)", "13/09/2026", "Smart home package", 142588.80, "142,588.80 (0% markup)", "3-month lead time for imported items"),
]
ws = sheet("7 Supplier Quotes", ["Supplier", "Date", "Item", "Cost (RM)", "Quoted to client", "Notes"], [24, 11, 52, 13, 26, 60])
for row in SUP:
    ws.append(list(row))
finish(ws, money_cols=(4,))

# ---------------------------------------------------------------- 0. Summary (first sheet)
qty_over = 0
smart_15 = 142588.80 * 0.15
ws = wb.active
ws.title = "0 Summary"
ws.column_dimensions["A"].width = 70
ws.column_dimensions["B"].width = 18
rows = [
    ("HANA RESIDENCE – QUOTATION AUDIT R2 (after Dong Peng + Porter Rosewood prices, 10 Oct 2026)", None),
    ("Quotation 261015 after R2 price update (Grand Total)", CURRENT_TOTAL),
    ("Previous total R1 (09 Oct)", 980113.34),
    ("Est. gross margin of R2 (see sheet 4; excl. Porter 10% commission)", "≈26.0%  (≈30.3% excl. smart home)"),
    ("", None),
    ("A. Missing items – Priority A (still open)", round(add_A, 2)),
    ("B. Missing items – Priority B (very likely, confirm)", round(add_B, 2)),
    ("C. Missing items – Priority C (optional/provisional)", round(add_C, 2)),
    ("D. Smart home 15% markup (recommended, still 0%)", round(smart_15, 2)),
    ("E. 'First Floor Bathroom' if it's a phantom (not Parents Bath)", -13419.16),
    ("", None),
    ("Revised total – A + D", round(CURRENT_TOTAL + add_A + smart_15, 2)),
    ("Revised total – A + B + D", round(CURRENT_TOTAL + add_A + add_B + smart_15, 2)),
    ("", None),
    ("R2 changes made in the Google Sheet: Ling Hua Bai labour 2000->1313 sqft; material 139.2 pcs@280 -> 91 pcs@330 (Dong Peng); Bellezza Foyer+Entrance 270 -> Entrance 45 sqft; "
     "screed 1230->1647 sqft; wood flooring -> Porter Art Deco E30 S&I 1647 sqft @39 (skirting incl.); staircase steps S&I RM18,000 added. Net +RM9,962. "
     "Backup of R1 kept in tab 'Hana Sheon & Tee - BACKUP R1 (09 Oct)'.", None),
]
for a, b in rows:
    ws.append([a, b])
ws["A1"].font = Font(bold=True, size=13)
for r in range(2, 15):
    if isinstance(ws.cell(row=r, column=2).value, (int, float)):
        ws.cell(row=r, column=2).number_format = '#,##0.00'
for r in (13, 14):
    ws.cell(row=r, column=1).font = Font(bold=True)
    ws.cell(row=r, column=2).font = Font(bold=True)
ws["A16"].alignment = Alignment(wrap_text=True, vertical="top")
ws.row_dimensions[16].height = 110

wb.save(OUT)
print(f"A={add_A:,.2f}  B={add_B:,.2f}  C={add_C:,.2f}  smart15={smart_15:,.2f}  qty_over={qty_over:,.2f}")
print(f"min fix total = {CURRENT_TOTAL + add_A + smart_15 - qty_over:,.2f}")
print(f"A+B total     = {CURRENT_TOTAL + add_A + add_B + smart_15 - qty_over:,.2f}")
