from core.models import DraftReply, RouteDecision, Ticket


class ShippingResponder:
    """
    Responder for shipping, tracking, and address update issues.
    """

    async def generate(self, ticket: Ticket, decision: RouteDecision) -> DraftReply:
        body = (
            f"Hi,\n\n"
            f"Thanks for contacting us about your shipment.\n\n"
            f"We've classified this ticket as a *Shipping* issue (strategy: {decision.strategy}, "
            f"confidence: {decision.confidence:.2f}). To help us resolve this quickly, please confirm:\n\n"
            f"- Your order ID\n"
            f"- The shipping address you expect\n"
            f"- Any tracking number(s) you’ve received\n\n"
            f"Our logistics team will review your order status (linked to ticket ID: {ticket.id}) and "
            f"provide an update, including any new estimated delivery date or tracking details.\n\n"
            f"Best regards,\n"
            f"Shipping Support Team"
        )
        return DraftReply(department="Shipping", body=body)