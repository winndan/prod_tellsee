"""
Complete example usage of the Competitive Strategy Decision System

Demonstrates:
1. Direct text analysis
2. Database-backed analysis
3. Caching behavior
4. Error handling
5. Diagnostics
"""

import json
from controller.orchestrator import (
    handle_request,
    handle_request_from_business,
)
from strategy_engine.engine import get_rule_diagnostics
from llm_analyst.extractor import extract_signals


def example_1_basic_usage():
    """
    Example 1: Basic competitor analysis
    """
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Competitor Analysis")
    print("="*60)
    
    raw_text = """
    Our main competitor just launched a new AI feature.
    People are excited but confused about how it works.
    The pricing seems unclear and the messaging is generic.
    Reviews mention the product is buggy.
    """
    
    print("\nInput:")
    print(raw_text)
    
    decision = handle_request(raw_text)
    
    print("\nDecision:")
    print(json.dumps(decision, indent=2))


def example_2_price_drop():
    """
    Example 2: Competitor drops price
    """
    print("\n" + "="*60)
    print("EXAMPLE 2: Competitor Price Drop")
    print("="*60)
    
    raw_text = """
    Competitor B reduced their prices by 30% yesterday.
    Their execution has been strong and customers love their product.
    The market is responding positively.
    """
    
    print("\nInput:")
    print(raw_text)
    
    decision = handle_request(raw_text)
    
    print("\nDecision:")
    print(json.dumps(decision, indent=2))
    
    print("\nKey Insight:")
    print(f"→ Strategy: {decision['best_move']}")
    print(f"→ Urgency: {decision['urgency']} (because execution is strong)")
    print(f"→ Focus: {decision['focus']}")
    print(f"→ Avoid: {', '.join(decision['avoid'])}")


def example_3_wait_and_see():
    """
    Example 3: Strategic wait (let competitor fail)
    """
    print("\n" + "="*60)
    print("EXAMPLE 3: Strategic Wait")
    print("="*60)
    
    raw_text = """
    Competitor C launched a new product last week.
    Initial reviews are very negative.
    The market seems confused about the value proposition.
    Customers are complaining on social media.
    """
    
    print("\nInput:")
    print(raw_text)
    
    decision = handle_request(raw_text)
    
    print("\nDecision:")
    print(json.dumps(decision, indent=2))
    
    print("\nKey Insight:")
    print(f"→ Best move: {decision['best_move']}")
    print(f"→ Why wait? {decision['reason']}")


def example_4_caching_behavior():
    """
    Example 4: Demonstrate caching
    """
    print("\n" + "="*60)
    print("EXAMPLE 4: Caching Behavior")
    print("="*60)
    
    # Same meaning, different wording
    text_1 = "Competitor dropped prices. Market is confused."
    text_2 = "Our rival reduced their pricing. Customers seem uncertain."
    
    print("\nFirst request (cache miss):")
    print(f"Input: {text_1}")
    decision_1 = handle_request(text_1)
    print(f"Decision: {decision_1['best_move']}")
    
    print("\nSecond request (same meaning, different words):")
    print(f"Input: {text_2}")
    decision_2 = handle_request(text_2)
    print(f"Decision: {decision_2['best_move']}")
    
    print("\nNote: If Phase 2 extracts same signals, this will be a cache hit")


def example_5_diagnostics():
    """
    Example 5: Using diagnostics for debugging
    """
    print("\n" + "="*60)
    print("EXAMPLE 5: Diagnostic Mode")
    print("="*60)
    
    raw_text = """
    Competitor launched strong product with clear messaging.
    Execution is excellent. Market loves it.
    """
    
    print("\nInput:")
    print(raw_text)
    
    # Extract signals first
    extracted = extract_signals(raw_text)
    
    # Get diagnostics
    diagnostics = get_rule_diagnostics(extracted)
    
    print("\nRule Evaluations:")
    for eval in diagnostics['rule_evaluations']:
        status = "✓ MATCHED" if eval['matched'] else "✗ No match"
        print(f"{status}: {eval['rule']}")
        if eval.get('decision'):
            print(f"  → Would choose: {eval['decision']['strategy_type']}")
    
    print("\nFallback:")
    print(f"  → {diagnostics['fallback']['strategy_type']}")


def example_6_database_backed():
    """
    Example 6: Database-backed decision (requires Supabase setup)
    """
    print("\n" + "="*60)
    print("EXAMPLE 6: Database-Backed Analysis")
    print("="*60)
    
    print("\nNote: This requires Supabase setup with:")
    print("  - 'businesses' table with description, target_audience")
    print("  - 'competitors' table with name, context, business_id")
    
    # Example (will fail if DB not set up)
    try:
        business_id = "your-business-id"
        decision = handle_request_from_business(business_id)
        print(f"\nDecision for business {business_id}:")
        print(json.dumps(decision, indent=2))
    except Exception as e:
        print(f"\n⚠ Database not configured: {e}")
        print("Set up Supabase and update business_id to use this feature")


def example_7_error_handling():
    """
    Example 7: Error handling
    """
    print("\n" + "="*60)
    print("EXAMPLE 7: Error Handling")
    print("="*60)
    
    # Test 1: Empty input
    print("\nTest 1: Empty input")
    try:
        handle_request("")
    except ValueError as e:
        print(f"✓ Caught: {e}")
    
    # Test 2: Too long input
    print("\nTest 2: Input too long")
    try:
        handle_request("x" * 3001)
    except ValueError as e:
        print(f"✓ Caught: {e}")
    
    # Test 3: Valid input (should work)
    print("\nTest 3: Valid input")
    try:
        decision = handle_request("Competitor launched a product")
        print(f"✓ Success: {decision['best_move']}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")


def run_all_examples():
    """
    Run all examples in sequence
    """
    print("\n" + "="*70)
    print(" COMPETITIVE STRATEGY DECISION SYSTEM - COMPLETE EXAMPLES")
    print("="*70)
    
    examples = [
        example_1_basic_usage,
        example_2_price_drop,
        example_3_wait_and_see,
        example_4_caching_behavior,
        example_5_diagnostics,
        example_6_database_backed,
        example_7_error_handling,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n⚠ Example failed: {e}")
            print("Continuing with next example...\n")
    
    print("\n" + "="*70)
    print(" EXAMPLES COMPLETE")
    print("="*70)
    print("\nNext steps:")
    print("1. Review the decisions above")
    print("2. Try your own competitor scenarios")
    print("3. Run test_strategy_engine.py for unit tests")
    print("4. Check diagnostics when decisions seem unexpected")
    print("\n")


if __name__ == "__main__":
    # Run specific example
    # example_1_basic_usage()
    
    # Or run all
    run_all_examples()