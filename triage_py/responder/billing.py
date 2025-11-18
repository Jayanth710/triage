from core.models import Ticket, RouteDecision, DraftReply

class BillingResponder:
    async def generate(self, t: Ticket, d: RouteDecision) -> DraftReply:
        body = ("Thanks for reaching out. This appears to be a billing issue. "
                "We’ve redacted sensitive details. We can review charges or process a refund if eligible. "
                "If you have an order number, reply with it (no card details).")
        return DraftReply(department="Billing", body=body)
