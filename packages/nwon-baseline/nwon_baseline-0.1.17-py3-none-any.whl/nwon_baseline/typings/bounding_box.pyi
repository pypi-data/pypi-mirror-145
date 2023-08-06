from pydantic import BaseModel
from typing import Any

BoundingBoxTuple: Any

class BoundingBoxCoordinates(BaseModel):
    top: int
    right: int
    bottom: int
    left: int
