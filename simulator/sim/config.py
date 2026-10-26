import hashlib
import os

import yaml

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARAMS_ASIS = os.path.join(BASE, "data", "parameters_asis.yaml")
FITTED_ASIS = os.path.join(BASE, "data", "fitted_asis.yaml")
PARAMS_TOBE = os.path.join(BASE, "data", "parameters_tobe.yaml")
PARAMS_ECON = os.path.join(BASE, "data", "parameters_econ.yaml")


def load_tobe():
    with open(PARAMS_TOBE) as f:
        return yaml.safe_load(f)


def load_econ():
    with open(PARAMS_ECON) as f:
        return yaml.safe_load(f)


def load_asis():
    """Hand-written parameters merged with machine-fitted values (if present)."""
    with open(PARAMS_ASIS) as f:
        params = yaml.safe_load(f)
    if os.path.exists(FITTED_ASIS):
        with open(FITTED_ASIS) as f:
            params["fitted"] = yaml.safe_load(f)
    else:
        params["fitted"] = None
    return params


def save_fitted(fitted):
    with open(FITTED_ASIS, "w") as f:
        f.write("# Written by `python -m sim fit`. External + administrative wait\n"
                "# per tier (contractor answers, pricing approval, dispatch\n"
                "# batching), calibrated to BASE-15/16. Do not edit by hand.\n")
        yaml.safe_dump(fitted, f, sort_keys=False)


def is_fitted(params):
    return params.get("fitted") is not None


def params_checksum():
    h = hashlib.sha256()
    for path in (PARAMS_ASIS, FITTED_ASIS, PARAMS_TOBE, PARAMS_ECON):
        if os.path.exists(path):
            with open(path, "rb") as f:
                h.update(f.read())
    return h.hexdigest()[:12]
