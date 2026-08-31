import json
from pathlib import Path
from openpyxl import load_workbook
import pandas as pd


def _norm(s):
    import re
    return re.sub(r'[^a-z0-9]+',' ',str(s).lower()).strip()

def _find_col(df, candidates):
    cmap={_norm(c):c for c in df.columns}
    for x in candidates:
        if _norm(x) in cmap:return cmap[_norm(x)]
    for c in df.columns:
        if any(_norm(x) in _norm(c) for x in candidates):return c
    return None

def _total(df,candidates):
    c=_find_col(df,candidates)
    if not c:return None,c
    return float(pd.to_numeric(df[c],errors='coerce').fillna(0).sum()),c

def build_qa(processor):
    required=['Cuadro de Mando','Comp 2025-2026','Comp PP 2025-2026','Comp Aportes','80-20','Oportunidad Crecimiento','Oport Crecimiento Zona']
    checks=[]
    for s in required:
        checks.append({'type':'required_sheet','sheet':s,'status':'OK' if s in processor.sheets else 'ERROR','message':'Hoja disponible' if s in processor.sheets else 'Hoja faltante'})
    for s, candidates in {
        'Comp Aportes':[['Aporte Total 2025'],['Aporte Parcial 2025'],['Aporte Parcial 2026'],['Diferencia Aporte','Dif Aporte']],
        'Oportunidad Crecimiento':[['Aporte Total 2025'],['1% Imponible'],['Diferencia Aporte','Dif Aporte']],
        '80-20':[['2025','Aporte 2025','Aportes 2025','Aporte Total 2025'],['2026','Aporte 2026','Aportes 2026','Aporte Total 2026']]
    }.items():
        df=processor.frames.get(s,pd.DataFrame())
        for cand in candidates:
            total,col=_total(df,cand)
            checks.append({'type':'independent_total','sheet':s,'column':str(col or ' / '.join(cand)),'records':len(df),'python_total':total,'status':'OK' if col else 'WARNING','message':'Total reproducible desde registros' if col else 'No se encontró columna equivalente'})
    return {'status':'ERROR' if any(x['status']=='ERROR' for x in checks) else ('WARNING' if any(x['status']=='WARNING' for x in checks) else 'OK'),'checks':len(checks),'errors':sum(x['status']=='ERROR' for x in checks),'warnings':sum(x['status']=='WARNING' for x in checks),'checks_detail':checks,'source':str(processor.path.name),'last_reload':processor.last_reload}
