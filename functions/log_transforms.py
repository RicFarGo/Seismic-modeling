import numpy as np
import pandas as pd


def add_time_domain_logs(df: pd.DataFrame) -> pd.DataFrame:
    """Add velocity and time-sampling related logs from depth-domain logs."""
    out = df.sort_values("DEPT").reset_index(drop=True).copy()

    out["VEL_FROM_SONIC_MPS"] = 304800.0 / out["DT"]
    out["DEPTH_SAMPLING_M"] = out["DEPT"].shift(-1) - out["DEPT"]
    out["TIME_SAMPLING_SEC"] = out["DEPTH_SAMPLING_M"] / out["VEL_FROM_SONIC_MPS"]
    out["TWT_SAMPLING_MS"] = 2.0 * out["TIME_SAMPLING_SEC"] * 1000.0

    twt_sampling = out["TWT_SAMPLING_MS"].replace([np.inf, -np.inf], np.nan).fillna(0.0)
    out["TWT_MS"] = twt_sampling.cumsum()

    return out


def add_ai(df: pd.DataFrame) -> pd.DataFrame:
    """Add acoustic impedance from sonic velocity and density."""
    out = df.copy()
    out["IA"] = out["VEL_FROM_SONIC_MPS"] * out["RHOB"]
    return out
