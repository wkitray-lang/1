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

## Payment terms（Groo 7-Step Flow，2026-10-13 起）
付款节点绑定项目进度。描述照下面写，%放 H，金额 `=ROUND($K$<grand>*H<row>,2)`。

**Landed（6 期）**
| # | 描述 | % |
|---|---|---|
| 1 | #1 Engagement - design stage, upon confirmation of proposal (Step 2) - incl. ID design fee | 10% |
| 2 | #2 Start Work - upon signing of contract & site commencement (Step 4) | 25% |
| 3 | #3 Upon Ceiling Done & Fabrication of Cabinetry (Step 5) | 25% |
| 4 | #4 Upon Delivery of Cabinetry to site, before installation (Step 5) | 25% |
| 5 | #5 Upon Installation of Table Top & Ironmongery (Step 5) | 10% |
| 6 | #6 Final - upon Handover, before defect rectification (Step 6) | 5% |

**Condo < RM250k（5 期）**：10% Engagement / 40% Start Work / 30% Ceiling + Fabrication / 15% Cabinetry delivery / 5% Handover。

## 7-Step Flow 对报价单的要求
- Step 2 提案报价 = 90% 准度；Step 3 在 3D 定案后 revise（收紧，不是重报）。
- ID 设计费单独列示（section 放在 Preliminaries 前面）。
- 表头放「Est. Move-in」预估搬入日期（E10/F10）；Step 4 起写进合同。

## 格式
- 不用蓝色底色（Hana 全部改白）。
- 有竖向合并的行不要做 D:F 合并（会失败）。
- Section 标题行不合并。

## 操作安全
- 写前重读；插行后检查所有 K 公式；大改前 duplicateSheet 备份。
- 用户同时编辑时，冲突的格（例如折扣）不要再碰，告诉用户。
