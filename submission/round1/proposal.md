# Warranty Receipt Graph

**Track:** Automate Your Workflow  
**Submitter:** Lance Munyao  
**Skill name:** `warranty-receipt-graph`  
**Date:** November 16, 2026

## 1. What does your Skill do?

Warranty Receipt Graph builds a report-only warranty and receipt lifecycle report from one authorized NAS folder, linking purchases to receipt or invoice evidence, products, and stated warranty terms, then reporting coverage, expiries, mismatches, and missing proof.

## 2. Who is your target user, and what is their problem?

Users are households and small offices with receipts, invoices, and warranty PDFs scattered across folders and phone-photo uploads. They cannot answer: What did I buy? Where is the proof? Is it still covered? Search returns files, not a lifecycle view.

## 3. What is your solution?

The Skill assembles a provenance-backed graph: Purchase → Receipt/Invoice → Line item/Product → Warranty. It reports active, expiring-soon, expired, and unknown coverage; flags missing purchase proof, amount/date mismatches, ambiguous matches, and unlinked warranties. Every fact links to a citation, OCR reference, or labeled inference. It proposes follow-ups but changes nothing.

## 4. What is the main user flow?

The user selects a folder and optionally asks a question. A file expert discovers bounded candidates. Document and photo experts extract receipt, invoice, warranty, and OCR facts in parallel. The parent applies matching and expiry rules to results and returns a report, JSON graph, evidence table, coverage, and findings.

## 5. How is your idea different from existing tools or common AI solutions?

NAS skills handle file search, extraction, photo OCR, or graph visualization separately. Chat tools answer from one upload but do not connect a receipt photo, invoice PDF, and warranty document into an auditable lifecycle. This Skill is cross-modal, lifecycle-oriented, report-only, and provenance-backed.

## 6. Which UGREEN AI NAS features does your Skill use, and at which step?

Read-only `ug-filesystem` discovery bounds scope. `ug-document` metadata, structured extraction (receipt, invoice, purchase_order, mixed, mixed_reconciliation), warranty QA, and reconciliation handle documents. `ug-photo` vision-ocr and meta handle receipt photos. Parent-side normalization assembles the graph; no write action is used.

## 7. What is your technical approach?

Inputs: authorized folder, optional question, expiry window (default 60 days), as-of date, limits. The parent delegates to `file-agent`, `document-agent`, or `photo-agent`, never `cli.invoke`. Only verified results pass downstream. The ontology defines Purchase, Receipt/Invoice, LineItem/Product, Warranty, Finding, and Coverage, with provenance on every node/edge. Matching uses exact identifiers, then one exact merchant/date/total/currency composite; ambiguity is reported. Expiry is explicit or computed from a stated term plus verified start date, labeled inferred. Actions are read-only; experts use configured models and the parent makes no external model call. Data stays on the NAS.

## 8. What have you built so far? What is not built yet? What still needs testing on a NAS?

Built: `SKILL.md`, ontology, provenance rules, report format, synthetic example, and a static-pass package using Uliya Skill Kit 0.7.7. Not built: runtime execution, UI rendering, and write actions (out of scope). Needs NAS testing: discovery, extraction, OCR, reconciliation, permissions, large-folder limits, failure handling.

## 9. How will you test your Skill if you become a Finalist?

Core 1: invoice PDF, matching photo receipt, and warranty PDF; expect one linked purchase, correct expiry, and evidence. Core 2: warranty references an order with no receipt/invoice; expect a missing-proof finding and no fabricated purchase. Edge: two receipts with the same merchant, date, and total but different order numbers; expect an ambiguous-match finding and no merge.

## 10. What are the known limits, risks, or outside dependencies of your Skill?

OCR/extraction can miss fields; warranty terms may be absent or ambiguous; matching depends on identifiers or exact composites; no merchant portal or warranty registry is queried. Large folders need bounds. It depends on UGREEN's experts and catalog; no third-party runtime dependency. It is not legal, insurance, or warranty advice.

---

**Third-party components:** None bundled in the Skill package. The package is Markdown only and uses UGREEN's registered experts; no third-party runtime library is redistributed.

**Build-time tooling:** WeasyPrint (BSD-3-Clause), Python-Markdown (BSD-3-Clause), and Python (PSF-2.0) for this PDF; not part of the Skill package.

**AI tools:** OpenCode with DeepSeek V4.1 Flash Free was used for research, drafting, scaffolding, and validation. All examples are synthetic; no real NAS or personal data was used.
