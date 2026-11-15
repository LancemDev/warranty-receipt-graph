---
name: warranty-receipt-graph
description: Builds a report-only warranty and receipt lifecycle report from a user-authorized NAS folder, linking purchases, receipt or invoice evidence, products, and stated warranty terms so users can see coverage, upcoming expiries, missing proof, and mismatches without changing files. Use when a user asks what is under warranty, what expires soon, which purchases lack receipts, or how receipts, invoices, and warranty documents connect.
---

# Goal

Produce a **report-only warranty and receipt lifecycle graph** for one user-authorized NAS folder. The report links:

- purchases,
- receipt and invoice evidence (documents or photos),
- products and line items,
- stated warranty terms and coverage,
- gaps, mismatches, and ambiguous matches,
- provenance for every fact, node, and edge.

The Skill is intentionally read-only. It does not move, rename, delete, tag, upload, create albums, save reports, or execute any other state change. Proposed actions are listed but never executed in this version.

# Required input

Collect only what the workflow needs:

- `scope_paths` (required): one or more real, user-authorized NAS folder or file paths. If the user names a folder without a real path, use the file expert to return verified candidate paths, then wait for the user to choose. Never guess a path.
- `question` (optional): the user question, passed verbatim. Default: "Build a warranty and receipt lifecycle report for this folder."
- `expiry_window_days` (optional): how many days count as "expiring soon". Default `60`. State the window in the report.
- `as_of_date` (optional): ISO date used for expiry status. If omitted, use the current date in the parent environment and label it as the report date.
- `limits` (optional): user-requested evidence limits. Apply conservative defaults and report truncation.

Do not pre-collect private parameters owned by a child expert. Do not include credentials, API keys, or real personal data in examples.

# Generation-time capability evidence

- `ug-filesystem` → `file-agent`
- `ug-document` → `document-agent`
- `ug-photo` → `photo-agent`

# Workflow

Use only the concrete single-line delegations below. Only the parent assembles the report and graph. The parent never executes NAS CLIs directly. Pass only real, verified results from the previous step to dependent experts. Preserve real paths, IDs, citations, and user constraints.

## 1. Discover and bound the scope

`delegate --target file-agent --instruction 'Discover read-only candidate evidence in the user-authorized warranty scope. If the user supplied a real folder or file path, use that exact scope. If the user only named a folder, list verified accessible folder candidates and return them without guessing. Within a confirmed scope, return only verified document and image paths with names, types, sizes, and modification times. Group candidates as receipt, invoice, purchase order, warranty, manual, or receipt photo when the filename or metadata supports that grouping; otherwise return them as unclassified. Respect max-depth and conservative limits, and report truncation. If no candidates are found, return an explicit empty result. Do not read document bodies, run OCR, move, rename, delete, tag, or write anything.'`

If the user has not confirmed a scope, present the verified candidates and stop in `waiting_user`. Do not run document or photo analysis until the scope is confirmed.

## 2. Analyze documents and photos in parallel where independent

Run these two delegations only after step 1 returns verified candidate paths.

`delegate --target document-agent --instruction 'Using only the verified document paths returned by file discovery, run read-only metadata, structured extraction, warranty QA, and reconciliation where applicable. Extract purchase date, merchant, total, currency, receipt or invoice number, order number, line items, product name, model, serial, quantity, and any stated warranty term, start date, end date, or coverage. Use receipt, invoice, purchase_order, mixed, or mixed_reconciliation schemas when they fit. When the verified set matches a supported reconciliation pair, use read-only reconciliation for amount consistency. Return field-level facts with source citations, page or location references, confidence when provided, coverage, and failures. Do not infer missing values, do not merge documents by similarity alone, and do not write, translate, or save anything.'`

`delegate --target photo-agent --instruction 'Using only the verified image paths returned by file discovery, run read-only vision OCR and capture metadata on candidate receipt, invoice, warranty, or product-label photos. Return OCR text, source references, capture timestamps, and failures. Do not create albums, tag or move photos, guess identities, or treat OCR text as verified until the expert returns it. If an image is unreadable or not a receipt, return that as a coverage note rather than inventing fields.'`

If one route fails, keep the verified results from the other route and produce a partial report. If both routes return no usable evidence, report an explicit empty result and stop.

## 3. Assemble the lifecycle graph (parent, report-only)

Normalize only verified expert results using [the ontology](references/ontology.md). For each node and edge, attach provenance using [the provenance rules](references/provenance.md). Apply these matching rules:

- Match a receipt to an invoice or purchase record only by exact receipt/invoice/order number, or by an exact verified combination of merchant, date, total, and currency. If only one signal matches, mark the edge `status=inferred` and state the rule. If several candidates match, mark the group `ambiguous` and do not merge.
- Link a line item to another line item only by exact model or serial. If only a normalized product name matches, keep separate nodes and add a `possible_match` finding with the rule.
- Link a warranty document to a purchase or product only when the document explicitly names the product, model, serial, order number, or invoice number. Otherwise keep it unlinked and report the gap.
- Compute a warranty end date only when the warranty document states a term and the required start date is verified, or when the document states an explicit end date. Mark computed dates `status=inferred` with the rule `stated_term_from_verified_start_date`. Never infer coverage from purchase date alone.
- Classify warranty status as `active`, `expiring_soon`, `expired`, or `unknown` relative to the report date and `expiry_window_days`. `unknown` is a valid result and must not be presented as expired.
- Report missing purchase proof only when a verified warranty document references a purchase or order that has no linked receipt or invoice. Report "no warranty document found" as a coverage gap, not as a defect.

Build the report using [the report format](references/report-format.md). Include a concise answer, a warranty timeline, a purchase table, findings, an evidence table, coverage, the graph, and proposed next actions. Link every claim to a verified source reference or a labeled inference.

# Completion and failure

Handle every delegation state explicitly:

- `completed`: accept only the expert's real result. An explicit empty result is a valid completed result. Report "no evidence found" for that route and stop dependent work that needs it.
- `failed`: do not present the route as successful. Report the failure, affected route, and any verified partial evidence already returned. Stop dependent steps that need the missing result.
- `cancelled`: report the cancellation and do not retry or claim completion. Do not assume any effects were rolled back.
- `waiting_user`: pause and ask for the missing scope or clarification. Do not launch parallel replacements. Resume the same delegation only after the user answers.
- `waiting_approval`: do not grant approval or continue past the checkpoint. This Skill contains no state-changing action, so report the unexpected checkpoint and stop rather than executing anything.

A partial report is not a success claim. Label it clearly with completed routes, missing routes, coverage, and provenance for the evidence that was actually returned. Never invent paths, IDs, facts, dates, amounts, product identities, warranty terms, or relationships.

# Output safety

- Report-only: no write effects, no approval-required actions, no external upload.
- Use only user-authorized scope and the minimum evidence needed.
- Keep all processing on the NAS and its registered experts; do not send data to external services.
- Use synthetic or anonymized examples only. Do not include real credentials, personal data, or API keys.

# References

Read these when assembling or reviewing the report:

- [Ontology](references/ontology.md) — node, edge, matching, and status rules.
- [Provenance](references/provenance.md) — required fields and inference labeling.
- [Report format](references/report-format.md) — output sections and JSON shape.
- [Synthetic example](references/example-report.md) — a complete report with fictional data.
- [Disclosures](references/disclosures.md) — third-party components, AI tools, and principal functionality.
