from responder.billing import BillingResponder
from responder.tech import TechResponder
from core.models import Ticket, RouteDecision, DraftReply

class ResponderFactory:
    @staticmethod
    def for_dept(dept: str):
        return {
            "Billing": BillingResponder(),
            "Tech": TechResponder(),
        }.get(dept, TechResponder())
