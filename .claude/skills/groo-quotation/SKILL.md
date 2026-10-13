---
name: groo-quotation
description: Groo Space quotation Audit & Assist. Use for ANY Groo interior design-and-build quotation work - drafting a new quotation from drawings/briefs, adding or repricing items, pricing supplier quotes into the sheet, auditing a quotation for missed items / wrong formulas / weak margins, or writing the client send-out message. Also use when the user gives pricing feedback or corrections, so the lesson gets logged and the system improves.
---

# Groo Quotation – Audit & Assist

Groo Space Sdn Bhd（KL 设计+施工）。Raymond Lau 负责报价。回复用中文，报价单内容用英文。

这个 skill 有三种模式。先判断用户要哪一种，可以连续做：

| 模式 | 什么时候 | 流程 |
|---|---|---|
| **A. Draft** | 新项目 / 新区域 / 新 section 要报价 | 下面 §1 |
| **B. Audit** | "帮我 check / review / 有没有漏" | 下面 §2 |
| **C. Learn** | 用户纠正价格、毛利、写法，或确认某个做法 | 下面 §3（每次都要做，不用等用户叫） |

开工前**必读**：`references/pricing-rules.md`、`references/sheet-conventions.md`、`learning/lessons.md`。
其他文件按需读。

---

## §1 Draft 流程

1. **Intake**：复制 `templates/project-brief.md` 到 `<project>/project-brief.md`，从用户给的资料填：
   客户、地址、面积、楼层、预算、风格、图纸清单、已有供应商报价。缺的标 `TBC`，不要停下来问，先做。
2. **量（Quantities）**：从图纸取量。每个数字记来源（图纸编号 / 量法）。
   - 天花 sqft、地砖 sqm、墙砖 sqm、踢脚线 m、灯位数、插座数、木作 W×D×H。
   - 读 PDF/DWG 用 pdftotext / pdftoppm / 图片直接看；量不到的写假设，进 Questions。
3. **价（Rates）**：按优先级取价：
   1. 本项目供应商报价 → `<project>/suppliers/*.md`（成本 → 按 pricing-rules 加毛利）
   2. `references/rate-card.csv`（Groo 卖价库）
   3. `references/supplier-library.md`（供应商价目表成本）
   4. 都没有 → 写 PC/PS 金额，描述里写 "PC rate RMxx/sqm, subject to final selection"，进 Questions
4. **写入**：按 `references/section-templates.md` 的 section 顺序和描述写法；
   按 `references/sheet-conventions.md` 写公式（单价要用公式留下成本，例如 `=ROUND(5800/(1-30%),2)`）。
5. **自检**：跑 §2 Audit 的第 1–4 步再交给用户。
6. **输出**：总价、各 section 小计、⭐ 待讨论项目合计、Questions 清单。

## §2 Audit 流程

详细见 `references/audit-procedure.md`。顺序：

1. **结构**：用 Sheets `get_values`（FORMULA 模式 + 数值模式各一次）读整张表，
   存成 JSON 后跑 `python3 scripts/audit_quote.py <dump.json>`，
   它会查：J≠H×I、section SUM 漏行、有数量没单价、单价离 rate-card 太远、⭐ 合计、关键字缺漏。
2. **漏项**：逐条对 `references/missed-items-checklist.md`。
3. **毛利**：每个单价反推成本，对 pricing-rules 的毛利目标；低于目标标红。
4. **重复计算**：同一工作出现在两个 section（自流平、门、楼梯、灯具点位等）。
5. **商务**：日期、地址、PM %、折扣公式（必须是负数）、付款条款金额、Exclusions、T&C、签名栏。
6. **报告**：分 🔴 必改 / 🟡 建议 / ⚪ 已核对没问题，给金额影响。**不要自己改表，等用户选。**

## §3 Learn 流程（越用越聪明）

每当用户：纠正价格 / 毛利 / 描述写法 / 指出漏项 / 说 "以后都这样"——

1. 在 `learning/lessons.md` 加一条（日期、项目、规则、原因）。规则要写成以后能直接执行的句子。
2. 如果是价格 → 同时更新 `references/rate-card.csv`（填 source + date）。
3. 如果是漏项 → 加进 `references/missed-items-checklist.md`。
4. 如果是供应商新报价 → 新建 `<project>/suppliers/YYYY-MM-DD_<Supplier>_<Item>.md`，
   并在 `references/supplier-library.md` 更新最新成本。
5. 项目结束（客户签约 / 最终版本）→ 在 `learning/project-log.md` 记：总价、每 sqft、各 section 占比、
   被砍掉的 ⭐ 项目、客户反应。这是以后估预算的基准。
6. commit + push 到当前分支，告诉用户学到了什么（一行）。

不要把一次性的决定写成通用规则；不确定就写进 lessons 并标 `(project-specific)`。

---

## 硬规则（每次都要遵守）

- **写之前先重读**：用户会同时改表，行号会变。每次写入前 `get_values` 确认目标行。
- **插行后检查 section SUM**：插在最后一行后面的行不会自动进 SUM 范围。
- **大改之前先备份 tab**（duplicateSheet，命名 `BACKUP Rn (dd Mon)`）。
- **单价公式保留成本**：`=ROUND(cost/(1-30%),2)`，不要直接打卖价数字。
- **PS / PC 项目**要在描述里写清楚是 Provisional Sum / Prime Cost。
- **⭐ = 待讨论 / 可选项目**，要单独算合计给用户看。
- 用户说 "不需要改别的" 就只改他说的。
- 不确定的东西进 Questions，不要猜了就写死。
