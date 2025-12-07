from responder.billing import BillingResponder
from responder.tech import TechResponder
from core.models import Ticket, RouteDecision, DraftReply
from responder.account import AccountResponder
from responder.fraud import FraudResponder
from responder.general import GeneralResponder
from responder.returns import ReturnsResponder
from responder.shipping import ShippingResponder

# class ResponderFactory:
#     @staticmethod
#     def for_dept(dept: str):
#         return {
#             "Billing": BillingResponder(),
#             "Tech": TechResponder(),
#         }.get(dept, TechResponder())
class ResponderFactory:
    """
    Simple responder factory that maps department names
    to responder instances. Case-insensitive.
    """
    _RESPONDERS = {
        "billing": BillingResponder(),
        "tech": TechResponder(),
        "account": AccountResponder(),
        "fraud": FraudResponder(),
        "shipping": ShippingResponder(),
        "returns": ReturnsResponder(),
    }

    _DEFAULT = GeneralResponder()  # nice generic fallback

    @staticmethod
    def for_dept(dept: str):
        if not dept:
            return ResponderFactory._DEFAULT
        key = dept.strip().lower()
        return ResponderFactory._RESPONDERS.get(key, ResponderFactory._DEFAULT)