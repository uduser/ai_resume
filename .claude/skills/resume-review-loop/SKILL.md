---
name: resume-review-loop
description: 第四步，核心的 loop engineering。每一輪平行啟動 HR、面試官、求職者三位審閱員加事實查核員，彙整計分卡，寫手修訂，直到停止條件成立或達最大輪數。使用者說「開始 review」「反覆審閱」「跑 loop」時用。可帶參數：起始版本與最大輪數，例如 `/resume-review-loop v2 3`。
---

# resume-review-loop：多視角迭代審閱

## 輸入
- 起始草稿 `work/drafts/resume_vN.md`（預設取最新版）
- `max_rounds`（預設 3；每輪約 5 個代理）
- `work/fact_sheet.md`、`profile.md`

## 每一輪

### Round R：審閱（四個代理同時啟動）
用 Agent tool，`subagent_type` 分別為 `hr-recruiter`、`interviewer`、`candidate`、`fact-checker`。prompt 用 `prompts/04_review_round.md`，替換 `{ROUND}`、`{DRAFT}`、`{OUT_DIR}`（= `work/reviews/round_R/`）。四份輸出：
```
work/reviews/round_R/hr.md
work/reviews/round_R/interviewer.md
work/reviews/round_R/candidate.md
work/reviews/round_R/factcheck.md
```

### 彙整計分卡（orchestrator 自己做，不開代理）
讀四份審閱，依 `templates/scorecard.md` 寫 `work/reviews/round_R/scorecard.md`：
1. 抄分數、算加權平均。
2. 合併修改清單，順序：事實查核 high → 面試官必改 → HR high/medium → 求職者被低估 → 求職者反駁。
3. 裁決衝突：事實 > 誠實歸屬 > 目標職缺命中 > 精簡。求職者有出處的反駁可以推翻 HR／面試官的刪除要求，改採折衷寫法。
4. 需要使用者拍板的事（角色歸屬、來源沒有的實績）用 AskUserQuestion 一次問完，不要每輪都問。

### 停止判斷
全部成立才停：
- 事實查核 PASS
- 面試官 high = 0
- 加權平均 ≥ 85%
- 與上一輪差 < 3%，或 R = max_rounds
- `check_style.py` PASS

沒停就進修訂。

### 修訂（一個 resume-writer 代理）
prompt 用 `prompts/05_revise.md`，替換 `{ROUND}`、`{DRAFT}`、`{SCORECARD}`、`{OUT}`（= `work/drafts/resume_v(N+1).md`）。寫手回報採納與拒絕清單後，跑 `check_style.py`，FAIL 退回一次。

然後 R ← R+1。

## 結束
1. 最終版複製到 `output/<姓名>_履歷_v<N>.md`。
2. 啟動 `editor` 子代理對最終版去 AI 味（必做）。有 `humanizer-zh-tw` 外掛就用外掛，沒有就依 `references/humanizer_checklist.md`；改完比對數字並跑 `check_style.py`。
3. 依 `templates/pre_submit_checklist.md` 寫 `output/投遞前確認.md`：從各輪 candidate 審閱蒐集「面試說法備忘」、從 scorecard 蒐集「刻意沒寫的東西」、從事實表第 10 節蒐集「只有本人能拍板的事」。
4. `/resume-export` 產出 docx 與 pdf。
5. 回報使用者：輪數、每輪加權平均（看得出收斂）、最終版路徑、還需要本人確認的清單。

## 調整旋鈕
- 只想快速過一輪：`max_rounds=1`。
- 投不同職缺：改 `profile.md` 的目標與 JD 關鍵字，從最終版再跑 1～2 輪，不必重做事實表。
- 英文版：寫手 prompt 加「輸出英文，姓名與公司保留官方英文名」，審閱員照跑；`check_style.py` 的 CJK 上限改 0 並忽略標點檢查。
- 審閱員過度保守：在 scorecard 裁決時明寫「candidate 的反駁有出處，採其寫法」。

## Workflow 版本
若環境允許 Workflow tool，`prompts/06_loop_workflow.js` 是同一個 loop 的確定性腳本，可一次跑完。
