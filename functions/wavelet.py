import numpy as np


def ricker_wavelet(f0_hz: float = 20.0, length_ms: float = 128.0, dt_ms: float = 2.0):
    """Return time axis (ms) and normalized Ricker wavelet."""
    half_len_ms = length_ms / 2.0
    tw_ms = np.arange(-half_len_ms, half_len_ms + dt_ms, dt_ms)
    tw_s = tw_ms / 1000.0

    pi2f2t2 = (np.pi**2) * (f0_hz**2) * (tw_s**2)
    wavelet = (1.0 - 2.0 * pi2f2t2) * np.exp(-pi2f2t2)

    max_abs = np.max(np.abs(wavelet))
    if max_abs > 0:
        wavelet = wavelet / max_abs

    return tw_ms, wavelet


def synthetic_from_rc(rc: np.ndarray, wavelet: np.ndarray) -> np.ndarray:
    """Create synthetic trace with same sample count as RC."""
    rc_conv = np.nan_to_num(rc, nan=0.0, posinf=0.0, neginf=0.0)
    return np.convolve(rc_conv, wavelet, mode="same")
