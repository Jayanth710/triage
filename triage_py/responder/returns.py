from core.models import DraftReply, RouteDecision, Ticket


class ReturnsResponder:
    """
    Responder for returns, exchanges, and defective product complaints.
    """

    async def generate(self, ticket: Ticket, decision: RouteDecision) -> DraftReply:
        body = (
            f"Hi,\n\n"
            f"Thanks for reaching out about a return or product issue.\n\n"
            f"We've classified this ticket as a *Returns* request (strategy: {decision.strategy}, "
            f"confidence: {decision.confidence:.2f}). We’re sorry to hear that the product did not meet "
            f"your expectations.\n\n"
            f"To process your return or exchange, please provide:\n"
            f"- Your order ID\n"
            f"- The item(s) you want to return\n"
            f"- A brief description of the issue (e.g., defective, damaged, not as described)\n\n"
            f"Once we receive this information, we’ll share instructions on how to ship the item back, "
            f"and we’ll confirm whether you prefer a refund or replacement.\n\n"
            f"Best regards,\n"
            f"Returns & Refunds Team"
        )
        return DraftReply(department="Return", body=body)