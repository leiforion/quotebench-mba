# Field-Scoring Rubric (Section 8.1) — Appendix E draft

Each of schema fields 1–11 (Appendix G) receives exactly one grade per inquiry.
The question is always: **where does this datum live in the documents as received,
and what would a machine need to do to obtain it?** Score the document, not the
estimator's skill.

## The four grades

**A — Cleanly present in machine-readable text.**
The value appears explicitly in selectable text (native PDF, email body) with
unambiguous units and labelling. A correctly configured extractor is near-certain
to capture it.
*Example: a native-PDF pump schedule states "Duty flow: 46 m³/h" in a labelled
column.*

**B — Present but embedded in an image, table or layout.**
The value exists in the documents but sits in a scanned image, a multi-column
table, a drawing annotation, or otherwise requires layout/vision interpretation.
Extraction is plausible at the degraded-accuracy end of the published ranges (5.3).
*Example: the same schedule scanned at an angle; static head readable off a riser
diagram's dimension line.*

**C — Ambiguous; requires judgement.**
The value is present (possibly more than once) but conflicting, ill-defined, or
dependent on engineering interpretation. No extraction accuracy resolves it; under
the 7.7 routing it must reach a person, flagged.
*Example: static head differs between two risers for the same building — the exact
Innovo near-miss; "suitable for potable water" where fluid class must be inferred.*

**D — Absent; requires clarification.**
Not in the documents at all. The machine's job is to detect the gap and draft the
consolidated clarification (7.3), not to extract.
*Example: transfer-set flow rate simply missing from schedule and spec — as in the
Innovo inquiry.*

## Boundary rules (apply in this order)

1. If two sources conflict → **C**, even if each is individually clean.
2. If the value must be computed from other fields (e.g., pipe run summed from a
   drawing) → grade the *inputs*, and grade this field **B** if the inputs are
   graded A/B, **C** if judgement is needed to combine them.
3. If the value exists only in a DWG/DXF → **B** is not available; score **C** and
   set the CAD flag (Phase 1 treats CAD as out of scope, 7.4).
4. A default that a competent estimator would assume without asking (e.g., 400 V
   3-phase for this market) is still **D** if not stated — the audit measures the
   documents, and the design's default-profile behaviour is scored separately in 8.3.
5. When genuinely torn between two grades, take the worse one and note it. The
   audit must under-promise.

## Worked example rows (fields × grades)

| # | Field | Typical grade pattern seen in practice |
|---|---|---|
| 1 | Contractor & project identity | A — email header/body almost always |
| 2 | System type | A/B — schedule column or spec heading |
| 3 | Number of hydraulic systems | B/C — often implicit across drawings |
| 4 | Design flow rate (per system) | A if native schedule; B if scanned |
| 5 | Static head (per system) | B/C — riser diagrams; the classic conflict field |
| 6 | Pipe run length | B/C/D — drawings or absent |
| 7 | Pipe diameter & material | A/B — spec text |
| 8 | Fittings summary | C/D — rarely explicit; default profiles |
| 9 | Fluid & temperature | A/B — spec |
| 10 | Power supply | A/D — stated or assumed |
| 11 | Required delivery date | A/D — email body or absent |

*The pattern column is expectation-setting only; scorers grade what they see.*
