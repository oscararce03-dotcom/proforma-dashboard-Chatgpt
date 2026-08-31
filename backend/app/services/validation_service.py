import math
import pandas as pd
from ..processors.excel_processor import REQUIRED_SHEETS

def clean_number(x):
    try:
        if pd.isna(x): return None
        y=float(x)
        if not math.isfinite(y): return None
        return y
    except: return None

def validate_workbook(processor):
    result={"status":"OK","checks":[],"sheets":processor.sheets,"records":{}}
    for s in REQUIRED_SHEETS:
        exists=s in processor.frames
        result["checks"].append({"name":f"Hoja requerida: {s}","status":"OK" if exists else "ERROR"})
    for s,df in processor.frames.items():
        result["records"][s]=int(len(df))
        result["checks"].append({
            "name":f"Datos legibles: {s}",
            "status":"OK" if isinstance(df,pd.DataFrame) else "ERROR"
        })
    if any(c["status"]=="ERROR" for c in result["checks"]): result["status"]="ERROR"
    return result
