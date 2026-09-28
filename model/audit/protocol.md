# Feasibility Audit Protocol (Section 8.1) — Appendix E draft

**Purpose.** Establish, from Khoory's own historical documents, an evidence-based range
for the achievable extraction-automation rate, by tier — the single most important
input to the process simulation (8.2) and the financial model (9.5). No software is
required; this is a structured scoring exercise on documents as they were received.

**Output.** (1) Field-grade distribution by tier; (2) document-complexity typology with
volume shares; (3) the audited automation-rate range (low / central / high) per tier,
via the benchmark mapping; (4) inter-rater agreement statistics.

---

## 1. Sampling frame

Draw **30 inquiries** from the 2025 RFQ log (n = 640), stratified by the Table 4.1
tiers:

| Tier | Population share | Audit sample | Rationale |
|---|---|---|---|
| Tier 1 — Simple | 55% (352) | 8 | Cleanest documents; small sample suffices |
| Tier 2 — Standard | 33% (211) | 12 | The economic core; largest sample |
| Tier 3 — Complex | 12% (77) | 10 | Deliberately oversampled: 47% of quoted value and the messiest documents |

Selection rules:
1. Within each stratum, sort by receipt date and take every k-th inquiry
   (k = stratum size / sample size), starting from a randomly chosen offset.
   Record the offset. Do not hand-pick.
2. The sample must include at least 3 inquiries where required data existed only in
   a CAD file (swap the nearest same-tier inquiry in if the systematic draw misses
   this; record every swap and its reason).
3. An inquiry enters the audit with **exactly the documents attached to the original
   email** — no cleaned-up versions, no documents obtained later.
4. Exclusions (log them): inquiries withdrawn before quoting; duplicates of a
   sampled inquiry from the same project.

## 2. Document-complexity typology

Before field scoring, classify **each attachment** of each sampled inquiry:

| Type | Definition |
|---|---|
| Clean digital PDF | Native (searchable) PDF; text selectable |
| Scanned schedule / drawing | Raster image content, any resolution |
| Email fragments | Requirements stated in email body or forwarded thread |
| CAD-dependent | Required fields recoverable only from DWG/DXF |

Record per inquiry: attachment count by type, the **primary carrier** (the type
holding the majority of required fields), and a CAD-dependency flag. The tally of
primary carriers by tier is the typology table reported in 8.1.

## 3. Scoring procedure

1. Two estimators score **independently**, using `rubric.md` and one row of
   `scoring_sheet.csv` per inquiry per scorer. No conferring until both are done.
2. Score fields 1–11 of the Appendix G schema (field 12 is system-generated and is
   not scored). For fields 4–8, which repeat per hydraulic system: score the
   **worst** grade across systems and record the system count — this is the
   conservative convention, stated as such in the paper.
3. Timebox: no more than 30 minutes per inquiry; the audit scores where data *is*,
   not whether it can be worked out with effort. If finding a field takes longer
   than a real estimation pass would, that is grade C or D by definition.
4. After both scorers finish: compute per-field agreement (percentage of identical
   grades) overall and by tier — the counterpart of the 91% tier-classification
   agreement in 4.2. Resolve disagreements jointly; record the resolved grade
   separately from the originals. Report agreement **before** resolution.

## 4. Aggregation

For each tier: the share of scored fields in each grade (A/B/C/D — see rubric).
Apply the mapping in `benchmark_mapping.md` to grades A and B to produce the
low / central / high automation rate per tier. Grades C and D are not extraction
candidates: C measures the judgement share (routes to engineer under 7.7),
D measures the clarification share (drives the 7.3 consolidated-clarification
benefit). Report all four shares — the C and D shares are findings, not waste.

## 5. Optional zero-build probe

If desired: run 5–10 redacted sampled documents through an off-the-shelf LLM
(no code) purely to sanity-check the benchmark mapping. Label any such result a
**directional probe**, not a prototype, and report it separately from the audit.
The audit stands without it.
