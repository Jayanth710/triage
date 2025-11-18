# Ticket Triage (Python, FastAPI, OO Patterns)

A working FastAPI service that triages support tickets using:
- **Chain of Responsibility** for preprocessing (language → PII scrub → normalization)
- **Strategy** for routing (rules → embeddings → LLM)
- **Adapter** for LLM provider (LangChain OpenAI client)
- **Proxy/Decorator** for caching, rate limiting, retries, circuit breaking
- **Factory** for department-specific draft replies

## 1. Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=$(pwd)
```

Optional (LLM): set your key
```bash
export OPENAI_API_KEY=sk-...
```

## 2. Run API
```bash
uvicorn triage_py.api.main:app --reload
```

Health check:
```
GET http://127.0.0.1:8000/health
```

Triage:
```
POST http://127.0.0.1:8000/triage
{
  "id": "1",
  "text": "I was charged twice for my order #A12345"
}
```

## 3. Behavior

- **Rules** are always active (config in `triage_py/config/rules.yaml`).
- **Embeddings** (FAISS + HuggingFace) auto-enable if deps/models load.
- **LLM** auto-enables if `OPENAI_API_KEY` is set.

Order: rules → embeddings → LLM (first high-confidence decision wins).

## 4. Notes

- No raw PII is logged; scrubbing happens before routing.
- Caching keys hash the normalized text; rate limits and circuit breakers guard provider calls.
- All components are replaceable via interfaces for easy experiments.
