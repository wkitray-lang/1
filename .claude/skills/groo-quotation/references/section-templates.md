# Section 模版（顺序 + 标准描述）

报价单固定顺序。每个 section 下面列「必有行」和「常见行」。描述用英文，写清楚 supply / install / 品牌 / 尺寸 / 不含什么。

## Interior Design Fee（最前面）
必有：设计服务描述（moodboard、space planning、3D、2D 详图、材料规格、3D 定案后 revise 报价、施工期设计协调），qty `=C10`（built-up sqft），单价 RM8。
附注：设计费包含在总价里，10% Engagement（含设计费）确认后启动设计阶段。

## Preliminaries
必有：Site protection（地板、楼梯、门框保护膜）；Debris disposal & lorry；Final cleaning；Insurance / CIDB / permit（如需）。
常见：Scaffolding（挑高区，RM3,500 L/S）；Hoarding；Temporary water & electricity。

## 1.0 Ceiling Works
必有：Plaster board ceiling per area（sqft，按区域分行）；L-box / light trough / curtain pelmet（ft）；Access panel；Fan holder；Chandelier support。
常见：Custom moulded profiles —— **按区域分行**（GF-A、GF-B…），不能 lump sum。描述："Supply & install custom moulded ceiling profile at <Area>, <profile description>"。
不含：painting（在 Painting section）。

## 2.0 Painting
必有：Ceiling（sqft）；Walls（sqft）；Sealer + 2 coats，品牌（Nippon / Dulux）。
常见：Texture paint / limewash（⭐）；Exterior；Gate & grille。

## 3.0 Wet Works
必有：Demolition L/S（**描述里列出每个被拆的房间**）；Debris；Hacking tiles；Screed；Waterproofing（浴室、阳台、平台，写 membrane 品牌 + 上墙高度）；Floor tiling labour；Wall tiling labour；Tile supply（PC + 20% 损耗，按 sqm 换算片数）。
常见：Raised screed（下沉 / 抬高）；Threshold；Core drill；Brick infill；Re-plaster；Making good；Self-levelling。
注意：自流平只报一次（不要 Wet works 和 Flooring 都有）。

## 4.0 Plumbing
必有：Water point per fixture；Floor trap；WC relocation；Garden tap；Cap-off（拆掉的浴室）。
常见：Water heater point；Pump；Filter。

## 5.0 Electrical
必有：Lighting point（= 灯位总数 + 余量，公式 `=SUM(...)+10+2`）；13A；15A；Aircond point；2-way switch；Hob 32A；Main DB；Data / TV point。
常见：Curtain motor point；Joinery LED point；BGM cabling；Amp socket；Pond pump；Irrigation；Outdoor weatherproof socket；Garden light；Exhaust fan point；Bath heater point。
注明："TNB meter upgrade / application by owner"。

## 6.0 Light Fittings
灯具 by owner（我们选）。我们报：bath heater / exhaust / kitchen aircond（AUPU 等）+ 开孔 + 安装。

## 7.0 Doors & Windows
必有：每扇门一行（尺寸、材料、五金）；浴室门；Sliding door（reeded glass 等）。
常见：Awning（sqft × RM75）；Window replacement PS；Door refurbishment。

## 8.0 Joinery
每件柜子一行，E/F/G 写尺寸，公式见 joinery-formulas.md。按区域排（Foyer → Living → Dining → Kitchen → GF rooms → Staircase → FF rooms）。
最后一行：⭐ PS cabinetry accessories RM5,000。

## 9.0 Table Top
Quartz / sintered / marble，写厚度、边型、开孔数量。Onyx / 天然石单独写 slab 数量。

## 10.0 Flooring
工程木 / SPC / 地毯：供货 + 安装 + 踢脚线 + quarter round。楼梯踏板、踢面、防滑条分开。

## 11.0 Window Finishings
窗帘按窗分行：布料、层数（sheer / dim-out）、轨道（电动 / 手动）。

## 12.0 Whole House System
AETHO 格式逐项：CCTV、Wi-Fi、BGM、curtain motor、cinema。单价 cost×1.15，安装 device×0.2×1.15。

## 13.0 Air-Cond
每台一行（HP、区域）；安装；trunking；drain。`=CEILING(cost/0.75,5)`。

## 14.0 Landscape
Softscape（m²）、Hardscape / walkway（m²）、Water feature（m²）、Irrigation、Lighting（电工在 Electrical）。注明不含的植物（例：Podocarpus / 罗汉松）。阳台景观 PS。

## 尾部
Project Management 1.5% → Subtotal → Discount → Grand Total → Payment Terms → Exclusions → T&C → Signature（Full Name / IC No.）。
