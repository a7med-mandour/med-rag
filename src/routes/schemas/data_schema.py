from pydantic import BaseModel
from typing import Optional


class DataSchema(BaseModel):
    file_id: str
    chunk_size : Optional[int]=300
    overlap: Optional[int]=20
    