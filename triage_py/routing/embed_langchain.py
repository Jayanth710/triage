from typing import Iterable, Tuple
from dataclasses import dataclass
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from core.models import Ticket, RouteDecision

@dataclass
class Exemplar:
    text: str
    department: str

class EmbeddingRouterLC:
    """LangChain FAISS + HF embeddings. Sync, but fast enough for API."""
    def __init__(self, exemplars: Iterable[Tuple[str, str]],
                 model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
                 k: int = 3, threshold: float = 0.60):
        self.k = k
        self.threshold = threshold
        self.embedding = HuggingFaceEmbeddings(model_name=model_name)
        docs = [Document(page_content=txt, metadata={"dept": dept}) for (txt, dept) in exemplars]
        self.store = FAISS.from_documents(docs, self.embedding)

    async def route(self, t: Ticket) -> RouteDecision:
        results = self.store.similarity_search_with_relevance_scores(t.text, k=self.k)
        if not results:
            return RouteDecision("General", 0.0, "embed")
        # results: List[(Document, score)] where score in [0,1] (higher is better)
        top_doc, top_score = max(results, key=lambda pair: pair[1])
        dept = top_doc.metadata.get("dept", "General")
        conf = float(min(1.0, max(0.0, top_score)))
        if conf >= self.threshold:
            return RouteDecision(department=dept, confidence=conf, strategy="embed")
        return RouteDecision("General", conf, "embed")
