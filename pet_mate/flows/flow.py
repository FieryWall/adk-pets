from abc import ABC, abstractmethod

class Flow(ABC):
    @abstractmethod
    async def setup(self):
        pass

    @abstractmethod
    async def run(self):
        pass