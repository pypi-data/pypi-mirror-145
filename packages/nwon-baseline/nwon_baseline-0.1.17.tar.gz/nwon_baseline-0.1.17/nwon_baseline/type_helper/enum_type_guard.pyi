from enum import Enum
from typing import Optional, Type, TypeVar

T = TypeVar('T', bound=Enum)

def enum_type_guard(value: str, enum_class: Type[T]) -> Optional[T]: ...
