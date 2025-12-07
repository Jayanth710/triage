from core.models import DraftReply, RouteDecision, Ticket


class FraudResponder:
    """
    Responder for suspected fraud / unauthorized activity.
    Emphasizes safety and next steps.
    """

    async def generate(self, ticket: Ticket, decision: RouteDecision) -> DraftReply:
        body = (
            f"Hi,\n\n"
            f"Thank you for alerting us about suspicious or unauthorized activity on your account.\n\n"
            f"We've classified this ticket as a *Fraud/Security* issue (strategy: {decision.strategy}, "
            f"confidence: {decision.confidence:.2f}). To protect your account, we recommend you:\n\n"
            f"1. Immediately change your account password and enable multi-factor authentication (if available).\n"
            f"2. Review recent activity on your account and note any transactions or changes you don't recognize.\n"
            f"3. Do not share your one-time passwords (OTPs) or verification codes with anyone.\n\n"
            f"Our security team will now review your case (ticket ID: {ticket.id}) and may temporarily "
            f"limit certain actions on your account while we investigate. We’ll follow up with you if we "
            f"need additional information.\n\n"
            f"Best regards,\n"
            f"Fraud & Security Team"
        )
        return DraftReply(department="Fraud", body=body)