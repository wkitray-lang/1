# Pricing Rules（毛利规则）

卖价公式一律保留成本在公式里，方便以后反查。

| 类别 | 规则 | 公式例子 | 来源 |
|---|---|---|---|
| 默认（分包 / 供应商报价） | 毛利 30% | `=ROUND(cost/(1-30%),2)` | Hana，Raymond 确认 |
| 天花（K TWO / K2 模具） | 毛利 30%（**不是** QS 表的 45%） | `=ROUND(4/0.7,2)` | Hana 12 Oct，Raymond 纠正 |
| 冷气 | 毛利 25%，取整到 5 | `=CEILING(cost/0.75,5)` | QS Markup Guide |
| Smart home（AETHO 等） | 成本 × 1.15 | 单价 `=ROUND(cost*1.15,2)`；安装 `=ROUND(device*0.2*1.15,2)` | Hana |
| Table top（石材） | 30%（QS 指南 35%，Hana 用 30%） | `=ROUND(12800*2/(1-30%),2)` | Hana |
| 灯具 / 洁具（AUPU 等设计师价） | cost/0.7 | `=ROUND(2299/0.7,2)` | Hana |
| 木作 | 按尺 rate（见 joinery-formulas.md），不是 cost+margin | `=E/300*1250` | Groo 标准 |
| 景观（分包） | 按分包价比例放大到目标卖价 | `=ROUND(54280/24.7*138000/125800,2)` | Hana |
| ID 设计费 | RM8 / sqft × built-up 面积，单独一个 section 放最前面 | H `=C10`，I `8` | 7-Step Flow，13 Oct |
| Project Management | **RM2.8 / sqft × built-up 面积**（2026-10-13 起；Hana 旧做法是施工总额 1.5%） | H `=C10`，I `2.8`，G `sqft` | Bromelia，Raymond 确认 |
| 折扣 | 负数公式 | `=-ROUND(K<subtotal>*2%,2)` | Hana（⚠️ 不能写 `=K421-2%`） |

## 客户自付 / 我们只选不赚
- 灯具（light fittings）、壁炉：我们帮选，客户付款（Hana 13 Oct）。报价里写 PS 或 "by owner"。

## PC / PS 默认值（没有供应商报价时）
| 项目 | PC 值 | 备注 |
|---|---|---|
| 地砖 Limestone / Travertine | RM95 / sqm | 供货，另加 20% 损耗 |
| 地砖 Bellezza | RM85 / sqm | |
| 大板 900×1800（Dong Peng） | RM285 / 片 | Hana 1F，成本 RM250 |
| 户外砖 600×600 | RM35 / sqm | Hana（原 25，用户改 35） |
| 木作五金配件 PS | RM5,000 | Blum 等 |
| 阳台景观 PS | RM10,000 | |

## 毛利自检
反推：`cost = sell × (1 − margin)`。低于目标 3% 以上 → 🔴；没有成本依据 → 🟡 标 "rate unverified"。
