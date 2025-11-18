import re, yaml
from core.models import Ticket, RouteDecision
from .base import RouterStrategy

class RuleBasedRouter(RouterStrategy):
    def __init__(self, rules_yaml_path: str):
        with open(rules_yaml_path, "r", encoding="utf-8") as f:
            self.rules = yaml.safe_load(f) or {}
        # Format: { "Billing": ["refund","charged twice"], ... }

    async def route(self, t: Ticket) -> RouteDecision:
        text = t.text.lower()
        best_dept, best_score = "General", 0.0
        for dept, terms in self.rules.items():
            score = 0
            for term in terms or []:
                if re.search(rf"\b{re.escape(str(term).lower())}\b", text):
                    score += 1
            if score > best_score:
                best_dept, best_score = dept, float(score)
        conf = float(min(1.0, best_score / 3.0)) if best_score > 0 else 0.0
        return RouteDecision(department=best_dept, confidence=conf, strategy="rules")
