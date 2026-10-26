#!/usr/bin/env python3
"""T12: draft Sections 10-13 from their outlines.

Budgets (improvements.md section 7): 10 = 800, 11 = 800, 12 = 280, 13 = 380
words. D20 amendments: 10.3 has no venture exhibit; 11.1 uses PILOT-01
(EUR ~30k derived); 11.2 uses ADKAR; 11.3 carries the conservative working
rule (engineer releases every quote) with the indemnity question as a named
Phase 1 legal check. G11 fixed in 10.2 (flywheel = 7.1 / Exhibit 7.3). Risk
register kept as structured prose (no appendix version exists). Style
contract: no em dashes, no announced rigor.
"""
import sys

from doc_editor import run

S101 = (
    "Set side by side, the as-is and to-be business model canvases differ in "
    "only three blocks, and they are the ones that matter. Key activities "
    "shift from producing quotations to handling exceptions and curating the "
    "product data layer: the work moves from transcription to judgement, "
    "which is where 7.7 routes it. Cost structure shifts from variable labour "
    "that scales with inquiry volume to a largely fixed platform cost (9.4), "
    "which is what turns the 40 percent demand surge of 9.6 from a breaking "
    "load into an operating gain. The deepest change is in key resources. "
    "Today the branch\u2019s scarce asset is engineer expertise, and it "
    "walks out the door with every resignation (2.2). Under QuoteBench the "
    "compounding asset is proprietary transaction data: every RFQ, "
    "selection, price and win/loss outcome lands as a structured record "
    "(7.5), and the correction flywheel of 7.1 (Exhibit 7.3) converts daily "
    "operations into training data. Competitors can hire estimators; they "
    "cannot buy the branch\u2019s inquiry history."
)

S102 = (
    "The disintermediation question planted in 2.1 can now be answered with "
    "the paper\u2019s own evidence. Three futures compete. In the first, "
    "manufacturers automate selection and quotation and go direct: pump "
    "makers already publish sizing tools, and nothing prevents one from "
    "wrapping them in a quoting front end. In the second, contractors "
    "self-serve through those manufacturer tools, and the distributor\u2019s "
    "technical function is not captured by anyone; it simply stops being "
    "paid for. In the third, the distributor automates first and becomes "
    "the platform of record for its market: the layer through which "
    "multi-brand inquiries are specified, priced and won.\n"
    "Moving first makes the third future attainable for three reasons "
    "grounded in the design. Neutrality: a manufacturer\u2019s tool sizes "
    "its own pumps, while QuoteBench selects across brands on the "
    "contractor\u2019s constraints (7.4), and neutrality is what a "
    "manufacturer cannot credibly offer. Embedded workflow: the system "
    "ingests the contractor\u2019s documents as they actually arrive "
    "(7.3), fragmented, scanned and incomplete, which is the form the "
    "manufacturers\u2019 clean-input configurators refuse (5.2); whoever "
    "absorbs that mess owns the relationship. Compounding data: the "
    "correction flywheel of 7.1 (Exhibit 7.3) turns every routed inquiry "
    "into labelled training data, so the first mover\u2019s accuracy "
    "advantage widens with every quote. This is the reintermediation move "
    "of Chircu and Kauffman (2000): absorb the technology into the "
    "function that made the intermediary valuable, before a substitute "
    "occupies the position.\n"
    "The concession is genuine: the first future wins anyway under "
    "stateable conditions. If selection commoditizes to the point that "
    "contractors trust single-brand tools, if a manufacturer subsidizes "
    "direct quoting to buy the channel, or if the distributor\u2019s own "
    "automation stalls while 640 inquiries a year keep queueing, then the "
    "window closes. Section 11\u2019s stage gates are therefore strategic "
    "as well as financial: each phase that clears keeps the "
    "reintermediation option alive, and the moment they stop clearing, "
    "the conclusion is that this market\u2019s automation will be done to "
    "the distributor rather than by it."
)

S103 = (
    "Three options open once the platform runs. All are options, not "
    "commitments, and none enters a Section 9 number. Quotes-as-a-product: "
    "a guaranteed two-hour response on standard configurations, sold as a "
    "service level rather than granted as a favour; the simulated Tier 1 "
    "cycle time of 2 working hours (8.2) is what would make the promise "
    "printable, and 9.3\u2019s evidence says the speed is worth paying "
    "for. A contractor self-service portal: the same intake and "
    "selection layers exposed directly for simple configurations, with "
    "the branch\u2019s engineers behind the escalation path.\n"
    "Licensing is the third and least obvious: the extraction and routing "
    "layers are product-agnostic by construction (7.3, 12.2), and a valve "
    "or switchgear distributor in a non-competing market faces the same "
    "document mess. Each option would monetize the platform beyond one "
    "branch\u2019s P&L; none is needed for the investment to clear, which "
    "is what makes them options rather than promises."
)

S111 = (
    "Phase 1 is the validation experiment this paper could not run, priced "
    "at roughly \u20ac30,000 (S: one quarter of the build engineer-year "
    "plus pilot-scale running costs) inside the \u20ac92,000 build budget. "
    "For three months the pipeline runs in shadow on Tier 2, the modal "
    "inquiry and the richest document mix: the system drafts every quote, "
    "the draft is scored against the version the estimator actually "
    "releases, and nothing reaches a contractor unreviewed. The phase "
    "opens with the feasibility audit of Appendix E (25\u201330 historical "
    "RFQs scored field by field), the instrument 8.1 defers. The gates "
    "are evidential rather than financial, because 9.6 found no single "
    "lever that sinks the case within its tested range; what can sink it "
    "is the capability evidence itself. Gate 1, after the audit: if "
    "Khoory\u2019s documents score below the pessimistic bound of the 5.3 "
    "range, stop before any build spend. Gate 2, after roughly fifty "
    "shadow inquiries: live extraction accuracy at or above the "
    "pessimistic variant, an engineer override rate falling month on "
    "month, and zero would-be escaped defects against the released "
    "versions. Breach any of these and the recommendation reverts to "
    "Option A, the hire, with \u20ac30,000 spent buying that answer "
    "early. Phase 2 opens auto-draft for Tier 1 behind the same accuracy "
    "gates and begins measuring the win-rate response against the 2025 "
    "baseline, the one input shadow mode cannot test. Phase 3 makes "
    "assisted routing the Tier 2 default and revisits the deferred items "
    "(pricing optimization, CAD) on the strength of accumulated data "
    "(7.10)."
)

S112 = (
    "Change is sized to a six-person office, so we apply ADKAR at the "
    "level it operates: the individual estimator. Awareness is built on "
    "the leak, not the tool: the roughly \u20ac850,000 of 4.4 is shared "
    "with the estimators as the problem statement, because nobody defends "
    "a status quo that discounts away many times their salary. Desire "
    "rests on the redeployment promise of 9.2, made public before the "
    "pilot starts: the automation removes retyping, not engineers, and "
    "the senior estimator\u2019s job migrates toward the hardest projects "
    "and the exception queue. Knowledge comes from co-design: the "
    "estimators score the shadow quotes, tune the audit rubric of "
    "Appendix E, and set the first routing thresholds, so the "
    "system\u2019s judgement is visibly calibrated against theirs. "
    "Ability is the shadow quarter itself: three months in the review "
    "workspace with no release pressure. Reinforcement is the KPI "
    "change, from quotes produced, which rewards the queue, to win rate "
    "and margin per quote (11.5), which rewards what the branch sells. "
    "The known failure mode is automation bias (5.4); the design "
    "counters it by displaying confidence per field and making override "
    "a single click that feeds the flywheel."
)

S113 = (
    "Who signs an automated quote is unresolved, and the paper treats it "
    "conservatively. The working rule, priced into every projection, is "
    "that an engineer releases every quotation whatever lane drafted it "
    "(7.7): the automation rates of 8.2 and 9.5 assume machine drafting, "
    "never machine release, so the rule places no new ceiling on them. "
    "Whether professional-indemnity cover or UAE practice additionally "
    "requires full re-verification of Tier 1 auto-drafts, rather than "
    "review and release, is a fact question we could not close; it is a "
    "named Phase 1 legal check. If the answer is re-verification, Tier 1 "
    "touch time reverts toward its manual level and the labour benefit "
    "shrinks; the floor case of 9.5 absorbs even that. Contractor-facing "
    "trust is designed rather than assumed: every quote states its review "
    "status, and complex quotes carry the responsible engineer\u2019s "
    "name."
)

S114 = (
    "Seven risks, each with likelihood, impact, mitigation and an owner. "
    "Technical, documents messier than the published benchmarks "
    "(likelihood medium, impact high): the feasibility audit runs before "
    "any build and the pessimistic variant is already priced; owner, "
    "build lead. Commercial, contractors discounting system-assembled "
    "quotes (medium, medium): review-status labelling, engineer names on "
    "complex work, and the in-progress contractor interviews; owner, "
    "sales manager. Organizational, estimator attrition during "
    "transition (medium, high): the public redeployment promise and the "
    "senior\u2019s ownership of the exception queue; owner, branch "
    "manager. Legal, mis-specification liability (low, high): the "
    "engineer-release rule and the 11.3 legal check; owner, management "
    "with counsel. Vendor and model dependency (medium, medium): the "
    "extraction layer is bought behind an abstraction with a "
    "second-vendor fallback (7.3); owner, build lead. Data protection, "
    "contractor documents in third-party models (low, medium): "
    "in-tenant processing and no training on client documents without "
    "consent; owner, build lead. Model risk, the simulation itself being "
    "wrong (medium, high): the calibration gate of 8.2, shadow-mode "
    "scoring against reality, and kill criteria that do not depend on "
    "the model being right; owner, the authors."
)

S115 = (
    "The pilot and any rollout run on seven indicators, each mapped to "
    "the simulation output it validates or refutes: automation rate "
    "(share of fields drafted without intervention, against the 8.2 "
    "variants); override rate (engineer corrections per quote, the "
    "flywheel\u2019s input and the adoption signal); extraction accuracy "
    "(field level, against the 5.3 range the case is priced on); cycle "
    "time median and P90 by tier (against Exhibit 8.1); win rate by "
    "tier (against the measured 2025 rates and, from Phase 2, the 9.3 "
    "uplift); margin per quote (against the measured discount spread and "
    "the plus or minus 1 percent band); and error escapes (against the "
    "parity constraint of 8.2). Targets tighten by phase, and every "
    "number the dashboard produces replaces a simulated input with a "
    "measured one."
)

S121 = (
    "The limitations are structural and we state them without "
    "qualification. This is an ex-ante study: no part of QuoteBench "
    "exists and no implementation evidence is offered. The projections "
    "rest on a calibrated simulation fed by published benchmark ranges, "
    "not observed performance, and the feasibility audit that would "
    "ground extraction capability in Khoory\u2019s own documents is "
    "designed but not yet run. Contractor evidence is thin: interviews "
    "are in progress, and stated preferences may differ from revealed "
    "behaviour when a system-assembled quote actually arrives. The "
    "speed\u2013win elasticity is triangulated, not measured (9.3). The "
    "revenue base is a management figure and the tier value bands are "
    "re-derived from it rather than independently measured (9.1). "
    "CAD-dependent inquiries are out of scope entirely. These "
    "limitations define precisely the evidentiary agenda of the Phase 1 "
    "pilot in Section 11: each maps to a gate, a metric or a named "
    "check, which is what an ex-ante case can do about its own "
    "weaknesses."
)

S122 = (
    "Two things generalize; the numbers do not. The architecture pattern "
    "(probabilistic intake, a deterministic engineering core, and "
    "confidence-based routing that reserves people for the hardest "
    "cases) transfers to any engineered-product distribution business "
    "whose quoting runs on document extraction plus catalogue logic: "
    "valves, switchgear, HVAC equipment. So does the method: measure "
    "the baseline, register every assumption, calibrate a simulation "
    "against the measured state, and let a pilot attack the weakest "
    "inputs first. The specific economics, a 24 percent margin on "
    "\u20ac34.5 million of pump revenue through one six-person office, "
    "belong to one branch in one market and travel nowhere."
)

S13 = (
    "The first research question asked what process architecture could "
    "automate RFQ handling while preserving quote quality, and what "
    "evidence supports its feasibility. The answer is the layered design "
    "of Section 7: probabilistic extraction quarantined behind "
    "confidence scores, a deterministic selection core, and routing that "
    "sends every uncertain field to an engineer, with every quote "
    "released by one. Its feasibility rests on published benchmark "
    "ranges carried as three variants (8.1) and on a process simulation "
    "that reproduced the measured 2025 baseline on fifteen checks before "
    "projecting anything (8.2); in the simulated central case, median "
    "cycle time falls from 18, 39 and 88 working hours by tier to 2, 9 "
    "and 56, with engineer touch time roughly halved.\n"
    "The second asked the projected financial impact and its robustness. "
    "The simulated central case is about \u20ac990,000 a year at full "
    "adoption on the branch\u2019s stated \u20ac34.5 million revenue, "
    "led by discounting discipline and the win-rate uplift; simulated "
    "five-year NPV spans \u20ac1.4 to \u20ac4.3 million from P10 to P90, "
    "and the floor case, with the uplift at zero and extraction at its "
    "pessimistic bound, still clears the 15 percent hurdle (9.5). "
    "Robustness was tested rather than asserted: across eight stress "
    "scenarios and six boundary searches, no single lever within its "
    "tested range sinks the case (9.6). What remains uncertain is not "
    "the arithmetic but the inputs beneath it, which no simulation can "
    "settle.\n"
    "The third asked what the transformation means for the "
    "distributor\u2019s position in the value chain. Section 10\u2019s "
    "answer: automated quoting converts inquiry flow into proprietary "
    "transaction data, the one asset in this channel that neither "
    "manufacturers nor marketplaces hold, and the reintermediation "
    "condition from the literature, moving before a substitute occupies "
    "the position, is satisfiable today and will not remain so "
    "indefinitely.\n"
    "We therefore recommend what Section 1 promised: not the system, "
    "the experiment. Approve Phase 1 only, a three-month \u20ac30,000 "
    "shadow-mode pilot with pre-committed kill criteria, opening with "
    "the feasibility audit on Khoory\u2019s own documents (11.1). Every "
    "number above the measured baseline is simulated; the pilot is "
    "priced at what it costs to replace the most important simulations "
    "with facts.\n"
    "If the pilot returns what the simulation projects, the Innovo "
    "inquiry of Section 2 would read differently the next time it "
    "arrives: the same RFQ, one day instead of seven, reviewed by an "
    "engineer whose expertise is spent on the ten hardest projects on "
    "her desk rather than the forty easiest, and a flagship package "
    "quoted inside its deadline instead of against it. That future is "
    "worth a \u20ac30,000 experiment to prove."
)

EDITS = [
    {"find": ("As-Is and proposed To-Be side by side (full size in appendix); "
              "commentary only on blocks that change. The key insight to "
              "surface: the key resource would migrate from engineer "
              "expertise to proprietary transaction data (RFQs \u00d7 "
              "selections \u00d7 prices \u00d7 win/loss outcomes), a "
              "compounding asset competitors cannot buy."),
     "replace": S101, "unbold": True},
    {"find": ("Three futures: (a) manufacturers automate selection and go "
              "direct; (b) contractors self-serve via manufacturer tools; "
              "(c) the distributor automates first and becomes the "
              "multi-manufacturer platform of record. Argue why moving first "
              "makes (c) attainable (neutrality across brands, embedded "
              "contractor workflow, the data flywheel from 7.6), and concede "
              "the conditions under which (a) wins anyway. The ex-ante frame "
              "strengthens this section: you are arguing about strategic "
              "option value, which is inherently forward-looking. Give it a "
              "full page; it is the paper\u2019s intellectual climax."),
     "replace": S102, "unbold": True},
    {"find": ("Two paragraphs, labelled as options not commitments: "
              "quotes-as-a-product (\u201c2-hour guaranteed response\u201d), "
              "a contractor self-service portal, licensing the capability to "
              "non-competing distributors."),
     "replace": S103, "unbold": True},
    {"find": ("Reframe Phase 1 explicitly as the validation experiment this "
              "paper could not run: a bounded pilot (e.g., 3 months, one RFQ "
              "tier, shadow-mode operation alongside the manual process) "
              "designed to test, one for one, the unproven-assumption "
              "register from 8.4: live extraction accuracy, review time, "
              "engineer adoption, contractor reaction. Each gate carries "
              "metric thresholds and kill criteria (\u201cif live extraction "
              "accuracy < X% after N RFQs, stop and revert to Option "
              "A\u201d). Recommending an investment with pre-committed kill "
              "criteria is the most credible posture available to an ex-ante "
              "business case."),
     "replace": S111, "unbold": True},
    {"find": ("One framework (Kotter or ADKAR), applied not recited. Core "
              "moves: engineers co-design and run the pilot; KPIs redesigned "
              "from quotes-produced to win-rate-and-margin; the redeployment "
              "promise from 9.2 made explicit and public early."),
     "replace": S112, "unbold": True},
    {"find": ("Who would legally sign an automated quote? Does "
              "professional-indemnity insurance require an engineer\u2019s "
              "approval, and if yes, what ceiling does that place on the "
              "automation rate assumed in 8.2 and 9.5? Close the loop "
              "explicitly; catching this circularity is worth real marks. "
              "Include contractor-facing trust design: quotes state review "
              "status; complex quotes always carry an engineer\u2019s name."),
     "replace": S113, "unbold": True},
    {"find": ("Table (full version in appendix): technical (real documents "
              "exceed audited sample messiness) \u00b7 commercial "
              "(contractors discount automated quotes) \u00b7 organizational "
              "(engineer attrition) \u00b7 legal (mis-specification "
              "liability) \u00b7 vendor/model dependency \u00b7 data "
              "protection \u00b7 model risk (new): the simulation itself may "
              "be wrong, mitigated by the calibration in 8.2 and the pilot "
              "in 11.1. Likelihood \u00d7 impact \u00d7 mitigation \u00d7 "
              "owner."),
     "replace": S114, "unbold": True},
    {"find": ("The seven KPIs the pilot and any rollout would run on: "
              "automation rate, override rate, extraction accuracy, cycle "
              "time (median/P90), win rate, margin per quote, error escapes, "
              "each with a target trajectory by phase, and each mapped to "
              "the simulation output it validates or refutes."),
     "replace": S115, "unbold": True},
    {"find": ("Stated plainly and without apology: ex-ante study, no "
              "implementation evidence; projections rest on a calibrated "
              "simulation and an audited sample, not observed performance; "
              "stated contractor preferences may differ from revealed "
              "behaviour; elasticities triangulated, not experimental; CAD "
              "out of scope. Then the turn: \u201cThese limitations define "
              "precisely the evidentiary agenda of the Phase 1 pilot "
              "proposed in Section 11.\u201d Limitations that flow into a "
              "designed next step read as strength, not weakness."),
     "replace": S121, "unbold": True},
    {"find": ("The architecture pattern (probabilistic intake + "
              "deterministic engineering + confidence routing) and the "
              "ex-ante evaluation method both generalize to "
              "engineered-product distribution (HVAC, valves, switchgear); "
              "the specific economics do not. One sentence of discipline."),
     "replace": S122, "unbold": True},
    {"find": ("\u2022    Answer RQ1, RQ2, RQ3 in order, one paragraph each, "
              "with the evidence tag visible in the prose (\u201cthe audited "
              "feasibility range\u2026\u201d, \u201cthe simulated P50 "
              "NPV\u2026\u201d).\n"
              "\u2022    State the recommendation exactly as framed in 1.5: "
              "a stage-gated pilot investment with explicit kill criteria: a "
              "decision under uncertainty, honestly priced.\n"
              "\u2022    Close on Innovo, in the conditional: the same RFQ, "
              "one day instead of seven, reviewed by an engineer whose "
              "expertise would be trained on the ten hardest projects on her "
              "desk rather than the forty easiest, a future this analysis "
              "suggests is worth a \u20acX experiment to prove. End the "
              "story you opened with.\n"),
     "replace": S13 + "\n", "unbold": True},
]

if __name__ == "__main__":
    for name, s in (("S10", S101 + S102 + S103), ("S11", S111 + S112 + S113 + S114 + S115),
                    ("S12", S121 + S122), ("S13", S13)):
        print(f"{name}: {len(s.split())} words")
    run(EDITS, apply="--apply" in sys.argv)
