# Lessons（越用越聪明）

每次用户纠正或确认一个做法就加一条。最新的在最上面。格式：
`- YYYY-MM-DD [项目] 规则 —— 原因`

## 价格 / 毛利
- 2026-10-14 [D'Hill] Sintered stone 成本 RM140/ft，卖 250/ft ≈ 44%；岛台卖 130/ft 只因为卖的尺数（15）比实际成本尺数（9.5）多才有 32%，单价本身低于成本——岛台按实际尺数报，单价不低于 200/ft。
- 2026-10-14 [D'Hill] 报价尺数要和供应商量的一致：后墙卖 13.5 ft，但供应商算 16 ft，少收约 RM625。开孔要按个数报（盆 + 炉头 = 2 个）。
- 2026-10-13 [Bromelia] Project Management 改为 RM2.8/sqft × built-up 面积（取代 1.5%）。
- 2026-10-13 [Bromelia] 新 7-Step Flow：ID 设计费 RM8/sqft（built-up），单独列在报价单最前面，PM 不算在设计费上。
- 2026-10-13 [Bromelia] 付款条款：Landed 10/25/25/25/10/5（6 期），Condo<250k 10/40/30/15/5（5 期），描述要写 Step 编号。
- 2026-10-13 [Bromelia] 拆旧砖 RM8/sqft（地 + 墙）。
- 2026-10-12 [Hana] 天花毛利用 30%，不是 QS 指南的 45% —— Raymond 纠正。
- 2026-10-12 [Hana] Smart home 只加 15%，按 AETHO 格式逐项列，不要 lump sum —— 用户说 lump sum 太随便。
- 2026-10-12 [Hana] 13A 插座维持 RM195。
- 2026-10-13 [Hana] PM 收 1.5%（L/S，按工程总额）。
- 2026-10-12 [Hana] 遮阳棚 awning RM75/sqft。
- 2026-10-12 [Hana] Powder vanity RM175/sqft，长宽超过 300 的部分进位到 0.5 sqft。

## 写法 / 结构
- 2026-10-13 [Bromelia] 灰色底 = Category（section 标题）；Area 写在 D 列（跟 description 同列）Bold + underline、无底色；item description Regular —— 用户纠正（之前复制格式错位一行）。
- 2026-10-13 [Bromelia] Landed 默认层高 3.0m，drop ceiling 300mm → 浴室墙砖贴到 2.7m。
- 2026-10-13 [Bromelia] 冰箱位要做 tall unit 包冰箱（900W），算 1350/ft。
- 2026-10-13 [Bromelia] 户外 / 半户外鞋柜用 plywood laminate（防潮）。
- 2026-10-13 [Bromelia] Powder room 小砖（kit kat）只贴半高，上面用 600x600 / 600x1200 大砖。(project-specific)
- 2026-10-12 [Hana] 定制天花模具按区域分行，不能 lump sum。
- 2026-10-12 [Hana] 木作要写 W/D/H，用 `=E/300*rate` 公式（参考 Parents bedhead 写法）。
- 2026-10-12 [Hana] D:F 在 E/F 空的行合并，报价单短一点。
- 2026-10-12 [Hana] 不用蓝色底色。
- 2026-10-13 [Hana] 付款条款旁边放金额（总价 × %）。
- 2026-10-13 [Hana] 签名栏下加 Full Name / IC No.。
- 2026-10-13 [Hana] ⭐ = 待讨论 / 不一定做，要算合计。

## 不要做
- 2026-10-12 [Hana] 不要报 sub-DB、wiring test、拆旧线路（RM2,500）—— 用户删掉。
- 2026-10-12 [Hana] Smart home 不要 KNX、不要灯光场景控制、不要电动轨（只留 BGM + 窗帘电机）。(project-specific)
- 2026-10-12 [Hana] LED 点位不要和灯带重复算（Hana 原本 36 + 20，改成 10）。
- 2026-10-13 [Hana] 客户信息里不要写 "准确度 90%"。

## 操作
- 2026-10-12 [Hana] 写表前一定重读，用户会同时改，行号会变。
- 2026-10-12 [Hana] 插行后 section SUM 不会自动扩展，要手动检查。
- 2026-10-13 [Hana] 折扣公式要写负数，`=K421-2%` 会让总价翻倍。
- 2026-10-13 [Hana] 日期格要设 numberFormat `dd mmm yyyy`。
