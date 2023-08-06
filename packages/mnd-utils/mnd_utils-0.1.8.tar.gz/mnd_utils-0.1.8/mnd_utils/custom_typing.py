from abc import abstractmethod
from typing_extensions import Protocol


class Sliceable(Protocol):

    @abstractmethod
    def __getitem__(self, item): ...
