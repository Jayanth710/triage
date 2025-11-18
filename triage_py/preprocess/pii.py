import re
from core.models import Ticket
from .base import Preprocessor

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"\+?\d[\d\- ]{7,}\d")
ORDER = re.compile(r"(?:order|ord|#)\s*[\w\-]{5,}", re.I)

def _redact(s: str) -> str:
    s = EMAIL.sub("<EMAIL>", s)
    s = PHONE.sub("<PHONE>", s)
    s = ORDER.sub("<ORDER_ID>", s)
    return s

class PiiScrubber(Preprocessor):
    async def process(self, t: Ticket) -> Ticket:
        return Ticket(id=t.id, text=_redact(t.text), locale=t.locale, meta=t.meta)
