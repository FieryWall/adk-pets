from abc import ABC, abstractmethod
from enum import Enum

class FlowAction(Enum):
    CONTINUE = "continue"
    EXIT = "exit"
    ERROR = "error"

class Flow(ABC):
    @abstractmethod
    async def setup(self):
        pass

    @abstractmethod
    async def run(self) -> FlowAction:
        pass

    @abstractmethod
    async def cleanup(self):
        pass