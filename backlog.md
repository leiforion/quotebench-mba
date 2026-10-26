# Backlog — RFQ Automation Paper

Tasks keyed to the phases in `plan.md`. Each carries a ready-to-use prompt for a
future working session. Conflict IDs (C1–C16) refer to the consistency ledger in
`improvements.md` §2. Dependencies gate start, not planning.

Legend: P1 = blocking the critical path · P2 = required for submission · P3 = quality

> **Style contract (binding on every prose task — see plan.md for the full text):**
> no em dashes anywhere; MBA register not journal register ("ex-ante" only in its
> single 3.1 definition); no meta-commentary about the paper's own rigor; "we"
> where the authors acted; setup thin, mechanics said once in Sections 8/9 and
> appendices. Applied to Sections 2–7 on 6 Sep (t15a/t15c); T12/T14/T17 must draft
> to it, and T15/T18 verify it (grep for "—" must return zero).

**Status (6 Sep 2026):** T01 ✅ · T02 ✅ · T03 ✅ (open: O3–O8 in decisions.md) ·
T04 ✅ (`model/conflict_resolutions.md`) · T05 ✅ **applied to the live Doc** (35
edits, snapshot in `source_docs/snapshots/`) · T06 superseded — the workbook is
now the 10.3 venture exhibit (D7); its EUR conversion and reconciliation move
into T13. · **T07 ✅ + T08 ✅ applied to the live Doc** (Phase 2 complete, 6 Sep):
all scaffolding/author-notes/meta stripped; heading styles normalized (H1
sections / H2 subsections / TITLE); missing Section 8 heading added; 4.6 moved
ahead of 4.7 with a provisional D6 stub; Appendix B/G extracts (incl. schema
table, renamed Table G.1) relocated after the Appendices list; Table 7.2→7.1;
new **Appendix J** holds the 7.5 database detail; Sections 2–5 & 7 compressed
(doc 12,675→11,086 words; prose sections all within ~10% of budget — residual
trim goes to T15). Bonus consistency fixes: 84–87%→86–88% queue share in 4.7,
pricing-engine cross-ref 7.5→7.6 in 4.4, routing cross-ref 7.6→7.7 in 5.4.
Snapshots + post-T08 DOCX in `source_docs/snapshots/`. · **T09 ✅ applied to the
live Doc** (6 Sep): Section 6 complete — Options A–E in final prose, Table 6.1
decision matrix (A wins cost and risk), 6.3 concession with a derived labour-only
crossover of ~1,000–1,300 pump RFQs/yr (provisional span, SEC6-01; refined in 9.5)
and the explicit "Option A becomes the recommendation" kill condition. ·
**T10 ✅ instruments drafted** in `model/audit/` (protocol, rubric, benchmark
mapping, scoring-sheet CSV) — *authors now run the audit: 2 estimators, 30
sampled RFQs, ~2 days*. · **T13 harness ✅ built** at `model/monte_carlo.py`:
internal-case driver model per D7, `--validate` reproduces the as-is baseline
from locked register rows (all checks pass), `--run` gated behind `--provisional`
until 8.1 audit / 9.3 / 9.4 inputs replace placeholders — provisional outputs
must not enter the paper. Authors must also supply branch pump revenue
(revenue_branch_eur) for the %-of-revenue benefit lines. Next: T12 (Sections
10–13) unblocked. 6 Sep (later): authors direct that no audited inputs will be
supplied; T11/T13 superseded by the SIM-0..6 series (see Phase 4 and
model/simulation_plan.md); T10 instruments retained as pilot-charter material per D12.

---

## Phase 0 — Access & instrumentation

### T01 · Enable APIs and ingest the P&L workbook — P1 · owner: authors + agent
Blocked on: authors enabling Sheets + Drive APIs (links in improvements.md §8).

> The Google Sheets and Drive APIs are now enabled for service account
> insead@measureofmind.iam.gserviceaccount.com. Re-run
> scripts/download_docs.py to fetch the P&L workbook
> (ID 1c0zkBq99q-QMyIM_ZavoNNthPUTxDFuW) into source_docs/. Then produce
> model/pnl_inventory.md: for every tab, list its purpose, row/column drivers,
> units, currency, hard-coded values vs formulas, and every figure that also
> appears in the paper (source_docs/paper.md). Flag each mismatch against the
> consistency ledger in improvements.md §2 and add new conflicts as C17+.
> Do not modify the workbook.

### T02 · Build the Assumptions Register — P1
Blocked on: T01 (to include P&L figures); can start on paper figures immediately.

> Create model/assumptions.csv as the single source of truth for every number in
> the paper and P&L. Columns: id (A1, A2…), name, value, unit, tag (M/E/A/S),
> source (record/interview/audit/model), sections_used, status (locked/pending/
> conflicted), note. Extract every quantitative claim from source_docs/paper.md
> (rates, volumes, hours, costs, percentages, thresholds) and every driver from
> the P&L inventory. Where the consistency ledger (improvements.md §2) shows a
> conflict, create one row with status=conflicted and record both values in the
> note. Do not resolve conflicts yourself — resolutions come from the decisions
> log (T03).

### T03 · Decisions log from author answers — P1 · owner: authors
Started: see `model/decisions.md`. Decided: EUR-only currency (D1), Section 4
figures are final (D2), appendices/references excluded from page count (D3),
restrained "we" voice (D4), direct Docs API write-back with snapshots (D5).
Still open: O1–O8 in the decisions log (FX rate confirmation, API enablement,
interviews, simulation-platform docs, branch name, pilot budget, referencing
standard, Monte Carlo timing).

---

## Phase 1 — Consistency & realignment

### T04 · Resolve the consistency ledger in the register — P1
Blocked on: T02, T03.

> Using model/assumptions.csv and the decisions log, resolve conflicts C1–C16
> from improvements.md §2. C1 is decided: EUR only, converted at the fixed rate
> in decision D1 and stated once in Section 3 — convert every monetary figure in
> the register and choose rounded values that keep internal arithmetic exact
> (touch hours × rate = cost per quote must still check out after rounding).
> For each remaining conflict: set the canonical value, mark the register
> row locked, and write a one-line rationale. Special cases: C7 (loaded rate)
> must show the arithmetic bridge from AED 96,000/yr to the hourly rate actually
> used; C8 must state explicitly how the 640-inquiry branch reconciles with the
> 16-estimator company-wide figures; C10 requires rebuilding Table 4.4 so touch
> hours still total 28 and the elapsed time matches the claimed 7 calendar days
> with issue two days after the Tuesday deadline. Output a propagation worksheet:
> for each conflict, the exact sentences in paper.md that must change and their
> replacement text.

### T05 · Propagate canonical numbers through Sections 1–8 — P1
Blocked on: T04.

> Apply the propagation worksheet from T04 to the manuscript. Edit only numbers,
> units, and the sentences that carry them — no restructuring, no voice changes.
> Every quantitative claim you touch must end up carrying its evidence tag
> (M/E/A/S) and, where the paper's convention requires it, its assumption ID.
> Specifically bring Section 6.1's untagged percentages (C14) and Section 2.2's
> lost-tender figure (C15) into compliance or cut them. Rewrite 7.9's Innovo
> walk-through arithmetic per C11 and C12 so it is a Tier 3 case start to finish.
> Produce a diff summary listing every changed sentence.

### T06 · Cross-check the P&L against the register — P1
Blocked on: T01, T04.

> Verify that every driver in the P&L workbook matches its locked register row:
> loaded labour rate, estimator count, inquiry volumes and tier mix, touch hours,
> error-cost percentage (1.2% of revenue), discount leakage (1.9%), win rates,
> gross margins by tier. Produce model/pnl_reconciliation.md listing each driver,
> the workbook value, the register value, and pass/fail. For failures, state
> which side should change and why. Do not edit the workbook until the authors
> confirm the direction of each fix.

---

## Phase 2 — Structure & length

### T07 · Strip scaffolding and fix document mechanics — P2
Blocked on: T05 (avoid merge conflicts).

> In the manuscript, remove: the "Revised Paper Architecture (v3)" preamble, all
> "Author's note (remove before submission)" blocks, and all embedded writing
> instructions ("Test:", "Score honestly", "worth real marks", "signature move",
> "intellectual climax", "Rule: every citation…"). Before deleting each, confirm
> its instruction is captured as a backlog task or already done — list any that
> are not. Then: reorder 4.5/4.6/4.7 per the decisions log, renumber tables and
> exhibits sequentially (fix Table 7.1/7.2 inversion), normalize heading styles
> (H1 sections, H2 subsections), and move the Appendix B and G extracts out of
> the body, leaving one-line pointers.

### T08 · Compression pass to word budget — P2
Blocked on: T07.

> Compress Sections 2–7 to the word budget in improvements.md §7 (2→950, 3→750,
> 4→1,800, 5→850, 7→1,450). Priority cuts, in order: (1) the duplicated Innovo
> retelling — 2.0 becomes a ~200-word hook, 4.5 keeps the table and the two
> near-misses; (2) the duplicated research-question statements in 2.3 — keep the
> prose form only; (3) Section 7.5 reduced to ~150 words with technical detail
> moved to a new appendix; (4) 5.3 benchmark taxonomy cut to one sentence plus
> citations, keeping the degradation point and the 0.95¹² arithmetic; (5) Option
> B in 6.1 restated as a delta from Option A; (6) pillars two and three in 2.1
> halved. Preserve all tables, all evidence tags, and the thesis/antithesis
> passages listed as "held well" in improvements.md §4. Do not touch voice yet.
> Report before/after word counts per section.

---

## Phase 3 — Missing analytical sections

### T09 · Complete Section 6 (Options D/E, matrix, concession) — P1
Blocked on: T04 (numbers), not on Phase 2.

> Write the missing parts of Section 6 at MBA-thesis standard, matching the
> analytical register of Sections 3–4 (no first-person informality): Option D
> (full custom AI platform, ~90 words) and Option E (the proposed hybrid, ~120
> words); the 6.2 decision matrix scoring A–E on cycle-time impact, margin
> impact, error-rate impact, cost, implementation risk, and strategic optionality
> — scored so Option A genuinely wins on cost and risk, with a two-sentence
> scoring rationale per criterion; and the 6.3 concession paragraph stating what
> each rejected option does better and the explicit RFQ-volume threshold below
> which hiring (Option A) dominates — derive that threshold from the register's
> estimator cost and capacity figures rather than asserting it. Every number
> tagged; total section ≤ 750 words. Note: T08 deliberately left Section 6
> uncompressed (currently ~925 words of draft prose + outline bullets) because
> this task rewrites it wholesale — restate Option B as a delta from Option A
> and Option C tightly, per the T08 cut list, while drafting.

### T10 · Feasibility audit instruments (8.1) — P1 · owner: agent drafts, authors run
Blocked on: T04.

> Draft the instruments for the Section 8.1 feasibility audit as appendix-ready
> documents: (1) a field-scoring rubric — for each of the 12 RFQ schema fields
> (Appendix G), the four-way classification (cleanly machine-readable / embedded
> in image or table / ambiguous, requires judgement / absent, requires
> clarification) with worked examples; (2) a sampling frame for 25–30 historical
> RFQs stratified by the Table 4.1 tiers; (3) the document-complexity typology
> template (clean digital PDF / scanned schedule / email fragments /
> CAD-dependent) with volume-share tallying; (4) the mapping table from each
> document type to the published accuracy ranges cited in 5.3, with mapping
> assumptions stated. Design so two estimators can score independently and
> inter-rater agreement can be reported, mirroring the 4.2 classification method.

### T11 · Process simulation build & calibration (8.2) — SUPERSEDED 6 Sep
Absorbed into the SIM series below (authors' direction: no audited inputs will be
supplied; the simulator generates its capability assumptions and calibrates to the
measured current state). The 8.2–8.4 drafting moves to SIM-6/T14.

### T12 · Draft Sections 10–13 — P2 — DONE (6 Sep, t27_sections1013)
Blocked on: T09, T11 (Section 9 numbers arrive later via T14; leave marked slots).

> Draft Sections 10, 11, 12, 13 to the budgets in improvements.md §7 (800/800/
> 280/380 words), following their existing outlines exactly — they are well
> designed, with two D20 amendments: 10.3 drops the venture-economics
> exhibit (licensing stays as a prose option only), and 11.1 develops the
> Phase 1 budget from PILOT-01 (EUR ~30k derived, basis stated). Section 10.2 gets the fullest treatment: the three futures, why
> moving first makes the platform-of-record outcome attainable, and the honest
> conditions under which manufacturers-go-direct wins anyway — this must resolve
> the tension planted in 2.1 using the IDR framing from 5.1. Section 11.3 must
> close the liability circularity: if professional-indemnity requires an
> engineer's signature, state the ceiling that places on the automation rate
> used in 8.2/9.5. Leave bracketed slots for financial figures pending the
> Monte Carlo. Match the register and tagging discipline of Sections 3–4;
> write 13's closing Innovo paragraph in the conditional tense per the
> narrative device.

---

## Phase 4 — Financial model simulator (SIM series, replaces T11 + T13)

Approach and rationale: `model/simulation_plan.md` (Option C, unified
inquiry-level simulation with embedded economics). Frame per decision D7:
Khoory's **internal** investment case; the subscription workbook feeds only the
10.3 licensing exhibit. `model/monte_carlo.py` (built 6 Sep) is absorbed by
SIM-3; its validation checks migrate into the SIM-1 gate. Prompts are final; the
five open decisions were resolved 6 Sep as D12–D16 in model/decisions.md.

### SIM-0 · Repo and environment scaffolding — P1 — DONE (6 Sep)
Delivered: `simulator/` tree with venv, `run.sh`, `sim/` package, anonymized
`data/register_snapshot.csv` (66 rows, values only, client names scrubbed),
manifest protocol (`sim/manifest.py` writes seed + git commit + parameter
checksums per run to `results/`), local git repo initialized (publish to
GitHub later per D15).

> Create the simulator tree at `simulator/` inside this workspace (D15; published to GitHub later). Set up an isolated environment: `python3 -m venv .venv`,
> `source .venv/bin/activate`, `pip install -r requirements.txt` (numpy, simpy, matplotlib,
> pytest, pyyaml per D16), and a Makefile or `run.sh` so a
> reader reproduces everything with one command. Layout: `sim/` package,
> `data/` (parameter CSVs generated from model/assumptions.csv, values only,
> no client-identifying text), `scenarios/*.yaml`, `results/` (gitignored),
> `tests/`, README explaining what the simulator claims and does not claim.
> Fixed-seed protocol: every run writes a manifest (seed, git hash, parameter
> file checksums). No code that computes anything yet; this phase is structure.

### SIM-1 · As-is engine + calibration gate — P1 — DONE (6 Sep)
Gate PASSED 15/15 (seed 42, 12 simulated years): all tier cycle medians/P90s,
touch, cost per quote, queue share, volume within tolerance; pickup median
13.5 vs 14 wh and clarification share 37% vs 38% emerge as diagnostics.
Two structural deviations from the prompt below, forced by the measured data
and documented in `model/simulation_plan.md` (SIM-1 build notes): desk
discipline is small-job-first (not FIFO), and the 41 wh clarification wait is
calibrated in aggregate (not additive) because additive components cannot
reproduce BASE-15/16.

> Build the discrete-event model of Exhibit 4.1 in `sim/asis.py`: Poisson
> arrivals by tier at 29/18/6 per month; steps = assignment queue, reading,
> clarification loop (p = 0.38, contractor wait lognormal with 41 wh median),
> calculation, selection, pricing approval, dispatch; estimators as resources
> with skill profiles per D14: branch = 1 senior + 1 mid (speed and error multipliers); FIFO within desk;
> pre-emption by large Tier 3 arrivals. Fit step time distributions (lognormal)
> such that a simulated year reproduces, within ±10%: tier cycle medians
> 18/39/88 wh and P90s 34/71/162 wh (BASE-15/16), touch 2.1/5.5/11.4 h
> (BASE-17), queue share 86–88% (BASE-22), cost per quote 25/66/137 EUR
> (BASE-18). Encode these as a pytest suite (`tests/test_calibration.py`);
> the CLI must refuse to run to-be scenarios while any assertion fails, and
> `sim report calibration` prints the measured-vs-simulated table that becomes
> the 8.2 calibration exhibit. Document every fitted parameter with its source
> register row in `data/parameters_asis.yaml`.

### SIM-2 · Capability and variance layer (to-be mode) — P1 — DONE (6 Sep)
Delivered: `sim/capability.py` (document classes, per-field extraction +
confidence, 7.7 routing verbatim, defect draws) and `sim/tobe.py` (system lane
+ engineer lanes on the shared DES). 21/21 tests pass including both
degradation gates: system-down reproduces the calibrated as-is baseline, and
extraction-forced-to-zero routes 100% manual at as-is touch and defect rates.
Two findings recorded in `model/simulation_plan.md` (SIM-2 build notes):
central-variant routing is far more manual than the paper's aspiration
(min-field-confidence compounding, the paper's own TOBE-08 honesty device),
and BASE-24's 41 wh clarification wait had to be tier-conditioned (4/20/41)
for consistency with BASE-15/16.

> Build `sim/tobe.py`. Each inquiry draws a document-quality class (clean
> digital / scanned / fragmented / CAD-dependent) from a tier-conditioned mix
> stated in YAML with a rationale note per row; per-field extraction success by
> class is seeded from the published ranges cited in Section 5.3 (NOT from any
> audit — authors' direction 6 Sep) with optimistic/central/pessimistic
> variants. Compute per-inquiry field confidence, apply the 7.7 routing
> (auto-draft / assisted / manual via thresholds C1, C2 and value gate V1 —
> parameters, not constants), assign engineer review times by skill profile,
> and model residual errors (defects that survive review, by error class and
> skill). System-lane step times from the TOBE register rows. Output per
> inquiry: route taken, touch by role, cycle time, defects. Sanity gate: with
> extraction success forced to zero, to-be mode must reproduce as-is results
> within tolerance (graceful-degradation check mirroring constraint four).

### SIM-3 · Economics layer and P&L assembly — P1 — DONE (6 Sep)
Delivered: `sim/economics.py` + `data/parameters_econ.yaml`; absorbs
`model/monte_carlo.py` (now retired). 27/27 tests pass. Revenue base derived
per D13 (EUR ~5.1M won / ~19.9M quoted, value shares hit BASE-11 within 1pp);
leakage reproduces BASE-33's 1.9%. Labour savings now EMERGE from paired DES
runs instead of an assumed automation rate. Headlines (seed 42, 20k draws):
NPV@12% P10/P50/P90 = 82k/232k/408k EUR, P(clears 15% hurdle) 98%, IRR median
64%, payback 1.7 yrs. THE 9.5 CONSERVATIVE CASE DOES NOT CLEAR the hurdle on
cost+error+discounting alone (NPV@15% = -121k): the single-branch floor
argument fails, consistent with SEC6-01's crossover; the case rests on the
win-rate elasticity and/or multi-branch scale. Full findings in
`model/simulation_plan.md` (SIM-3 build notes).

> Build `sim/economics.py`: per inquiry, labour cost (touch × EUR 12), quoted
> value drawn from tier value bands calibrated to BASE-11/12, with the revenue base derived
> from tier volumes, value bands and win rates (D13, S-tagged), error-cost events by class at BASE-30 unit costs, discount drawn
> against a reference price (as-is: the 4–18% spread; to-be: the banded
> engine), win draw at tier base rates (BASE-20) adjusted by a response-time
> elasticity floored at zero and capped by the 9.3 triangulation, margin by
> tier (BASE-21). Aggregate simulated years into a projected P&L: labour,
> quality cost, discount recovery, incremental gross margin from wins and
> capacity, minus run costs; five-year cash flows with build (EUR 92,000,
> FIN-08) and change costs; NPV at 12%, hurdle 15%, IRR, payback. Monte Carlo
> outer loop across seeds and parameter draws; report P10/P50/P90 and
> P(clears hurdle). The old harness's conservative case (extraction at
> pessimistic bound, elasticity zero, +30% build) must clear or fail the
> hurdle on cost + error + discounting alone, and say which.

### SIM-4 · Stress-test harness — P1 — DONE (6 Sep)
Delivered as specified; only elasticity_zero fails; kill boundaries: uplift
<0.2pp, build >3.3x, run cost >83k/yr, demand <50%. See simulation_plan.md
SIM-4 build notes. Manifest results/stress_20260906_152724.json.

> Build `sim/stress.py` + `scenarios/*.yaml`: named scenarios for demand surge
> and collapse (±40% arrivals), senior-estimator attrition (skill mix
> degradation), extraction at the pessimistic end of published ranges,
> elasticity = 0, build overrun +30/+60%, adoption failure (Tier 2 stays
> assisted, never auto-draft). Tornado across the six most influential
> parameters. A kill-criteria finder: bisection on each stressor to the value
> where NPV at the hurdle turns negative, reported as explicit boundaries
> ("the case fails if X falls below Y") — these feed Section 11 kill criteria
> and 9.6 sensitivity. CLI: `sim stress --all` produces every table and figure
> used by the paper in one run.

### SIM-5 · Self-improvement loop — P2 — DONE (6 Sep)
Grid search delivered; chosen point C1=0.85 C2=0.70 hw=1% written to register
as SIM5-01..04 (proposed). Key finding: discount-band width dominates routing
tuning; defect constraint binds at negligible cost. See simulation_plan.md
SIM-5 build notes. Manifest results/optimize_20260906_153149.json.

> Build `sim/optimize.py`: treat C1, C2, V1, tier routing defaults,
> discount-band width and staffing plan as decision variables; grid or
> evolutionary search maximizing P50 NPV subject to constraints (error-escape
> rate ≤ as-is baseline, P10 NPV ≥ 0 at the hurdle). Write the chosen
> operating point back to model/assumptions.csv as S-tagged rows with the run
> manifest as source; these values become the design parameters the paper
> recommends for the pilot (7.7, 11.1). Report which constraints bind — that
> is the managerial finding, not just the optimum.

### SIM-6 · Reader package and paper integration — P2 — DONE (6 Sep)
Repo packaging complete: README quality pass with headline outputs, run.sh
runs everything end to end, register snapshot refreshed (incl. SIM5 rows),
five figures exported to figures/ (calibration table, cycle-time
distributions, benefits waterfall, NPV fan, tornado). Doc integration done
with T14 (t19 scripts): 3.1/3.3 re-sourced per D12 (Estimated tag replaces
Audited; audit reframed as pilot instrument in Table 3.1), repository pointer
sentence added in 3.3 ([repository URL] placeholder pending the GitHub push),
all five figures inserted as Exhibits 8.1/8.2/9.1/9.2/9.3 with captions.

> Package for GitHub: README quality pass, one-command reproduction, seeds and
> parameter data committed, figures exported (calibration table, cycle-time
> distributions as-is vs to-be, NPV fan, tornado) sized for the Doc. Then the
> paper edits: re-source the simulation-input language in 3.3, 8.1–8.2 and 9.5
> per D12 (audit reframed as recommended pilot activity) — automation capability from published ranges + skill/complexity
> variance + current-state calibration, not from an audit — and add the single
> sentence pointing readers to the public repository. Keep the style contract;
> every changed number re-tagged (S) with its register row.

### T14 · Write Section 9 + Innovo unit economics — P1 — DONE (6 Sep)
Sections 8 AND 9 written from the run manifests (Section 8 prose was orphaned
when T11 was superseded, so t19 covers both): 8.1 capability evidence per
D12, 8.2 calibration + projections, 8.3 validation status, 8.4 synthesis;
9.1–9.6 per the prompt including the floor-case verdict (does not clear on
cost + error + discounting alone) and Innovo as-is vs to-be (28h/€340/2 days
late vs ~15h/€180/1 day early; T14-01). 7.9 touch placeholder resolved.
Exec-summary slots (1.3) left for T17 as planned. Scripts: t19_sections89.py,
t19b_images.py.

> Write Section 9 (~1,500 words) from the Monte Carlo results: 9.1 baseline
> economics (register figures only, no new numbers), 9.2 benefits waterfall with
> each bar tagged and de-overlapped and the redeployment assumption stated, 9.3
> the speed–win elasticity triangulation using the low end in the base case,
> 9.4 cost model with sourcing stated, 9.5 NPV as P10/P50/P90 plus the floor
> case, 9.6 tornado + the Innovo RFQ priced as-is (measured) vs to-be
> (simulated). Then backfill the bracketed financial slots in Sections 1.3, 8,
> and 13. Every figure traces to a register row or a run-manifest output.

---

## Phase 5 — Voice & citations

### T15 · Voice normalization / anti-generation pass — P2 — DONE for Sections 2–9 (6 Sep)
Applied (t21_voice.py) on top of the earlier t15a (em dashes: zero in prose;
the one remaining — sits inside the O9 scaffolding note, deleted with it) and
t15c (tone) passes. This pass: removed announced-rigor phrases ("an honest
matrix says so", "measured honestly", "what we honestly have", "stated
plainly"), cut emphasis "exactly" (7→5, survivors are functional), thinned
the stacked "X, not Y" pattern in Section 9, dropped one "deliberately".
Aphorism density now ≤1 per section (kept: "It is not enough." /
"The work is not slow; the waiting is." / "not this paper's fallback but its
recommendation" / "a runtime has no inbox" / "cheap to run and expensive to
get wrong"). Banned filler: zero matches. REMAINING: Sections 1 and 10–13 are
still outline bullets; T12/T17 must draft to the style contract and get a
final spot-check at T18.

> Perform a full-voice edit of the manuscript. Goals: one register throughout
> (restrained first-person plural, per the decisions log); at most one rhetorical
> aphorism per section — currently the text stacks constructions like "The work
> itself is not slow. The waiting is." and "X is not Y; it is Z" (10+ instances)
> which read as machine-generated; vary sentence length and paragraph rhythm;
> reduce em-dash density by roughly half; remove list-like triads where prose
> serves. Do not change any number, tag, table, or the meaning of any claim. Do
> not introduce academic filler ("Moreover", "It is worth noting", "delve",
> "landscape", "leverage") or consultant filler ("unlock", "journey",
> "seamless"). The test: a faculty reader should hear two specific practitioners
> who measured their own shop, not a model or a McKinsey deck. Produce a
> before/after sample of five paragraphs for author sign-off before applying
> throughout.

### T16 · Citation verification — DONE (6 Sep, t28_citations) — P2
Blocked on: T12 (all citing text exists).

> Verify every reference in Section 5 and the reference list against the
> original source: bibliographic accuracy, page-check any quoted figures
> (especially the DocVQA/benchmark accuracy claims in 5.3), and confirm each is
> re-cited in Sections 6–11 or delete it per the paper's own rule. APA 7th is
> the standard (D18, applied 6 Sep by t22_apa.py); specifically verify the
> reconstructed full author lists, page ranges and venue details added to the
> Kim 2022 (Donut), Xu 2020 (LayoutLM), Jaume 2019 (FUNSD) and Mathew 2021
> (DocVQA) entries. Resolve the
> placeholder enterprise-extraction citation (bracketed at the end of the
> reference list) with a real, verifiable APA source. Write 3.3 (simulation-methods placeholder) (~120 words) from
> the public simulator repository with 2–3 APA citations situating
> discrete-event and Monte Carlo simulation of service operations. Format all
> references to the programme standard from the decisions log.

---

## Phase 6 — Final assembly

### T17 · Executive summary — P1 (write absolutely last) — DONE 2026-09-06
Written per user instruction at a half-page limit (290 words, tighter than the
original ≤400-word spec) while T12 (Sections 10–13) was still outstanding; the
summary draws only on finished sections (4, 8, 9) plus the 11.1 pilot frame
already fixed in outline. Five paragraphs per the 1.1–1.5 outline; measured
vs simulated stated in words rather than tags for readability. Script:
t23_execsummary.py. NOTE for T12/T18: if drafting Sections 10–13 changes the
pilot's shape (duration, tier scope, budget) or the strategic claim, re-check
paragraphs 4 and 5. [Abu Dhabi] branch placeholder (O1) appears in sentence 1.
Blocked on: everything above.

> Write Section 1 (≤ 400 words, one page) from the finished manuscript only,
> following the 1.1–1.5 outline: the problem in one sentence with the three
> measured baseline numbers; the solution in one sentence with the headline
> audited feasibility finding and simulated cycle-time projection; NPV as a
> P10/P50/P90 range with payback and the conservative floor case; the data-moat
> claim; and the recommendation phrased exactly as a stage-gated pilot
> investment with go/no-go criteria, in the register's canonical currency. Every
> number must carry its evidence character in the prose (measured / audited /
> simulated). The acceptance test is the paper's own: a professor reading only
> this page knows what is fact, what is projection, and what decision is being
> recommended.

### T18 · Final QA gate — DONE (6 Sep; see QA notes below) — P1
Blocked on: T17.

> Run the submission gate: (1) mechanical tag audit — scan for numerals lacking
> M/E/A/S tags or register IDs; (2) re-export the Google Doc and measure true
> page count at 1.5 spacing — body ≤ 30 pages excluding references and
> appendices; (3) scaffolding sweep — zero author's notes, placeholders,
> bracketed values, or meta-commentary remain; (4) exhibit/table numbering
> sequential and every exhibit referenced from the text; (5) appendices A–I
> present and pointed to; (6) the three narrative-device touchpoints intact
> (2.0 hook, 7.9 labelled simulation, 13 conditional close). Output a pass/fail
> checklist with locations for any failure.

### T19 · Move reference tables to appendices (30-page limit) — P1 — DONE (6 Sep)
Applied to the live Doc (t20_movetables.py + t20b_bridges.py): Tables 3.1,
4.1, 4.3, 4.4, 7.1 recreated under a new Appendix K (extract) with captions
and numbering unchanged; Exhibit 8.1 calibration image moved to a new
Appendix F (extract) as Exhibit F.1; originals deleted; bridge sentences with
the key figures left in place; all body cross-references updated (6.2, 4.3,
7.8, 8.2); K added to the appendix list. Table 4.2, Table 6.1 and the four
simulation exhibits stay in the body as planned. True page saving to be
confirmed at the T18 export.

> Move to a new **Appendix H (Detail Tables)**: Table 3.1 (evidence base),
> Table 4.1 (segmentation criteria), Table 4.3 (error taxonomy), Table 4.4
> (Innovo timeline) and Table 7.1 (sourcing per component); move the Exhibit
> 8.1 calibration table image to Appendix F beside the simulator methodology.
> KEEP IN BODY: Table 4.2 (baseline metrics — every improvement claim in the
> paper cites one of its cells) and Table 6.1 (decision matrix — it is the
> Section 6 argument), plus the four remaining simulation exhibits (8.2,
> 9.1–9.3), which are the evidence Sections 8–9 exist to present. For each
> moved table, leave a one-to-two-sentence bridge in place stating the key
> line and the appendix pointer (e.g. 4.4: extraction dominates frequency at
> 41% of defects, selection dominates cost; 4.4 Innovo: 28 touch hours, seven
> days, two days late; 3.1: seven sources, no other data enters). Renumber
> nothing in the body; appendix tables keep their section-based numbers so
> cross-references survive. Verify with a re-export that body length drops
> ~3–4 pages and no dangling "Table X above" references remain.

---

## Open items register (consolidated 6 Sep, post-simulation) — for the revision pass

### A. Author inputs — numbers only Khoory/the authors can supply
| # | Item | Where it bites | Status |
|---|---|---|---|
| A1 | ~~O9: actual revenue~~ RESOLVED 6 Sep (D19): ~AED 150M won pump-only, 24% avg margin on revenue. Full rebase executed (simulator x6.125, Doc Sections 1/4/6.3/8.4/9, figures). Residual -> A10d | 9.1 (bold Doc note), 9.2, O9 | open — highest stakes |
| A2 | ~~internal interview count~~ RESOLVED 6 Sep: 6 (t25_placeholders) | Table 3.1 | resolved |
| A3 | BASE-41/D6: contractor interviews [4–6] to complete; 9.3 takes no credit yet; include ≥1 dissent when written. Authors confirmed 6 Sep: genuinely in progress; keep the bracket and framing | 3.2, 4.6, 8.3, 9.3 | in progress (authors) |
| A4 | ~~branch designation~~ RESOLVED 6 Sep: named plainly, brackets dropped (t25_placeholders) | 3.1, exec summary | resolved |
| A5 | ~~pilot budget~~ RESOLVED 6 Sep (D20): EUR ~30k derived (0.25x engineer-year + pilot run costs), PILOT-01 in register; stated in 1.5; T12 develops it in 11.1/13 | 1.5, 11.1, 13 | resolved |
| A6 | ~~O7: referencing standard~~ RESOLVED: APA 7th (D18), applied 6 Sep; T16 verifies the reconstructed entry details | T16 | resolved |
| A7 | ~~Quality-cost reconciliation~~ RESOLVED 6 Sep (D19): BASE-31 pct target retired; BASE-30 unit costs value-scaled x6.125; quality cost now emerges at EUR ~177k = 0.51% of revenueed the anchor | 4.4, 9.2, econ params | open |
| A8 | ~~FIN-06/07 '??'~~ RESOLVED 6 Sep (D20): 10.3 venture exhibit CUT; cells stay unresolved in the workbook only | none | resolved |
| A9 | 8.3 validation: structured design review / mini-Delphi of the Section 7 architecture still to be run and reported | 8.3 | scheduled (authors) |
| A10 | **BASE-12 value bands are now re-derived (D19 x6.125), not measured**: re-measure the tier value thresholds and shares from the RFQ log at actual order values; also re-check BASE-30 defect unit costs against the credit-note ledger at true order sizes | Table 4.1, 4.4, econ layer | open (authors) |

### B. Placeholders standing in the Doc
| # | Placeholder | Resolves when |
|---|---|---|
| B1 | [repository URL] in 3.3 + Appendix F | authors will create and push the repo themselves (D20, 6 Sep); placeholder stays until they supply the URL |
| B2 | [PLACEHOLDER: 2–3 simulation-methods citations] in 3.3 + the References stub for 5.3 benchmark sources | T16 |
| B3 | ~~[n]~~ resolved (6); [4–6] contractor bracket stays by author decision until interviews complete | A3 above |
| B4 | ~~[the Abu Dhabi estimation office]~~ resolved: named plainly | done |
| B5 | "€X" pilot investment in 1.5 | A5 above; T17 writes it |
| B6 | ~~Section 1 outline bullets~~ RESOLVED 6 Sep: executive summary written (t23_execsummary.py, 290 words / half page) | done |
| B7 | Sections 10–13 are still outline bullets | T12 |
| B8 | O4: Appendix F (simulator methodology) not yet written; seed it from simulator README + simulation_plan.md | T12/T16 window |
| B9-done | AUTHORS-TO-CONFIRM note at 9.1 (contains the paper's only remaining em dash, by design: it is scaffolding) | deleted when A1 resolves |

### C. Simulation parameters flagged provisional (fine for the paper, replace before a build decision)
| # | Parameter | Current basis | Replace with |
|---|---|---|---|
| C1 | Run cost EUR 15–27k/yr | analogy estimate | vendor quotations (9.4 says so in prose) |
| C2 | Change cost EUR 10–30k | author judgement | training plan pricing |
| C3 | Pricing adoption 40–90% | author judgement | pilot measurement |
| C4 | Win uplift 0–2–5pp | triangulation floor/cap | contractor interviews (A3), then pilot |
| C5 | SIM5-01..04 operating point (C1 0.85 / C2 0.70 / band ±1%) | optimizer, "proposed" | pilot validates; ±1% band is "narrowest governance accepts", adoption risk vs band width is unmodelled |
| C6 | TOBE-05 review-queue median: 7.2 claims 2.5 h; simulator's emergent value is ~0 wh (reviews start at once at 68% utilization) | design assumption vs model | reconcile at T15: either soften 7.2's number or state it as a busy-period figure |
| C7 | Innovo to-be touch ~15 h (T14-01) sits in 7.9/9.6; derived by ratio, not a mega-specific run | tier-3 median ratio | optional: simulate the 75-pump inquiry explicitly in SIM-7 if challenged |

### D. Known tensions to keep in view
- ~~Mega-project cap~~ moot since D19 (actual revenue known; bands rescaled). New tension: D17 flagship range (EUR 4.9–9.2M after x6.125) now rests on scaling, not on the trade-price research, which D19 superseded. Original: quoted value was capped near EUR 22–27M however fat the Tier 3 tail is (ties to A1/O9).
- INVERTED by D19: the floor case now CLEARS the hurdle (+EUR 304k); no kill boundary in any tested stress range. Sections 1/9 restated 6 Sep; T12 (Sections 10–13) must present the case as evidence-limited rather than economics-limited, and 11.1 kill criteria are evidential (extraction accuracy, override rates, escaped defects), not NPV thresholds.
- Defect parity in 8.2 (9.1% vs 9.2%) is a constraint, not a benefit; do not let later prose claim "fewer errors" without the mix-shift caveat.

### E. Logic-flow review findings (6 Sep, full-document read; canvas: paper-logic-map)
New gaps not previously registered. G1–G3 are argument breaks; G4–G6 falsifiable claims; G7–G15 QA.

| # | Where | Gap | Fix at |
|---|---|---|---|
| G1 | 3.1 → 6.3 → 9.1 | ~~RESOLVED 6 Sep (t24_rebase)~~: 3.1 now states all figures are single-branch with no scaling; 6.3 rewritten to rest on leakage recovery (the D19 EUR ~850k leak), not multi-branch deployment. **Original:** 3.1: "company-wide figures appear only where Section 9 scales the branch findings"; 6.3 rests the Option E case "explicitly on multi-branch deployment (9.1)"; Section 9 is single-branch throughout. Load-bearing because 6.3's own crossover puts 640 RFQs below break-even on cost alone. Either add the scaling passage to 9 or rewrite 6.3 to rest on win uplift + leakage | T12 window |
| G2 | 9.3 ← 5 | **Phantom citation:** 9.3's third triangulation leg cites "response-time literature reviewed in Section 5"; Section 5 contains none. Add 1–2 quote-responsiveness/win-rate sources to 5 or drop the leg | T16 |
| G3 | 2.4 | ~~**Submittal stage in scope, never addressed again.** Cut from 2.4 or add a Phase-3 sentence in 7 + exclusion note in 9~~ RESOLVED 6 Sep (t26): submittal clause cut from 2.4 | T12 window |
| G4 | 2.1/T4.1 → 7, 8.2 | ~~Manufacturer special-quote loop (part of the Tier 3 definition) absent from the to-be design; 88→56 wh projection buries it in the fitted external wait. One carrying sentence in 7.6 or 8.2~~ RESOLVED 6 Sep (t26): 8.2 states the manufacturer special-quote round trip is carried at measured pace inside the fitted external waits | T12 window |
| G5 | 8.2 → 9.6 | ~~8.2 cites a 40% demand-surge result "of 9.6"; 9.6 doesn't report it (scenario exists: demand_surge.yaml). Add to 9.6 or repoint~~ RESOLVED 6 Sep (t26): 40% surge result (~EUR 1.2M benefits) now reported in 9.6 | T12 window |
| G6 | 9.4 | ~~0.2–0.5 FTE maintenance can't fit in EUR 15–27k/yr at the EUR 92k engineer-year rate (0.2 FTE = 18k alone). State rate basis or widen range; sharpens C1~~ RESOLVED 6 Sep (t26): authors clarified EUR 92k is build-only, maintenance ~40k/yr; run cost 45-65k in 9.4, model re-run (FIN-15) | T12 window |
| G7 | 9.1 vs 4 | 640 (log) vs 636 (quoted) never reconciled (still open); ~~Tier 3 cost 137 vs 136~~ fixed 6 Sep (t24) | T18 |
| G8 | 9.6 | ~~RESOLVED 6 Sep (t24_rebase)~~: restated EUR 1.4–2.6M (S, register arithmetic) at D19 flagship range × Tier 3 margin. **Original:** Innovo margin "EUR 200–300k (M)" was derived (D17 band × Tier 3 margin), not measured; retag E/S or get actual won-deal margin (ties to A1) | T18 |
| G9 | 8.2 | ~~"9.1 versus 9.2 percent" reads as section numbers; reword with % signs~~ RESOLVED 6 Sep (t26): rephrased as simulated 9.2% vs measured 9.1% | T18 |
| G10 | 4.1 vs T4.2 | ~~"EUR 66 of direct labour" = 5.5h×12 exactly, but T4.2's 66 includes licence allocation; one is off by the licence share~~ RESOLVED 6 Sep (t26): 4.1 says direct cost (labour plus licence allocation) | T18 |
| G11 | 10.2 outline | ~~RESOLVED 6 Sep (t27)~~: 10.2 cites the correction flywheel of 7.1 (Exhibit 7.3) | done |
| G12 | Section 8 | ~~Body exhibit numbering skips 8.1 (moved to F.1); renumber or note~~ RESOLVED 6 Sep (t26): cycle-time exhibit renumbered 8.1 | T18 |
| G13 | 5.1 | ~~RESOLVED 6 Sep (t28)~~: Mudambi & Aggarwal (2003, Industrial Marketing Management 32(4)) added and cited | done |
| G14 | 9.2 | ~~Fifth benefit "declined volume is real but unmodelled" has no Section 4 anchor; evidence or soften~~ RESOLVED 6 Sep (t26): softened to unevidenced upside the pilot can log | T12 window |
| G15 | 1 vs 9.5 | ~~Exec summary floor case omits the build +30% condition 9.5 includes in the −83k figure~~ RESOLVED 6 Sep (t24 rebase): exec floor case states all three conservative settings | T18 |


## Phase 7 — Readability & figure legibility (fresh-eyes review, 6 Sep evening)

**Status:** Exhibit 4.1 regenerated legibly and swapped into the live Doc
(`scripts/fig_swimlane.py` + `scripts/e9_swimlane_swap.py`): fonts now 7–9 pt at
print width against ~5 pt before, the stray artifact box and the em dash in the
embedded title are gone, same Tier 2 medians (touch sums to 5.5 h; BASE-17/24/25/26).
New size 450×324 pt vs old 468×236 pt (≈ +0.25 page; see the open page-budget
decision). Table 4.2 caption now defines the M/E tags in words. Cross-ref error
found by the read and fixed: 4.3 cited "criteria of 4.2" for the tier taxonomy
defined in 4.1.

### T20 · Readability revision from the fresh-eyes read — P2 · APPLIED 6 Sep (t/e10, e11)
Author answers (6 Sep): strip internal IDs but keep M/E/S; do NOT thin
cross-references for brevity, favour interpretability even at more words;
add the three glosses; execute all four page-recovery items. Applied:
F1, F3–F11, F13, F14 (F11 minimally: "a UAE pump distributor" — **authors
verify the company description**). F2 handled as targeted sentence rewrites,
not ref-thinning, per the answer. F12 (hydraulic terms) intentionally left.
Also fixed while applying: three stale "11.3" liability refs -> 11.2.
Page recovery: "three readings" paragraph cut (CUTS log in chat), 7.3
walk-through tail compressed (numbers live in 9.3), Table 6.1 -> Appendix K
(between 4.4 and 7.1), Exhibit 9.2 -> Appendix F (between 8.1 and 9.3).
Body after the pass: 10,216 prose words, 2 in-body images (Ex 4.1, 9.1),
1 in-body table (4.2) — roughly at the 30-page limit.

Severity: H = blocks comprehension for a non-specialist reader, M = causes
re-reading, L = polish.

| # | Where | Issue | Proposed fix | Sev |
|---|---|---|---|---|
| F1 | body-wide | Internal register/decision IDs leak into prose: (D19) in 4.2 and the Table 4.2 caption, (D17) and "(S, run manifest…)" in 9.1, [A1]–[A7] through 7.1–7.3. Meaningless to any reader without Appendix A open | Keep M/E/S; move the IDs to the appendix versions of the claims or drop them; 3.1 already carries the traceability promise | H |
| F2 | body-wide | Bare decimal cross-refs at high density ("(8.2, 4.4)", "(9.1, 11.2)", "the 5.2 range"); sentences read like code and the reader loses the argument thread | Keep only load-bearing refs; write "Section 9" for real jumps; delete refs the sentence survives without | H |
| F3 | 10.1 | "the as-is and to-be business model canvases differ in only three blocks" assumes the reader knows the BMC framework and its blocks | One-clause gloss at first mention, within the one-sentence framework rule | M |
| F4 | 11.2 | ADKAR walked letter by letter (Awareness/Desire/Knowledge/Ability/Reinforcement) without saying those five words are what ADKAR abbreviates | One clause at first mention; keep the five-step structure | M |
| F5 | 3.2, Table 4.2, 8.2, 9.2 | P10/P50/P90 and "P90 cycle time" never glossed | One parenthetical at first use, e.g. "P90, the value nine cases in ten stay under" | M |
| F6 | 7.1 | Five design constraints in one 120-word block ("First… Fifth…"); hard to hold while reading Section 7 | Compact numbered list, content unchanged | M |
| F7 | 7.3, 8.2 | Colon-chain sentences stacking 5–7 clauses (e.g. the Monday walk-through sentence, the routing-shares sentence) | Split at the colon into two sentences each | M |
| F8 | 6.2 | "the concession" as heading term is rhetorical and unclear until the paragraph ends; "ordinally" is jargon | Heading "…and where hiring wins"; drop "ordinally" | M |
| F9 | 11.1 | "Tier 2, the modal inquiry" — statistics jargon | "the most common inquiry" | L |
| F10 | 12 | "ex-ante" reused outside its single permitted 3.1 definition (style contract) | Rephrase ("evaluates the investment before it is made") | L |
| F11 | 2.0/2.1 | Khoory is never plainly introduced; a fresh reader infers "UAE pump distributor" from scattered context | One plain introducing sentence at the vignette's end — wording needs author sign-off (near-new fact) | M |
| F12 | 4.3, 7.3 | Unglossed domain terms carrying the near-miss story: static head, duty point, booster set | Gloss the two that matter (static head, duty point) or leave for a technical reader | L |
| F13 | 9.1 | "the simulator's value model reproduces it with about €136 million quoted implied by the measured win rates (S)" — very hard parse | Rewrite as one plain sentence (backwards from win rates, €136M quoted implies the €34.5M won) | M |
| F14 | 12 | "stated preferences may differ from revealed behaviour" — economics jargon | "what contractors say may differ from what they do when a system-assembled quote arrives" | L |

Open questions to authors (asked in chat, 6 Sep): (1) evidence-tag treatment in
prose (legend only / strip IDs, keep M-E-S / tags in tables only); (2) how hard
to thin cross-references (F2); (3) approve the small glosses F3–F5;
(4) the standing page-budget decision: move Table 6.1 + Exhibit 9.2 to
appendices plus two small cuts, now more pressing since the new Exhibit 4.1 is
a quarter page taller.

## T18 QA notes (6 Sep)
- Em dashes: 0. Scaffolding (PLACEHOLDER/TODO/AUTHORS TO CONFIRM/euro-X): 0. Style tics (honest/stated plainly): 0.
- Stale pre-D19 numbers: 0 across the full export.
- Exhibits 4.1-4.3, 7.1-7.3, 8.1, 9.1-9.3, F.1 and Tables 3.1, 4.1-4.4, 6.1, 7.1: gap-free, all cited.
- Cycle-time medians (18/39/88 -> 2/9/56) consistent across Sections 1, 8.2, 13.
- 3.3 placeholder citations resolved (Law 2015; Robinson 2014; Hertz 1964); ExtractBench scaffolding note deleted; 5 new APA entries inserted alphabetically with italics.
- Body word count ~12,200 (~26-29 pp with exhibits): inside the 30-page limit; authors do the final visual pagination check.
- Deliberate placeholders remaining (author-owned): [repository URL] (B1: authors push the repo), [4-6] contractor interview count (A3: in progress).
