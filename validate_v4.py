from pathlib import Path
import sys, json
sys.path.insert(0,str(Path(__file__).parent/"backend"))
from app.processors.excel_processor import ExcelProcessor
from app.services.validation_service import validate_workbook
from app.config import DATA_FILE
p=ExcelProcessor(DATA_FILE).load()
r=validate_workbook(p)
print(json.dumps(r,ensure_ascii=False,indent=2))
sys.exit(0 if r["status"]=="OK" else 1)
