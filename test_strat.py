"""
Test suite for the Strategy Engine

Validates that:
1. Rules fire correctly
2. Same input produces same output (determinism)
3. Fallback works when no rules match
4. Edge cases are handled
"""

from strategy_engine.models import (
    ExtractedContext,
    Competitor,
    CompetitorSignals,
    StrategyDecision,
)
from strategy_engine.enums import (
    EventType,
    Sentiment,
    Clarity,
    PriceInfo,
    ExecutionQuality,
    MessagingStrength,
    MarketConfusion,
    StrategyType,
    Urgency,
)
from strategy_engine.engine import decide_strategy, get_rule_diagnostics


def test_positioning_rule():
    """Test: Confusing product launch with positive sentiment"""
    print("\n=== Test 1: Positioning Rule ===")
    
    context = ExtractedContext(
        competitors=[
            Competitor(
                name="Competitor A",
                signals=CompetitorSignals(
                    event=EventType.NEW_PRODUCT_LAUNCH,
                    sentiment=Sentiment.MIXED_POSITIVE,
                    clarity=Clarity.CONFUSING,
                    price_info=PriceInfo.UNKNOWN,
                    execution_quality=ExecutionQuality.UNKNOWN,
                    messaging_strength=MessagingStrength.UNKNOWN,
                    market_confusion=MarketConfusion.UNKNOWN,
                )
            )
        ],
        market_signals=[],
        user_intent="seeking_response"
    )
    
    decision = decide_strategy(context)
    
    assert decision.strategy_type == StrategyType.POSITIONING
    assert decision.focus == "clarity_and_simplicity"
    assert decision.urgency == Urgency.MEDIUM
    assert "price_war" in decision.avoid
    
    print(f"✓ Strategy: {decision.strategy_type.value}")
    print(f"✓ Focus: {decision.focus}")
    print(f"✓ Urgency: {decision.urgency.value}")
    print(f"✓ Avoid: {decision.avoid}")


def test_pricing_rule():
    """Test: Competitor drops price"""
    print("\n=== Test 2: Pricing Rule ===")
    
    context = ExtractedContext(
        competitors=[
            Competitor(
                name="Competitor B",
                signals=CompetitorSignals(
                    event=EventType.PRICE_CHANGE,
                    sentiment=Sentiment.NEUTRAL,
                    clarity=Clarity.CLEAR,
                    price_info=PriceInfo.LOWER,
                    execution_quality=ExecutionQuality.STRONG,
                    messaging_strength=MessagingStrength.CLEAR,
                    market_confusion=MarketConfusion.LOW,
                )
            )
        ],
        market_signals=[],
        user_intent="seeking_response"
    )
    
    decision = decide_strategy(context)
    
    assert decision.strategy_type == StrategyType.PRICING
    assert decision.focus == "value_not_discount"
    assert decision.urgency == Urgency.HIGH  # High because execution is strong
    assert "race_to_bottom" in decision.avoid
    
    print(f"✓ Strategy: {decision.strategy_type.value}")
    print(f"✓ Focus: {decision.focus}")
    print(f"✓ Urgency: {decision.urgency.value}")
    print(f"✓ Avoid: {decision.avoid}")


def test_wait_fallback():
    """Test: No rules match, fallback to wait"""
    print("\n=== Test 3: Wait Fallback ===")
    
    context = ExtractedContext(
        competitors=[
            Competitor(
                name="Competitor C",
                signals=CompetitorSignals(
                    event=EventType.NONE,
                    sentiment=Sentiment.NEUTRAL,
                    clarity=Clarity.UNKNOWN,
                    price_info=PriceInfo.UNKNOWN,
                    execution_quality=ExecutionQuality.UNKNOWN,
                    messaging_strength=MessagingStrength.UNKNOWN,
                    market_confusion=MarketConfusion.UNKNOWN,
                )
            )
        ],
        market_signals=[],
        user_intent="monitoring"
    )
    
    decision = decide_strategy(context)
    
    assert decision.strategy_type == StrategyType.WAIT
    assert decision.focus == "monitoring"
    assert decision.urgency == Urgency.LOW
    
    print(f"✓ Strategy: {decision.strategy_type.value}")
    print(f"✓ Focus: {decision.focus}")
    print(f"✓ Urgency: {decision.urgency.value}")


def test_determinism():
    """Test: Same input produces same output"""
    print("\n=== Test 4: Determinism ===")
    
    context = ExtractedContext(
        competitors=[
            Competitor(
                name="Competitor D",
                signals=CompetitorSignals(
                    event=EventType.NEW_PRODUCT_LAUNCH,
                    sentiment=Sentiment.POSITIVE,
                    clarity=Clarity.CONFUSING,
                    price_info=PriceInfo.UNKNOWN,
                    execution_quality=ExecutionQuality.UNKNOWN,
                    messaging_strength=MessagingStrength.UNKNOWN,
                    market_confusion=MarketConfusion.UNKNOWN,
                )
            )
        ],
        market_signals=[],
        user_intent="seeking_response"
    )
    
    # Run 10 times
    decisions = [decide_strategy(context) for _ in range(10)]
    
    # All should be identical
    first = decisions[0]
    for d in decisions[1:]:
        assert d.strategy_type == first.strategy_type
        assert d.focus == first.focus
        assert d.urgency == first.urgency
        assert d.avoid == first.avoid
    
    print(f"✓ Ran 10 times, all decisions identical")
    print(f"✓ Strategy: {first.strategy_type.value}")


def test_market_leader_rule():
    """Test: Strong competitor with good execution"""
    print("\n=== Test 5: Market Leader Defense ===")
    
    context = ExtractedContext(
        competitors=[
            Competitor(
                name="Market Leader",
                signals=CompetitorSignals(
                    event=EventType.NEW_PRODUCT_LAUNCH,
                    sentiment=Sentiment.POSITIVE,
                    clarity=Clarity.CLEAR,
                    price_info=PriceInfo.UNKNOWN,
                    execution_quality=ExecutionQuality.STRONG,
                    messaging_strength=MessagingStrength.CLEAR,
                    market_confusion=MarketConfusion.LOW,
                )
            )
        ],
        market_signals=[],
        user_intent="seeking_response"
    )
    
    decision = decide_strategy(context)
    
    assert decision.strategy_type == StrategyType.POSITIONING
    assert decision.focus == "defend_differentiation"
    assert decision.urgency == Urgency.HIGH
    
    print(f"✓ Strategy: {decision.strategy_type.value}")
    print(f"✓ Focus: {decision.focus}")
    print(f"✓ Urgency: {decision.urgency.value}")


def test_diagnostics():
    """Test: Diagnostic utility works"""
    print("\n=== Test 6: Diagnostics ===")
    
    context = ExtractedContext(
        competitors=[
            Competitor(
                name="Test Competitor",
                signals=CompetitorSignals(
                    event=EventType.PRICE_CHANGE,
                    sentiment=Sentiment.NEUTRAL,
                    clarity=Clarity.CLEAR,
                    price_info=PriceInfo.LOWER,
                    execution_quality=ExecutionQuality.WEAK,
                    messaging_strength=MessagingStrength.GENERIC,
                    market_confusion=MarketConfusion.MEDIUM,
                )
            )
        ],
        market_signals=[],
        user_intent="seeking_response"
    )
    
    diagnostics = get_rule_diagnostics(context)
    
    assert "context_summary" in diagnostics
    assert "rule_evaluations" in diagnostics
    assert "fallback" in diagnostics
    
    print(f"✓ Diagnostics generated successfully")
    print(f"✓ Rules evaluated: {len(diagnostics['rule_evaluations'])}")
    
    # Show which rule matched
    for eval in diagnostics['rule_evaluations']:
        if eval['matched']:
            print(f"✓ Matched rule: {eval['rule']}")
            print(f"  Decision: {eval['decision']}")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("STRATEGY ENGINE TEST SUITE")
    print("=" * 60)
    
    try:
        test_positioning_rule()
        test_pricing_rule()
        test_wait_fallback()
        test_determinism()
        test_market_leader_rule()
        test_diagnostics()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        raise
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        raise


if __name__ == "__main__":
    run_all_tests()