# Review Loop 計分卡 round N

由 orchestrator 彙整三位審閱員與事實查核員的結果，決定是否進下一輪。

## 分數

| 審閱員 | 總分 | 滿分 | 百分比 | high 問題數 |
|---|---|---|---|---|
| hr-recruiter | | 50 | | |
| interviewer | | 50 | | |
| candidate | | 40 | | |
| fact-checker | PASS / FAIL | | | |

加權平均 = （HR% ＋ 面試官% × 1.5 ＋ 求職者% ＋ 事實查核 PASS 視為 100%、FAIL 視為 0%）÷ 4.5

## 停止條件（全部成立才停）
- [ ] 事實查核 PASS（無 high）
- [ ] 面試官 high 問題 = 0
- [ ] 加權平均 ≥ 85%
- [ ] 本輪與上一輪的加權平均差 < 3%（收斂），或已達 max_rounds
- [ ] `check_style.py` PASS

## 本輪合併後的修改清單（給 resume-writer）
依序：事實查核 high → 面試官必改 → HR high/medium → 求職者被低估 → 求職者反駁（採折衷）

| # | 來源 | 履歷原句 | 改法 | 採納？ |
|---|---|---|---|---|

## 衝突裁決
審閱員之間意見相反時，orchestrator 在此寫裁決與理由（原則：事實 > 誠實歸屬 > 目標職缺命中 > 精簡）。

## 下一輪指示
一段話給 resume-writer。
