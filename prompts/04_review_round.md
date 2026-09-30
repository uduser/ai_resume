# Prompt：審閱回合（四個代理同時啟動）

替換：`{ROUND}` 輪次、`{DRAFT}` 草稿路徑、`{OUT_DIR}` 輸出資料夾（`work/reviews/round_{ROUND}/`）、`{PREV_DIR}` 上一輪資料夾（第一輪填「無」）。

四個代理用同一段 prompt，`subagent_type` 分別填 `hr-recruiter`、`interviewer`、`candidate`、`fact-checker`；`{OUT_FILE}` 分別為 `hr.md`、`interviewer.md`, `candidate.md`、`factcheck.md`。

---

這是履歷 review loop 的第 {ROUND} 輪。

待審草稿：`{DRAFT}`
上一輪審閱（若有）：`{PREV_DIR}`，請先看上一輪的 scorecard.md，避免重複提已經處理過的問題，並確認上一輪「做得好的三件事」有沒有被改壞。

請依你的代理說明中的「開始前一定要讀」讀完必要檔案，再依你的輸出格式寫入 `{OUT_DIR}/{OUT_FILE}`。

補充要求：
- 每個問題都要附「原句」與「建議改法」，改法要能直接貼進履歷。
- 嚴重度只用 high／medium／low；high 的定義是「投出去會在 reference check 或第一輪面試被打臉」。
- 最後一行寫 `SCORE: <總分>/<滿分>`（事實查核寫 `VERDICT: PASS|FAIL`），方便 orchestrator 解析。

回覆只要兩行：輸出檔案路徑；SCORE 或 VERDICT。
