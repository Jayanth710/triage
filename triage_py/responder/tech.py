from core.models import Ticket, RouteDecision, DraftReply

class TechResponder:
    async def generate(self, t: Ticket, d: RouteDecision) -> DraftReply:
        body = ("Thanks for the details. This looks like a technical support request. "
                "Please confirm your device/OS and the exact error. Meanwhile, try restarting the app "
                "and checking your network connection.")
        return DraftReply(department="Tech", body=body)
