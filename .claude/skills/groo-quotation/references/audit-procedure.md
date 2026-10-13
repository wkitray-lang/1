# Audit 流程（详细）

## 0. 读表
用 Google Sheets `get_values` 读整张 tab（范围 `A1:L600`）两次：
- `valueRenderOption: FORMULA` → formulas
- 默认（FORMATTED / UNFORMATTED）→ values

存成一个 JSON：`{"formulas": [[...]], "values": [[...]]}`，放 scratchpad，然后：

```bash
python3 .claude/skills/groo-quotation/scripts/audit_quote.py /path/dump.json
```

脚本输出：结构错误（🔴）、价格偏离（🟡）、清单关键字缺漏（🟡）、⭐ 合计、各 section 小计。
**脚本只是第一道筛选，第 1–5 步还是要人眼过。**

## 1. 结构
- 每个 section 标题行 K 的 SUM 范围要覆盖到下一个 section 标题前一行。
- J = H × I。
- 有 H 没有 I，或有 I 没有 H。
- Grand total = Subtotal + Discount；Subtotal 包含 PM。

## 2. 漏项
逐条过 `missed-items-checklist.md`，再对图纸：每个房间是否在天花、油漆、地板、电器、木作都出现。

## 3. 毛利
每个单价反推成本（看公式里的 cost），对 `pricing-rules.md`。没有公式的直接打数字 → 🟡 "cost unknown"。

## 4. 重复计算
常见：自流平（Wet works + Flooring）；暗门（Joinery + Doors）；楼梯（Painting texture + Joinery panel + Flooring）；
窗帘电机（Window + Smart home）；LED 点位（Electrical + Joinery）；scaffolding（Prelim + Curtain）。

## 5. 商务
日期、地址、PM、折扣、付款条款、Exclusions、T&C、签名栏。

## 6. 报告格式（中文）
```
🔴 必改（影响金额 / 错误）
1. <行号> <问题> → 建议 <改法>（±RMx）
🟡 建议
⚪ 已核对 OK：<列出 section>
⭐ 待讨论合计：RMx；去掉后总价 RMy
```
等用户选了再改表。
