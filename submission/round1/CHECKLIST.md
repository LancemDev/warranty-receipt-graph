# Round 1 submission checklist

Deadline shown on the Devpost page: **November 16, 2026 at 10:45 AM GMT+3** (07:45 UTC). Verify the countdown on Devpost before uploading.

## Upload these two files

1. **Project Proposal (PDF)**
   - `submission/round1/UGREEN_Hackathon_2026_Warranty_Receipt_Graph_Proposal.pdf`
   - A4, 2 pages, 24 KB.
   - Ten substantive responses: **491 words** (limit 500; excludes title, headings, and disclosure footer).
   - Under 1 MB.

2. **Pre-test Skill Package (ZIP)**
   - `submission/round1/warranty-receipt-graph-round1.zip`
   - 15 KB, 8 ZIP entries, 6 Markdown files.
   - Top-level folder: `warranty-receipt-graph/`.
   - `SKILL.md` + `references/*.md` only; no scripts, binaries, manifests, or credentials.
   - Under 10 MB; every file under 1 MB; fewer than 100 files.

## Static check

The extracted ZIP was checked with the official Uliya Skill Kit 0.7.7 checker:

- `status: static-pass`
- `errors: 0`
- `warnings: 0`

## Devpost fields

- **Project name:** Warranty Receipt Graph
- **Track:** Automate Your Workflow
- **Short description:** A report-only warranty and receipt lifecycle graph for UGREEN AI NAS.
- **Built with:** Uliya, UGOS, UGREEN AI NAS capabilities, Markdown. The PDF was rendered separately with Python, Python-Markdown, and WeasyPrint.
- **Repository:** optional in Round 1; do not paste secrets.

## Before submitting

- Confirm the PDF opens and both files upload without errors.
- Confirm the ZIP has the `warranty-receipt-graph/` top-level folder.
- Verify checksums with `sha256sum -c SHA256SUMS.txt`.
- Do not add real NAS paths, personal data, credentials, or API keys.
- Round 1 does not require a demo video or a code repository link.
