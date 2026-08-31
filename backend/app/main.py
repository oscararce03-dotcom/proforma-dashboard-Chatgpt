from .services.lazy_data import get_processor
import logging
from typing import Optional
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .config import DATA_FILE, FRONTEND_URL
from .auth import authenticate, current_user
from .processors.excel_processor import ExcelProcessor
from .services.dashboard_service import metrics_aportes, metrics_oportunidad, filter_rows, unique_values
from .services.validation_service import validate_workbook
from .services.qa_service import build_qa

logging.basicConfig(level=logging.INFO)
app=FastAPI(title='PROFORMA DASHBOARD API',version='5.0.0')

@app.get("/api/health")
def health():
    return {"status":"ok","excel_loaded":False}

app.add_middleware(CORSMiddleware,allow_origins=[FRONTEND_URL,'http://localhost:5173'],allow_credentials=True,allow_methods=['GET','POST'],allow_headers=['*'])
processor=ExcelProcessor(DATA_FILE); processor.load()
class LoginRequest(BaseModel): username:str; password:str
@app.get('/api/health')
def health(): return {'status':'ok','version':'5.0.0'}
@app.post('/api/auth/login')
def login(body:LoginRequest): return {'access_token':authenticate(body.username,body.password)}
@app.get('/api/me')
def me(user=Depends(current_user)): return user
@app.get('/api/admin/status')
def status(user=Depends(current_user)): return processor.summary()
@app.get('/api/admin/validation')
def validation(user=Depends(current_user)): return validate_workbook(processor)
@app.get('/api/admin/qa')
def qa(user=Depends(current_user)): return build_qa(processor)
@app.post('/api/admin/reload')
def reload_data(user=Depends(current_user)): processor.reload(); return processor.summary()
@app.get('/api/general/resumen')
def resumen(user=Depends(current_user)): return processor.process_cuadro_mando()
@app.get('/api/general/objetivo')
def objetivo(user=Depends(current_user)):
    rows=processor.process_cuadro_mando()['rows']; return {'rows':rows[15:20] if len(rows)>=20 else rows}
@app.get('/api/general/comparativos')
def comparativos(user=Depends(current_user)):
    rows=processor.process_cuadro_mando()['rows']; return {'cuadro_1':rows[31:44],'cuadro_2':rows[46:59]}
@app.get('/api/general/detalle')
def detalle(user=Depends(current_user)): return {'rows':processor.process_cuadro_mando()['rows'][:73]}
@app.get('/api/comercial/comparativo')
def comparativo(user=Depends(current_user)): return processor.process_comp_2025_2026()
@app.get('/api/comercial/comparativo-parcial')
def parcial(user=Depends(current_user)): return processor.process_comp_pp()
@app.get('/api/comercial/aportes')
def aportes(holding:Optional[str]=None,ejecutiva:Optional[str]=None,user=Depends(current_user)):
    rows=processor.process_comp_aportes()['rows']; filtered=filter_rows(rows,holding,ejecutiva)
    return {'rows':filtered.to_dict(orient='records'),'metrics':metrics_aportes(rows,holding,ejecutiva),'holdings':unique_values(rows,'holding'),'ejecutivas':unique_values(rows,'ejecutiva')}
@app.get('/api/comercial/80-20')
def analisis_8020(user=Depends(current_user)): return processor.process_80_20()
@app.get('/api/comercial/oportunidad')
def oportunidad(ejecutiva:Optional[str]=None,zona:Optional[str]=None,user=Depends(current_user)):
    rows=processor.process_oportunidad()['rows']; filtered=filter_rows(rows,ejecutiva=ejecutiva,zona=zona)
    return {'rows':filtered.to_dict(orient='records'),'metrics':metrics_oportunidad(rows,ejecutiva,zona),'ejecutivas':unique_values(rows,'ejecutiva'),'zonas':unique_values(rows,'zona')}
@app.get('/api/comercial/oportunidad-zona')
def oportunidad_zona(user=Depends(current_user)): return processor.process_oportunidad_zona()


@app.get("/api/admin/diagnostics")
def diagnostics():
    import sys, os, platform
    from pathlib import Path
    data_dir=Path(__file__).resolve().parents[2]/"data"
    files=list(data_dir.glob("*.xlsm"))
    return {"python":sys.version,"platform":platform.platform(),"pid":os.getpid(),"xlsm_files":[{"name":p.name,"size_bytes":p.stat().st_size} for p in files],"excel_loaded":False}
