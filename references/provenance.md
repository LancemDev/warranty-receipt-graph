# Provenance rules (report-only)

Every node and edge in the evidence graph must carry provenance so users and judges can audit where information came from.

## Required provenance fields

```json
{
  "source_type": "expert_result|user_input|parent_inference",
  "agent": "file-agent|document-agent|knowledge-agent|photo-agent|media-agent|parent",
  "cli": "ug-filesystem|ug-filemgr|ug-document|ug-knowledge|ug-photo|ug-video|ug-music|none",
  "action": "find|qa|collect-evidence|...",
  "route_state": "completed|failed|cancelled|waiting_user|waiting_approval|not_run",
  "source_ref": "verified path/id/ref/transcript ref/evidence ref as returned by expert",
  "query": "original or delegated query text when relevant",
  "timestamp": "optional report timestamp",
  "notes": "optional coverage/partial/failure note"
}
```

## Rules

1. **Use verified references only.** `source_ref` must come from expert output or user input. Never synthesize IDs/paths.
2. **Preserve route state.** If a route failed, nodes derived before failure may still be included with their own provenance; do not mark failed-route evidence as completed.
3. **Label inference.** For `parent_inference`, set `cli=none`, `action=none`, and include the inference rule in `notes` and on the edge (`status=inferred`, `rule=...`).
4. **Quote carefully.** Transcript/document quotes included in summaries should reference a verified `transcript_ref`/segment or document evidence reference.
5. **Coverage is first-class.** Include route-level coverage/failure/warning summaries alongside item-level provenance.
6. **No sensitive leakage in samples.** Round 1 demos and sample data must use synthetic/anonymized content. Do not include real credentials, private NAS paths from real systems, or personal data.
