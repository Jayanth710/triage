from typing import Protocol
from core.models import Ticket

class Preprocessor(Protocol):
    async def process(self, t: Ticket) -> Ticket: ...
