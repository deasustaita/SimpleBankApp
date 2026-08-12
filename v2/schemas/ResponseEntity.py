from typing import Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class ResponseEntity(BaseModel, Generic[T]):
    status_code: int
    message: str
    data: Optional[T] = None
