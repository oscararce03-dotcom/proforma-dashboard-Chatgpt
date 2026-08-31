import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'backend'))
from app.config import DATA_FILE
from app.processors.excel_processor import ExcelProcessor
from app.services.qa_service import build_qa
p=ExcelProcessor(DATA_FILE).load(); r=build_qa(p)
print(f"PROFORMA V5 QA | {r['source']} | {r['status']} | controles={r['checks']} errores={r['errors']} warnings={r['warnings']}")
for c in r['checks_detail']:
    print(c['status'],c['type'],c.get('sheet'),c.get('column',''))
sys.exit(1 if r['errors'] else 0)
