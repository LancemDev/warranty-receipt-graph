---
name: nas-evidence-search-graph
description: Searches NAS sources for a user query and returns a report-only answer with an evidence knowledge graph, provenance, and coverage; routes across files, documents, knowledge, photos, and media using verified expert results.
---

# Goal

Produce a **safe, report-only** evidence search result for a UGREEN AI NAS user query. The Skill answers with:
- a concise summary grounded in verified evidence,
- a small **knowledge graph** (ontology-mapped nodes/edges) showing how evidence connects,
- **provenance** for every claim/node/edge (real source path, ID, transcript ref, query, or expert evidence reference),
- **coverage/failures/partials** reported explicitly.

Supported scope (Round 1, report-only): discovery and analysis across files, documents, collected knowledge evidence, audio transcripts, photos, and media metadata/search results. This Skill **does not execute state-changing NAS actions** (no move/delete/tag mutation/album creation/subtitle download/save-text execution). It only reports findings and may propose next actions that would require explicit user confirmation in a future execution flow.

# Required input

Collect only information required by the parent workflow:
- `query` (required): the user’s search question or topic.
- `scope_paths` (optional): NAS path(s) or folder(s) to prioritize/search within. If omitted, ask the user to provide a target path or confirm a safe default scope returned by experts.
- `intent_hints` (optional): `files`, `documents`, `knowledge`, `audio`, `photos`, `media`, or `mixed` (default `mixed`).
- `limits` (optional): user-requested limits (e.g., max files/evidence items). Apply conservative limits and report truncation.

Do not pre-collect private parameters owned by a child expert.

# Capability evidence

Selected capabilities and their catalog agent mapping (CLI -> agent):
- `ug-filesystem` -> `file-agent`
- `ug-filemgr` -> `file-agent`
- `ug-document` -> `document-agent`
- `ug-knowledge` -> `knowledge-agent`
- `ug-photo` -> `photo-agent`
- `ug-video` -> `media-agent`

# Expert orchestration

Delegate with self-contained instructions using only:
`delegate --target <agent-id> --instruction '<task>'`

Pass only **verified real results** to dependent steps. Preserve real user entities, paths, constraints, and query text. Do not invent file paths, IDs, document facts, transcript text, photo/media identities, or relationships.

## 1. Resolve scope and discover sources (`file-agent`)
Delegate to `file-agent`:
- Resolve the user-provided `scope_paths` (or a safe user-confirmed scope). Use read-only filesystem discovery appropriate to the request (find/list/stat/category as needed) and return only verified paths, names, types, sizes, and timestamps.
- If the query targets documents/audio/media/images, return candidate files grouped by type with real paths/IDs.
- If no candidates are found, return an explicit empty result and stop dependent analysis except any independent read-only route the user explicitly requested.

## 2. Route read-only evidence collection by intent (parallel where independent)

### 2a. Documents (`document-agent`)
When intent includes `documents` or candidates include document files, delegate to `document-agent`:
- Analyze only verified document paths from step 1 (or user-provided verified paths).
- Use read-only document capabilities (e.g., QA/extraction/metadata as appropriate) to answer the query with evidence and coverage.
- Return: answer fragments, extracted facts, evidence references, coverage, and failures/partials. Do not fabricate missing fields.

### 2b. Knowledge evidence and audio (`knowledge-agent`)
When intent includes `knowledge` or `audio`, or broad NAS evidence is useful, delegate to `knowledge-agent`:
- For general evidence, collect evidence scoped to verified paths/query constraints and return evidence, sources, coverage, failures, and warnings.
- For audio candidates with verified paths, transcribe only those real files and return transcript text/refs/segments, quality, coverage, and failures.
- For NAS how-to questions (not user-data search), answer from official knowledge only when appropriate; label source type clearly.
- Return only verified evidence/transcription results.

### 2c. Photos (`photo-agent`)
When intent includes `photos`, delegate to `photo-agent`:
- Run read-only photo search/screen/classify/hint/metadata operations relevant to the query.
- Return only verified photo/album/figure/object/location/OCR results and IDs provided by the expert. Do not guess identities.

### 2d. Media (`media-agent`)
When intent includes `media`, delegate to `media-agent`:
- Run read-only video/music search operations relevant to the query.
- Return only verified media results/IDs/paths. Do not perform playback control, subtitle download, or other state changes.

## 3. Assemble the evidence knowledge graph (parent, report-only)
After required delegations complete, assemble a report without calling NAS execution CLIs:
- Normalize verified results into the ontology in `references/ontology.md`.
- Create nodes/edges only from verified expert outputs or clearly labeled inferences (e.g., same-folder grouping) with the inference rule stated.
- Attach provenance to every node/edge using `references/provenance.md`.
- Build: (1) user-facing answer, (2) evidence table, (3) graph output (JSON and/or Mermaid), (4) coverage/failures/partials, (5) proposed next actions (confirmation required; not executed).

# Completion and failure

Handle every delegation state explicitly:
- `completed`: include the verified result in the report/graph. A completed expert with empty evidence is a valid empty result — report “no evidence found” for that route.
- `failed`: do not present success. Report the failure, affected route, and any safe partial evidence already verified. Stop dependent steps that require the missing result.
- `cancelled`: report cancellation and do not continue dependent work that needs that result.
- `waiting_user`: pause the workflow, present what is needed, and resume only with the user’s input.
- `waiting_approval`: do not execute or bypass approval. Report the pending approval state. For this report-only Skill, avoid requesting state-changing actions.

Partial-result rule: if some routes complete and others fail/cancel/wait, return a **partial report** clearly labeled with completed routes, missing routes, coverage, and provenance for included evidence.

The Skill is complete only when the final report is assembled from available verified results and all terminal/waiting states are reported accurately.
