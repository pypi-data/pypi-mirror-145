from pydantic import BaseModel
from typing import Any

class PydanticBaseDjango(BaseModel):
    class Config:
        extra: str
        allow_population_by_field_name: bool
        alias_generator: Any
