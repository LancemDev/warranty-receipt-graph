# UGREEN SkillHub landscape and differentiation

Research date: 2026-11-16. Source: `https://skills.ugreen.com/us/` (public SkillHub API).

## What the official (first-party) SkillHub already covers

The SkillHub lists **31 “UGREEN SkillHub” first-party skills** plus community/GitHub skills. The first-party set is largely **single-domain capability wrappers**:

| Area | Existing first-party examples |
|---|---|
| Files | basic mutation, read-only search, tags, organization, rename/classify, cleanup, dedupe |
| Photos | timeline, album creation, natural-language photo search |
| Documents | summary, QA, structured extraction, translation, cross-document retrieval/summary |
| Knowledge/notes | topic search QA with citations, audio transcription/knowledge extraction, knowledge graph visualization, note organization/linking, mind maps, review planning, writing |
| Media | video/music playback, recommendations, subtitle search/download |
| Surveillance | event query, identity resolve, event evidence |
| Support | official UGREEN NAS RAG QA |

## Overlap warning for the original concept

The initial `nas-evidence-search-graph` idea overlaps significantly with existing first-party skills:

- `ugreen-topic-search-qa` — knowledge-base retrieval Q&A with source citations.
- `ugreen-cross-document-retrieval-summary` — cross-document search, comparison, conflict flagging, source attribution.
- `ugreen-knowledge-graph-visualization` — extract entities/relationships and render a relationship diagram.
- `ugreen-document-qa` / `ugreen-document-structured-extraction` — document answers and structured fields with citations.

A generic “search + citations + graph” submission risks being judged as a recombination of these, not a new idea.

## Differentiation strategy

Build a **domain-specific ontology** and a **cross-modal workflow** that no first-party skill combines. The knowledge graph should be the *reasoning/audit layer* for a concrete user job, not the headline feature alone.

Good differentiators:

1. **Cross-modal** — link photos, documents, audio, media, and files in one evidence chain.
2. **Lifecycle** — track state over time (warranty expiry, renewals, completeness, versions).
3. **Reconciliation** — match/compare records across formats (receipt photo vs PDF invoice).
4. **Report-only safety** — explain findings and propose actions without executing mutations.

## Candidate concepts

| Concept | User job | Ontology core | Cross-modal sources | Why it is differentiated |
|---|---|---|---|---|
| **Warranty & receipt lifecycle graph** (recommended) | “What did I buy, what is still under warranty, what expires soon, what proof is missing?” | Purchase, Receipt, Invoice, Product/LineItem, Warranty, Merchant, Document/Photo | `ug-photo vision-ocr`, `ug-document extract/reconcile/qa`, `ug-filesystem find` | No first-party skill connects photo receipts + PDF invoices + warranty terms into a lifecycle graph. |
| **Media library completeness graph** | “Which series are incomplete, which files lack subtitles, what is duplicated/orphaned?” | Movie, Series, Season, Episode, MediaFile, Subtitle, DuplicateGroup | `ug-video search`, `ug-filesystem find`, `ug-filemgr mediainfo`, `ug-video subtitle-search` | First-party media skills control playback/recommend/download; none map library completeness. |
| **Paper trail: photo↔document reconciliation** | “Which photographed documents have no scanned copy, and do their fields match?” | PaperDocument, PhotoCapture, Scan, Field, Match, Discrepancy | `ug-photo vision-ocr`, `ug-document extract/reconcile`, `ug-filesystem find` | Cross-modal reconciliation is not covered by document-only or photo-only skills. |
| **Home inventory & insurance evidence graph** | “What do I own, what is it worth, and what evidence is missing for insurance?” | Item, Purchase, Receipt, Warranty, PhotoEvidence, Value | `ug-document extract`, `ug-photo vision-ocr`, `ug-filesystem find`, `ug-document qa` | No first-party inventory/insurance workflow. |
| **Trip memory graph** | “Build a trip timeline from photos, bookings, tickets, and voice notes.” | Trip, Day, Place, Photo, Booking, Document, Expense | `ug-photo search-picture`, `ug-document extract/qa`, `ug-knowledge audio-transcription`, `ug-filesystem find` | Cross-modal memory; first-party photo search is single-domain. |
| **Cross-domain duplicate/version graph** | “Find the same content across files, photos, and media, not just exact duplicates.” | ContentIdentity, FileRepresentation, HashGroup, DocumentVersion | `ug-filemgr scan-dedupe`, `ug-filesystem md5sum/sha256sum`, `ug-photo meta`, `ug-video search` | First-party dedupe is hash-based files only. |

## Recommendation (implemented)

The repo was pivoted to **Warranty & Receipt Lifecycle Graph** (working name `warranty-receipt-graph`):

- Concrete, consumer-relevant “AI NAS home admin” story.
- Uses strong first-party capabilities: OCR, structured extraction (`receipt`/`invoice` schemas), reconciliation, document QA.
- The ontology is meaningful: a real purchase → receipt → product → warranty chain with provenance.
- Round 1 report-only is natural: timeline/report/graph, no file moves or tag writes.
- Easy synthetic demo: receipt photo + PDF invoice + warranty PDF → linked graph and expiry table.

## Round 1 report-only boundary

Allowed: discovery, OCR, extraction, QA, reconciliation, graph/report assembly.
Not executed: move/delete/tag mutation, album creation, subtitle download, save-text, or any other state-changing action. Proposed actions are labeled “requires confirmation” and left unexecuted.
