from pydantic import BaseModel

class FunctionCreate(BaseModel):
    name: str
    language: str  # "python" or "javascript"
    timeout: int
