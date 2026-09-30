---
name: resume
description: 唯一入口。使用者說「幫我做履歷」「開始」「/resume」就用這個。它會自己檢查環境、用幾個問題建立側寫、讀 input/ 的資料、寫初稿、跑多視角審閱、輸出 Word 與 PDF。全程只在三個時點問使用者。
---

# /resume：一鍵做履歷

使用者只需要做兩件事：把資料丟進 `input/`、回答你的問題。其他都由你完成。每個階段開始前用一句話告訴使用者現在在做什麼，不要解釋內部流程。

## 0. 環境（靜默）
```bash
python setup.py
```
會安裝 `python-docx pymupdf`、建 `input/ work/ output/`。失敗就把錯誤原文給使用者，並說明手動指令。

## 1. 側寫（第一次問使用者，不可跳過）

**關卡規則**：`profile.md` 開頭必須有 `confirmed_by_user: true`，而且這個值只能在使用者回答完本步的 AskUserQuestion 之後由你寫入。沒有這個標記就不准進第 2 步。就算舊履歷、對話記憶、上一位使用者的檔案裡有足夠資訊，也不能代替提問：目標職缺與定位是使用者現在的意願，不是歷史資料。

流程：
1. 若 `profile.md` 已存在且 `confirmed_by_user: true`，跳過本步。
2. 否則先讀 `input/` 的舊履歷（若有）抽出姓名、聯絡方式、學歷、現職，這些不用問，之後直接填進側寫。
3. 用 **一次** AskUserQuestion 問下列四題（每題可多選，選項留 Other 讓他補充）。有舊履歷時，第 1 題選項可以把舊履歷的「希望職稱」列為其中一個選項，但仍然要問：
   1. 這次想投什麼職缺？（給 4 個選項）
   2. 你現在的身分是？（純工程／主管兼工程／純管理／轉職）
   3. 最想被看到的一到三件事是什麼？（自由填）
   4. 有沒有來源檔案裡沒有、但你確認為真的成果？（自由填，可留空）
4. 依 `templates/profile.template.md` 結構寫 `profile.md`，第一行寫 `confirmed_by_user: true`，答不到的欄位留空。
5. 用兩三行向使用者覆述你理解的定位，讓他有機會糾正；不必等他回覆才繼續。

若 `input/` 是空的，停下來請使用者放檔案，並列出可放的類型：舊履歷、月報週報、簡報、專案清單、績效評語、任何文字紀錄。子資料夾不必分。

## 2. 讀資料（不問）
```bash
python .claude/skills/resume-extract/scripts/extract.py input work/extract --png
```
讀 `work/extract/index.md`。有 ERROR 的檔案（多半是掃描或 DRM PDF）記下來，最後一起告訴使用者，不要中斷。

## 3. 事實表（第二次問使用者）
依來源量開 2～4 個 general-purpose 子代理，prompt 用 `prompts/02_extract_facts.md`。合併成 `work/fact_sheet.md`（結構見 `templates/fact_sheet_template.md`），把 `profile.md` 的「本人確認事實」併入，出處標 `[profile]`。

事實表裡「角色歸屬不明」「數字衝突」「進行中還是完成」的項目，合併成 **一次** AskUserQuestion 問完（最多 4 題，每題多選）。答案寫回事實表第 10 節。

## 4. 初稿（不問）
一個 `resume-writer` 子代理，角度依 `profile.md` 的第一目標職缺，寫 `work/drafts/resume_v1.md`。跑 `check_style.py`，FAIL 退回一次。

## 5. 審閱迴圈（不問）
照 `.claude/skills/resume-review-loop/SKILL.md` 跑，預設 `max_rounds=2`。每輪結束用一行告訴使用者分數：「第 1 輪：HR 41/50、面試官 38/50、求職者 33/40、事實查核 PASS，加權 84%，再修一版」。

## 6. 定稿與輸出（不問）
1. 最終版複製到 `output/<姓名>_履歷.md`。
2. 啟動 `editor` 子代理對它去 AI 味（必做，不是可選）。它會先試 `humanizer-zh-tw` 外掛，沒有就依 `references/humanizer_checklist.md` 自己改，改完比對數字並跑 `check_style.py`。
3. 依 `templates/pre_submit_checklist.md` 寫 `output/投遞前確認.md`。
4. 照 `.claude/skills/resume-export/SKILL.md` 出 `.docx` 與 `.pdf`，頁數超過就依該 skill 的順序縮。
5. 用 SendUserFile 送出 PDF、Word、Markdown、投遞前確認。

## 7. 收尾（第三次問使用者，可省）
用三到五句話說：做了幾輪、最後分數、還有哪幾句只有他能拍板（列在投遞前確認第一節）、抽不出來的檔案。然後問一句要不要再修或換職缺；不要就結束。

## 使用者中途說的話
- 「不夠好／再修」→ 從最新版再跑一輪 loop。
- 「換投 X」→ 改 `profile.md` 目標與關鍵字，再跑一輪 loop，不重做事實表。
- 「太長／太短」→ 改 `profile.md` 的字數上限，寫手重修，不跑 loop。
- 「英文版」→ 寫手依最終中文版出 `output/<name>_resume_en.md`，跑一輪 interviewer＋fact-checker，輸出。
- 「只要 Word」→ 直接跑 export。

## 不要做的事
- 不要要求使用者先分類資料夾、先填長表單、先看流程說明。
- 不要每輪都問問題。
- 不要把內部檔名、代理名稱、計分公式講給使用者聽，除非他問。
