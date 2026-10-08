"""Joinery specifications (CF series) read from 3D PROPOSAL R1 + FLP 30/07 handwritten dims.

All sizes are R0 design sizes for verification on site (V.I.F.). Widths follow the
plan footprints in data.py so plan and elevation agree.
"""
from .cabinets import Cabinet, Col, Part as P

# ---------------------------------------------------------------- helpers
BASE_H, TOP_T = 760, 40          # base carcass height above plinth, worktop thickness


def kitchen_col(w, base="doors", n=2, wall="liftup", splash=700, cl_top=3180, plinth=100, label="", mat="M01",
                wall_mat="M01", top_mat="S01"):
    """Base + worktop + backsplash + wall cabinet + filler up to cl_top (above FFL)."""
    parts = []
    if base == "doors":
        parts.append(P(BASE_H, "doors", mat, n=n, shelves=1))
    elif base == "drawers3":
        parts += [P(220, "drawers", mat, n=1), P(250, "drawers", mat, n=1), P(290, "drawers", mat, n=1)]
    elif base == "sink":
        parts.append(P(BASE_H, "doors", mat, n=n, label="SINK"))
    elif base == "hob":
        parts += [P(300, "drawers", mat, n=1, label="HOB ABOVE"), P(460, "drawers", mat, n=1)]
    elif base == "dw":
        parts.append(P(BASE_H, "appliance", mat, label="DISHWASHER"))
    elif base == "washer":
        parts.append(P(BASE_H + 90, "appliance", mat, label=label or "WASHER"))
    parts.append(P(TOP_T, "counter", top_mat))
    used = plinth + sum(p.h for p in parts)
    if wall == "hood":
        parts.append(P(splash, "gap", "T05", label="BACKSPLASH T05"))
        parts.append(P(700, "appliance", wall_mat, label="COOKER HOOD"))
    elif wall == "window":
        parts.append(P(splash, "gap", "T05", label="WINDOW (EXISTING)"))
        parts.append(P(700, "liftup", wall_mat, shelves=1))
    elif wall == "open":
        parts.append(P(splash, "gap", "T05", label="BACKSPLASH T05"))
        parts.append(P(700, "open", wall_mat, shelves=1, led=True))
    else:
        parts.append(P(splash, "gap", "T05", label="BACKSPLASH T05"))
        parts.append(P(700, "liftup", wall_mat, shelves=1))
    used = plinth + sum(p.h for p in parts)
    if cl_top - used > 5:
        parts.append(P(cl_top - used, "panel", wall_mat))
    return Col(w, parts)


def full(w, h, kind="pair", mat="M02", shelves=5, **kw):
    return Col(w, [P(h, kind, mat, shelves=shelves, **kw)])


# ---------------------------------------------------------------- GROUND FLOOR
CABINETS = []

CABINETS.append(Cabinet(
    "CF01", "SHOE CABINET", "ENTRANCE", depth=580, cl=3000, plinth=180, plinth_kind="float", sheet_no="ID.02.01",
    cols=[Col(600, [P(1800, "door", "M05", shelves=6, hinge="L"), P(1000, "door", "M05", shelves=2, hinge="L")]),
          Col(600, [P(1800, "door", "M05", shelves=6, hinge="R"), P(1000, "door", "M05", shelves=2, hinge="R")])],
    details=["infill", "finger", "plinth"],
    notes=["SHOE CABINET 580MM DEEP (SITE MEASURE 1200 x 580).", "VENTILATION SLOT AT PLINTH, FLOATING LED 3000K.",
           "BENCH 525 x 755 OPPOSITE: SOLID TOP ON BLACK LEG (REFER 3D)."]))

CABINETS.append(Cabinet(
    "CF02", "ALTAR & STORAGE WALL", "FOYER", depth=570, cl=3300, plinth=120, sheet_no="ID.02.02",
    cols=[Col(1080, [P(1000, "pair", "M02", shelves=2), P(2160, "pair", "M02", shelves=4)]),
          full(750, 3160, "door", "M02", shelves=6, hinge="L"),
          Col(620, [P(3160, "niche", "L01", led=True, label="LED NICHE")]),
          Col(1930, [P(880, "doors", "M02", n=3, shelves=1), P(60, "counter", "S01"),
                     P(1500, "niche", "L01", led=True, label="ALTAR NICHE"), P(720, "panel", "M02")]),
          Col(1030, [P(3160, "panel", "M02", label="HIDDEN DOOR")])],
    details=["infill", "led", "hidden", "finger"],
    notes=["ALTAR NICHE BACK PANEL: PL0242 OAK C/W CONCEALED LED 3000K.", "HIDDEN DOOR TO UTILITY 2: FLUSH, CONCEALED HINGE, PUSH LATCH.",
           "ALTAR COUNTER SINTERED STONE 60MM (BUILT-UP EDGE)."]))

CABINETS.append(Cabinet(
    "CF03", "TV FEATURE WALL", "LIVING", depth=450, cl=3300, plinth=100, plinth_kind="float", sheet_no="ID.02.03",
    cols=[full(1100, 3180, "pair", "L03", shelves=6),
          Col(3950, [P(350, "drawers", "L03", n=3), P(150, "panel", "L01"), P(1650, "niche", "L01", led=True, label='85" TV (TBC)'),
                     P(1030, "doors", "L03", n=3, shelves=1)]),
          full(1100, 3180, "pair", "L03", shelves=6)],
    details=["infill", "finger", "led", "plinth"],
    notes=["TV RECESS BACKED WITH FLUTED OAK PANEL C/W LED COVE.", "CONCEALED CABLE TRUNKING TO CONSOLE.",
           "SOUND BAR / AV EQUIPMENT IN CONSOLE - VENTILATED BACK."]))

CABINETS.append(Cabinet(
    "CF04", "FRONT WALL STORAGE & KEY CONSOLE", "LOUNGE", depth=400, cl=3300, plinth=100, plinth_kind="float", top_gap=0,
    sheet_no="ID.02.04",
    cols=[Col(1450, [P(450, "doors", "L03", n=2, shelves=1)]),
          Col(1350, [P(450, "panel", "L03", label="PIANO (BY OWNER)")]),
          Col(1700, [P(450, "doors", "L03", n=2, shelves=1)]),
          Col(1600, [P(2300, "panel", "L01", label="FEATURE WALL")]),
          Col(1430, [P(840, "doors", "L03", n=2, shelves=1), P(60, "counter", "S01")])],
    details=["finger", "plinth", "stone"],
    notes=["LOW STORAGE UNDER FRONT WINDOWS - WINDOW SILL TO BE V.I.F.", "KEY CONSOLE SINTERED STONE TOP 60MM.",
           "FEATURE WALL: OAK PANEL C/W 3MM GROOVE LINE @ 300MM."]))

CABINETS.append(Cabinet(
    "CF05", "DRINK COUNTER & STORAGE WALL", "DRY KITCHEN", depth=600, cl=3600, plinth=100, sheet_no="ID.02.05",
    cols=[Col(850, [P(3480, "panel", "M02", label="HIDDEN DOOR")]),
          Col(1100, [P(2100, "pair", "M02", shelves=4), P(1380, "pair", "M02", shelves=1)]),
          Col(1500, [P(260, "drawers", "L01", n=2), P(260, "drawers", "L01", n=2), P(260, "drawers", "L01", n=2),
                     P(30, "counter", "S01"), P(1500, "niche", "L01", shelves=2, led=True), P(1130, "pair", "M02", shelves=1)]),
          Col(850, [P(820, "appliance", "M02", label="WINE CHILLER"), P(30, "counter", "S01"),
                    P(1300, "niche", "L01", shelves=3, led=True, label="WINE DISPLAY"), P(1330, "pair", "M02", shelves=1)]),
          full(860, 3480, "door", "M02", shelves=6, hinge="R")],
    details=["infill", "led", "finger", "hidden"],
    notes=["COFFEE STATION: 13A TWIN @ FFL 1050, WATER POINT FOR COFFEE MACHINE (TBC).",
           "WINE CHILLER SUPPLIED BY OWNER - CUT-OUT TO MODEL SPEC.", "OPEN NICHE BACK: SINTERED STONE / OAK (TBC)."]))

CABINETS.append(Cabinet(
    "CF06", "ISLAND", "DRY KITCHEN", depth=900, cl=1000, plinth=100, free=True, top_gap=0, sheet_no="ID.02.06",
    worktop=(900, 30, "S01"),
    cols=[Col(2200, [P(770, "panel", "L03", label="SEATING SIDE")]), Col(600, [P(770, "panel", "L03", label="WATERFALL LEG")])],
    details=["stone", "plinth"],
    notes=["ISLAND 2800 x 900, SINTERED STONE 30MM C/W WATERFALL & CURVED END.", "UNDERMOUNT ROUND SINK + POP-UP SOCKET.",
           "WORKING SIDE: 2 x DOOR + 1 x DRAWER STACK (REFER PLAN)."]))

CABINETS.append(Cabinet(
    "CF07", "HOB WALL BASE & WALL CABINET", "WET KITCHEN", depth=600, cl=3200, plinth=100, sheet_no="ID.02.07",
    worktop=(900, 40, "S01"),
    cols=[full(1200, 3080, "pair", "M01", shelves=6),
          kitchen_col(900, "drawers3"), kitchen_col(900, "hob", wall="hood"),
          kitchen_col(800, "doors", 2), kitchen_col(610, "doors", 1)],
    details=["infill", "handle", "stone", "led"],
    notes=["BACKSPLASH: LIMESTONE JH12352GZ 600x1200 STRUCTURED (T05).", "HOB & HOOD BY OWNER - CUT-OUT TO MODEL SPEC.",
           "LIFT-UP WALL CABINET C/W BLUM AVENTOS (TBC). UNDER-CABINET LED."]))

CABINETS.append(Cabinet(
    "CF08", "SINK WALL BASE CABINET", "WET KITCHEN", depth=600, cl=3200, plinth=100, sheet_no="ID.02.08",
    worktop=(900, 40, "S01"),
    cols=[kitchen_col(900, "doors", 2), kitchen_col(600, "dw"), kitchen_col(1000, "sink", 2, wall="window"),
          kitchen_col(800, "drawers3", wall="window"), kitchen_col(810, "doors", 2)],
    details=["handle", "stone", "led"],
    notes=["WINDOW W2400 FFL920 H450 (SITE MEASURE) - WALL CABINET STOPS AT WINDOW.", "DISHWASHER BY OWNER (600 BUILT-IN).",
           "UNDERMOUNT DOUBLE SINK + PULL-OUT TAP (BY OWNER)."]))

CABINETS.append(Cabinet(
    "CF09", "TALL UNIT / OVEN / FRIDGE", "WET KITCHEN", depth=600, cl=3200, plinth=100, sheet_no="ID.02.09",
    cols=[full(600, 3080, "door", "M01", shelves=7, hinge="L"),
          Col(600, [P(800, "drawers", "M01"), P(600, "appliance", "M01", label="OVEN"), P(450, "appliance", "M01", label="MICROWAVE"),
                    P(1230, "door", "M01", shelves=2)]),
          Col(1060, [P(1900, "appliance", "M01", label="SIDE-BY-SIDE FRIDGE"), P(1180, "pair", "M01", shelves=2)])],
    details=["infill", "finger"],
    notes=["FRIDGE HOUSING: 30MM VENT GAP EACH SIDE & TOP, VENT GRILLE AT PLINTH.", "OVEN / MICROWAVE MODEL TBC - CUT-OUT TO SPEC."]))

CABINETS.append(Cabinet(
    "CF10", "FOOD PREPARATION ISLAND", "WET KITCHEN", depth=1100, cl=1000, plinth=100, free=True, top_gap=0, sheet_no="ID.02.10",
    worktop=(900, 30, "S01"),
    cols=[Col(700, [P(770, "doors", "M01", n=1, shelves=1)]), Col(700, [P(770, "drawers", "M01", n=1)]),
          Col(700, [P(770, "doors", "M01", n=1, shelves=1)])],
    details=["stone", "plinth"],
    notes=["CURVED (SOFT TRIANGLE) ISLAND - SET OUT FROM PLAN TEMPLATE ON SITE.", "BODY CLAD WITH TERRAZZO-LOOK SINTERED STONE.",
           "TOP: SINTERED STONE 30MM, BULLNOSE EDGE."]))

CABINETS.append(Cabinet(
    "CF11", "WASHER & BASE UNIT", "LAUNDRY AREA", depth=600, cl=3000, plinth=100, sheet_no="ID.02.11",
    worktop=(990, 40, "S01"),
    cols=[kitchen_col(1300, "washer", label="WASHER + DRYER", wall="window", cl_top=2980, mat="M05", wall_mat="M05"),
          kitchen_col(970, "doors", 2, wall="window", cl_top=2980, mat="M05", wall_mat="M05")],
    details=["handle", "stone"],
    notes=["WASHER & DRYER SIDE BY SIDE UNDER COUNTER (FRONT LOAD, BY OWNER).", "WINDOW W1500 FFL900 H1450 ABOVE (SITE MEASURE).",
           "EAST WALL: BASE UNIT + CEILING HUNG BLACK HANGING ROD (REFER PLAN)."]))

CABINETS.append(Cabinet(
    "CF12", "OPEN WARDROBE", "PARENT'S ROOM", depth=560, cl=3000, plinth=100, sheet_no="ID.02.12",
    cols=[Col(800, [P(300, "drawers", "L01"), P(1700, "hang", "L01"), P(880, "pair", "L01", shelves=1)]),
          Col(800, [P(300, "drawers", "L01"), P(1700, "open", "L01", shelves=4, led=True), P(880, "pair", "L01", shelves=1)])],
    details=["infill", "led", "finger"],
    notes=["OPEN WARDROBE 1600 x 560 (SITE 2030 RECESS - V.I.F.).", "LOW CABINET 2450 x 440 x 750H ON EAST WALL - CURVED END (REFER 3D)."]))

CABINETS.append(Cabinet(
    "CF13", "STORAGE CABINET & TATAMI", "MAID ROOM", depth=600, cl=2800, plinth=100, sheet_no="ID.02.13",
    cols=[full(950, 2680, "pair", "M05", shelves=5), full(1000, 2680, "pair", "M05", shelves=5)],
    details=["infill", "finger"],
    notes=["TATAMI 1160 x 2100 x 400H C/W LIFT-UP STORAGE (GAS STRUT).", "HEADBOARD SHELF C/W LED (REFER 3D)."]))

CABINETS.append(Cabinet(
    "CF14", "VANITY", "POWDER ROOM", depth=500, cl=2600, plinth=0, top_gap=0, sheet_no="ID.02.14",
    cols=[Col(800, [P(350, "gap", "T04"), P(450, "doors", "L01", n=1), P(40, "counter", "S01"), P(900, "panel", "M02", label="MIRROR")])],
    details=["stone"],
    notes=["PEDESTAL STONE BASIN (BY OWNER) - REFER 3D.", "WALL & FLOOR: AMAZON TRAVERTINE 600x1200 MATT (T04)."]))

# ---------------------------------------------------------------- FIRST FLOOR
CABINETS.append(Cabinet(
    "CF15", "HEADBOARD & BEDSIDE", "MASTER BEDROOM", depth=250, cl=3000, plinth=0, top_gap=0, sheet_no="ID.03.01",
    cols=[Col(500, [P(450, "gap", "P02"), P(180, "drawers", "L01"), P(2350, "panel", "L01")]),
          Col(3700, [P(1150, "panel", "L01", label="HEADBOARD (UPHOLSTERED, BY OWNER)"), P(1830, "panel", "P02", label="LIMEWASH P02")]),
          Col(500, [P(450, "gap", "P02"), P(180, "drawers", "L01"), P(2350, "panel", "L01")])],
    details=["led"],
    notes=["FLOATING BEDSIDE DRAWER C/W UNDER-LED.", "WALL PANEL REVEAL 3MM BLACK GROOVE (REFER 3D)."]))

CABINETS.append(Cabinet(
    "CF16", "TV DIVIDER W/ FIREPLACE", "MASTER BEDROOM", depth=450, cl=3000, plinth=0, sheet_no="ID.03.02",
    cols=[Col(700, [P(2980, "niche", "L01", shelves=3, led=True)]),
          Col(1600, [P(420, "appliance", "S01", label="BIO-ETHANOL FIREPLACE"), P(160, "panel", "S01"),
                     P(900, "void", "M02", label='65" TV'), P(1500, "panel", "M02")]),
          full(700, 2980, "door", "M02", shelves=6, hinge="R")],
    details=["infill", "led", "stone"],
    notes=["FIREPLACE SUPPLIED BY OWNER - NON-COMBUSTIBLE LINING (SINTERED STONE) AROUND FIREBOX.",
           "OPT 2: TWIN TIMBER COLUMNS EITHER SIDE (REFER 3D)."]))

CABINETS.append(Cabinet(
    "CF17", "WARDROBE (GLASS DOOR)", "WALK IN CLOSET", depth=590, cl=3000, plinth=100, sheet_no="ID.03.03",
    cols=[Col(900, [P(450, "drawers", "M02"), P(2430, "glass", "M02", shelves=4, led=True)]) for _ in range(5)],
    details=["infill", "glass", "led"],
    notes=["20MM BLACK ALU FRAME C/W TINTED / FLUTED GLASS DOOR.", "LED PROFILE AT EACH SHELF, DOOR-ACTIVATED SENSOR."]))

CABINETS.append(Cabinet(
    "CF18", "DOUBLE VANITY", "MASTER BATH", depth=550, cl=2600, plinth=0, top_gap=0, sheet_no="ID.03.04",
    cols=[Col(1200, [P(350, "gap", "T03"), P(500, "doors", "L01", n=2), P(40, "counter", "S01"), P(250, "gap", "T03"),
                     P(800, "door", "M02", label="MIRROR CAB.")]) for _ in range(2)],
    details=["stone", "led"],
    notes=["FLOATING VANITY C/W UNDER-CABINET LED.", "MARBLE-LOOK SINTERED STONE TOP C/W 2 x COUNTERTOP BASIN (BY OWNER)."]))

CABINETS.append(Cabinet(
    "CF19", "FEATURE WALL / PIANO WALL", "FAMILY AREA", depth=400, cl=3000, plinth=100, sheet_no="ID.03.05",
    cols=[full(800, 2880, "door", "M02", shelves=6, hinge="L"),
          Col(1500, [P(1100, "panel", "M02", label="PIANO (BY OWNER)"), P(1780, "niche", "L01", shelves=2, led=True)]),
          full(800, 2880, "door", "M02", shelves=6, hinge="R")],
    details=["infill", "led", "finger"],
    notes=["FEATURE PANEL C/W NICHE & CONCEALED LED.", "ROUND PENDANT (BY OWNER) - REFER LIGHTING PLAN."]))

CABINETS.append(Cabinet(
    "CF20", "WARDROBE & DISPLAY", "SON'S ROOM", depth=600, cl=2900, plinth=100, sheet_no="ID.03.06",
    cols=[full(1000, 2780, "pair", "L02", shelves=6),
          Col(900, [P(450, "drawers", "L02"), P(1500, "hang", "L02"), P(830, "pair", "L02", shelves=1)]),
          Col(900, [P(2780, "open", "M02", shelves=5, led=True, label="DISPLAY")]),
          full(1200, 2780, "pair", "L02", shelves=6), full(1190, 2780, "pair", "L02", shelves=6)],
    details=["infill", "led", "finger"],
    notes=["DARK FINISH TS4-1017 M BLACK (L02) C/W WARM DISPLAY BACK PANEL.", "STUDY DESK C/W WALL-HUNG DISPLAY - REFER PLAN."]))

CABINETS.append(Cabinet(
    "CF21", "WARDROBE & DISPLAY", "DAUGHTER'S ROOM", depth=600, cl=2900, plinth=100, sheet_no="ID.03.07",
    cols=[full(900, 2780, "pair", "M02", shelves=6),
          Col(1640, [P(850, "doors", "M01", n=2, shelves=1), P(30, "counter", "M01"), P(1200, "open", "M01", shelves=2, led=True),
                     P(700, "doors", "M01", n=2, shelves=1)]),
          full(900, 2780, "pair", "M02", shelves=6)],
    details=["infill", "led", "finger"],
    notes=["OAK FRAME C/W WHITE DOOR PANEL (REFER 3D).", "DRESSING / STUDY DESK AT WINDOW - REFER PLAN."]))

CABINETS.append(Cabinet(
    "CF22", "VANITY", "SON'S / DAUGHTER'S BATH", depth=500, cl=2600, plinth=0, top_gap=0, sheet_no="ID.03.08",
    cols=[Col(1100, [P(350, "gap", "T03"), P(450, "doors", "L01", n=2), P(40, "counter", "S01"), P(200, "gap", "T03"),
                     P(800, "doors", "M02", n=2, label="MIRROR CAB.")])],
    details=["stone", "led"],
    notes=["SON'S BATH: DARK FINISH (L02). DAUGHTER'S BATH: OAK (L01).", "WALL-HUNG MIRROR CABINET C/W LED."]))
