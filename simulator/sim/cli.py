import argparse
import sys


def main():
    ap = argparse.ArgumentParser(prog="sim", description="QuoteBench branch simulator")
    sub = ap.add_subparsers(dest="cmd")
    f = sub.add_parser("fit", help="calibrate as-is residual-queue parameters")
    f.add_argument("--years", type=int, default=6)
    r = sub.add_parser("report", help="reports")
    r.add_argument("what", choices=["calibration"])
    r.add_argument("--seed", type=int, default=42)
    r.add_argument("--years", type=int, default=12)
    tb = sub.add_parser("tobe", help="to-be projection vs the calibrated baseline")
    tb.add_argument("--variant", choices=["optimistic", "central", "pessimistic"],
                    default="central")
    tb.add_argument("--seed", type=int, default=42)
    tb.add_argument("--years", type=int, default=8)
    pl = sub.add_parser("pnl", help="economics: P&L + five-year Monte Carlo case")
    pl.add_argument("--seed", type=int, default=42)
    pl.add_argument("--jobs", type=int, default=None,
                    help="parallel DES workers (default: cores-1; env SIM_JOBS)")
    st = sub.add_parser("stress", help="stress scenarios, tornado, kill criteria")
    st.add_argument("--all", action="store_true", default=True)
    st.add_argument("--seed", type=int, default=42)
    st.add_argument("--jobs", type=int, default=None,
                    help="parallel DES workers (default: cores-1; env SIM_JOBS)")
    op = sub.add_parser("optimize", help="SIM-5: search the design operating point")
    op.add_argument("--seed", type=int, default=42)
    op.add_argument("--jobs", type=int, default=None,
                    help="parallel DES workers (default: cores-1; env SIM_JOBS)")
    op.add_argument("--no-register", action="store_true",
                    help="do not write SIM5-* rows to model/assumptions.csv")
    fg = sub.add_parser("figures", help="SIM-6: export the four paper figures")
    fg.add_argument("--seed", type=int, default=42)
    fg.add_argument("--jobs", type=int, default=None,
                    help="parallel DES workers (default: cores-1; env SIM_JOBS)")
    al = sub.add_parser("all", help="run every simulation with written "
                        "descriptions + findings, then export figures")
    al.add_argument("--seed", type=int, default=42)
    al.add_argument("--jobs", type=int, default=None,
                    help="parallel DES workers (default: cores-1; env SIM_JOBS)")
    al.add_argument("--no-figures", action="store_true",
                    help="skip figure export (written output only)")
    t = sub.add_parser("run", help="run scenarios")
    t.add_argument("--mode", choices=["asis", "tobe"], default="tobe")
    t.add_argument("--variant", choices=["optimistic", "central", "pessimistic"],
                   default="central")
    t.add_argument("--seed", type=int, default=42)
    t.add_argument("--years", type=int, default=8)
    args = ap.parse_args()

    if args.cmd == "fit":
        from .fit import fit
        fit(years=args.years)
    elif args.cmd == "report":
        from .report import calibration_report
        sys.exit(0 if calibration_report(seed=args.seed, years=args.years) else 1)
    elif args.cmd == "tobe":
        from .report import calibration_report, tobe_report
        print("Checking calibration gate first...\n")
        if not calibration_report():
            sys.exit("To-be mode locked: calibration gate failed.")
        print()
        tobe_report(variant=args.variant, seed=args.seed, years=args.years)
    elif args.cmd == "pnl":
        from .report import calibration_report, pnl_report
        print("Checking calibration gate first...\n")
        if not calibration_report():
            sys.exit("Economics locked: calibration gate failed.")
        print()
        sys.exit(0 if pnl_report(seed=args.seed, jobs=args.jobs) else 1)
    elif args.cmd == "stress":
        from .report import calibration_report
        from .stress import stress_all
        print("Checking calibration gate first...\n")
        if not calibration_report():
            sys.exit("Stress harness locked: calibration gate failed.")
        print()
        stress_all(seed=args.seed, jobs=args.jobs)
    elif args.cmd == "optimize":
        from .report import calibration_report
        from .optimize import optimize
        print("Checking calibration gate first...\n")
        if not calibration_report():
            sys.exit("Optimizer locked: calibration gate failed.")
        print()
        optimize(seed=args.seed, write_register=not args.no_register,
                 jobs=args.jobs)
    elif args.cmd == "figures":
        from .figures import export_all
        export_all(seed=args.seed, jobs=args.jobs)
    elif args.cmd == "all":
        from .runall import run_all
        sys.exit(0 if run_all(seed=args.seed, jobs=args.jobs,
                              make_figures=not args.no_figures) else 1)
    elif args.cmd == "run":
        from .report import calibration_report, tobe_report
        if args.mode == "tobe":
            print("Checking calibration gate first...\n")
            if not calibration_report():
                sys.exit("To-be mode locked: calibration gate failed.")
            print()
            tobe_report(variant=args.variant, seed=args.seed, years=args.years)
        else:
            sys.exit(0 if calibration_report(seed=args.seed, years=args.years) else 1)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
