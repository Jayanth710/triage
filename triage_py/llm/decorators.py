import hashlib
from cachetools import TTLCache
from aiolimiter import AsyncLimiter
from tenacity import retry, stop_after_attempt, wait_exponential_jitter
import pybreaker

from llm.base import LlmClient, Classification

def _key(text: str, schema_id: str, provider: str, version: str) -> str:
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return f"{provider}:{version}:{schema_id}:{h}"

class CachedLlmClient(LlmClient):
    def __init__(self, delegate: LlmClient, ttl_seconds: int = 3600, maxsize: int = 10_000):
        self.delegate = delegate
        self.cache = TTLCache(maxsize=maxsize, ttl=ttl_seconds)
        self.provider = delegate.__class__.__name__
        self.version = "v1"

    async def classify(self, normalized_text: str, schema_id: str) -> Classification:
        k = _key(normalized_text, schema_id, self.provider, self.version)
        if k in self.cache:
            return self.cache[k]
        res = await self.delegate.classify(normalized_text, schema_id)
        self.cache[k] = res
        return res

class RateLimitedLlmClient(LlmClient):
    def __init__(self, delegate: LlmClient, rate_per_sec: float = 5.0):
        self.delegate = delegate
        self.limiter = AsyncLimiter(max_rate=rate_per_sec, time_period=1)

    async def classify(self, normalized_text: str, schema_id: str) -> Classification:
        async with self.limiter:
            return await self.delegate.classify(normalized_text, schema_id)

class RetryingLlmClient(LlmClient):
    def __init__(self, delegate: LlmClient):
        self.delegate = delegate

    @retry(stop=stop_after_attempt(3), wait=wait_exponential_jitter(initial=0.5, max=4))
    async def classify(self, normalized_text: str, schema_id: str) -> Classification:
        return await self.delegate.classify(normalized_text, schema_id)

class CircuitBreakerLlmClient(LlmClient):
    def __init__(self, delegate: LlmClient, fail_max: int = 5, reset_timeout: int = 30):
        self.delegate = delegate
        self.breaker = pybreaker.CircuitBreaker(fail_max=fail_max, reset_timeout=reset_timeout)

    async def classify(self, normalized_text: str, schema_id: str) -> Classification:
        # pybreaker is sync; wrap delegate call via anyio
        @self.breaker
        def _sync_call():
            import anyio
            return anyio.run(self.delegate.classify, normalized_text, schema_id)
        return _sync_call()
