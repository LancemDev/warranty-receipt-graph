# Devpost project page copy

> **Use this on the UGREEN Hackathon 2026 on AI NAS page, not on the Relate by Neo4j Hackathon page.** The Neo4j page has a different deadline and does not match this project.

## Project name

Warranty Receipt Graph

## Tagline / short description

A report-only warranty and receipt lifecycle graph for UGREEN AI NAS.

## About the project

```markdown
## Inspiration

Receipts, invoices, warranty PDFs, and photos of paper receipts end up in different folders on a NAS. When a product fails, the important questions are simple but hard to answer: What did I buy? Where is the proof? Is it still covered? Which document matches which purchase? I built Warranty Receipt Graph to turn that scattered evidence into an auditable lifecycle view instead of another list of search hits.

## What it does

Warranty Receipt Graph is a report-only Uliya Skill for UGREEN AI NAS, built for the Automate Your Workflow track. Given one user-authorized folder, it links:

Purchase → Receipt/Invoice → Line item/Product → Warranty

It reports active, expiring-soon, expired, and unknown warranty coverage; flags missing purchase proof, amount/date mismatches, ambiguous matches, and unlinked warranty documents; and shows the evidence behind every claim. It never moves, deletes, renames, tags, uploads, or saves anything. Proposed follow-ups are listed but not executed.

## How I built it

The Skill delegates read-only work to three registered experts:

- `file-agent` discovers bounded document and image candidates.
- `document-agent` extracts receipt, invoice, purchase-order, and warranty facts, runs warranty QA, and reconciles supported document pairs.
- `photo-agent` runs OCR and capture-metadata lookup on receipt photos.

The parent assembles the graph from verified results only. I wrote an ontology for purchases, receipts, invoices, line items, products, warranties, findings, and coverage; provenance rules for every node and edge; explicit matching rules; and a report format with a synthetic example. Matching uses exact identifiers first, then one exact merchant/date/total/currency composite. Ambiguity is reported, not merged. Warranty expiry is either explicit or computed from a stated term plus a verified start date and labeled inferred. The package passes the official Uliya Skill Kit 0.7.7 static checker with zero errors and zero warnings.

## Challenges

The hard part was not OCR; it was avoiding false certainty. Two receipts can share a merchant, date, and total but be different purchases. A warranty document can name a product without proving the purchase. A missing warranty document is not the same as missing purchase proof. I handled these as explicit findings and kept unresolved candidates separate instead of guessing. I also had to keep the parent inside the delegation boundary: it can normalize verified results but must never call NAS CLIs directly.

## What I learned

A useful knowledge graph needs provenance and ambiguity handling more than visual complexity. Read-only workflows also need clear boundaries: saying "no writes" is not enough unless the orchestration, report, and proposed actions all reflect it.

## What's next

The next step is NAS validation: real folder discovery, document extraction schemas, OCR quality, reconciliation, permissions, large-folder limits, and failure handling. Runtime UI and any state-changing actions are intentionally out of scope for this report-only Round 1 version.
```

## Built with tags

```text
Uliya
UGOS
UGREEN AI NAS
Markdown
Knowledge Graph
Provenance
Document AI
OCR
JSON
Mermaid
```

## Try it out links

- **Code:** leave blank unless the GitHub repo is made public. The current repo is private, so judges cannot open it.
- If you make it public, use: `https://github.com/LancemDev/warranty-receipt-graph`
- **Demo:** none for Round 1. The required artifacts are the PDF and ZIP uploaded in the Submit step.

## Image gallery

Optional. If you want a cover, use a 3:2 image with the title, the pipeline `Purchase → Receipt/Invoice → Line item/Product → Warranty`, and the line `UGREEN Hackathon 2026 · Automate Your Workflow`.

## Video demo link

UGREEN Round 1 does not require a demo video. If the UGREEN form does not require this field, leave it blank. If it blocks you, record a short 30–60 second walkthrough of the PDF, architecture, and synthetic report; do not use a fake or unrelated link.
