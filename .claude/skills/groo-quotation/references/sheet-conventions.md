# Google Sheet 报价单格式

| 列 | 内容 |
|---|---|
| C | 项目编号（1.0、1.1 …） |
| D | Description（D:F 在 E/F 空的行合并 MERGE_ROWS，让报价单短一点） |
| E / F / G | 木作：W / D / H（mm）；其他行：G 放单位（sqft、m、nos、L/S） |
| H | Qty（可以是公式，如 `=ROUNDUP((H122+H128)*1.2/7.75,0)`） |
| I | Unit price（公式保留成本） |
| J | `=H*I` |
| K | Section 小计，只写在 section 标题行：`=SUM(J<first>:J<last>)` |

## 表头
- F6 日期，numberFormat `dd mmm yyyy`（不然会变 10/8/2026）。
- F9 工地地址；J8 公司地址（Wisma JAG）；C10 面积 sqft。

## 尾部顺序
Project Management（1.5% L/S）→ SUBTOTAL → Discount（负数）→ GRAND TOTAL →
Payment Terms（H 放 %，I 放 `=ROUND($K$<grand>*H<row>,2)`）→ Exclusions → T&C → 签名栏（Full Name / IC No.）。

## Payment terms（Groo 标准，Hana 用）
10% / 25% / 25% / 25% / 10% / 5%（按 Hana 金额推算）。以项目实际为准。

## 格式
- 不用蓝色底色（Hana 全部改白）。
- 有竖向合并的行不要做 D:F 合并（会失败）。
- Section 标题行不合并。

## 操作安全
- 写前重读；插行后检查所有 K 公式；大改前 duplicateSheet 备份。
- 用户同时编辑时，冲突的格（例如折扣）不要再碰，告诉用户。
