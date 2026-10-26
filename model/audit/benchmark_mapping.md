# Benchmark Mapping (Section 8.1) — Appendix E draft

Converts the audit's field-grade distribution into the automation-rate range used
in 8.2 and 9.5. The mapping is deliberately conservative and every assumption is
stated; the audit measures *where the data lives*, published evidence supplies
*how reliably machines read data that lives there* (Section 5.3).

## Mapping table

| Grade × document type | Assumed per-field extraction success | Basis |
|---|---|---|
| A in clean digital PDF / email text | 0.92 – 0.97 | Upper published range for key-field extraction on clean text; haircut from near-ceiling benchmark results because production schemas are wider than benchmark schemas |
| A in any other carrier | 0.88 – 0.95 | Same, with layout risk |
| B in scanned schedule / drawing | 0.65 – 0.85 | Published degradation on noisy scans and wide schemas; the interval is wide because variance across pipelines is itself a documented finding |
| B in email fragments | 0.75 – 0.90 | Free text is easier than raster tables, harder than labelled fields |
| C (ambiguous) | 0 (not automatable) | By definition routes to a person under 7.7; counted as the judgement share |
| D (absent) | 0 (not extractable) | Counted as the clarification share; automated *detection* of D-fields is part of the 7.3 benefit, not of the extraction rate |

## Computation

For tier *t*:

- automation_rate_low(t)  = Σ over fields [ share_A(t) × p_low(A) + share_B(t) × p_low(B) ]
- automation_rate_high(t) = Σ over fields [ share_A(t) × p_high(A) + share_B(t) × p_high(B) ]
- central(t) = midpoint, reported with both ends

Also report per tier: judgement share (C) and clarification share (D) — these
parameterize the 7.7 routing volumes and the 7.3 clarification benefit in the
simulation.

## Stated assumptions (to appear verbatim in 8.1)

1. Published benchmarks measure adjacent tasks (document QA, receipt key-fields),
   not pump-schedule extraction; the mapping assumes task similarity at the level
   of *reading mechanics* (locating a labelled value in text or layout), which is
   why grade C is excluded entirely rather than given a partial rate.
2. Field-level success is treated as independent when compounding to whole-inquiry
   correctness; 5.3's 0.95¹² arithmetic shows why whole-inquiry automation is not
   claimed anywhere — the design reviews per-field confidence, not whole documents.
3. Rates assume the validation gates of 7.4 are in place (schema constraints,
   unit checks); the ranges are for *accepted* extractions reaching review, not
   raw model output.
4. If the optional zero-build probe contradicts the mapping in either direction,
   the audit range widens to include the probe result; it never narrows.
