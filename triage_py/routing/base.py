from typing import Protocol
from core.models import Ticket, RouteDecision

class RouterStrategy(Protocol):
    async def route(self, t: Ticket) -> RouteDecision: ...
