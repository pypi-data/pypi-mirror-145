from enum import Enum
from typing import List, Type, TypeVar

T = TypeVar('T', bound=Enum)

def enum_value_list(enum_class: Type[T]) -> List[str]: ...
def enum_value_list_as_string(enum_class: Type[T], separator: str = ...) -> str: ...
