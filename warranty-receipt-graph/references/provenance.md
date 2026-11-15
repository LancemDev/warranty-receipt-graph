# Provenance rules

Every node and edge in the warranty lifecycle graph must carry provenance so the user can audit where a claim came from. Provenance is part of the result, not an optional appendix.

## Required fields

```json
{
  "source_type": "expert_result|user_input|parent_inference",
  "agent": "file-agent|document-agent|photo-agent|parent",
  "cli": "ug-filesystem|ug-document|ug-photo|none",
  "action": "find|metadata|extract|qa|reconcile|vision-ocr|meta|compare|none",
  "route_state": "completed|failed|cancelled|waiting_user|waiting_approval|not_run",
  "source_ref": "verified path, citation, OCR source reference, or parent rule reference",
  "query": "the original or delegated question when relevant",
  "timestamp": "optional report timestamp",
  "notes": "optional coverage, partial, failure, or rule note"
}
```

## Rules

1. **Use verified references only.** `source_ref` must come from expert output or user input. Never synthesize paths, citations, IDs, or OCR references.
2. **Preserve route state.** If a route failed, evidence returned before the failure keeps its own provenance and is not marked as if the full route completed.
3. **Label inference.** For `parent_inference`, set `cli=none`, `action=compare` or `action=none`, and put the rule in `notes`; on the edge use `status=inferred` and a `rule` field.
4. **Quote carefully.** A quoted receipt, invoice, or warranty term must reference the verified document citation or OCR source reference. Do not paraphrase a warranty term without keeping the source link.
5. **Coverage is first-class.** Include a `Coverage` row for every route, including routes that were not run, returned empty, or failed.
6. **Empty is not failure.** An expert `completed` result with no matching evidence is a valid empty route. Record it as completed with zero items.
7. **No sensitive leakage.** Round 1 examples are synthetic. Do not include real credentials, personal data, or private NAS paths from a real system.

## Provenance for computed warranty status

A computed warranty status needs two layers:

- the verified facts used (term, start date, source citations),
- a parent provenance entry with `source_type=parent_inference`, `cli=none`, `action=compare`, `notes=stated_term_from_verified_start_date`.

The report must expose both. A status without its term and start-date evidence is not reportable.

## Provenance for matches

- Exact identifier match: `source_type=expert_result` when the expert returned the identifier, plus a parent edge with `status=asserted` and the identifier.
- Composite match: `source_type=parent_inference`, `status=inferred`, `rule=exact_merchant_date_total_currency`.
- Ambiguous match: no merged entity; a `Finding` with `source_type=parent_inference` and the candidate references.
