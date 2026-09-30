---
name: resume-export
description: 最後一步。把 Markdown 履歷轉成 Word（python-docx，微軟正黑體）與 PDF（Word COM），跑風格檢查，控制頁數。使用者說「輸出 Word」「轉 PDF」「排版」時用。
---

# resume-export：輸出 Word 與 PDF

## 前置
- `pip install python-docx pymupdf`
- Windows + Microsoft Word（PDF 用 Word COM）。沒有 Word 就用 LibreOffice：`soffice --headless --convert-to pdf <docx>`。

## 流程
1. 風格門檻（FAIL 不輸出）：
   ```bash
   python .claude/skills/resume-export/scripts/check_style.py output/<檔名>.md
   ```
2. 轉 Word：
   ```bash
   python .claude/skills/resume-export/scripts/md2docx.py output/<檔名>.md output/<檔名>.docx
   ```
3. 轉 PDF 並看頁數：
   ```bash
   powershell -NoProfile -ExecutionPolicy Bypass -File .claude/skills/resume-export/scripts/docx2pdf.ps1 output/<檔名>.docx
   ```
4. 頁數超過上限時，依序處理，每改一次重跑 2～3：
   - 合併「學歷」「語言」成一節一行
   - 代表專案「做法」各砍到一行
   - 管理面 bullet 刪掉沒有結果的那條
   - 調 `md2docx.py` 頂部的字級與邊界（預設 9.5pt、邊界 1.3～1.5cm，不要再小）
5. 用 PyMuPDF 把 PDF 每頁轉 PNG 看一眼版面（標題不要孤行、bullet 不要跨頁斷在第一行）。
6. 檔名改成 `姓名_職稱_履歷.pdf`，送給使用者。

## md2docx.py 支援的 Markdown
`#`/`##`/`###`、`-` 清單（兩層）、`**粗體**`、表格、`---`、段落。HTML 註解會被略過，但仍應在 check_style 階段清掉。
