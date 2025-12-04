from fastapi import FastAPI
from pydantic import BaseModel
import logging, os

from core.models import Ticket
from preprocess.pipeline import Pipeline
from preprocess.language import LanguageDetector
from preprocess.pii import PiiScrubber
from preprocess.normalize import Normalizer
from routing.rules import RuleBasedRouter
from routing.orchestrator import RoutingOrchestrator
from responder.factory import ResponderFactory
from dotenv import load_dotenv

load_dotenv()
# Optional imports guarded for graceful fallback
embed_router = None
llm_router = None
try:
    from routing.embed_langchain import EmbeddingRouterLC
except Exception as _e:
    EmbeddingRouterLC = None

try:
    from llm.langchain_adapter import LangChainLlmClient
    from llm.decorators import CachedLlmClient, RateLimitedLlmClient, RetryingLlmClient, CircuitBreakerLlmClient
    from routing.llm_router import LlmRouter
except Exception as _e:
    LangChainLlmClient = None

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("triage")

app = FastAPI(title="Ticket Triage (Python, FastAPI)")

# --------- Preprocess chain ---------
pipeline = Pipeline([LanguageDetector(), PiiScrubber(), Normalizer(512)])

# --------- Routers ---------
# Rules (always available)
rules_path = os.getenv("TRIAGE_RULES_PATH", "config/rules.yaml")
rules = RuleBasedRouter(rules_path)

# Embeddings (optional, FAISS + HF embeddings via LangChain)
if EmbeddingRouterLC is not None:
    try:
        embed_router = EmbeddingRouterLC(
            exemplars=[
                ("I was charged twice for my order", "Billing"),
                ("cannot connect to wifi on my device", "Tech"),
                ("reset my password verification code not received", "Account"),
                ("suspicious activity report and account locked", "Fraud"),
                ("update my shipping address", "Shipping"),
                ("return my product it is defective", "Returns"),
            ],
            threshold=0.62
        )
        log.info("EmbeddingRouterLC initialized.")
    except Exception as e:
        log.warning(f"Embedding router disabled: {e}")

# LLM (optional, requires OPENAI_API_KEY)
# print(os.getenv("OPENAI_API_KEY"))
if LangChainLlmClient is not None and os.getenv("OPENAI_API_KEY"):
    try:
        lc_client = LangChainLlmClient(allowed_labels=["Billing","Tech","Account","Fraud","Shipping","Returns","General"])
        wrapped = CachedLlmClient(lc_client)               # cache first
        wrapped = RateLimitedLlmClient(wrapped, rate_per_sec=5.0)
        wrapped = RetryingLlmClient(wrapped)
        wrapped = CircuitBreakerLlmClient(wrapped, fail_max=5, reset_timeout=30)
        llm_router = LlmRouter(wrapped, threshold=0.55)
        log.info("LLM router initialized (LangChain/OpenAI).")
    except Exception as e:
        log.warning(f"LLM router disabled: {e}")
else:
    log.info("No OPENAI_API_KEY or LangChain not available; LLM router disabled.")

# Order: rules -> embeddings -> LLM (only include available)
strategies = [rules] + [r for r in [embed_router, llm_router] if r is not None]
orchestrator = RoutingOrchestrator(strategies)

# --------- API Models ---------
class TriageIn(BaseModel):
    id: str
    text: str
    locale: str | None = None

class TriageOut(BaseModel):
    department: str
    confidence: float
    strategy: str
    draft: str

@app.get("/health")
async def health():
    return {"status": "ok", "strategies": [type(s).__name__ for s in strategies]}

@app.post("/triage", response_model=TriageOut)
async def triage(inp: TriageIn):
    t0 = Ticket(id=inp.id, text=inp.text, locale=inp.locale)
    t = await pipeline.process(t0)
    decision = await orchestrator.decide(t)
    responder = ResponderFactory.for_dept(decision.department)
    draft = await responder.generate(t, decision)
    return TriageOut(department=decision.department, confidence=decision.confidence,
                     strategy=decision.strategy, draft=draft.body)
