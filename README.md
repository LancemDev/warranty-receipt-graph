# Warranty Receipt Graph

A **report-only** Uliya Skill for the **UGREEN Hackathon 2026 on AI NAS**. It builds an auditable warranty and receipt lifecycle report from one user-authorized NAS folder, linking purchases, receipt or invoice evidence, products, and stated warranty terms.

## What it does

Given a folder path and an optional question, the Skill routes read-only work across:

- files (`ug-filesystem` -> `file-agent`)
- documents (`ug-document` -> `document-agent`)
- photos (`ug-photo` -> `photo-agent`)

It returns:

1. a grounded answer,
2. a warranty timeline with active, expiring-soon, expired, and unknown states,
3. a purchase and line-item table,
4. findings for missing proof, amount/date mismatches, ambiguous matches, and unlinked warranties,
5. an evidence table and a provenance-backed knowledge graph,
6. coverage, failures, and partial results,
7. proposed next actions that are never executed in this version.

## Why this is different

Generic NAS search, document QA, photo OCR, and knowledge-graph visualization already exist as separate single-domain skills. This Skill combines them into a **cross-modal lifecycle**:

`Purchase -> Receipt/Invoice -> Line item/Product -> Warranty`

Every node and edge carries provenance. Matching uses exact identifiers first, then one exact merchant/date/total/currency composite. Ambiguity is reported, not silently merged. Warranty expiry is either explicit or computed from a stated term plus a verified start date and labeled as inferred.

## Safety / Round 1 scope

- **Report-only:** no move, delete, rename, tag mutation, album creation, subtitle download, save-text, or other state change.
- **Verified results only:** never invent paths, IDs, facts, dates, amounts, product identities, warranty terms, or relationships.
- **Explicit states:** handles `completed`, `failed`, `cancelled`, `waiting_user`, and `waiting_approval`.
- **Synthetic demo data:** all examples are fictional; no real credentials or personal data.
- **No external transmission:** data stays on the NAS and its registered experts.

## Package

The Uliya Skill package is in [`warranty-receipt-graph/`](warranty-receipt-graph/):

- `SKILL.md` — required entry point.
- `references/ontology.md` — node, edge, matching, and warranty-status rules.
- `references/provenance.md` — provenance fields and inference labeling.
- `references/report-format.md` — report sections and JSON shape.
- `references/example-report.md` — synthetic complete example.
- `references/disclosures.md` — third-party, AI-tool, and principal-functionality disclosure.

The package is Markdown only, contains no scripts or binaries, and passes the Uliya Skill Kit 0.7.7 static checker with zero errors and zero warnings.

## Round 1 submission materials

- Proposal PDF: [`submission/round1/UGREEN_Hackathon_2026_Warranty_Receipt_Graph_Proposal.pdf`](submission/round1/UGREEN_Hackathon_2026_Warranty_Receipt_Graph_Proposal.pdf)
- Pre-test Skill Package: [`submission/round1/warranty-receipt-graph-round1.zip`](submission/round1/warranty-receipt-graph-round1.zip)
- Proposal source: [`submission/round1/proposal.md`](submission/round1/proposal.md)
- Synthetic report JSON: [`examples/warranty-report.json`](examples/warranty-report.json)

## Local checks

- Static Skill check (Uliya Skill Kit 0.7.7): `static-pass`, 0 errors, 0 warnings.
- Synthetic report validator: `python3 tests/validate_example_report.py` (checks sections, graph references, provenance fields, warranty status, and synthetic-data guards).

## Research

The SkillHub landscape and the reason for the pivot from a generic evidence graph are documented in [`docs/skillhub-landscape.md`](docs/skillhub-landscape.md).
