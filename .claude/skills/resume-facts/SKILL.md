---
name: resume-facts
description: 第二步。用多個平行子代理讀 work/extract/ 的來源，萃取帶出處的事實，合併成 work/fact_sheet.md（履歷唯一事實來源）。使用者說「整理事實」「建事實表」「萃取成果」時用。
---

# resume-facts：建立事實表

## 為什麼要這一步
草稿與審閱都只能引用事實表。沒有事實表，寫手會憑印象補數字，查核員也沒有基準。

## 流程

### 1. 分組來源
讀 `work/extract/index.md`，把檔案分成 3～6 組（例：舊履歷、本人月報、成員月報、全組進度表、簡報、外部系統摘要）。每組一個讀取代理。

### 2. 平行萃取（Agent tool，general-purpose，同時送出）
每個代理的 prompt 用 `prompts/02_extract_facts.md`，替換 `{FILES}` 與 `{FOCUS}`。要求回傳 JSON 陣列，每筆：
```
{category, fact, person_role（親自執行／主導與管理／團隊成員執行／不明）, source, resume_value（high/medium/low）, is_estimate（bool）, status（done/ongoing/planned）}
```

### 3. 職缺市場研究（可選，一個代理）
用 `prompts/00_research_principles.md` 的第二段，查目標職缺的 JD 關鍵字與薪資帶，結果放事實表第 8 節。`references/resume_principles.md` 超過一年也在這一步更新。

### 4. 合併
把所有 JSON 交給一個代理（或自己做），依 `templates/fact_sheet_template.md` 合併成 `work/fact_sheet.md`：
- 去重；數字衝突並列並標出處。
- `profile.md`「來源檔案裡沒有、但你確認為真的事實」整節搬進來，出處標 `[profile]`。
- 第 10 節「已知衝突與待確認」一定要填，這是投遞前清單的來源。
- 第 11 節「亮點 Top 12」每點附出處。

### 5. 回報
事實筆數、high 價值筆數、衝突數、需要使用者確認的問題（直接用 AskUserQuestion 問，尤其是角色歸屬與來源沒寫的實績）。

## 品質檢查
- 隨機抽 10 筆事實，用 Grep 回 `work/extract/` 找原文；找不到的刪。
- 每個「準確率、金額、人數」都要有樣本或基準。
