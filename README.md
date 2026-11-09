# nas-evidence-search-graph

A **report-only** Uliya Skill concept for the **UGREEN Hackathon 2026 on AI NAS**. It answers NAS search questions by delegating to registered UGREEN/Uliya experts and assembling an **evidence knowledge graph** with provenance and coverage.

## What it does

Given a user query (and optional NAS scope/intent), the Skill routes read-only discovery and analysis across:
- files (`ug-filesystem`, `ug-filemgr` -> `file-agent`)
- documents (`ug-document` -> `document-agent`)
- knowledge/evidence/audio transcripts (`ug-knowledge` -> `knowledge-agent`)
- photos (`ug-photo` -> `photo-agent`)
- media (`ug-video` -> `media-agent`)

It returns:
1. a grounded answer/summary,
2. an ontology-mapped evidence graph (nodes/edges),
3. provenance for every node/edge,
4. coverage/failures/partial results,
5. proposed next actions (not executed).

## Safety / Round 1 scope

- **Report-only:** no state-changing NAS actions are executed (no move/delete/tag mutation, no album creation, no subtitle download, no save-text execution).
- **Verified results only:** never invent paths, IDs, facts, transcript text, identities, or relationships.
- **Explicit states:** handles `completed`, `failed`, `cancelled`, `waiting_user`, and `waiting_approval`.
- **Synthetic demo data:** sample data/examples must be synthetic/anonymized; no real credentials or sensitive personal data.

## Repo contents

- `SKILL.md` — Uliya orchestration Skill (required entry point).
- `references/ontology.md` — evidence KG ontology.
- `references/provenance.md` — provenance rules.
- `examples/sample-report.json` — synthetic example output.

## Hackathon notes

Round 1 submission requires the PDF and Pre-test Skill Package (ZIP) per the UGREEN Hackathon Official Rules and Skill Developer Package. This repository is the working source for that package; confirm final file structure/manifests against the official package before submission.
