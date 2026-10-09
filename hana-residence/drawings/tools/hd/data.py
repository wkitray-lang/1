"""Hana Residence design data (model mm).

Sources: wall geometry from the AutoCAD PDF (HANA RESIDENCE DWG 01-02/10/2026),
layout from FLP 30/07/2026 + site-measured handwritten dims, design intent from
3D PROPOSAL R1.  Everything here is R0 for designer verification (V.I.F.).

Coordinate systems
  GF: X=0 at grid A, Y=0 at grid 10 (developer grid, see GRID_GF).
  FF: X=0 at FF grid A, Y=0 at FF grid 8 (see GRID_FF).
Joinery rect = (x0, y0, x1, y1, front) where front is the side doors face: N/S/E/W.
"""

# ------------------------------------------------------------------ grids
GRID_GF = {
    "x": [("A", 0), ("B", 3060), ("C", 7754), ("D", 9654), ("E", 11784), ("F", 15070), ("G", 18095)],
    "y": [("10", 0), ("9", 3170), ("8", 6927), ("7", 8285), ("6", 12655), ("5", 15860),
          ("4", 21520), ("3", 23743), ("2", 27150), ("1", 30187)],
}
GRID_FF = {
    "x": [("A", 0), ("B", 3890), ("C", 5670), ("D", 7140), ("E", 11130)],
    "y": [("8", 0), ("7", 3696), ("6", 6728), ("5", 9850), ("4", 11545), ("3", 15015),
          ("2", 17261), ("1", 20608)],
}

# plan windows (model) to show on each sheet: x0, y0, x1, y1
CLIP_GF = (1500, 5800, 16400, 28400)
CLIP_FF = (-2000, -1200, 12400, 21400)

# ------------------------------------------------------------------ rooms
# name, label xy, ceiling level (CL) mm, floor finish code, wall paint code
ROOMS_GF = [
    ("ENTRANCE", (12650, 7550), "CL 3000", "T02", "P01"),
    ("FOYER", (13000, 10400), "CL 3300", "T02", "P01"),
    ("LOUNGE", (5600, 9600), "CL 3300", "T01", "P01"),
    ("LIVING", (5600, 14300), "VOID", "T01", "P01"),
    ("DINING", (4800, 19200), "CL 3600", "T01", "P01"),
    ("DRY KITCHEN", (7700, 20300), "CL 3600", "T01", "P01"),
    ("WET KITCHEN", (11950, 17200), "CL 3200", "T01", "P01"),
    ("POWDER ROOM", (11300, 15100), "CL 2600", "T04", "-"),
    ("UTILITY 2", (13950, 14300), "CL 2600", "T02", "P01"),
    ("LAUNDRY AREA", (12900, 24800), "CL 3000", "T02", "P01"),
    ("MAID ROOM", (10700, 23200), "CL 2800", "T02", "P01"),
    ("MAID BATH", (10700, 26100), "CL 2500", "EXIST", "-"),
    ("PARENT'S ROOM", (5800, 24300), "CL 3000", "W01", "P01"),
    ("PARENT'S BATH", (8700, 25300), "CL 2600", "T04", "-"),
    ("STAIRCASE", (12200, 13500), "-", "W01", "P01"),
]

ROOMS_FF = [
    ("MASTER BEDROOM", (2600, 18400), "CL 3000", "W01", "P02"),
    ("MASTER BATH", (9000, 18400), "CL 2600", "T03", "-"),
    ("WALK IN CLOSET", (7900, 13600), "CL 3000", "W01", "P01"),
    ("FAMILY AREA", (1500, 13300), "CL 3000", "W01", "P01"),
    ("VOID", (1500, 9300), "-", "-", "-"),
    ("CORRIDOR", (4650, 5200), "CL 3000", "W01", "P01"),
    ("STAIRCASE", (8200, 8400), "-", "W01", "P01"),
    ("DAUGHTER'S ROOM", (1700, 5200), "CL 2900", "W01", "P02"),
    ("DAUGHTER'S BATH", (430, 1700), "CL 2600", "T03", "-"),
    ("SON'S ROOM", (8300, 4600), "CL 2900", "W01", "P03"),
    ("SON'S BATH", (4650, 1300), "CL 2600", "T03", "-"),
]

# ------------------------------------------------------------------ joinery footprints
# code, label, rect(x0,y0,x1,y1), front, kind ('full','base','wall','tall','island','panel')
JOIN_GF = [
    ("CF01", "SHOE CABINET", (10860, 6960, 11440, 8160), "E", "full"),
    ("CF01", "BENCH", (13950, 7470, 14475, 8190), "W", "base"),
    ("CF02", "STORAGE", (9580, 11930, 10660, 12500), "S", "full"),
    ("CF02", "TALL UNIT", (10660, 11930, 11410, 12500), "S", "full"),
    ("CF02", "TALL UNIT", (11410, 11930, 12030, 12500), "S", "full"),
    ("CF02", "ALTAR", (12030, 11930, 13960, 12500), "S", "base"),
    ("CF02", "HIDDEN DOOR", (13960, 12380, 14990, 12500), "S", "panel"),
    ("CF03", "TV FEATURE WALL", (3150, 12050, 9300, 12500), "N", "full"),
    ("CF04", "STORAGE", (3150, 8360, 4600, 8760), "N", "base"),
    ("CF04", "PIANO NICHE", (4600, 8360, 5950, 8560), "N", "panel"),
    ("CF04", "STORAGE", (5950, 8360, 7650, 8760), "N", "base"),
    ("CF04", "FEATURE WALL", (7650, 8360, 9250, 8460), "N", "panel"),
    ("CF04", "KEY CONSOLE", (9250, 8360, 10680, 8760), "N", "base"),
    ("CF05", "HIDDEN DOOR PANEL", (4400, 21450, 5250, 22050), "S", "panel"),
    ("CF05", "TALL STORAGE", (5250, 21450, 6350, 22050), "S", "full"),
    ("CF05", "OPEN DISPLAY + DRAWER", (6350, 21450, 7850, 22050), "S", "full"),
    ("CF05", "DRINK COUNTER", (7850, 21450, 8700, 22050), "S", "full"),
    ("CF05", "TALL STORAGE", (8700, 21450, 9560, 22050), "S", "full"),
    ("CF06", "ISLAND", (5900, 19500, 8700, 20400), "S", "island"),
    ("CF09", "TALL UNIT / OVEN / REF", (9740, 20650, 12000, 21250), "S", "full"),
    ("CF08", "SINK BASE + WALL UNIT", (13550, 16540, 14150, 20650), "W", "base"),
    ("CF07", "HOB BASE + WALL UNIT", (9740, 15940, 14150, 16540), "N", "base"),
    ("CF10", "FOOD PREP ISLAND", (10900, 17700, 13000, 19250), "S", "island"),
    ("CF11", "WASHER & DRYER / BASE UNIT", (11870, 26450, 14140, 27040), "S", "base"),
    ("CF11", "BASE UNIT + HANGING ROD", (13550, 23350, 14140, 26000), "W", "base"),
    ("CF11", "STORAGE", (13550, 22300, 14140, 23350), "W", "full"),
    ("CF12", "LOW CABINET", (7250, 23700, 7690, 26150), "W", "base"),
    ("CF12", "OPEN WARDROBE", (9000, 22300, 9560, 23900), "W", "full"),
    ("CF13", "STORAGE CABINET", (9740, 21500, 11690, 22100), "N", "full"),
    ("CF13", "TATAMI W/ STORAGE", (9740, 22100, 10900, 24200), "E", "base"),
    ("CF14", "VANITY", (9740, 14500, 10400, 15300), "E", "base"),
]

JOIN_FF = [
    ("CF15", "HEADBOARD PANEL", (80, 16300, 330, 20000), "E", "panel"),
    ("CF15", "BEDSIDE", (330, 15800, 830, 16300), "E", "base"),
    ("CF15", "BEDSIDE", (330, 20000, 830, 20440), "E", "base"),
    ("CF16", "TV DIVIDER W/ FIREPLACE", (4600, 16400, 5050, 19400), "W", "full"),
    ("CF16", "MINI BAR", (5050, 16900, 5500, 18900), "E", "full"),
    ("CF17", "WARDROBE (GLASS DOOR)", (9550, 12050, 10140, 16550), "W", "full"),
    ("CF17", "WARDROBE", (5710, 12050, 6300, 16550), "E", "full"),
    ("CF17", "OPEN WARDROBE", (6300, 16000, 9550, 16550), "S", "full"),
    ("CF17", "ISLAND", (7300, 13300, 8800, 14100), "S", "island"),
    ("CF17", "DRESSING TABLE", (5710, 10010, 7500, 10510), "N", "base"),
    ("CF18", "DOUBLE VANITY", (10350, 17300, 10900, 19700), "W", "base"),
    ("CF19", "FEATURE WALL / PIANO", (-840, 11800, -440, 14900), "E", "full"),
    ("CF20", "WARDROBE", (5710, 5550, 10900, 6150), "S", "full"),
    ("CF20", "STUDY DESK + DISPLAY", (5710, 3200, 6310, 5400), "E", "base"),
    ("CF21", "WARDROBE", (-840, 6150, 2600, 6750), "S", "full"),
    ("CF21", "DRESSING / STUDY", (2600, 4200, 3640, 4800), "N", "base"),
    ("CF22", "VANITY", (-840, 2200, -340, 3300), "E", "base"),
    ("CF22", "VANITY", (3810, 2200, 4310, 3300), "E", "base"),
]

# ------------------------------------------------------------------ materials (AC.R3 style list)
MATERIALS = [
    # code, group, brand, description, finish, area
    ("M01", "MELAMINE", "PANEL PLUS", "69A OAK", "MELAMINE 16MM", "WHOLE AREA - CARCASS FRONT"),
    ("M02", "MELAMINE", "TOP MIX", "M1-1002DM COTTON WHITE", "MELAMINE 16MM", "FOYER / LIVING / DRY KITCHEN"),
    ("M03", "MELAMINE", "PANEL PLUS", "BX6 SUPER BLACK", "MELAMINE 16MM", "SON'S ROOM / LAUNDRY"),
    ("M04", "MELAMINE", "-", "INNER CARCASS WHITE", "MELAMINE 16MM", "ALL INNER CARCASS"),
    ("M05", "MELAMINE", "PANEL PLUS", "DARK OAK (TBC)", "MELAMINE 16MM", "ENTRANCE / LAUNDRY / MAID"),
    ("L01", "LAMINATE", "PANEL PLUS", "PL0242 BW OAK", "PLYWOOD + LAMINATE", "DRY KITCHEN / MASTER / M.BATH"),
    ("L02", "LAMINATE", "TOPMIX", "TS4-1017 M BLACK", "PLYWOOD + LAMINATE", "SON'S ROOM / LAUNDRY"),
    ("L03", "LAMINATE", "TOPMIX", "TS8-1251 VM IVORY WHITE", "PLYWOOD + LAMINATE", "LIVING / FOYER"),
    ("T01", "TILES", "DONG PENG", "LING HUA BAI 900x1800", "SINTERED STONE", "LIVING / DINING / KITCHEN FLOOR"),
    ("T02", "TILES", "BELLEZZA", "X-OLIVETTI X01 BLANCO 600x1200", "PORCELAIN", "FOYER / ENTRANCE / LAUNDRY"),
    ("T03", "TILES", "DONG PENG", "750x1500 (TBC)", "PORCELAIN", "FF BATHROOMS"),
    ("T04", "TILES", "DONG PENG", "AMAZON TRAVERTINE 600x1200 MATT", "PORCELAIN", "POWDER / PARENT'S BATH"),
    ("T05", "TILES", "DONG PENG", "LIMESTONE JH12352GZ 600x1200", "STRUCTURED", "WET KITCHEN / LAUNDRY WALL"),
    ("W01", "FLOORING", "PORTER", "ROSEWOOD ENGINEERED WOOD", "15-20MM", "PARENT'S ROOM / FIRST FLOOR"),
    ("S01", "STONE", "TBC", "SINTERED STONE 12MM", "SINTERED", "KITCHEN / VANITY TOPS"),
    ("P01", "PAINT", "JOTUN", "TBC (WARM WHITE)", "EMULSION MATT", "WHOLE UNIT"),
    ("P02", "PAINT", "SUZUKA", "TBC (LIMEWASH)", "TEXTURE", "MASTER / DAUGHTER FEATURE WALL"),
    ("P03", "PAINT", "JOTUN", "TBC (WARM GREY)", "EMULSION MATT", "SON'S ROOM"),
]

# ------------------------------------------------------------------ room rectangles (for hatch / lighting grid)
RECT_GF = {
    "ENTRANCE": [(10840, 6990, 13950, 8200)],
    "LOUNGE": [(3140, 8760, 9560, 11930)],
    "FOYER": [(9560, 8360, 14990, 11930)],
    "LIVING": [(3140, 12500, 9560, 16500)],
    "DINING": [(3140, 16500, 6300, 21450)],
    "DRY KITCHEN": [(6300, 16500, 9560, 21450)],
    "STAIRCASE": [(10790, 12650, 13950, 14340)],
    "POWDER ROOM": [(9730, 14500, 12720, 15780)],
    "UTILITY 2": [(12880, 12650, 14990, 15780)],
    "WET KITCHEN": [(9730, 15940, 14150, 21330)],
    "LAUNDRY AREA": [(11870, 21480, 14150, 27050)],
    "MAID ROOM": [(9730, 21480, 11700, 24980)],
    "MAID BATH": [(9730, 25150, 11700, 27050)],
    "PARENT'S ROOM": [(4040, 22200, 7690, 26200)],
    "PARENT'S BATH": [(7840, 23850, 9560, 26950)],
}
RECT_FF = {
    "MASTER BEDROOM": [(70, 15100, 7000, 20440)],
    "MASTER BATH": [(7050, 16750, 10950, 20000)],
    "WALK IN CLOSET": [(5710, 10000, 10140, 16600)],
    "FAMILY AREA": [(-840, 11700, 5550, 14950)],
    "VOID": [(-840, 6950, 3780, 11700)],
    "CORRIDOR": [(3800, 3900, 5550, 11700)],
    "STAIRCASE": [(5560, 6950, 10940, 9850)],
    "DAUGHTER'S ROOM": [(-840, 3450, 3650, 6800), (1750, 50, 3650, 3450)],
    "DAUGHTER'S BATH": [(-840, 50, 1700, 3400)],
    "SON'S BATH": [(3800, 50, 5550, 3750)],
    "SON'S ROOM": [(5710, 1000, 10940, 6800)],
}
