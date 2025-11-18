from core.models import Ticket
from .base import Preprocessor

class LanguageDetector(Preprocessor):
    async def process(self, t: Ticket) -> Ticket:
        # Stubbed language detection (could integrate fasttext/langdetect)
        locale = t.locale or "en"
        return Ticket(id=t.id, text=t.text, locale=locale, meta=t.meta)
