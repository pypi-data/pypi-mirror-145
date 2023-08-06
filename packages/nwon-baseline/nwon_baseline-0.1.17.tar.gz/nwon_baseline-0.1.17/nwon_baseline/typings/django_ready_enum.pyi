from enum import Enum

class DjangoReadyEnum(Enum):
    @classmethod
    def choices(cls) -> None: ...
