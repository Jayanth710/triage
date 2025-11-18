from typing import Protocol, TypedDict

class Classification(TypedDict):
    label: str
    confidence: float
    rationale: str

class LlmClient(Protocol):
    async def classify(self, normalized_text: str, schema_id: str) -> Classification: ...
