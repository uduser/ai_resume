---
name: resume-draft
description: 第三步。用 2～3 個不同定位的寫手代理各寫一版履歷，評審選骨架並融合成 work/drafts/resume_v1.md。使用者說「寫初稿」「開始寫履歷」時用。需要先有 work/fact_sheet.md。
---

# resume-draft：初稿競寫

## 流程

### 1. 決定定位角度
從 `profile.md` 的目標職缺推 2～3 個角度，例如：
- 技術主管定位（帶人、決策、治理為主，工程為可信度）
- 實作工程師定位（親手做的系統與數字為主，管理為加分）
- 落地價值定位（每條問題→方案→成果數字）
- 導入顧問定位（變革管理、工具導入、跨部門）

### 2. 平行競寫
同時啟動 2～3 個 `resume-writer` 子代理（Agent tool，subagent_type 填 `resume-writer`），prompt 用 `prompts/03_draft.md`，替換 `{ANGLE}` 與輸出路徑 `work/drafts/draft_<angle>.md`。

### 3. 評審選骨架
啟動 2～3 個評審代理（可直接用 `hr-recruiter`、`interviewer`、`candidate`），每位讀全部草稿與事實表，給每版五維評分、各版值得保留的句子、優勝者與融合建議。

### 4. 融合
一個 `resume-writer` 代理以優勝版為骨架，嫁接其他版被點名保留的句子，修掉評審指出的問題，輸出 `work/drafts/resume_v1.md`。

### 5. 風格門檻
```bash
python .claude/skills/resume-export/scripts/check_style.py work/drafts/resume_v1.md
```
FAIL 就退回寫手。

### 6. 下一步
`/resume-review-loop` 從 v1 開始迭代。

## 省 token 的做法
資料少或時間緊時，可跳過競寫，直接一個寫手用主軸角度寫 v1，讓 review loop 去磨。
