"""
Enhanced Orchestrator with Memory and Guardrails

Integrates:
- Memory system for decision tracking
- Guardrails for safety and validation
- Original deterministic pipeline
"""

import uuid
from dataclasses import asdict

from controller.validator import validate_input
from controller.hasher import hash_context
from controller.cache import get_cached, set_cached
from controller.adapters import (
    to_strategy_context,
    load_snapshot_from_supabase,
)
from controller.response_builder import build_response
from controller.memory import memory_store
from controller.guardrails import guardrails

from llm_analyst.extractor import extract_signals
from strategy_engine.engine import decide_strategy
from llm_advisor.advisor import explain_strategy


class GuardrailException(Exception):
    """Raised when guardrails block a request"""
    pass


def handle_request(
    raw_text: str,
    business_id: str = None,
    user_id: str = None,
    enable_memory: bool = True
):
    """
    Enhanced Phase 4 orchestration with memory and guardrails:

    - Guardrails: Validate input
    - Validate input
    - Phase 2: Extract signals (LLM Analyst)
    - Hash + cache lookup
    - Phase 1: Decide strategy (deterministic)
    - Phase 3: Explain strategy (LLM Advisor)
    - Guardrails: Validate output
    - Build final response
    - Cache result
    - Memory: Store decision (async, non-blocking)
    """
    
    # Generate decision ID
    decision_id = str(uuid.uuid4())
    
    # ==========================================
    # PHASE 0: GUARDRAILS (Input Validation)
    # ==========================================
    guardrail_result = guardrails.validate_input(
        raw_text,
        business_id=business_id,
        user_id=user_id
    )
    
    if not guardrail_result.passed:
        # Log violations
        for violation in guardrail_result.violations:
            guardrails.log_violation(violation)
        
        # Block request
        raise GuardrailException(
            f"Request blocked by guardrails: {guardrail_result.violations[0].message}"
        )
    
    # Log warnings (but don't block)
    for warning in guardrail_result.warnings:
        print(f"GUARDRAIL WARNING: {warning}")
    
    # ==========================================
    # PHASE 1-4: Original Pipeline
    # ==========================================
    
    # 1. Validate input (legacy check)
    validate_input(raw_text)

    # 2. Phase 2 - Extract structured competitive signals
    extracted = extract_signals(raw_text)
    
    # Extract competitor name for memory
    competitor_name = extracted.competitors[0].name if extracted.competitors else "Unknown"

    # 3. Hash extracted meaning + cache lookup
    context_hash = hash_context(asdict(extracted))
    cached = get_cached(context_hash)
    
    if cached:
        # Cache hit - still track in memory if enabled
        if enable_memory and business_id:
            try:
                memory_store.save_decision(
                    decision_id=decision_id,
                    business_id=business_id,
                    competitor_name=competitor_name,
                    extracted_signals=asdict(extracted),
                    strategy_decision=cached,
                    advisor_output={
                        "confidence": cached.get("confidence", "unknown")
                    },
                    context_hash=context_hash,
                    cache_hit=True,
                )
            except Exception as e:
                print(f"Memory storage failed (non-critical): {e}")
        
        return cached

    # 4. Phase 1 - Decide strategy
    strategy_context = to_strategy_context(extracted)
    strategy = decide_strategy(strategy_context)

    # 5. Phase 3 - Explain strategy
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

    # 6. Build final response
    response = build_response(strategy, advisor)
    
    # ==========================================
    # PHASE 5: GUARDRAILS (Output Validation)
    # ==========================================
    output_guardrail = guardrails.validate_output(response)
    
    if not output_guardrail.passed:
        # Log violations
        for violation in output_guardrail.violations:
            guardrails.log_violation(violation)
        
        # Fallback to safe strategy
        print("WARNING: Output guardrail triggered, falling back to wait strategy")
        response = {
            "best_move": "wait_and_observe",
            "focus": "monitoring",
            "urgency": "low",
            "avoid": [],
            "advice": "Recommend careful monitoring before taking action.",
            "reason": "Output validation required conservative approach.",
            "confidence": "low",
        }
    
    # Log output warnings
    for warning in output_guardrail.warnings:
        print(f"OUTPUT WARNING: {warning}")
    
    # ==========================================
    # PHASE 6: CACHE & MEMORY
    # ==========================================
    
    # 7. Cache final response
    set_cached(context_hash, response)
    
    # 8. Store in long-term memory (non-blocking)
    if enable_memory and business_id:
        try:
            memory_store.save_decision(
                decision_id=decision_id,
                business_id=business_id,
                competitor_name=competitor_name,
                extracted_signals=asdict(extracted),
                strategy_decision=response,
                advisor_output={
                    "advice": advisor.advice,
                    "reason": advisor.reason,
                    "confidence": advisor.confidence,
                },
                context_hash=context_hash,
                cache_hit=False,
            )
        except Exception as e:
            print(f"Memory storage failed (non-critical): {e}")

    return response


def handle_request_from_business(
    business_id: str,
    user_id: str = None,
    enable_memory: bool = True
):
    """
    Enhanced Phase 4 entry point (DB-backed) with memory and guardrails:

    Business ID
      -> Guardrails (business validation)
      -> Supabase adapter
      -> snapshot text
      -> canonical handle_request()
    """
    
    # Validate business access
    access_result = guardrails.business_guardrail.validate_business_access(
        business_id,
        user_id
    )
    
    if not access_result.passed:
        raise GuardrailException(
            f"Business access denied: {access_result.violations[0].message}"
        )
    
    # Load snapshot
    snapshot_text = load_snapshot_from_supabase(business_id)
    
    # Process with full pipeline
    return handle_request(
        snapshot_text,
        business_id=business_id,
        user_id=user_id,
        enable_memory=enable_memory
    )


def get_business_insights(business_id: str):
    """
    Get memory-based insights for a business
    
    Returns:
    - Recent decision history
    - Behavioral patterns
    - Competitor trends
    - Reactive spiral detection
    """
    from controller.memory import memory_insights
    
    profile = memory_store.build_business_profile(business_id)
    spiral = memory_insights.detect_reactive_spiral(business_id)
    
    return {
        "profile": profile,
        "spiral_warning": spiral,
    }


def get_competitor_history(
    business_id: str,
    competitor_name: str
):
    """
    Get all past decisions about a specific competitor
    """
    from controller.memory import memory_insights
    
    trend = memory_insights.get_competitor_trend(
        business_id,
        competitor_name
    )
    
    decisions = memory_store.get_decisions_by_competitor(
        business_id,
        competitor_name
    )
    
    return {
        "trend": trend,
        "decisions": [asdict(d) for d in decisions],
    }