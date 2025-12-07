from core.models import DraftReply, RouteDecision, Ticket


class GeneralResponder:
    """
    Default responder used when we don't have a more specific department.
    Generates a safe, high-level acknowledgement that can be routed internally.
    """

    async def generate(self, ticket: Ticket, decision: RouteDecision) -> DraftReply:
        body = (
            f"Hi,\n\n"
            f"Thanks for contacting us. We've received your request (ticket ID: {ticket.id}) "
            f"and classified it as a general inquiry. A member of our support team will "
            f"review the details and get back to you shortly.\n\n"
            f"If you have any additional information or screenshots that might help us, "
            f"please reply to this message with those details.\n\n"
            f"Best regards,\n"
            f"Customer Support Team"
        )
        return DraftReply(department="General", body=body)