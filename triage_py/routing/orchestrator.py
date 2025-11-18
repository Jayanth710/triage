from typing import List
from core.models import Ticket, RouteDecision
from .base import RouterStrategy

class RoutingOrchestrator:
    def __init__(self, strategies: List[RouterStrategy]):
        assert strategies, "At least one strategy is required"
        self.strategies = strategies

    async def decide(self, t: Ticket) -> RouteDecision:
        for s in self.strategies:
            d = await s.route(t)
            # accept the first non-General or any with confidence > 0
            if d.department != "General" and d.confidence >= 0.0:
                return d
        return RouteDecision("General", 0.0, "fallback")
