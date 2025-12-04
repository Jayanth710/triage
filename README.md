# Ticket Triage (Python, FastAPI, OO Patterns)

This project implements an **object-oriented support ticket triage service** as part of the CSCI 5448 OOAD Graduate Research Project.

The system exposes a simple HTTP API that accepts raw support tickets and automatically:

1. **Preprocesses** the text via a **Chain of Responsibility**:
   - Language detection  
   - PII scrubbing  
   - Text normalization  

2. **Routes** the ticket using the **Strategy pattern**:
   - `RuleBasedRouter`: keyword / regex rules
   - `EmbeddingRouterLC`: semantic similarity with sentence embeddings + FAISS
   - `LlmRouter`: LLM-based classification (OpenAI via LangChain) with confidence scores

3. **Generates a draft response** using a **Responder Factory**, which returns department-specific responders (e.g., Billing, Tech, Returns) to produce a first reply for the agent.

The project demonstrates multiple OO patterns: **Strategy, Chain of Responsibility, Factory, Adapter, Decorator/Proxy**, and is fully tested with `pytest`.

---

A working FastAPI service that triages support tickets using:
- **Chain of Responsibility** for preprocessing (language → PII scrub → normalization)
- **Strategy** for routing (rules → embeddings → LLM)
- **Adapter** for LLM provider (LangChain OpenAI client)
- **Proxy/Decorator** for caching, rate limiting, retries, circuit breaking
- **Factory** for department-specific draft replies

## 1. Dependencies

- Python **3.11+** (3.12 works)
- [uv](https://github.com/astral-sh/uv) (recommended, but you can also use `pip`)
- Required Python libraries (managed via `pyproject.toml` / `uv`), including:
  - `fastapi`
  - `uvicorn[standard]`
  - `httpx`
  - `pydantic>=2`
  - `PyYAML`
  - `cachetools`
  - `aiolimiter`
  - `tenacity`
  - `aiobreaker` (if used), or custom circuit breaker
  - `anyio`
  - `langchain`
  - `langchain-openai`
  - `langchain-community`
  - `faiss-cpu`
  - `sentence-transformers`
  - `numpy`
  - `pytest`, `pytest-asyncio`, `pytest-cov` (for tests)

> **Optional LLM**:  
> Set `OPENAI_API_KEY` if you want the `LlmRouter` (OpenAI + LangChain) to be active.  
> Without it, the system still works with rules + embeddings.

---

## 2. Setup & Build Instructions

### 2.1 Clone the repository

```bash
git clone <your-repo-url>.git
cd triage_py_project

# Create venv (if not already created)
uv venv

# Activate on Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Or on Windows (cmd.exe)
.\.venv\Scripts\activate.bat

# Or on macOS/Linux
source .venv/bin/activate

uv sync

Optional (LLM): set your key
```bash
export OPENAI_API_KEY=sk-...
```

## 2. Run API
```bash
uv run uvicorn triage_py.api.main:app --reload
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

## Test Instructions

Run the test suite (from project root, venv active):

```bash
uv run pytest -q
```

With coverage (optional, if pytest-cov is installed):
```bash
uv run pytest --cov=triage_py
```