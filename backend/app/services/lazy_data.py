import threading
import logging
from pathlib import Path
log=logging.getLogger(__name__)
_lock=threading.Lock()
_processor=None
_load_error=None
def _data_file():
    project_root=Path(__file__).resolve().parents[3]
    candidates=list((project_root/"data").glob("*.xlsm"))
    if not candidates: raise FileNotFoundError(f"No XLSM found in {project_root/'data'}")
    return candidates[0]
def get_processor():
    global _processor,_load_error
    if _processor is not None: return _processor
    if _load_error is not None: raise _load_error
    with _lock:
        if _processor is not None: return _processor
        try:
            from ..processors.excel_processor import ExcelProcessor
            p=ExcelProcessor(_data_file()).load()
            _processor=p
            return p
        except Exception as exc:
            _load_error=exc
            log.exception("Deferred XLSM load failed")
            raise
def reset_processor():
    global _processor,_load_error
    with _lock:
        _processor=None; _load_error=None
