import asyncio, os
from core.models import Ticket
from preprocess.pipeline import Pipeline
from preprocess.language import LanguageDetector
from preprocess.pii import PiiScrubber
from preprocess.normalize import Normalizer
from routing.rules import RuleBasedRouter
from routing.orchestrator import RoutingOrchestrator

async def main():
    pipe = Pipeline([LanguageDetector(), PiiScrubber(), Normalizer(512)])
    t = await pipe.process(Ticket(id="x", text="Email me a refund; I was charged twice. order #Z9Q"))
    rules = RuleBasedRouter("config/rules.yaml")
    print("Preprocessed:", t)
    print("Rules decision:", await rules.route(t))
    orch = RoutingOrchestrator([rules])
    print("Final decision:", await orch.decide(t))

asyncio.run(main())