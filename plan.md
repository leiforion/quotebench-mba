# Working Plan — RFQ Automation Paper (INSEAD FMP)

How the documents get read, analyzed, and improved — in phases, each gated on the
one before it. Perspectives applied throughout: supply-chain/distribution economics,
commercial development, software engineering, finance, and MBA-thesis craft.

## Ground rules

- **The Google Doc is the single source of truth for prose.** Local markdown
  (`source_docs/paper.md`) is the working copy; edits are written back directly via
  the Docs API (batchUpdate), with a snapshot taken before every editing session
  (decision D5 in `model/decisions.md`).
- **The Assumptions Register (Appendix A) is the single source of truth for
  numbers.** It gets built as a machine-readable file (`model/assumptions.csv`)
  before any prose fix, so every figure in the paper traces to one row. This is also
  what the Monte Carlo will consume later — one register serves both.
- **Evidence tags (M/E/A/S) are enforced mechanically.** A lint script scans the
  manuscript for numerals and flags any quantitative claim without a tag or an
  Appendix A ID.
- **No section is polished before its numbers are locked.** Voice work happens last;
  otherwise it gets redone.

## Style contract (authors' direction, 6 Sep 2026 — binding on all drafting)

Applies to every task that writes prose (T12, T14, T15, T17 and any revision):

1. **No em dashes (—), ever.** Restructure the sentence instead: parentheses or
   commas for asides, colons for lists/explanations, semicolons or new sentences
   for appended clauses. En dashes in numeric ranges (4–18%) are fine.
2. **MBA register, not journal register.** The reader is a board, not a referee.
   Banned or rationed: "ex-ante" (keep the single definitional use in 3.1; elsewhere
   say "before anything is built"), "decision-grade", "empirical", "instrumentally",
   "probabilistic investment case" (say "investment case stated as ranges"),
   "epistemic/methodological" framings.
3. **No meta-commentary about the paper's own rigor or credibility** ("this proves
   the conclusion was not predetermined", "the signature move of a first-class
   paper", "the reader is entitled to..."). Show honesty through zero-floored
   assumptions and kill criteria; never announce it.
4. **Say "we" where the authors acted** ("we timestamped 22 inquiries"), passive
   voice only where the actor is irrelevant.
5. **Setup stays thin.** Methodology text states what was done and where the detail
   lives; mechanics belong in Sections 8/9 and the appendices, said once.

## Phase 0 — Access & instrumentation (now)

1. Paper downloaded (done: markdown + raw Docs JSON for write-back mapping).
2. Authors enable Sheets + Drive APIs; download P&L workbook, inventory its tabs,
   units, and drivers.
3. Build `model/assumptions.csv` from every number currently in the paper, with
   columns: id, value, unit, tag, source, sections-used. Conflicts (the C1–C16
   ledger in improvements.md) get one canonical row each with a decision note.
4. Snapshot the Doc (docx export) as the pre-edit baseline.

**Gate:** P&L readable, register drafted, currency and data-status questions answered.

## Phase 1 — Consistency & realignment pass (the authors' stated priority)

Fix every C1–C16 conflict in the register first, then propagate into the prose of
Sections 1–8. This is the "re-alignment in pricing and units" the authors asked for:
Sections 5–8 re-anchored to the Section 2/4 canonical figures (tiers, hours, rates,
error rates, Innovo timeline), and Table 4.4 rebuilt so the chronology sums.
Cross-check the P&L workbook against the same register — same loaded rate, same
inquiry volumes, same tier mix, same leakage percentages.

**Gate:** zero register conflicts; lint script passes on Sections 2–8.

## Phase 2 — Structure & length

Renumber (4.5→4.6→4.7 order decision), normalize heading styles, move Appendix B/G
extracts out of the body, delete scaffolding (capturing its instructions into the
backlog first), deduplicate (vignette, research questions, options A/B overlap),
compress 7.5 and 5.3 per the drift table, and enforce the word budget in
improvements.md §7. Target: existing prose lands at ~8,500 words, leaving ~3,100
for Sections 6 (completion) and 8–13.

**Gate:** re-exported Doc measures ≤ ~19 pages before Sections 8–13 are drafted.

**Status (6 Sep 2026): ✅ complete.** Scaffolding gone, headings normalized,
4.6/4.7 reordered, extracts + new Appendix J moved after the Appendices list,
tables renumbered (7.1, G.1). Sections 2–5 & 7 compressed: doc 12,675 → 11,086
words; prose-only counts land within ~10% of budget (S2 ~1,081 / S3 ~1,110 /
S4 ~2,233 / S5 ~1,063 / S7 ~1,819 — each including table text, which the budget
excluded). Sections 1–7 currently total ~8,400 words including tables ≈ the
~19-page gate at 1.5 spacing. Residual trimming folds into T15 (voice pass).

## Phase 3 — Draft the missing analytical sections

Order matters — evidence before argument:

1. **6.1 D/E + 6.2 decision matrix + 6.3 concession** (needs only Phase 1 numbers).
2. **8.1 feasibility audit** — the authors run the 25–30 RFQ scoring protocol (only
   they have the documents); we draft the rubric, the document-complexity typology
   template, and the benchmark mapping, then write 8.1 from results.
3. **8.2 process simulation** — calibrate to Table 4.2, then to-be runs across the
   audited automation range; write 8.2–8.4.
4. **10, 11, 12, 13** — argumentative sections, drafted to budget once 8 exists.
   (9 waits for Phase 4.)

**Gate:** all sections exist in prose; unproven-assumption register (8.4) hands off
verbatim to the pilot charter (11.1).

## Phase 4 — Financial model & Monte Carlo (run "at the right time")

1. Rebuild the P&L drivers to consume `model/assumptions.csv` directly.
2. Build the Monte Carlo harness (Python, in this repo): input distributions from
   8.1 (automation rate), 9.3 (win-rate uplift, floored at zero in the conservative
   case), 9.4 (build cost, +30% overrun scenario); outputs NPV P10/P50/P90,
   probability of clearing the hurdle rate, tornado sensitivities, and the hostile
   conservative case.
3. Validate: model reproduces the as-is P&L before any to-be scenario is trusted —
   same calibration discipline as the process model.
4. Write Section 9 and the Innovo unit economics (9.6); backfill headline numbers
   into 1.3, 8, 13.

**Gate:** every Simulated tag in the paper traces to a register row and a model run.

## Phase 5 — Voice & anti-generation pass

One register throughout (recommend restrained first-person plural). Prune aphorisms
to ~one per section; break the "X is not Y; it is Z" habit; vary sentence rhythm;
reduce em-dash density; kill remaining meta-commentary. Verify every citation
against the original source and enforce the "re-cited downstream or deleted" rule.
Read-aloud test on Sections 1, 2.0, 7.9, 13 — the story-carrying passages.

## Phase 6 — Executive summary & final QA

Write Section 1 last, from the finished paper only. Then: mechanical tag audit;
page count measured on the actual formatted Doc at 1.5 spacing (not word-count
proxy); references formatted to programme standard; appendices confirmed excluded
from count; scaffolding sweep; final read by both authors.
