from abc import ABC, abstractmethod
from enum import Enum

class FlowAction(Enum):
    CONTINUE = "Continue"
    BREAK = "Break"

class Flow(ABC):
    @abstractmethod
    async def setup(self):
        pass

    @abstractmethod
    async def run(self) -> FlowAction:
        pass