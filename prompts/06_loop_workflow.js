// Workflow 版本的 review loop（Claude Code Workflow tool）。
// 使用者需明確要求跑 workflow；一般情況用 /resume-review-loop 以子代理逐輪執行即可。
// 啟動方式：Workflow({ script: <本檔內容>, args: { startDraft: "work/drafts/resume_v1.md", maxRounds: 3, target: 85 } })

export const meta = {
  name: 'resume-review-loop',
  description: '每輪 HR／面試官／求職者／事實查核四路審閱，計分卡彙整後寫手修訂，收斂即停',
  phases: [
    { title: '審閱', detail: '四個審閱代理平行' },
    { title: '彙整', detail: '計分卡與裁決' },
    { title: '修訂', detail: '寫手依計分卡修稿' },
  ],
}

const startDraft = (args && args.startDraft) || 'work/drafts/resume_v1.md'
const maxRounds = (args && args.maxRounds) || 3
const target = (args && args.target) || 85

const REVIEWERS = [
  { type: 'hr-recruiter', file: 'hr.md', max: 50, weight: 1 },
  { type: 'interviewer', file: 'interviewer.md', max: 50, weight: 1.5 },
  { type: 'candidate', file: 'candidate.md', max: 40, weight: 1 },
  { type: 'fact-checker', file: 'factcheck.md', max: 1, weight: 1 },
]

const REVIEW_SCHEMA = {
  type: 'object',
  properties: {
    out_file: { type: 'string' },
    score: { type: 'number', description: '總分；事實查核 PASS=1 FAIL=0' },
    high_count: { type: 'number' },
    issues: { type: 'array', items: { type: 'object', properties: { severity: { type: 'string' }, quote: { type: 'string' }, fix: { type: 'string' }, reason: { type: 'string' } }, required: ['severity', 'quote', 'fix'] } },
    keep: { type: 'array', items: { type: 'string' }, description: '做得好、下一版不要改壞的句子' },
  },
  required: ['out_file', 'score', 'high_count', 'issues'],
}

const reviewPrompt = (r, round, draft, prevDir) => `這是履歷 review loop 的第 ${round} 輪。待審草稿：${draft}。上一輪資料夾：${prevDir}（第一輪為「無」）。
請依你的代理說明讀完必要檔案，把完整審閱寫入 work/reviews/round_${round}/${r.file}，然後以結構化輸出回傳分數、high 數、問題清單（每筆含原句與可直接貼上的改法）與應保留的句子。事實查核的 score 用 1（PASS）或 0（FAIL）。`

let draft = startDraft
let version = parseInt((draft.match(/_v(\d+)\.md$/) || [0, 1])[1], 10)
let prevAvg = null
const history = []

for (let round = 1; round <= maxRounds; round++) {
  phase('審閱')
  const prevDir = round === 1 ? '無' : `work/reviews/round_${round - 1}/`
  const reviews = (await parallel(REVIEWERS.map(r => () =>
    agent(reviewPrompt(r, round, draft, prevDir), { label: `${r.type} r${round}`, phase: '審閱', schema: REVIEW_SCHEMA, agentType: r.type })
      .then(v => ({ ...r, ...v }))
  ))).filter(Boolean)

  phase('彙整')
  let weighted = 0, wsum = 0
  for (const r of reviews) { weighted += (r.score / r.max) * 100 * r.weight; wsum += r.weight }
  const avg = wsum ? weighted / wsum : 0
  const fact = reviews.find(r => r.type === 'fact-checker')
  const interviewer = reviews.find(r => r.type === 'interviewer')
  const factPass = fact ? fact.score >= 1 : false
  const noHigh = interviewer ? interviewer.high_count === 0 : false
  const converged = prevAvg !== null && Math.abs(avg - prevAvg) < 3
  history.push({ round, avg: Math.round(avg * 10) / 10, factPass, interviewerHigh: interviewer ? interviewer.high_count : null })
  log(`round ${round}: 加權 ${avg.toFixed(1)}%, 事實查核 ${factPass ? 'PASS' : 'FAIL'}, 面試官 high ${interviewer ? interviewer.high_count : '?'}`)

  const scorecard = await agent(`你是 review loop 的 orchestrator。讀 work/reviews/round_${round}/ 四份審閱，依 templates/scorecard.md 寫 work/reviews/round_${round}/scorecard.md：抄分數、合併修改清單（順序：事實查核 high → 面試官必改 → HR high/medium → 求職者被低估 → 求職者反駁採折衷）、裁決衝突（事實 > 誠實歸屬 > 目標職缺命中 > 精簡）、寫下一輪指示。加權平均 ${avg.toFixed(1)}%。回傳 scorecard 路徑。`, { label: `scorecard r${round}`, phase: '彙整' })

  if (factPass && noHigh && avg >= target && (converged || round === maxRounds)) {
    log(`收斂於 round ${round}`)
    break
  }
  if (round === maxRounds) { log('達最大輪數，以最後一版交付'); break }

  phase('修訂')
  const next = draft.replace(/_v\d+\.md$/, `_v${version + 1}.md`)
  await agent(`這是履歷 review loop 第 ${round} 輪的修訂。上一版 ${draft}，計分卡 work/reviews/round_${round}/scorecard.md。依 resume-writer 代理說明的優先順序逐條處理修改清單，輸出 ${next}，不新增事實表沒有的內容，字數不超過 profile.md 上限，跑 check_style.py 到 PASS。回傳新版路徑與採納／拒絕摘要。`, { label: `writer v${version + 1}`, phase: '修訂', agentType: 'resume-writer' })
  draft = next; version += 1; prevAvg = avg
}

return { finalDraft: draft, history }
