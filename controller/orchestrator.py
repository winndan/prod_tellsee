from dataclasses import asdict

from controller.validator import validate_input
from controller.hasher import hash_context
from controller.cache import get_cached, set_cached
from controller.adapters import (
    to_strategy_context,
    load_snapshot_from_supabase,
)
from controller.response_builder import build_response

from llm_analyst.extractor import extract_signals
from strategy_engine.engine import decide_strategy
from llm_advisor.advisor import explain_strategy


def handle_request(raw_text: str):
    """
    Phase 4 orchestration (canonical pipeline):

    - Validate input
    - Phase 2: Extract signals (LLM Analyst)
    - Hash + cache lookup
    - Phase 1: Decide strategy (deterministic)
    - Phase 3: Explain strategy (LLM Advisor)
    - Build final response
    - Cache result
    """

    # 1️⃣ Validate input
    validate_input(raw_text)

    # 2️⃣ Phase 2 — Extract structured competitive signals
    extracted = extract_signals(raw_text)

    # 3️⃣ Hash extracted meaning (dataclass-safe) + cache lookup
    context_hash = hash_context(asdict(extracted))
    cached = get_cached(context_hash)
    if cached:
        return cached

    # 4️⃣ Phase 1 — Decide strategy
    strategy_context = to_strategy_context(extracted)
    strategy = decide_strategy(strategy_context)

    # 5️⃣ Phase 3 — Explain strategy
    # IMPORTANT: advisor gets STRUCTURED signals, not empty lists
    advisor_input = {
        "strategy_type": strategy.strategy_type.value,
        "focus": strategy.focus,
        "urgency": strategy.urgency.value,
        "signals": [
            (
                f"{c.name}: "
                f"event={c.signals.event.value}, "
                f"sentiment={c.signals.sentiment.value}, "
                f"clarity={c.signals.clarity.value}, "
                f"execution={c.signals.execution_quality.value}, "
                f"messaging={c.signals.messaging_strength.value}, "
                f"confusion={c.signals.market_confusion.value}"
            )
            for c in extracted.competitors
        ],
    }

    advisor = explain_strategy(advisor_input)

    # 6️⃣ Build final response
    response = build_response(strategy, advisor)

    # 7️⃣ Cache final response
    set_cached(context_hash, response)

    return response


def handle_request_from_business(business_id: str):
    """
    Phase 4 entry point (DB-backed):

    Business ID
      → Supabase adapter
      → snapshot text
      → canonical handle_request()
    """

    snapshot_text = load_snapshot_from_supabase(business_id)
    return handle_request(snapshot_text)
