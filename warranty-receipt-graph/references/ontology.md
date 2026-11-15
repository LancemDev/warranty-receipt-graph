# Warranty and receipt lifecycle ontology

This ontology is the small knowledge-graph schema used by `warranty-receipt-graph`. The parent assembles the graph from **verified expert results**. It is a report artifact, not a claim that a graph database or a warranty registry exists on the NAS.

## Principles

- **Provenance required:** every node and edge carries provenance (see [provenance](provenance.md)).
- **Evidence before identity:** keep source artifacts and extracted facts separate from normalized business entities.
- **No fabrication:** never create a path, ID, amount, date, product, serial, merchant, warranty term, or relationship that is not present in verified results.
- **No silent merging:** merge only by the exact rules below. Ambiguity is a finding, not a reason to guess.
- **Partial is valid:** missing routes produce missing subgraphs; represent gaps explicitly.

## Node types

| Type | Purpose | Key properties | Verified source |
|---|---|---|---|
| `Run` | One report request | `run_id`, `question`, `as_of_date`, `expiry_window_days`, `scope_paths` | Parent input |
| `Scope` | Confirmed folder or file scope | `path`, `kind` | `ug-filesystem` via `file-agent` |
| `SourceArtifact` | A real document or image used as evidence | `path`, `media_type`, `name`, `size`, `mtime`, `artifact_kind` | `ug-filesystem`, `ug-document metadata`, `ug-photo meta` |
| `Document` | A document artifact | `path`, `title`, `page_count`, `document_kind` | `ug-document metadata` |
| `Receipt` | A receipt document or receipt photo | `source_ref`, `merchant`, `date`, `total`, `currency`, `receipt_number` | `ug-document extract`, `ug-photo vision-ocr` |
| `Invoice` | An invoice document | `source_ref`, `merchant`, `date`, `total`, `currency`, `invoice_number` | `ug-document extract` |
| `Purchase` | A normalized purchase event | `purchase_id`, `merchant`, `date`, `total`, `currency`, `order_number` | Parent normalization from verified facts |
| `Merchant` | A merchant named in evidence | `name`, `normalized_name` | Parent normalization from verified facts |
| `LineItem` | One line on a receipt or invoice | `description`, `product_name`, `model`, `serial`, `quantity`, `amount` | `ug-document extract`, `ug-photo vision-ocr` |
| `Product` | A product entity merged only by exact model or serial | `name`, `model`, `serial` | Parent normalization from verified facts |
| `Warranty` | Stated coverage for a product or purchase | `term_text`, `start_date`, `end_date`, `coverage`, `status`, `status_rule` | `ug-document qa`, `ug-document extract` |
| `ExtractedFact` | One field-level fact with a citation | `field`, `value`, `confidence`, `citation_ref` | `ug-document extract`, `ug-document qa`, `ug-photo vision-ocr` |
| `Finding` | A reportable gap, mismatch, ambiguity, or status | `finding_type`, `summary`, `severity` | Parent rules over verified facts |
| `Coverage` | Route-level completeness | `route`, `state`, `item_count`, `failures`, `truncated` | Expert result envelopes |
| `ProposedAction` | A suggested follow-up, never executed | `action`, `requires_confirmation`, `executed` | Parent output |

## Edge types

| Edge | From → To | Status | Meaning |
|---|---|---|---|
| `HAS_SCOPE` | `Run` → `Scope` | asserted | The run is bounded to a confirmed scope. |
| `FOUND` | `Coverage` or route → `SourceArtifact` | asserted | An expert returned the real artifact. |
| `DERIVED_FROM` | `ExtractedFact` or `Warranty` → `SourceArtifact` | asserted | The fact or term comes from the artifact. |
| `SUPPORTS` | `ExtractedFact` → `Receipt`/`Invoice`/`Purchase`/`LineItem`/`Warranty` | asserted | The fact supports that entity. |
| `PROVES` | `Receipt`/`Invoice` → `Purchase` | asserted or inferred | The source proves the purchase. |
| `CONTAINS` | `Receipt`/`Invoice` → `LineItem` | asserted | The line item appears on the source. |
| `SOLD_BY` | `Purchase` → `Merchant` | asserted | The purchase names the merchant. |
| `REPRESENTS` | `LineItem` → `Product` | asserted only by exact model or serial | The line item is the product entity. |
| `COVERS` | `Warranty` → `Product`/`LineItem`/`Purchase` | asserted or inferred | The warranty document covers that entity. |
| `EVIDENCED_BY` | `Purchase`/`LineItem`/`Product`/`Warranty` → `SourceArtifact` | asserted | The entity is backed by that source. |
| `MATCHES` | `Receipt`/`Invoice`/`LineItem` → `Purchase`/`LineItem` | asserted, inferred, or ambiguous | The records refer to the same transaction or item. |
| `MISMATCHES` | any entity → `Finding` | asserted | Verified values conflict. |
| `HAS_FINDING` | `Run`/`Purchase`/`LineItem`/`Warranty` → `Finding` | asserted or inferred | The finding applies to the entity. |
| `HAS_COVERAGE` | `Run` → `Coverage` | asserted | Route coverage is part of the report. |
| `PROPOSES` | `Run` → `ProposedAction` | asserted | A follow-up is suggested, not executed. |
| `RELATED_TO` | any → any | inferred only | Non-asserted relationship; must include a rule. |

## Matching rules

1. **Exact identifiers first.** Normalize case and surrounding whitespace only. Do not use fuzzy matching for receipt, invoice, order, model, or serial numbers.
2. **Composite purchase match.** If no identifier exists, a receipt may match a purchase by the exact verified combination of merchant, date, total, and currency. If exactly one candidate matches, create `MATCHES` with `status=inferred` and `rule=exact_merchant_date_total_currency`. If more than one candidate matches, create an `ambiguous_match` finding and do not merge.
3. **Line-item identity.** Merge line items into one `Product` only by exact model or serial. A normalized product-name match is a `possible_match` finding, not a merge.
4. **Warranty linkage.** Link a warranty only when the document explicitly names the product, model, serial, order number, or invoice number. Otherwise create an `unlinked_warranty` finding.
5. **Merchant identity.** Keep merchant names as written. A case-insensitive exact match may share a `Merchant` node; a variant is a `possible_match` finding, not a merge.
6. **No cross-purchase inference.** Do not assume two receipts for the same product are the same purchase. Report a duplicate-candidate finding instead.

## Warranty status rules

Use `as_of_date`, or the current date when omitted, and `expiry_window_days` (default 60).

| Status | Rule |
|---|---|
| `expired` | A verified or inferred end date is before the report date. |
| `expiring_soon` | A verified or inferred end date is on or after the report date and within the window. |
| `active` | A verified or inferred end date is after the window. |
| `unknown` | No explicit end date and no computable start-date-plus-term. Never treat `unknown` as expired. |

An end date is valid only when:

- the warranty document states an explicit end date, or
- the warranty document states a term and the required start date is verified; then compute the end date and set `status=inferred`, `rule=stated_term_from_verified_start_date`.

A purchase date alone is not proof of a warranty start date.

## Inference rules

- **Same-folder grouping:** artifacts under the same verified parent folder may be linked with `RELATED_TO` (`rule=same_parent_folder`, `status=inferred`). This is navigation, not proof.
- **Warranty end-date computation:** only the rule above.
- **Ambiguity:** if two or more candidates satisfy a matching rule, create a finding and keep the candidate set unresolved.
- **No identity resolution beyond evidence:** do not merge people, merchants, products, or purchases without the exact rules above.

## Output shape

See [report format](report-format.md) for the complete JSON shape and a synthetic example in [example report](example-report.md).
