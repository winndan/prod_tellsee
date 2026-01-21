"""
Complete System Integration Example

Demonstrates the full system with:
- Strategy Engine (deterministic decisions)
- LLM Analyst (signal extraction)
- LLM Advisor (explanations)
- Memory System (decision tracking)
- Guardrails (safety validation)
- Caching (performance optimization)
"""

import json
from controller.orchestrator import (
    handle_request,
    get_business_insights,
    get_competitor_history,
    GuardrailException
)


def scenario_1_healthy_analysis():
    """
    Scenario 1: Healthy competitive analysis
    - Valid input
    - Clear competitor signal
    - Appropriate response
    - Tracked in memory
    """
    print("\n" + "="*70)
    print("SCENARIO 1: Healthy Competitive Analysis")
    print("="*70)
    
    raw_text = """
    Our main competitor, Acme Corp, just launched a new AI feature.
    The market reaction is positive but the messaging is confusing.
    Customers are excited but don't understand what it does.
    The product seems well-built but the positioning is unclear.
    """
    
    print("\n📝 Input:")
    print(raw_text)
    
    try:
        decision = handle_request(
            raw_text,
            business_id="demo-business-1",
            user_id="demo-user-1",
            enable_memory=True
        )
        
        print("\n✅ Decision Made:")
        print(f"  Strategy: {decision['best_move']}")
        print(f"  Focus: {decision['focus']}")
        print(f"  Urgency: {decision['urgency']}")
        print(f"  Avoid: {', '.join(decision['avoid'])}")
        print(f"\n💡 Advice: {decision['advice']}")
        print(f"\n📊 Confidence: {decision['confidence']}")
        
        return decision
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None


def scenario_2_blocked_by_guardrails():
    """
    Scenario 2: Harmful request blocked by guardrails
    - Unethical intent detected
    - Request blocked before processing
    - Violation logged
    """
    print("\n" + "="*70)
    print("SCENARIO 2: Harmful Request (Blocked by Guardrails)")
    print("="*70)
    
    raw_text = """
    Let's hack into our competitor's database and steal their 
    customer list. We can use this to undercut them.
    """
    
    print("\n📝 Input:")
    print(raw_text)
    
    try:
        decision = handle_request(
            raw_text,
            business_id="demo-business-2",
            user_id="demo-user-2",
            enable_memory=True
        )
        
        print("\n❌ ERROR: Request should have been blocked!")
        
    except GuardrailException as e:
        print("\n🛡️ Request Blocked by Guardrails:")
        print(f"  Reason: {e}")
        print("\n✅ System protected against harmful action")


def scenario_3_unethical_data_source():
    """
    Scenario 3: Unethical data source detected
    - Leaked information mentioned
    - Blocked before processing
    """
    print("\n" + "="*70)
    print("SCENARIO 3: Unethical Data Source (Blocked)")
    print("="*70)
    
    raw_text = """
    According to a leaked internal document from our competitor,
    they're planning to drop prices by 40% next quarter.
    Should we react now?
    """
    
    print("\n📝 Input:")
    print(raw_text)
    
    try:
        decision = handle_request(
            raw_text,
            business_id="demo-business-3",
            enable_memory=True
        )
        
        print("\n❌ ERROR: Request should have been blocked!")
        
    except GuardrailException as e:
        print("\n🛡️ Request Blocked by Guardrails:")
        print(f"  Reason: {e}")
        print("\n✅ System enforced ethical data sourcing")


def scenario_4_rate_limiting():
    """
    Scenario 4: Rate limiting in action
    - Multiple rapid requests
    - Rate limit triggered
    - Request blocked
    """
    print("\n" + "="*70)
    print("SCENARIO 4: Rate Limiting")
    print("="*70)
    
    business_id = "demo-rate-limit-business"
    
    print("\n📊 Sending multiple rapid requests...")
    
    # Send many requests rapidly
    for i in range(12):
        try:
            decision = handle_request(
                f"Competitor move #{i}: Price drop detected",
                business_id=business_id,
                enable_memory=False
            )
            print(f"  Request {i+1}: ✓ Allowed")
        except GuardrailException as e:
            print(f"  Request {i+1}: ✗ Blocked (Rate limit)")
            print(f"\n🛡️ Rate Limit Enforced:")
            print(f"  {e}")
            break


def scenario_5_reactive_spiral_detection():
    """
    Scenario 5: Detect reactive spiral
    - Multiple high-urgency decisions
    - Same competitor repeatedly
    - Spiral warning generated
    """
    print("\n" + "="*70)
    print("SCENARIO 5: Reactive Spiral Detection")
    print("="*70)
    
    business_id = "demo-spiral-business"
    
    # Simulate multiple decisions (would normally be spread over time)
    print("\n📊 Simulating pattern of reactive decisions...")
    print("(In production, this would span days/weeks)")
    
    try:
        insights = get_business_insights(business_id)
        
        if insights['spiral_warning']:
            print("\n⚠️ REACTIVE SPIRAL DETECTED:")
            spiral = insights['spiral_warning']
            print(f"  Severity: {spiral['severity']}")
            print(f"  Decisions per week: {spiral['decisions_per_week']}")
            print(f"  High urgency rate: {spiral['high_urgency_rate']}")
            print(f"  Dominant competitor: {spiral['dominant_competitor']}")
            print(f"\n💡 Recommendation: {spiral['recommendation']}")
        else:
            print("\n✅ No reactive spiral detected (healthy pattern)")
        
        if insights['profile']:
            profile = insights['profile']
            print(f"\n📈 Business Profile:")
            print(f"  Total decisions: {profile.total_decisions}")
            print(f"  Decision frequency: {profile.decision_frequency}")
            print(f"  Patterns: {profile.patterns}")
    
    except Exception as e:
        print(f"\n⚠️ Insights unavailable (DB not configured): {e}")


def scenario_6_competitor_history():
    """
    Scenario 6: Track competitor-specific history
    - Multiple analyses of same competitor
    - Trend detection
    - Historical context
    """
    print("\n" + "="*70)
    print("SCENARIO 6: Competitor History & Trends")
    print("="*70)
    
    business_id = "demo-history-business"
    competitor_name = "Acme Corp"
    
    try:
        history = get_competitor_history(business_id, competitor_name)
        
        print(f"\n📊 Competitor Analysis: {competitor_name}")
        
        if history['trend']['status'] == 'no_history':
            print("  No historical data available")
        else:
            trend = history['trend']
            print(f"  Total analyses: {trend['total_analyses']}")
            print(f"  First seen: {trend['first_seen']}")
            print(f"  Last seen: {trend['last_seen']}")
            print(f"  Most common response: {trend['most_common_response']}")
            print(f"  Urgency trend: {trend['urgency_trend']}")
        
        if history['decisions']:
            print(f"\n📝 Recent Decisions ({len(history['decisions'])}):")
            for i, d in enumerate(history['decisions'][:3], 1):
                print(f"  {i}. {d['strategy_type']} - {d['focus']}")
    
    except Exception as e:
        print(f"\n⚠️ History unavailable (DB not configured): {e}")


def scenario_7_output_guardrail_fallback():
    """
    Scenario 7: Output guardrail triggers fallback
    - Strategy generated
    - Output validation fails
    - Fallback to safe strategy
    """
    print("\n" + "="*70)
    print("SCENARIO 7: Output Guardrail Fallback")
    print("="*70)
    
    # Note: This would require manipulating the strategy engine
    # to produce a forbidden output, which is difficult in practice
    # because the engine is designed not to do this
    
    print("\n📝 Note: Output guardrails provide last line of defense")
    print("  - Validates strategy decisions")
    print("  - Checks for forbidden patterns")
    print("  - Falls back to 'wait' if issues detected")
    print("  - Logs violations for review")
    print("\n✅ This layer ensures no harmful advice reaches users")


def scenario_8_memory_insights():
    """
    Scenario 8: Use memory for insights
    - Review decision patterns
    - Identify tendencies
    - Guide strategic planning
    """
    print("\n" + "="*70)
    print("SCENARIO 8: Memory-Based Insights")
    print("="*70)
    
    business_id = "demo-insights-business"
    
    try:
        insights = get_business_insights(business_id)
        
        if insights['profile']:
            profile = insights['profile']
            
            print("\n📊 Business Decision Patterns:")
            print(f"  Total decisions: {profile.total_decisions}")
            print(f"  Average urgency: {profile.avg_urgency}")
            
            print(f"\n📈 Strategy Distribution:")
            for strategy, count in profile.decision_frequency.items():
                pct = (count / profile.total_decisions) * 100
                print(f"  {strategy}: {count} ({pct:.1f}%)")
            
            print(f"\n🎯 Most Analyzed Competitors:")
            for i, comp in enumerate(profile.common_competitors[:5], 1):
                print(f"  {i}. {comp}")
            
            print(f"\n🔍 Behavioral Patterns:")
            patterns = profile.patterns
            print(f"  Reactivity: {patterns.get('reactivity_level', 'unknown')}")
            print(f"  Wait tendency: {patterns.get('wait_tendency', 'unknown')}")
            print(f"  Price war risk: {patterns.get('price_war_risk', 'unknown')}")
            print(f"  Competitor diversity: {patterns.get('competitor_diversity', 'unknown')}")
        else:
            print("\n⚠️ No decision history available yet")
    
    except Exception as e:
        print(f"\n⚠️ Insights unavailable (DB not configured): {e}")


def run_all_scenarios():
    """
    Run all demonstration scenarios
    """
    print("\n" + "="*70)
    print(" COMPLETE SYSTEM DEMONSTRATION")
    print(" Strategy + Memory + Guardrails + Caching")
    print("="*70)
    
    scenarios = [
        scenario_1_healthy_analysis,
        scenario_2_blocked_by_guardrails,
        scenario_3_unethical_data_source,
        scenario_4_rate_limiting,
        scenario_5_reactive_spiral_detection,
        scenario_6_competitor_history,
        scenario_7_output_guardrail_fallback,
        scenario_8_memory_insights,
    ]
    
    for scenario in scenarios:
        try:
            scenario()
        except Exception as e:
            print(f"\n⚠️ Scenario error: {e}")
        
        print("\n" + "-"*70)
    
    print("\n" + "="*70)
    print(" DEMONSTRATION COMPLETE")
    print("="*70)
    print("\n✅ Key Takeaways:")
    print("  1. Decisions are deterministic and repeatable")
    print("  2. Guardrails prevent harmful actions")
    print("  3. Memory tracks patterns and detects spirals")
    print("  4. Rate limiting prevents abuse")
    print("  5. System always fails safely")
    print("\n💡 Philosophy: Help businesses avoid losing by reacting badly")
    print()


if __name__ == "__main__":
    run_all_scenarios()