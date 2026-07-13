---
type: workflow
workflow_id: transcript-ingestion
status: active
owner: shared
generated_by: system-setup
machine_generated: true
human_review_required: true
confidence: high
tags: [workflow, transcript, ingestion]
---

<div class="sb-banner sb-banner-research">Keep the words · mark uncertainty · derive separately</div>

# Transcript ingestion

> [!warning] Verbatim boundary
> Do not silently “correct” spoken words, speaker names, timestamps, or inaudible segments in the preserved transcript.

## Purpose
Store a transcript as immutable source evidence and create separate, traceable summaries and topic links.

## Inputs
- Transcript text/file, recording metadata, provenance, speakers if known, and consent/privacy constraints.

## Outputs
- Transcript source note under `07_Sources/Transcripts/`.
- Summary and topic/link suggestions in `08_Machine/`.

## Allowed folders
- Read: supplied transcript/metadata and relevant policies.
- Write: new `07_Sources/Transcripts/` capture and `08_Machine/Summaries/`/`Link-Suggestions/`.

## Forbidden actions
- Filling gaps by inference; missing facts remain `unknown` until evidence is supplied.
- Editing human-owned notes or immutable sources without explicit approval.
- Guessing speakers, reconstructing inaudible speech, or exposing private/secret material.
- Replacing the preserved transcript with a cleaned version.
- Treating conversational speculation as verified fact.

## Process
1. Record provenance, consent/privacy boundary, recording date, language, transcription method, and coverage.
2. Store the transcript without semantic edits; mark gaps `[inaudible]`, `[unclear]`, or `unknown`.
3. If cleanup is useful, create a separate derived version labeled non-verbatim.
4. Segment by available timestamps/speakers without inventing either.
5. Create a machine summary of topics, decisions, questions, and actions with timestamp references when possible.
6. Label statements as participant claims, decisions, proposals, or uncertain interpretations.
7. Propose concept/project links and contradiction checks separately.
8. Verify private material is handled according to policy before committing to Git.

## Agent prompts
### Codex
> Read `AGENTS.md`; ingest `<transcript>` with the supplied privacy boundary. Preserve a verbatim source note, mark unclear portions, and create a separate timestamp-linked machine summary.

### Claude
> Read `CLAUDE.md`; store the transcript immutably and derive a review-required summary. Do not guess speakers or elevate conversational claims to facts.

### Gemini
> Read `GEMINI.md`; ingest the named transcript, recording provenance and coverage. Keep any cleaned text separate and propose links without editing human notes.

## Validation checklist
- [ ] Provenance, privacy/consent, method, and coverage are recorded.
- [ ] Verbatim transcript is separate from cleanup and synthesis.
- [ ] Speakers/timestamps/unclear speech were not invented.
- [ ] Summary claims link to transcript locations where possible.
- [ ] Sensitive material is not exposed or committed contrary to policy.
