import unicodedata, re
from core.models import Ticket
from .base import Preprocessor

class Normalizer(Preprocessor):
    def __init__(self, max_chars: int = 512):
        self.max_chars = max_chars
    async def process(self, t: Ticket) -> Ticket:
        text = unicodedata.normalize("NFC", t.text)
        text = re.sub(r"\s+", " ", text).strip()
        text = text[: self.max_chars]
        return Ticket(id=t.id, text=text, locale=t.locale, meta=t.meta)
