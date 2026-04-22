import numpy as np
import pandas as pd


def filter_ai_and_resample(ai_df: pd.DataFrame, dt_ms: float = 2.0, median_window: int = 10) -> pd.DataFrame:
    """
    Filter AI with median window and resample to constant TWT step.
    Expects columns: TWT_MS, IA, GR, RHOB, VEL_FROM_SONIC_MPS
    """
    work = ai_df.copy().sort_values("TWT_MS")
    work["AI_FILTERED"] = work["IA"].rolling(window=median_window, center=True, min_periods=1).median()

    # Use filtered AI support as base grid range.
    twt_src = work["TWT_MS"].astype(float).to_numpy()
    ai_src = work["AI_FILTERED"].astype(float).to_numpy()
    valid_ai = np.isfinite(twt_src) & np.isfinite(ai_src)
    if np.sum(valid_ai) < 2:
        raise ValueError("No hay suficientes muestras validas de AI_FILTERED para remuestrear.")

    twt_reg = np.arange(twt_src[valid_ai].min(), twt_src[valid_ai].max() + dt_ms, dt_ms)

    def _interp(col: str) -> np.ndarray:
        arr = work[col].astype(float).to_numpy()
        valid = np.isfinite(arr) & np.isfinite(twt_src)
        if np.sum(valid) < 2:
            return np.full_like(twt_reg, np.nan, dtype=float)
        return np.interp(twt_reg, twt_src[valid], arr[valid])

    out = pd.DataFrame(
        {
            "TWT_MS_REG": twt_reg,
            "GR": _interp("GR"),
            "RHOB": _interp("RHOB"),
            "VEL_FROM_SONIC_MPS": _interp("VEL_FROM_SONIC_MPS"),
            "AI_FILTERED": np.interp(twt_reg, twt_src[valid_ai], ai_src[valid_ai]),
        }
    )

    ai = out["AI_FILTERED"].to_numpy()
    ai_next = np.roll(ai, -1)
    denom = ai_next + ai
    rc = np.where(denom != 0, (ai_next - ai) / denom, np.nan)
    rc[-1] = np.nan
    out["RC"] = rc

    return out
