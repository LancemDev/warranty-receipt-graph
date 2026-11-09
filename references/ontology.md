# Evidence Search Ontology (report-only)

This ontology defines the small knowledge-graph schema used by `nas-evidence-search-graph`. The graph is assembled by the parent Skill from **verified expert results**. It is a report artifact, not a claim that a graph database exists on the NAS.

## Principles

- **Provenance required:** every node and edge must include provenance (see `provenance.md`).
- **No fabrication:** do not create nodes/edges for entities, facts, IDs, paths, or relationships not present in verified expert results unless marked `inferred` with an explicit rule.
- **Evidence over assertion:** prefer `ExtractedFact`/`Evidence` nodes linked to sources rather than asserting high-level claims without evidence.
- **Partial is valid:** missing routes or failed experts produce missing subgraphs; represent gaps explicitly.

## Node types

| Type | Description | Key properties | Typical verified source |
|---|---|---|---|
| `Query` | User search request | `query_id`, `text`, `intent_hints`, `scope_paths`, `timestamp` | Parent input |
| `File` | NAS file/folder candidate | `path`, `name`, `kind`, `size`, `mtime`, `source_route` | `ug-filesystem` (file-agent) |
| `Document` | Document analyzed for the query | `path`, `title`, `page_count`, `metadata_ref` | `ug-document` metadata/page-count |
| `ExtractedFact` | Structured or QA-derived fact | `schema`/`field`, `value`, `confidence` (if provided), `evidence_ref` | `ug-document` extract/qa/reconcile |
| `Evidence` | Evidence item returned by knowledge collection or QA | `summary`, `source_ref`, `coverage` | `ug-knowledge` collect-evidence, `ug-document` qa |
| `Transcript` | Audio transcription result | `source_path`, `transcript_ref`, `language`, `quality` | `ug-knowledge` audio-transcription |
| `TranscriptSegment` | Segment/quote from transcript | `transcript_ref`, `segment_id`/`time` (if provided), `text` | `ug-knowledge` audio-transcription |
| `Photo` | Photo search result | `photo_id`/ref, `album_ref`, `matched_signals` | `ug-photo` search-* |
| `MediaAsset` | Video/music search result | `asset_id`/ref, `title`, `kind`, `path` (if provided) | `ug-video`/`ug-music` search |
| `Concept` | Normalized topic/entity label used for navigation | `label`, `kind` (`topic`/`project`/`entity_mention`), `status` (`evidenced`/`inferred`) | Parent normalization; must cite evidence |
| `Coverage` | Route coverage/failure summary | `route`, `status`, `item_count`, `failures`, `warnings` | Expert result envelopes/summaries |

## Edge types

| Edge | From -> To | Assertion | Meaning |
|---|---|---|---|
| `HAS_SCOPE` | `Query` -> `File`/scope | asserted/inferred | Query scoped to path or discovered candidate. |
| `ROUTED_TO` | `Query` -> `Coverage` | asserted | A route was delegated/executed. |
| `FOUND` | `Coverage`/agent route -> `File`/`Document`/`Photo`/`MediaAsset`/`Evidence` | asserted | Expert returned the item. |
| `DERIVED_FROM` | `Document`/`ExtractedFact`/`Transcript`/`Evidence` -> `File` | asserted | Analysis derived from a verified source file/path. |
| `SUPPORTS` | `Evidence`/`ExtractedFact`/`TranscriptSegment` -> `Query` or `Concept` | asserted | Evidence supports answering the query or an evidenced concept. |
| `MENTIONS` | `Document`/`TranscriptSegment`/`Evidence` -> `Concept` | evidenced/inferred | Text/entity mention; include quote/ref when available. Inferred mentions must be labeled and rule-based. |
| `LOCATED_IN` | `File`/`Photo`/`MediaAsset` -> `File` (folder) | asserted | Verified location/container relationship. |
| `RELATED_TO` | any -> any | inferred only | Non-asserted relationship (e.g., same folder/name pattern). Must include `rule` and never be presented as fact. |

## Inference rules (allowed, labeled)

- **Same-folder grouping:** files under the same verified parent folder may be linked with `RELATED_TO` (`rule=same_parent_folder`, `status=inferred`).
- **Name/topic normalization:** a `Concept` may normalize repeated evidenced terms; keep original evidence links.
- **No identity/entity resolution beyond evidence:** do not merge people/orgs/assets unless the same verified ID/ref is returned by experts.

## Output shape (recommended)

```json
{
  "query": {"text": "...", "intent_hints": ["mixed"], "scope_paths": ["..."]},
  "summary": "...",
  "graph": {
    "nodes": [{"id": "n1", "type": "File", "props": {"path": "..."}, "provenance": {...}}],
    "edges": [{"id": "e1", "type": "DERIVED_FROM", "from": "n2", "to": "n1", "status": "asserted", "provenance": {...}}]
  },
  "coverage": [{"route": "document-agent", "state": "completed", "failures": []}],
  "proposed_next_actions": [{"action": "...", "requires_confirmation": true, "executed": false}]
}
```
