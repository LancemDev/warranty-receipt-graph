#!/usr/bin/env python3
"""Build the Round 1 proposal PDF from proposal.md using WeasyPrint."""
from pathlib import Path
import re
import markdown
from weasyprint import HTML

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "proposal.md"
OUTPUT = ROOT / "UGREEN_Hackathon_2026_Warranty_Receipt_Graph_Proposal.pdf"

text = SOURCE.read_text(encoding="utf-8")

# Count only the ten substantive responses (headings, metadata, and disclosures excluded).
parts = re.split(r"\n## (\d+)\. .*?\n\n", text)
counts = []
for i in range(1, len(parts), 2):
    body = parts[i + 1].strip().split("\n---")[0].strip()
    counts.append(len(body.split()))
word_count = sum(counts)

body_markdown = text[text.index("## 1."):]
body_html = markdown.markdown(
    body_markdown,
    extensions=["extra", "sane_lists"],
    output_format="html5",
)

# Wrap the disclosure footer in a styled box.
if "<hr />" in body_html:
    body_html = body_html.replace(
        "<hr />",
        '<hr /><div class="disclosure">',
        1,
    ) + "</div>"

html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="author" content="Lance Munyao">
<title>Warranty Receipt Graph - Round 1 Project Proposal</title>
<style>
  @page {{
    size: A4;
    margin: 17mm 18mm 18mm 18mm;
    @bottom-left {{
      content: "UGREEN Hackathon 2026 on AI NAS  |  Round 1 Project Proposal";
      font-family: "DejaVu Sans", sans-serif;
      font-size: 7.5pt;
      color: #6b7280;
    }}
    @bottom-right {{
      content: "Page " counter(page) " of " counter(pages);
      font-family: "DejaVu Sans", sans-serif;
      font-size: 7.5pt;
      color: #6b7280;
    }}
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: "DejaVu Sans", "Noto Sans", sans-serif;
    font-size: 9.8pt;
    line-height: 1.38;
    color: #111827;
    margin: 0;
  }}
  .top-rule {{
    height: 4px;
    background: linear-gradient(90deg, #0f766e 0%, #14b8a6 55%, #99f6e4 100%);
    margin-bottom: 10px;
  }}
  .badge {{
    display: inline-block;
    font-size: 7.8pt;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #0f766e;
    font-weight: 700;
    margin-bottom: 6px;
  }}
  h1 {{
    font-size: 25pt;
    line-height: 1.05;
    margin: 0 0 4px 0;
    letter-spacing: -0.02em;
    color: #0b1220;
  }}
  .subtitle {{
    font-size: 11pt;
    color: #374151;
    margin: 0 0 12px 0;
  }}
  .meta {{
    display: table;
    width: 100%;
    border-collapse: collapse;
    margin: 0 0 14px 0;
    font-size: 8.6pt;
  }}
  .meta div {{
    display: table-cell;
    padding: 5px 10px 5px 0;
    border-top: 1px solid #d1d5db;
    border-bottom: 1px solid #d1d5db;
    color: #374151;
  }}
  .meta strong {{ color: #0b1220; }}
  .pipeline {{
    display: table;
    width: 100%;
    margin: 0 0 14px 0;
    border: 1px solid #99f6e4;
    background: #f0fdfa;
    padding: 7px 9px;
    font-size: 8.8pt;
    color: #115e59;
  }}
  .pipeline span {{
    display: table-cell;
    text-align: center;
    font-weight: 700;
  }}
  .pipeline .arrow {{
    width: 18px;
    color: #14b8a6;
    font-weight: 400;
  }}
  h2 {{
    font-size: 10.6pt;
    line-height: 1.25;
    margin: 11px 0 3px 0;
    color: #0f766e;
    page-break-after: avoid;
  }}
  p {{
    margin: 0 0 5px 0;
    text-align: left;
  }}
  code {{
    font-family: "DejaVu Sans Mono", monospace;
    font-size: 8.7pt;
    background: #f3f4f6;
    border-radius: 3px;
    padding: 0 3px;
    color: #111827;
  }}
  hr {{
    border: 0;
    border-top: 1px solid #e5e7eb;
    margin: 13px 0 9px 0;
  }}
  .disclosure {{
    font-size: 7.8pt;
    line-height: 1.35;
    color: #4b5563;
    background: #f9fafb;
    border-left: 3px solid #14b8a6;
    padding: 7px 9px;
    margin-top: 8px;
  }}
  .disclosure p {{ margin: 0 0 3px 0; }}
  .disclosure strong {{ color: #111827; }}
  .wordcount {{
    font-size: 7.8pt;
    color: #6b7280;
    margin: 0 0 10px 0;
  }}
  h2, p {{ page-break-inside: avoid; }}
</style>
</head>
<body>
  <div class="top-rule"></div>
  <div class="badge">UGREEN Hackathon 2026 on AI NAS &middot; Round 1</div>
  <h1>Warranty Receipt Graph</h1>
  <p class="subtitle">A report-only warranty and receipt lifecycle graph for UGREEN AI NAS</p>
  <div class="meta">
    <div><strong>Track:</strong> Automate Your Workflow</div>
    <div><strong>Submitter:</strong> Lance Munyao</div>
    <div><strong>Skill:</strong> warranty-receipt-graph</div>
    <div><strong>Date:</strong> November 16, 2026</div>
  </div>
  <div class="pipeline">
    <span>Purchase</span><span class="arrow">&rarr;</span>
    <span>Receipt / Invoice</span><span class="arrow">&rarr;</span>
    <span>Line item / Product</span><span class="arrow">&rarr;</span>
    <span>Warranty</span>
  </div>
  <p class="wordcount">Ten substantive responses: {word_count} words (excluding title, headings, and disclosure footer).</p>
  {body_html}
</body>
</html>
"""

HTML(string=html, base_url=str(ROOT)).write_pdf(str(OUTPUT))
print(f"Wrote {OUTPUT}")
print(f"Substantive response word count: {word_count} (per response: {counts})")
