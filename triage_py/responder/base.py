from typing import Protocol
from core.models import Ticket, RouteDecision, DraftReply

class Responder(Protocol):
    async def generate(self, t: Ticket, d: RouteDecision) -> DraftReply: ...
