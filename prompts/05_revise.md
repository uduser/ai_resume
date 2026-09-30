# Prompt：修訂回合（一個 resume-writer 子代理）

替換：`{ROUND}`、`{DRAFT}` 上一版路徑、`{SCORECARD}` 本輪計分卡路徑、`{OUT}` 新版路徑。

---

這是履歷 review loop 第 {ROUND} 輪的修訂。

上一版：`{DRAFT}`
本輪計分卡（含合併後的修改清單與衝突裁決）：`{SCORECARD}`
四份審閱在同一個資料夾，需要細節時再讀。

請依 `resume-writer` 代理說明的「修訂時的優先順序」逐條處理計分卡的修改清單，輸出 `{OUT}`。規則：
- 計分卡標「採納」的一定改；標「拒絕」的不改；標「折衷」的照計分卡給的寫法。
- 不新增事實表沒有的內容；字數不得超過 `profile.md` 的上限。
- 上一輪「做得好的三件事」保持原句或只做最小修改。
- 寫完跑 `python .claude/skills/resume-export/scripts/check_style.py {OUT}` 到 PASS。

回覆三行：路徑；中文字數；採納幾條、拒絕幾條與拒絕原因（一句）。
