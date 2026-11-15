# Disclosures

## Principal functionality developed for this Hackathon

The following were newly developed for this Hackathon submission:

- the warranty and receipt lifecycle ontology,
- the cross-modal orchestration between files, documents, and photos,
- the matching, ambiguity, missing-proof, and warranty-status rules,
- the provenance model for every node and edge,
- the report format and synthetic example,
- the read-only safety boundary for this version.

No previously developed Skill or submission material is reused. The Skill package was created during the Hackathon period.

## Third-party components and open-source libraries

The Skill package contains **Markdown only**. It does not bundle or redistribute scripts, executables, binaries, manifests, libraries, or external downloads. It uses the UGREEN/NAS capabilities exposed through the registered Uliya experts; those platform capabilities are provided under UGREEN's terms and are not redistributed in this package.

No third-party runtime dependency is required by this Skill.

## AI tools used

- **OpenCode** coding agent with the **DeepSeek V4.1 Flash Free** model was used for research, drafting, file scaffolding, consistency checks, and package validation.
- The public **UGREEN SkillHub** and the **UGOS Skill Creation Tool / Uliya Skill Kit 0.7.7** were used as reference documentation for capability names, package structure, and static checks.
- AI assistance did not use real NAS data, personal data, credentials, or API keys. All examples in this package are synthetic.

## Build-time tooling (not part of the Skill package)

The Round 1 proposal PDF was rendered locally with WeasyPrint (BSD-3-Clause), Python-Markdown (BSD-3-Clause), and Python (PSF-2.0). These tools are not included in the ZIP and are not runtime dependencies of the Skill.

## Data handling

- The Skill processes only user-authorized NAS scope.
- The parent passes verified results between registered experts and does not call NAS CLIs directly.
- No content is sent to an external service by this Skill.
- The Skill is report-only: it does not move, rename, delete, tag, upload, create albums, save text, or perform any other state change.
- Proposed actions are labeled as requiring confirmation and are not executed in this version.
