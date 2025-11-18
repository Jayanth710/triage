from typing import List
from core.models import Ticket
from .base import Preprocessor

class Pipeline:
    def __init__(self, stages: List[Preprocessor]):
        self.stages = stages
    async def process(self, t: Ticket) -> Ticket:
        for s in self.stages:
            t = await s.process(t)
        return t
