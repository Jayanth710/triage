from typing import Optional
from pydantic import BaseModel, Field, confloat
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

class ClassificationModel(BaseModel):
    label: str = Field(..., description="Department label")
    confidence: confloat(ge=0.0, le=1.0) = 0.0
    rationale: str = Field("", description="One-sentence justification")

class LangChainLlmClient:
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.0, timeout: int = 20,
                 allowed_labels: Optional[list[str]] = None):
        self.llm = ChatOpenAI(model=model, temperature=temperature, timeout=timeout)
        self.allowed_labels = allowed_labels or ["Billing","Tech","Account","Fraud","Shipping","Returns","General"]
        self.prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are a ticket classifier. Return ONLY a JSON object matching the provided schema. "
             "Never echo PII. Allowed labels: {labels}"),
            ("user",
             "Ticket:\n{ticket}\n\nClassify to one label; set confidence in [0,1]. Keep rationale concise.")
        ])
        self.chain = self.prompt | self.llm.with_structured_output(ClassificationModel)

    async def classify(self, normalized_text: str, schema_id: str = "departments_v1") -> dict:
        result: ClassificationModel = await self.chain.ainvoke({
            "labels": ", ".join(self.allowed_labels),
            "ticket": normalized_text
        })
        return result.model_dump()
