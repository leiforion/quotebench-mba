"""SIM-7: AWS infrastructure cost model, broken down by service.

Prices are OnDemand list, region Middle East (UAE) me-central-1, captured from
the AWS Price List API on 2026-09-13 (see data/parameters_infra.yaml for the
per-line source usage-type). Textract is priced in Mumbai (not offered in UAE);
OpenAI CAD reading is an external non-AWS line.

The model is deliberately transparent arithmetic on volume drivers: at
~5,500 inquiries/year the per-call AI cost is small and the always-on data
services (Aurora, OpenSearch) dominate. Everything returns USD internally and
is converted to EUR with eur_per_usd.

Usage-linked lines scale with the adoption ramp when scale_by_ramp is passed;
always-on lines (Aurora, OpenSearch, Fargate, Cognito) do not.
"""
import os

import yaml

from .config import BASE

HOURS_PER_MONTH = 730.0
MONTHS = 12.0

PARAMS_INFRA = os.path.join(BASE, "data", "parameters_infra.yaml")


def load_infra():
    with open(PARAMS_INFRA) as f:
        return yaml.safe_load(f)


# lines that scale with processed volume (adoption ramp) vs always-on
USAGE_LINKED = {"Bedrock (extraction)", "Textract (OCR, cross-border)",
                "OpenAI (CAD, external)", "Step Functions", "Lambda", "SES",
                "S3 (documents)", "DynamoDB (catalogue)"}


def annual_usd_by_service(p, n_inquiries=None):
    """Full-adoption annual cost in USD per service (dict, ordered largest ...)."""
    n = p["inquiries_per_year"] if n_inquiries is None else n_inquiries
    out = {}

    # ---- Bedrock extraction ----
    m = p["bedrock"]["models"][p["bedrock"]["model"]]
    in_tok = p["bedrock"]["input_tokens_per_inquiry"] * n / 1000.0
    out_tok = p["bedrock"]["output_tokens_per_inquiry"] * n / 1000.0
    out["Bedrock (extraction)"] = in_tok * m["in_per_1k"] + out_tok * m["out_per_1k"]

    # ---- Textract OCR (cross-border) or folded into Bedrock ----
    tx = p["textract"]
    if tx["enabled"]:
        pages = n * tx["ocr_share_of_inquiries"] * tx["pages_per_ocr_inquiry"]
        out["Textract (OCR, cross-border)"] = pages * tx["price_per_page"]

    # ---- OpenAI CAD (external) ----
    cad = p["openai_cad"]
    if cad["enabled"]:
        calls = n * cad["cad_share_of_inquiries"]
        out["OpenAI (CAD, external)"] = (
            calls * (cad["input_tokens_per_call"] / 1000.0 * cad["in_per_1k"]
                     + cad["output_tokens_per_call"] / 1000.0 * cad["out_per_1k"]))

    # ---- Aurora (always-on) ----
    a = p["aurora"]
    out["Aurora PostgreSQL"] = (
        a["avg_acu"] * a["acu_price_hr"] * HOURS_PER_MONTH * MONTHS
        + a["storage_gb"] * a["storage_price_gb_mo"] * MONTHS
        + a["io_millions_per_year"] * a["io_price_per_million"])

    # ---- DynamoDB (usage + storage) ----
    d = p["dynamodb"]
    out["DynamoDB (catalogue)"] = (
        n * d["writes_per_inquiry"] / 1e6 * d["write_per_million"]
        + n * d["reads_per_inquiry"] / 1e6 * d["read_per_million"]
        + d["storage_gb"] * d["storage_price_gb_mo"] * MONTHS)

    # ---- OpenSearch managed (always-on) ----
    o = p["opensearch"]
    inst = o["instances"][o["option"]]
    out["OpenSearch (vector)"] = (
        inst["count"] * inst["price_hr"] * HOURS_PER_MONTH * MONTHS
        + inst["count"] * o["ebs_gb_per_node"] * o["ebs_price_gb_mo"] * MONTHS)

    # ---- S3 (accumulating store, averaged over retention) ----
    s = p["s3"]
    gb_added_per_year = n * s["mb_per_inquiry"] / 1024.0
    # average GB present over the horizon given accumulation up to retention
    horizon = p["horizon_years"]
    avg_gb = gb_added_per_year * min(horizon, s["retention_years"] + 1) / 2.0
    out["S3 (documents)"] = avg_gb * s["storage_price_gb_mo"] * MONTHS

    # ---- Step Functions ----
    sf = p["step_functions"]
    out["Step Functions"] = (n * sf["transitions_per_inquiry"]
                             * sf["price_per_transition"])

    # ---- Lambda ----
    l = p["lambda"]
    inv = n * l["invocations_per_inquiry"]
    out["Lambda"] = (inv * l["price_per_request"]
                     + inv * l["gb_seconds_per_invocation"] * l["price_per_gb_second"])

    # ---- SES ----
    se = p["ses"]
    out["SES (email)"] = n * se["emails_per_inquiry"] * se["price_per_email"]

    # ---- Cognito ----
    out["Cognito (auth)"] = p["cognito"]["monthly_cost"] * MONTHS

    # ---- Fargate web app (always-on) ----
    fg = p["fargate"]
    out["Fargate (web app)"] = (
        fg["tasks"] * (fg["vcpu_per_task"] * fg["vcpu_price_hr"]
                       + fg["gb_per_task"] * fg["gb_price_hr"])
        * HOURS_PER_MONTH * MONTHS)

    return dict(sorted(out.items(), key=lambda kv: -kv[1]))


def cost_model(p=None, ramp=None):
    """Full 5-year infrastructure cost model.

    ramp: optional per-year adoption fractions (usage-linked lines scale by it,
    always-on lines are full from year 1). Returns a dict with per-service
    annual (full-adoption) EUR, the by-year EUR total, and the 5-year total.
    """
    p = p or load_infra()
    fx = p["eur_per_usd"]
    usd = annual_usd_by_service(p)
    eur = {k: v * fx for k, v in usd.items()}
    annual_full_eur = sum(eur.values())

    horizon = p["horizon_years"]
    ramp = ramp or [1.0] * horizon
    by_year = []
    for y in range(horizon):
        r = ramp[y] if y < len(ramp) else 1.0
        yr = 0.0
        for k, v in eur.items():
            yr += v * (r if k in USAGE_LINKED else 1.0)
        by_year.append(yr)

    return {
        "eur_per_usd": fx,
        "by_service_eur": eur,          # full-adoption annual, per service
        "by_service_usd": usd,
        "annual_full_eur": annual_full_eur,
        "by_year_eur": by_year,         # respects ramp on usage-linked lines
        "five_year_eur": sum(by_year),
        "model": p["bedrock"]["model"],
        "opensearch_option": p["opensearch"]["option"],
    }


def _svc_type(service):
    return "per-inquiry" if service in USAGE_LINKED else "always-on"


def format_breakdown(cm):
    """A report-ready, bordered table of the AWS cost by service (annual EUR at
    full adoption) plus the 5-year ramped view. All prices are OnDemand list,
    Middle East (UAE) me-central-1 (Textract: Mumbai), captured 2026-09-13."""
    total = cm["annual_full_eur"]
    SVC, TYP, USD, EUR, SH = 30, 12, 11, 11, 7
    inner = 1 + SVC + TYP + USD + EUR + SH + 1          # incl. edge spaces
    W = inner + 2
    top = "+" + "-" * (W - 2) + "+"
    rule = "|" + "-" * (W - 2) + "|"

    def band(text):                                     # full-width text row
        return "| " + f"{text[:inner - 2]:<{inner - 2}}" + " |"

    def cells(svc, typ, usd, eur, sh):
        svc = svc if len(svc) <= SVC - 1 else svc[:SVC - 2] + "\u2026"
        return ("| " + f"{svc:<{SVC}}{typ:<{TYP}}{usd:>{USD}}"
                f"{eur:>{EUR}}{sh:>{SH}}" + " |")

    lines = [top,
             band("AWS INFRASTRUCTURE COST BY SERVICE  (EUR/yr, full adoption)"),
             band(f"Bedrock={cm['model']}  OpenSearch={cm['opensearch_option']}"
                  f"  FX: 1 USD = {cm['eur_per_usd']:.4f} EUR"),
             rule,
             cells("Service", "Type", "USD/yr", "EUR/yr", "Share"),
             rule]
    for k, v in cm["by_service_eur"].items():
        lines.append(cells(k, _svc_type(k), f"{cm['by_service_usd'][k]:,.0f}",
                           f"{v:,.0f}", f"{100 * v / total:.1f}%"))
    lines.append(rule)
    tot_usd = sum(cm["by_service_usd"].values())
    lines.append(cells("TOTAL (annual, full)", "", f"{tot_usd:,.0f}",
                       f"{total:,.0f}", "100.0%"))
    lines.append(top)

    # 5-year ramped view
    by_year = cm["by_year_eur"]
    lines.append("")
    lines.append("5-YEAR VIEW (usage-linked lines scale with the adoption ramp;"
                 " always-on lines full from Y1):")
    lines.append("  " + "".join(f"{'Y' + str(i + 1):>12}"
                                for i in range(len(by_year)))
                 + f"{'5-yr total':>14}")
    lines.append("  " + "".join(f"{y:>12,.0f}" for y in by_year)
                 + f"{cm['five_year_eur']:>14,.0f}")
    return "\n".join(lines)


def write_cost_csv(cm, path):
    """Write the by-service breakdown to CSV for direct use in a report."""
    import csv
    total = cm["annual_full_eur"]
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["service", "type", "usd_per_year", "eur_per_year",
                    "share_pct"])
        for k, v in cm["by_service_eur"].items():
            w.writerow([k, _svc_type(k), round(cm["by_service_usd"][k], 2),
                        round(v, 2), round(100 * v / total, 2)])
        w.writerow(["TOTAL annual (full adoption)", "",
                    round(sum(cm["by_service_usd"].values()), 2),
                    round(total, 2), 100.0])
        w.writerow([])
        w.writerow(["year"] + [f"Y{i + 1}" for i in range(len(cm["by_year_eur"]))]
                   + ["5yr_total"])
        w.writerow(["eur"] + [round(y, 2) for y in cm["by_year_eur"]]
                   + [round(cm["five_year_eur"], 2)])
    return path


if __name__ == "__main__":
    print(format_breakdown(cost_model()))
