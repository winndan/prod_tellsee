from strategy_engine.models import ExtractedContext, StrategyDecision
from strategy_engine.rules import (
    evaluate_aggressive_positioning_rule,
    evaluate_defensive_wait_rule,
    evaluate_market_leader_rule,
    evaluate_positioning_rule,
    evaluate_pricing_rule,
    evaluate_price_increase_rule,
    evaluate_wait_rule,
)


# Rule evaluation order (priority-based)
# Higher priority rules are evaluated first
RULES = [
    # Tier 1: High-urgency threats
    evaluate_market_leader_rule,           # Strong competitor with good execution
    evaluate_aggressive_positioning_rule,   # Strike during messaging weakness
    
    # Tier 2: Standard competitive responses
    evaluate_pricing_rule,                  # Price changes
    evaluate_positioning_rule,              # Confusing launches
    
    # Tier 3: Opportunistic moves
    evaluate_price_increase_rule,           # Competitor raises prices
    
    # Tier 4: Strategic patience
    evaluate_defensive_wait_rule,           # Let competitor fail
]


def decide_strategy(context: ExtractedContext) -> StrategyDecision:
    """
    Phase 1 - Strategy Engine (Decision Layer)
    
    Evaluates competitive context against priority-ordered rules.
    Returns the FIRST matching rule's decision.
    
    Guarantees:
    - Deterministic: Same input always produces same output
    - Complete: Always returns a decision (fallback to wait)
    - Auditable: Clear rule evaluation order
    - Stateless: No side effects or memory
    
    Args:
        context: ExtractedContext from Phase 2 (LLM Analyst)
        
    Returns:
        StrategyDecision with strategy_type, focus, urgency, and avoid list
    """
    
    # Validate input
    if not context or not isinstance(context, ExtractedContext):
        raise ValueError("Invalid context provided to strategy engine")
    
    # Evaluate rules in priority order
    for rule in RULES:
        try:
            decision = rule(context)
            if decision:
                return decision
        except Exception as e:
            # Log error but continue to next rule
            # This ensures one broken rule doesn't crash the system
            print(f"Error evaluating rule {rule.__name__}: {e}")
            continue
    
    # Fallback: Always returns a decision
    return evaluate_wait_rule(context)


def get_rule_diagnostics(context: ExtractedContext) -> dict:
    """
    Debugging utility: Shows which rules matched for a given context.
    
    This is NOT used in production but useful for:
    - Testing rule logic
    - Understanding why a decision was made
    - Debugging unexpected outcomes
    
    Returns:
        dict with rule names and their decisions
    """
    diagnostics = {
        "context_summary": {
            "num_competitors": len(context.competitors),
            "user_intent": context.user_intent,
        },
        "rule_evaluations": []
    }
    
    for rule in RULES:
        try:
            decision = rule(context)
            diagnostics["rule_evaluations"].append({
                "rule": rule.__name__,
                "matched": decision is not None,
                "decision": {
                    "strategy_type": decision.strategy_type.value,
                    "focus": decision.focus,
                    "urgency": decision.urgency.value,
                } if decision else None
            })
        except Exception as e:
            diagnostics["rule_evaluations"].append({
                "rule": rule.__name__,
                "matched": False,
                "error": str(e)
            })
    
    # Add fallback
    fallback = evaluate_wait_rule(context)
    diagnostics["fallback"] = {
        "strategy_type": fallback.strategy_type.value,
        "focus": fallback.focus,
        "urgency": fallback.urgency.value,
    }
    
    return diagnostics