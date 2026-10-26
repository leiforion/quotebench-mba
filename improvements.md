# Improvements — "Leif_edit of INSEAD Final Outline"

Reviewed against the source Google Doc (downloaded 6 Sep 2026; ~12,945 words).
Reviewer lenses: supply chain / distribution economics, commercial development,
software engineering, finance, and MBA thesis standards (INSEAD FMP conventions).

---

## 1. Where the document actually stands

| Doc section | State | Words | Notes |
|---|---|---|---|
| Preamble ("Revised Paper Architecture v3") | Scaffolding | 118 | Must be deleted before submission |
| 1 Executive Summary | Outline only (intentional) | 203 | Write last — agreed |
| 2 Introduction & Problem Definition | Full prose | 1,645 | Strong; over its own 2.5-page budget |
| 3 Methodology | Full prose | 1,373 | Strong; no page budget stated; long |
| 4 Current State Analysis | Full prose + tables | 2,763 | The paper's best section; 4.6 missing, 4.6/4.7 out of order |
| 5 Literature | Full prose | 1,414 | 5.5 placeholder; citation verification pending |
| 6 Solution Options | Half prose, half outline | 926 | Options A–C drafted (rough voice), D/E, matrix, concession missing |
| 7 To-Be Design (+ App. B/G extracts) | Full prose | ~2,300 | Polished but over-engineered in places |
| 8 Feasibility Evidence | Outline only | ~600 | The evidentiary heart — unwritten |
| 9 Financial Analysis | Outline only | 383 | Depends on P&L model + Monte Carlo (future) |
| 10 Strategy | Outline only | 194 | The "intellectual climax" — unwritten |
| 11 Implementation / Risk | Outline only | 333 | |
| 12 Limitations | Outline only | 118 | |
| 13 Conclusion + Appendices + Refs | Outline + reference list | 579 | |

**Length verdict.** At ~380–400 words per 1.5-spaced page, current prose ≈ 26 pages
of text + ~5 pages of exhibits/tables. Writing Sections 8–13 to their own stated
budgets adds ~14 pages. Projected total without cuts: **~45 pages vs. a 30-page cap.**
Required: cut existing prose ~35% AND hold new sections to strict word budgets
(see §7 below for the proposed budget).

---

## 2. Consistency ledger — numbers, units, pricing that disagree

These are the misalignments between Sections 1–4 and 5–8 (and internal to 2–4).
Each needs one canonical value in the Assumptions Register (Appendix A), then
propagation.

| # | Conflict | Locations | Detail | Suggested resolution |
|---|---|---|---|---|
| C1 | Currency: € vs AED | 1.3, 1.5, 13 vs everywhere else | Exec summary and conclusion price the pilot in "€ X"; all measured data is AED | **Decided (D1): EUR only**, converted at a fixed stated rate — see model/decisions.md |
| C2 | Tier 2 definition vs prose | 2.2 vs Table 4.1 | 2.2: "standard inquiry, ten to twenty pumps across up to three product types"; Table 4.1 Tier 2: 3–12 pumps, ≤2 applications | Align 2.2 prose to the Table 4.1 taxonomy |
| C3 | Tier 2 effort | 2.2 vs Table 4.2 | 2.2: "roughly one full working day" (~8h); Table 4.2 Tier 2 touch time: 5.5h | Pick one; 5.5h is the measured figure — rewrite 2.2 |
| C4 | Large-inquiry size | 2.2 vs 4.2/4.5 | 2.2: "well over one hundred pumps"; Tier 3 threshold is >12; the archetype case (Innovo) is 75 | Rephrase 2.2 ("can run to a hundred or more" or align to Innovo's 75) |
| C5 | Large-inquiry effort | 2.2 vs 4.5 | 2.2: "four or five working days" (32–40h); Innovo measured 28h | Align to ~28h / "three to four working days" |
| C6 | Error rate | 2.2 vs Table 4.2 | 2.2: "of ten line items, one or two contain a mistake" (implies ~most inquiries defective); Table 4.2: 6/11/19% of inquiries with ≥1 defect | These are different units (line-item vs inquiry rate) but read as contradictory; restate 2.2 in inquiry terms |
| C7 | Loaded labour rate | 2.2 vs 4.1 | AED 96,000/yr ÷ 2,080h ≈ AED 46/h, but 4.1 uses AED 52/h | State the bridge (working-hours base, benefits, software) or fix one number |
| C8 | Inquiries per estimator-week | 2.2/3.1 vs 4-section data | 16 estimators × 12 RFQs/wk company-wide; but the study branch: 2 estimators, 640 inquiries/yr ≈ 6.7/estimator-wk | The 3.1 scoping sentence flags this — resolve, don't just flag. Either the 12/wk is wrong or branch mix differs; say which |
| C9 | Queue-share range | Exhibit 4.2 caption vs Table 4.2 arithmetic | Caption: "84–87%"; Tier 1 computes to 88.3% ((18−2.1)/18) | Recompute and restate the range |
| C10 | Innovo Table 4.4 chronology | 4.5 | Rows run Thu→Fri→Sat→Tue→Wed→Thu→**Fri**→**"Thu (next)"** yet the caption claims 7 calendar days and issue 2 days after the Tuesday deadline (= the first Thursday). Pricing on Friday cannot precede a next-Thursday issue and still total 7 days | Rebuild the table so rows sum to the claimed elapsed time; touch total (28h) already checks out |
| C11 | Innovo touch vs Tier 2 rhetoric | 7.9 (also 7.2) | Walk-through says "5.5 touch hours would become roughly 25 minutes" — that's the Tier 2 median inside a Tier 3 (28h) case study | In 7.9 use Innovo's own 28h → projected Tier 3 review time; keep 5.5h→25min for the generic Tier 2 claim in 7.2 only |
| C12 | Contractor reply time treated inconsistently | 7.2 vs 7.9 | 7.2: contractor wait "carried over unchanged from measurement" (41 working hours); 7.9: clarification out Thu 16:53, reply Fri 11:05 (~18h) | Either justify (consolidated request sent same-evening reaches contractor before their weekend) or re-time the walk-through; state the assumption ID |
| C13 | "22 hours" triage claim | 7.3, 7.9 vs 4.1 | 7.3/7.9 cite "22 working hours" before the as-is clarification; 4.1 gives a 14h assignment median (+ reading). Innovo's actual was ~21.5 elapsed | Verify against Exhibit 4.1; cite one number with its source |
| C14 | Untagged percentages | 6.1 | "20 to 30 percent of manual effort", "10 to 15 percent of the problem" carry no M/E/A/S tag and no source | Tag or cut; Section 6 must obey the paper's own evidence contract |
| C15 | "15% of tenders lost" untagged | 2.2 | Load-bearing for 9.3 win-rate uplift; no tag, no source | Tag (E, interviews) and cross-reference the 9.3 triangulation |
| C16 | Innovo table numbering | 4.5, 7.8, App. G | Table 7.2 appears before Table 7.1; Exhibit 4.2 caption references "tiers defined in 4.2" before tiers appear | Renumber once structure is final |

---

## 3. Structural and formatting issues

1. **Scaffolding still embedded.** The preamble ("Revised Paper Architecture (v3)…
   which is itself an elegant structural signal"), the "Author's note (remove before
   submission)" blocks (3, 4, 5), the writing instructions inside outline sections
   ("Score honestly", "worth real marks", "the signature move of a first-class
   ex-ante paper", "it is the paper's intellectual climax"), and the "Test:" line in
   Section 1. Some contain real work instructions — extract them into this backlog,
   then delete from the manuscript.
2. **Section ordering.** 4.5 → **4.7** → **4.6** (root causes before voice-of-customer,
   numbered out of order). Decide the order (recommend: 4.5 Innovo → 4.6 VoC → 4.7
   Root causes, since root causes should compress *all* evidence including VoC).
3. **Heading hierarchy is inconsistent** (in the Doc: some section titles are plain
   bold text, some Heading 1; subsections oscillate between H1 and H2). Normalize:
   H1 = Section, H2 = subsection, and use Google Docs styles so the TOC builds.
4. **Appendix extracts live mid-document** (Appendix B extract and Appendix G extract
   sit between 7.10 and 8.1). Move to the actual appendix; leave one-line pointers.
5. **Two voices.** Sections 3/4/5/7 are polished impersonal analysis; Section 6 is a
   rough first-person draft ("the problem we are trying to solve", "solves the wrong
   end for us", "makes little sense"). Pick one register (recommend measured
   first-person plural, used sparingly — INSEAD FMPs allow "we") and normalize.
6. **Duplication to cut** (cheapest length wins available):
   - The Innovo vignette is told in full twice (2.0 and 4.5, ~250 words overlap,
     some sentences near-verbatim). 2.0 should be the 200-word hook; 4.5 should be
     the table + the two near-misses, referencing 2.0 rather than retelling.
   - 2.3 states the three research questions twice — once as bullets, once as prose
     paragraphs saying the same thing. Keep one form.
   - Options A and B in 6.1 narrate the same manual process twice; B should state
     only the delta ("identical to A until the selection step").
   - The narrative-device paragraph (preamble), 3.1, and 7.9 each explain the
     tense-change device. Explain it once, in 3.1.
7. **No page budgets on the prose sections.** Sections 2, 6, 9–13 carry budgets in
   their headings; 3, 4, 5, 7 don't — and they are the sections that overran. The
   proposed budget is in §7 below.
8. **References**: Harvard-ish but unverified (the doc's own author note says so);
   one placeholder citation ("ExtractBench (arXiv, 2026) — verify"). Every Section 5
   citation must be page-checked and re-cited downstream or deleted (the doc's own
   rule — currently not yet enforced since 6–11 are partly unwritten).

---

## 4. Narrative drift — thesis, antithesis, and where the text wanders

**Thesis (as the paper implies it):** the distributor's technical-expertise function —
reading, calculating, selecting, pricing — can be automated with current AI plus
deterministic engineering, cutting cycle time and cost and error rates, and the
transaction data this generates becomes the distributor's next moat.

**Antithesis:** automating the expertise that justifies the distributor's existence
may simply write the manual for its own disintermediation (manufacturers go direct,
contractors self-serve) — and, in the near term, hiring more estimators (Option A)
is cheaper and less risky.

The paper is at its best when every paragraph is doing work for one of these two.
Places where it strays:

| Where | Drift | Severity | Fix |
|---|---|---|---|
| 7.5 Product data layer | ~500 words of implementation detail: PostgreSQL vs pgvector, ETIM attribute naming, curve coefficients, ingestion pipelines, supersession chains. An MBA reader needs 4 sentences: reasoning is separated from memory; product data is exact, versioned, sourced; every quote can name its data version. The rest is software architecture, not business argument | High (also the easiest big cut) | Compress to ~150 words; move detail to a new technical appendix |
| 5.3 Document-AI benchmarks | Naming FUNSD, SROIE, CORD, Donut, LayoutLM and their benchmark mechanics drifts into an ML lit review. The section earns its keep with two moves: published accuracy is high on clean documents and degrades on messy ones, and the 0.95¹² ≈ 54% arithmetic | Medium | Keep both moves, cut benchmark taxonomy to one sentence + citations |
| 6.1 Options A–C | Re-teaches the manual process the reader just left in Section 4, twice | Medium | Options should be evaluated against decision criteria, not narrated; cut ~40% |
| 3.1 | The methodological essay spends words admiring its own design ("The absence of an implementation is not a gap in the method; it is the method's defining condition") | Low-Medium | Keep the contract-with-the-reader paragraph; trim the self-commentary |
| 7.9 | Rhetorical flourishes stack up ("It is waiting on someone, rather than someone waiting on it, and that inversion is the whole design") | Low | Keep one flourish per section, not three |
| 2.1 | The credit and local-presence pillars each get a full paragraph though the paper only automates pillar one | Low | Halve both; they exist to set up the tension, not to be analyzed |

**Where the thesis/antithesis line is held well** (do not touch): 2.1's planted
tension; 5.1's IDR cycle doing exactly the work 10.2 needs; 6.2's instruction that
"Option A must win on cost and risk"; 6.3's concession paragraph concept; 10.2's
three-futures structure; 12.1's limitations-into-pilot turn.

---

## 5. Strong feedback — what is genuinely good

- **The evidence-tag system (Measured / Estimated / Audited / Simulated) is the best
  thing in the paper.** "The vocabulary is the paper's contract with its reader" is
  exactly the right standard for an ex-ante study, and Sections 3–4 actually honour
  it. This is distinction-level methodology if enforced end-to-end.
- **Section 4 is publishable-quality current-state analysis.** The touch/queue
  decomposition ("Six hours out of every seven, nobody was working on the inquiry"),
  the tier segmentation with the value inversion (12% of inquiries = 47% of quoted
  value), the error taxonomy priced per class, and above all the discount-leakage
  finding (1.9% of revenue — larger than all four error classes combined, and
  invisible because no single decision was wrong). That last finding is the
  commercial sleeper of the paper and is correctly flagged as such in 9.2.
- **The Innovo device works.** One RFQ opening the paper, carrying the as-is
  measurement, re-run as a labelled simulation, priced in 9.6, and closing the
  conclusion in the conditional tense — that is a genuinely elegant structure, and
  the discipline of changing tense at the halfway point is well conceived.
- **Root causes → design constraints traceability** (4.7's four causes mapping
  one-to-one onto 7.1's five constraints and the 7.x layers) is the kind of
  requirements discipline most student papers never achieve.
- **5.4 is an unusually good literature application** — automation bias research
  translated directly into design features (visible confidence, flagged uncertainty,
  named release, override logging) rather than recited.
- **The 0.95¹² ≈ 54% arithmetic** is a memorable, honest device that pre-empts the
  obvious "LLMs are 95% accurate" objection.
- **7.8's build/buy/partner table** is crisp, defensible, and correctly locates
  defensibility in the thin built layers.
- **The stage-gated recommendation with kill criteria** (1.5, 11.1) is the right
  answer for an ex-ante paper and will read as maturity, not hedging.

## 6. Strong feedback — what is weak or wrong

- **The paper's analytical heart is missing.** Sections 8 and 9 are outlines. Every
  headline the executive summary needs (audited automation range, calibration error,
  P10/P50/P90 NPV) does not exist yet. Until the feasibility audit is run and the
  financial model built, Sections 1, 8, 9, 13 cannot be written — this is the
  critical path, not the prose polish.
- **Section 6 undermines the paper's own evidence contract.** Rough voice, untagged
  percentages, and an unfinished option set in the one section whose entire purpose
  is to prove the conclusion wasn't predetermined. As written it would cost real
  marks.
- **Aphorism density reads as generated.** "The work itself is not slow. The waiting
  is." / "narrow, then read" / "The current state, measured honestly, is the design
  brief." / "queues have not been compressed; they have been removed" — each is fine
  alone; a dozen of them in sequence is a fingerprint (of exactly the kind the
  authors want to avoid). The de-AI pass should keep perhaps one per section and
  vary sentence rhythm elsewhere. Same for the em-dash-everywhere habit and the
  "X is not Y; it is Z" construction (used 10+ times).
- **Table 4.4 doesn't add up** (see C10) — in the paper's single most scrutinized
  exhibit, the timeline the whole narrative hangs on.
- **The placeholder status of Section 4 data is a submission risk.** The author's
  note says all figures are illustrative pending real data. Everything downstream
  (simulation calibration, financial model, Monte Carlo ranges) inherits whatever
  changes. Locking real values is a gating dependency for Phases 3–4, not a
  cleanup task.
- **4.6 (voice of customer) is empty**, yet 9.3 declares contractor interviews one
  of only three legs under the paper's "single most attackable assumption." This is
  the largest evidence gap that only the authors can close.
- **5.5 placeholder** — the simulation platform underpinning all "Simulated" tags is
  undocumented. A grader who cannot see the instrument will discount the output.

---

## 7. Proposed length budget (30 pages ≈ ~11,200 words + exhibits)

| Section | Now (words) | Target (words) | Action |
|---|---|---|---|
| 1 Exec Summary | — | 400 | Write last |
| 2 Intro & Problem | 1,645 | 950 | Cut vignette duplication, halve pillars 2–3, fix C2–C6 |
| 3 Methodology | 1,373 | 750 | Trim self-commentary; keep tags contract + Table 3.1 |
| 4 Current State | 2,763 | 1,800 | Tables carry the load; cut prose around them; merge 4.5 retelling |
| 5 Literature | 1,414 | 850 | Trim 5.3 benchmark detail; write 5.5 (~120 words) |
| 6 Options | 926 | 750 | Full rewrite: A–E at ~90 words each + matrix + concession |
| 7 To-Be Design | ~2,300 | 1,450 | Compress 7.5 (−350), trim flourishes, move extracts to appendix |
| 8 Feasibility | outline | 900 | Draft from audit results |
| 9 Financials | outline | 1,500 | Draft from model + Monte Carlo |
| 10 Strategy | outline | 800 | 10.2 gets the full page as planned |
| 11 Implementation | outline | 800 | |
| 12 Limitations | outline | 280 | |
| 13 Conclusion | outline | 380 | |
| **Total** | | **~11,600** | ≈ 30 pages at 1.5 spacing incl. in-text exhibits |

---

## 8. Blocked / needs the authors

1. **P&L spreadsheet unreadable** — Google Sheets API (and Drive API) disabled on
   the service-account project. Enable both, then re-run `scripts/download_docs.py`:
   - https://console.developers.google.com/apis/api/sheets.googleapis.com/overview?project=791844662929
   - https://console.developers.google.com/apis/api/drive.googleapis.com/overview?project=791844662929
2. Real Khoory data to replace Section 4 placeholders (or a decision to submit with
   the illustrative-data caveat removed and values asserted).
3. Contractor interviews (4.6) and internal interview counts (Table 3.1 brackets).
4. Documentation of the authors' operations-simulation platform (for the 3.3 placeholder and App. F).
5. Currency decision (C1), branch designation in 3.1, pilot budget figure for 1.5/13.

---

## Structure review (6 Sep 2026, post em-dash/tone pass)

Verdict: the 13-section architecture is fundamentally sound and should not be
reshuffled. The dependency chain reads correctly for a board-style reader:
problem (2) → method (3) → measured evidence (4) → what is already known (5) →
decision (6) → design (7) → proof the design would work (8) → what it is worth (9)
→ what it means strategically (10) → how to do it safely (11) → limits (12) →
close (13). The Innovo thread (2.0 → 4.5 → 7.9 → 9.6 → 13) is the spine and
survives every section boundary.

Changes recommended:
1. **Fold 5.5 into 3.3.** [DONE 6 Sep] "Ex-ante evaluation and simulation in operations"
   grounds the method, not the solution space; it is also still a placeholder.
   One cited paragraph inside 3.3 removes a placeholder subsection, thins the
   setup further, and leaves Section 5 with four subsections, each consumed
   directly by 6.1 (5.2 → Option C, 5.3 → Options D/E risk, 5.4 → 7.7 routing)
   or by 10.2 (5.1).
2. **Appendix assembly order (T18).** The "(extract)" appendices currently sit
   between the appendix list and References; final assembly should place full
   appendices after References per programme convention.

Considered and deliberately kept:
- S5 after S4 (not before): the reader needs the measured problem before the
  solution-space evidence means anything, and 5.x flows directly into 6.1.
- Executive summary numbered as Section 1: renumbering to unnumbered front
  matter would break every cross-reference for zero content gain.
- 9.3 (speed–win elasticity) between benefits and costs: it defends the most
  attackable benefit at the moment it is claimed.
- 7.10 phasing preview separate from 11.1: one paragraph that hands off; the
  roadmap itself stays in 11.
- S12 standalone (not merged into 13): its "limitations become the pilot
  agenda" turn is load-bearing for the recommendation.
