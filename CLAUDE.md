# Groo Space – Claude 工作说明

Groo Space Sdn Bhd，KL 室内设计 + 施工公司。用户：Raymond Lau。**回复用中文**，报价单内容用英文。

## 报价相关的一切 → 用 `groo-quotation` skill
`.claude/skills/groo-quotation/`：Draft（起草）、Audit（审核）、Learn（记录用户纠正）。
- 规则：`references/pricing-rules.md`、`references/sheet-conventions.md`
- 费率库：`references/rate-card.csv`；供应商：`references/supplier-library.md`
- 木作公式：`references/joinery-formulas.md`
- 漏项清单：`references/missed-items-checklist.md`
- 学到的东西：`learning/lessons.md`、`learning/project-log.md`

用户纠正价格 / 写法时，**当场**写进 lessons 和 rate-card，commit + push。

## 项目文件夹
每个项目一个文件夹（例：`hana-residence/`），里面：`project-brief.md`、`suppliers/`（每份供应商报价一个 md）、`drawings/`、审核表。
新项目：复制 `.claude/skills/groo-quotation/templates/project-brief.md`。
