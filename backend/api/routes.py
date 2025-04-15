from fastapi import APIRouter, UploadFile, Form, File, HTTPException
from backend.schemas.function_schema import FunctionCreate
from backend.db.models import insert_function, get_all_functions, delete_function_by_id
from backend.utils.file_handler import save_function_file
from backend.core.docker_executor import run_function_in_container
from backend.db.models import get_execution_logs

router = APIRouter()

@router.post("/functions/")
async def upload_function(
    name: str = Form(...),
    language: str = Form(...),
    timeout: int = Form(...),
    file: UploadFile = File(...)
):
    path = save_function_file(file, language)
    function_id = insert_function(name, language, path, timeout)  # Ensure function_id is returned
    return {"message": "Function uploaded successfully", "path": path, "function_id": function_id}

@router.get("/functions/")
async def list_functions():
    return get_all_functions()

@router.post("/functions/run/")
async def run_function(
    file_path: str = Form(...),
    language: str = Form(...),
    timeout: int = Form(5),
    use_gvisor: bool = Form(False)  # Option to use gVisor
):
    performance_data = run_function_in_container(file_path, language, timeout, use_gvisor)
    return performance_data



@router.delete("/functions/{function_id}")
def delete_function(function_id: int):
    try:
        delete_function_by_id(function_id)
        return {"message": f"Function with ID {function_id} deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/functions/{function_id}/logs")
def fetch_logs(function_id: int):
    logs = get_execution_logs(function_id)
    if not logs:
        raise HTTPException(status_code=404, detail="No logs found for the specified function ID")
    return logs
