from core.models import Ticket, RouteDecision
from llm.base import LlmClient
from .base import RouterStrategy

class LlmRouter(RouterStrategy):
    def __init__(self, client: LlmClient, threshold: float = 0.55, schema_id: str = "departments_v1"):
        self.client, self.threshold, self.schema_id = client, threshold, schema_id

    async def route(self, t: Ticket) -> RouteDecision:
        res = await self.client.classify(t.text, self.schema_id)
        conf = float(res.get("confidence", 0.0))
        dept = res.get("label", "General")
        if conf >= self.threshold:
            return RouteDecision(department=dept, confidence=conf, strategy="llm")
        return RouteDecision(department="General", confidence=conf, strategy="llm")
