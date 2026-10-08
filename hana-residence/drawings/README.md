# Hana Residence：2D 施工图 R0（参照 AC.R3 Boon Ping 格式）

**主文件：`HANA_RESIDENCE_2D_WORKING_DRAWINGS_R0.pdf`**（A3 横向，46 张）

| 编号 | 内容 |
|---|---|
| ID.00.01–02 | 图纸目录 Tender Drawing List、材料表 Material List |
| ID.01.01–22 | GF / FF 各 11 张：原始平面、拆除及泥水、家具平面、家具平面尺寸、天花、插座 M&E、灯位（含数量）、墙面、地坪（含面积）、窗帘（含尺数）、立面索引 |
| ID.02.01–14 | GF 柜体立面详图 CF01–CF14 |
| ID.03.01–08 | FF 柜体立面详图 CF15–CF22 |

每张柜体详图包含：Plan Key（平面索引 + 剖切/立面符号）、ELEVATION A、INNER CARCASS A、SECTION X-X、1:5 节点（Infill Recess 20MM、45° Finger Pull、LED、Plinth、J&C Handle、Sintered 45° Corner、Hidden Door、Slim Frame Glass）、材料标签（M01 / L01 / S01 …）、蓝色尺寸、红色注释、CL / FFL 标高。

## 文件夹

- `dxf/`：每张图一个 DXF（R2018，可用 AutoCAD 打开），按 1:1 纸面毫米绘制，图层按用途分：A-WALL、I-JOIN、I-DIM、I-LITE、I-POWR …
- `src_*.dxf`：从 YS / Yanxiang 的 AutoCAD PDF 矢量转回的毫米底图（GF ori / new、FF exist / new），比例已用轴网尺寸校准。可以直接贴进 CAD 继续画。
- `quantities_R0.json`：从图上自动统计的数量（灯数、LED 米数、插座、地坪面积、窗帘尺数），可以和报价对照。
- `tools/`：生成脚本。改 `hd/data.py`（房间、柜体位置）或 `hd/cf_data.py`（柜体分格、材料）后运行 `python3 tools/build_set.py`，整套图会重新出。

## 依据

1. **墙体几何**：HANA RESIDENCE DWG（02/10/2026）PDF 的矢量。核对结果：湿厨房 5401 vs 手写 5427，早餐区 6443 vs 6427，误差在 30mm 以内。
2. **布局**：FLP 30/07/2026 加现场手写尺寸。例如鞋柜 1200×580、Foyer 柜带 570 深、湿厨房窗 W2400 FFL920 H450、洗衣房窗 W1500 FFL900 H1450，以及各处 SH / CH 净高。
3. **设计**：3D PROPOSAL R1（79 页），包括柜体分格、材质、灯光、天花造型。

## R0 需要设计师核对的地方（V.I.F.）

- **FLP 光栅图和 DWG 在 Y 方向差约 4%**。墙体以 DWG 为准，FLP 只用来定柜体的相对位置。
- **柜体内部分格、门板数量、层板数**：按 3D 目测推算，需要 YS 逐张确认。
- **天花 CL 是设计标高（TBC）**。现场净高：Foyer S3814、Living SH4207、早餐区 SH4273、Dining SH8118（挑空）、湿厨房 CH3539、Entrance CH3334、Master CH3614、Family CH3627。
- **灯位、开关位置**：按房间自动排布（约 1.35m 间距）。最终要和 M Vida（AETHO）的智能灯光图对齐。
- **窗位、窗帘宽度**：按图估算，需现场量。
- **Son's / Daughter's 浴室是否重做**：拆除图上标了 TBC。

## 下一步可以加的

- 柜体 ISO 3D 视图（AC.R3 有）。
- 楼梯与玻璃栏杆详图、门窗表。
- 浴室墙砖排版立面。
- 收到 DWG 原档后，把柜体和灯位直接写进同一个 model space DWG。
