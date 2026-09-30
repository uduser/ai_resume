# Prompt：初稿競寫（每個定位角度一個 resume-writer 子代理）

替換：`{ANGLE}` 定位角度描述、`{OUT}` 輸出路徑。

---

請先讀 `profile.md`、`work/fact_sheet.md`、`references/style_rules.md`、`references/role_attribution.md`、`templates/resume_template.md`。

你的定位角度：{ANGLE}

依 `resume-writer` 代理的寫作規則，寫一份完整履歷 Markdown 到 `{OUT}`。不要前言、不要 HTML 註解。

寫完跑 `python .claude/skills/resume-export/scripts/check_style.py {OUT}`，FAIL 就自己修到 PASS。

回覆三行：路徑；中文字數；你刻意沒寫的東西與原因。

---

# Prompt：評審選骨架（2～3 個評審子代理）

替換：`{LENS}` 評審身分（可直接用 hr-recruiter／interviewer／candidate 三個 agent）、`{DRAFTS}` 草稿路徑清單。

---

{LENS}

請先讀 `work/fact_sheet.md` 與 `profile.md`，再讀這幾版草稿：{DRAFTS}

對每版給五維評分（0～10）：truthfulness（可追溯）、concision（精簡）、job_fit（對目標職缺的吸引力與關鍵字）、dual_role（多重身分是否都清楚）、tone（有人味、無 AI 味、無公文腔）。列出每版值得保留到最終版的句子、每版的問題、優勝者，以及「以優勝版為骨架、嫁接其他版亮點」的具體融合建議。

回傳 JSON：`{scores:[{draft, truthfulness, concision, job_fit, dual_role, tone, total, best_parts[], problems[]}], winner, synthesis_advice}`。

---

# Prompt：融合（一個 resume-writer 子代理）

---

請讀 `work/fact_sheet.md`、`profile.md`、`references/style_rules.md`、`references/role_attribution.md`，以及 `work/drafts/` 下所有 `draft_*.md` 與評審結果（貼在下方）。

以總分最高的版本為骨架，嫁接其他版被評審點名「值得保留」的句子，修掉所有被指出的問題，輸出 `work/drafts/resume_v1.md`。跑 `check_style.py` 到 PASS。

評審結果：
{JUDGEMENTS}
