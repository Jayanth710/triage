from core.models import DraftReply, RouteDecision, Ticket


class AccountResponder:
    """
    Responder for account-related issues (login, password reset, verification, profile).
    """

    async def generate(self, ticket: Ticket, decision: RouteDecision) -> DraftReply:
        body = (
            f"Hi,\n\n"
            f"Thanks for reaching out about your account.\n\n"
            f"We've classified this ticket as an *Account* issue (strategy: {decision.strategy}, "
            f"confidence: {decision.confidence:.2f}). Based on your description, it sounds like "
            f"there may be a problem with your login, password, or account settings.\n\n"
            f"Common steps that often resolve account issues:\n"
            f"1. Try resetting your password using the 'Forgot password' option on the login page.\n"
            f"2. Check your spam/junk folder for any verification or reset emails.\n"
            f"3. Ensure you're using the correct email/username associated with your account.\n\n"
            f"Our team will review your specific case (ticket ID: {ticket.id}) and, if needed, "
            f"manually verify your identity or update your account settings.\n\n"
            f"Best regards,\n"
            f"Account Support Team"
        )
        return DraftReply(department="Account", body=body)