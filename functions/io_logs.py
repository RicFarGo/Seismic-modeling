import numpy as np
import pandas as pd


def parse_ascii_las_like(file_path: str, null_value: float = -999.25) -> pd.DataFrame:
    """Parse LAS-like text file and return standard log dataframe."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    start_idx = None
    for i, line in enumerate(lines):
        if line.strip().upper().startswith("~ASCII"):
            start_idx = i + 1
            break

    if start_idx is None:
        raise ValueError("No se encontro la seccion ~Ascii Data Section en el archivo.")

    rows = []
    for line in lines[start_idx:]:
        text = line.strip()
        if not text or text.startswith("#") or text.startswith("~"):
            continue

        parts = text.split()
        if len(parts) < 5:
            continue

        try:
            rows.append([float(parts[0]), float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])])
        except ValueError:
            continue

    if not rows:
        raise ValueError("No se pudieron extraer datos numericos del bloque ASCII.")

    df = pd.DataFrame(rows, columns=["DEPT", "DT", "GR", "RHOB", "PVEL"])
    return df.replace(null_value, np.nan)
