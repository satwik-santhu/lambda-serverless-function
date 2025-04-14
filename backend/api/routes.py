from fastapi import APIRouter, UploadFile, Form,File,HTTPException
from backend.schemas.function_schema import FunctionCreate
from backend.db.models import insert_function, get_all_functions,delete_function_by_id
from backend.utils.file_handler import save_function_file
from backend.core.docker_executor import run_function_in_docker

router = APIRouter()

@router.post("/functions/")
async def upload_function(
    name: str = Form(...),
    language: str = Form(...),
    timeout: int = Form(...),
    file: UploadFile = File(...)
):
    path = save_function_file(file, language)
    insert_function(name, language, path, timeout)
    return {"message": "Function uploaded successfully", "path": path}

@router.get("/functions/")
async def list_functions():
    return get_all_functions()

@router.post("/functions/run/")
async def run_function(
    file_path: str = Form(...),
    language: str = Form(...),
    timeout: int = Form(5)
):
    return run_function_in_docker(file_path, language, timeout)


@router.delete("/functions/{function_id}")
def delete_function(function_id: int):
    try:
        delete_function_by_id(function_id)
        return {"message": f"Function with ID {function_id} deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

