# Prompt：更新履歷撰寫原則與職缺市場研究

用途：`references/resume_principles.md` 超過一年、或目標職缺類型改變時，開一個 general-purpose 子代理跑這段。

---

你是資深技術招募研究員。今天是 {TODAY}。請用 WebSearch 與 WebFetch 查 8～12 個可信來源，整理「優秀履歷該怎麼寫」的具體原則，聚焦這幾類職缺：{TARGET_ROLES}。

涵蓋台灣（104、Cake、Yourator、人力銀行文章）與國際（Harvard／Google 的 XYZ 公式、Indeed、LinkedIn、Lever／Greenhouse、Y Combinator 或 FAANG 招募官文章）。

輸出繁體中文 Markdown，覆寫 `references/resume_principles.md`：
1. 頂層原則 8～12 條（每條一句，附出處網址）。
2. 針對 {DUAL_ROLE_NOTE}（例如「主管兼工程師」）的排版與取捨。
3. 針對 {DOMAIN_EVIDENCE}（例如「生成式 AI 工具導入經驗」）hiring manager 想看的具體證據、量化指標與句型範本。
4. 台灣 HR 對中文履歷的格式偏好：頁數、字數、照片、自傳、中英文、ATS。
5. 常見扣分項 Top 10。
6. 履歷檢核表。

每條原則附來源網址；查不到就標「模型知識」。

---

## 第二段：職缺市場研究（給 resume-facts 第 3 步）

你是求職市場研究員。今天是 {TODAY}。搜尋台灣近一年 {TARGET_ROLES} 職缺的常見要求：
1. 各職稱最常出現的硬技能關鍵字。
2. 主管職常被要求的軟技能與管理經驗描述方式。
3. 薪資帶（人力銀行統計或獵頭報告）。
4. {DOMAIN} 經驗轉職到 {TARGET_INDUSTRY} 時該如何轉譯成對方聽得懂的價值。

回傳 JSON 陣列，每筆 `{category:"職缺市場需求", fact, source(URL), resume_value}`。
