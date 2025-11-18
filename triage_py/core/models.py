from dataclasses import dataclass
from typing import Dict, Optional

@dataclass(frozen=True)
class Ticket:
    id: str
    text: str
    locale: Optional[str] = None
    meta: Optional[Dict[str, str]] = None

@dataclass(frozen=True)
class RouteDecision:
    department: str
    confidence: float
    strategy: str

@dataclass(frozen=True)
class DraftReply:
    department: str
    body: str
