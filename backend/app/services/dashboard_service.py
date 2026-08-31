from typing import Optional
import pandas as pd

def _find_col(df, candidates):
    normalized = {str(c).strip().lower(): c for c in df.columns}
    for candidate in candidates:
        if candidate.lower() in normalized:
            return normalized[candidate.lower()]
    for c in df.columns:
        lc = str(c).lower()
        if any(candidate.lower() in lc for candidate in candidates):
            return c
    return None

def filter_rows(rows, holding=None, ejecutiva=None, zona=None):
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    for param, candidates in [
        (holding, ["holding"]),
        (ejecutiva, ["ejecutiva"]),
        (zona, ["zona"]),
    ]:
        if param:
            col = _find_col(df, candidates)
            if col:
                values = {x.strip().lower() for x in str(param).split(",")}
                df = df[df[col].astype(str).str.strip().str.lower().isin(values)]
    return df

def numeric_sum(df, candidates):
    col = _find_col(df, candidates)
    if not col:
        return 0
    return float(pd.to_numeric(df[col], errors="coerce").fillna(0).sum())

def metrics_aportes(rows, holding=None, ejecutiva=None):
    df = filter_rows(rows, holding, ejecutiva)
    total_2025 = numeric_sum(df, ["Aporte Total 2025"])
    parcial_2025 = numeric_sum(df, ["Aporte Parcial 2025"])
    parcial_2026 = numeric_sum(df, ["Aporte Parcial 2026"])
    diff = numeric_sum(df, ["Diferencia Aporte"])
    growth = (diff / parcial_2025 * 100) if parcial_2025 else None
    return {
        "aporte_total_2025": total_2025,
        "aporte_parcial_2025": parcial_2025,
        "aporte_parcial_2026": parcial_2026,
        "diferencia": diff,
        "crecimiento_pct": growth,
        "empresas": int(len(df)),
    }

def metrics_oportunidad(rows, ejecutiva=None, zona=None):
    df = filter_rows(rows, ejecutiva=ejecutiva, zona=zona)
    actual = numeric_sum(df, ["Aporte Total 2025"])
    potential = numeric_sum(df, ["1% Imponible", "1% imponible"])
    opportunity = numeric_sum(df, ["Diferencia Aporte"])
    return {
        "aporte_actual": actual,
        "potencial": potential,
        "oportunidad": opportunity,
        "empresas": int(len(df)),
        "potencial_pct": (opportunity / actual * 100) if actual else None,
    }

def unique_values(rows, candidate):
    df = pd.DataFrame(rows)
    col = _find_col(df, [candidate]) if not df.empty else None
    if not col:
        return []
    return sorted([str(x) for x in df[col].dropna().unique()])
