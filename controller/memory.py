"""
Agent Memory System

Tracks decision history and context across multiple analyses.
Enables pattern detection and learning from past decisions.

Design Principles:
- Read-only for decision engine (no memory affects decisions)
- Write-only for analytics and learning
- Separate from operational cache
- Privacy-aware (business-scoped)
"""

import json
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, asdict
from dbase.supabase_client import supabase


@dataclass
class DecisionMemory:
    """
    Historical decision record
    """
    decision_id: str
    business_id: str
    timestamp: str
    
    # Input context
    competitor_name: str
    extracted_signals: Dict[str, Any]
    
    # Decision output
    strategy_type: str
    focus: str
    urgency: str
    avoid: List[str]
    
    # Metadata
    confidence: str
    context_hash: str
    cache_hit: bool


@dataclass
class BusinessMemoryProfile:
    """
    Aggregated memory profile for a business
    """
    business_id: str
    total_decisions: int
    decision_frequency: Dict[str, int]  # strategy_type -> count
    common_competitors: List[str]
    avg_urgency: str
    last_decision_date: str
    patterns: Dict[str, Any]


class MemoryStore:
    """
    Manages long-term decision memory
    """
    
    def __init__(self):
        self.table = "decision_memory"
    
    def save_decision(
        self,
        decision_id: str,
        business_id: str,
        competitor_name: str,
        extracted_signals: dict,
        strategy_decision: dict,
        advisor_output: dict,
        context_hash: str,
        cache_hit: bool
    ) -> None:
        """
        Store decision in long-term memory
        
        This runs AFTER decision is made, never blocks the pipeline.
        """
        try:
            memory = DecisionMemory(
                decision_id=decision_id,
                business_id=business_id,
                timestamp=datetime.utcnow().isoformat(),
                competitor_name=competitor_name,
                extracted_signals=extracted_signals,
                strategy_type=strategy_decision["best_move"],
                focus=strategy_decision["focus"],
                urgency=strategy_decision["urgency"],
                avoid=strategy_decision["avoid"],
                confidence=advisor_output["confidence"],
                context_hash=context_hash,
                cache_hit=cache_hit,
            )
            
            supabase.table(self.table).insert(
                asdict(memory)
            ).execute()
            
        except Exception as e:
            # Memory storage failures must never break the pipeline
            print(f"Memory storage failed (non-critical): {e}")
    
    def get_recent_decisions(
        self,
        business_id: str,
        limit: int = 10
    ) -> List[DecisionMemory]:
        """
        Retrieve recent decisions for a business
        """
        try:
            result = (
                supabase.table(self.table)
                .select("*")
                .eq("business_id", business_id)
                .order("timestamp", desc=True)
                .limit(limit)
                .execute()
            )
            
            return [DecisionMemory(**row) for row in result.data]
        
        except Exception as e:
            print(f"Memory retrieval failed: {e}")
            return []
    
    def get_decisions_by_competitor(
        self,
        business_id: str,
        competitor_name: str,
        days: int = 90
    ) -> List[DecisionMemory]:
        """
        Get all decisions about a specific competitor
        """
        try:
            cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()
            
            result = (
                supabase.table(self.table)
                .select("*")
                .eq("business_id", business_id)
                .eq("competitor_name", competitor_name)
                .gte("timestamp", cutoff)
                .order("timestamp", desc=True)
                .execute()
            )
            
            return [DecisionMemory(**row) for row in result.data]
        
        except Exception as e:
            print(f"Competitor history retrieval failed: {e}")
            return []
    
    def build_business_profile(
        self,
        business_id: str,
        days: int = 90
    ) -> Optional[BusinessMemoryProfile]:
        """
        Build aggregated memory profile
        
        Useful for:
        - Understanding decision patterns
        - Detecting reactive tendencies
        - Identifying over-monitored competitors
        """
        try:
            cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()
            
            result = (
                supabase.table(self.table)
                .select("*")
                .eq("business_id", business_id)
                .gte("timestamp", cutoff)
                .execute()
            )
            
            if not result.data:
                return None
            
            decisions = [DecisionMemory(**row) for row in result.data]
            
            # Aggregate stats
            strategy_counts = {}
            urgency_counts = {"low": 0, "medium": 0, "high": 0}
            competitor_counts = {}
            
            for d in decisions:
                strategy_counts[d.strategy_type] = strategy_counts.get(d.strategy_type, 0) + 1
                urgency_counts[d.urgency] = urgency_counts.get(d.urgency, 0) + 1
                competitor_counts[d.competitor_name] = competitor_counts.get(d.competitor_name, 0) + 1
            
            # Determine average urgency
            if urgency_counts["high"] > urgency_counts["medium"]:
                avg_urgency = "high"
            elif urgency_counts["medium"] > urgency_counts["low"]:
                avg_urgency = "medium"
            else:
                avg_urgency = "low"
            
            # Pattern detection
            patterns = self._detect_patterns(decisions)
            
            return BusinessMemoryProfile(
                business_id=business_id,
                total_decisions=len(decisions),
                decision_frequency=strategy_counts,
                common_competitors=sorted(
                    competitor_counts,
                    key=competitor_counts.get,
                    reverse=True
                )[:5],
                avg_urgency=avg_urgency,
                last_decision_date=decisions[0].timestamp if decisions else None,
                patterns=patterns,
            )
        
        except Exception as e:
            print(f"Profile building failed: {e}")
            return None
    
    def _detect_patterns(self, decisions: List[DecisionMemory]) -> Dict[str, Any]:
        """
        Detect behavioral patterns
        
        Patterns to identify:
        - Over-reactivity (too many high urgency decisions)
        - Analysis paralysis (too many wait decisions)
        - Competitor obsession (same competitor repeatedly)
        - Price war tendency (frequent pricing responses)
        """
        if not decisions:
            return {}
        
        total = len(decisions)
        
        # Calculate metrics
        high_urgency_pct = sum(1 for d in decisions if d.urgency == "high") / total
        wait_pct = sum(1 for d in decisions if d.strategy_type == "wait_and_observe") / total
        pricing_pct = sum(1 for d in decisions if d.strategy_type == "pricing_response") / total
        
        patterns = {
            "reactivity_level": "high" if high_urgency_pct > 0.5 else "moderate" if high_urgency_pct > 0.25 else "low",
            "wait_tendency": "high" if wait_pct > 0.6 else "moderate" if wait_pct > 0.3 else "low",
            "price_war_risk": "high" if pricing_pct > 0.4 else "moderate" if pricing_pct > 0.2 else "low",
        }
        
        # Competitor diversity
        unique_competitors = len(set(d.competitor_name for d in decisions))
        patterns["competitor_diversity"] = "high" if unique_competitors > 5 else "moderate" if unique_competitors > 2 else "low"
        
        return patterns


class MemoryInsights:
    """
    Generate insights from decision memory
    """
    
    def __init__(self, memory_store: MemoryStore):
        self.store = memory_store
    
    def get_competitor_trend(
        self,
        business_id: str,
        competitor_name: str
    ) -> Dict[str, Any]:
        """
        Analyze how responses to a competitor have evolved
        """
        decisions = self.store.get_decisions_by_competitor(
            business_id,
            competitor_name,
            days=180
        )
        
        if not decisions:
            return {"status": "no_history"}
        
        # Group by month
        monthly_urgency = {}
        for d in decisions:
            month = d.timestamp[:7]  # YYYY-MM
            if month not in monthly_urgency:
                monthly_urgency[month] = []
            monthly_urgency[month].append(d.urgency)
        
        return {
            "total_analyses": len(decisions),
            "first_seen": decisions[-1].timestamp,
            "last_seen": decisions[0].timestamp,
            "most_common_response": max(
                set(d.strategy_type for d in decisions),
                key=lambda x: sum(1 for d in decisions if d.strategy_type == x)
            ),
            "urgency_trend": self._calculate_urgency_trend(monthly_urgency),
        }
    
    def _calculate_urgency_trend(
        self,
        monthly_urgency: Dict[str, List[str]]
    ) -> str:
        """
        Determine if urgency is increasing, decreasing, or stable
        """
        if len(monthly_urgency) < 2:
            return "insufficient_data"
        
        urgency_map = {"low": 1, "medium": 2, "high": 3}
        
        months = sorted(monthly_urgency.keys())
        early_avg = sum(urgency_map[u] for u in monthly_urgency[months[0]]) / len(monthly_urgency[months[0]])
        late_avg = sum(urgency_map[u] for u in monthly_urgency[months[-1]]) / len(monthly_urgency[months[-1]])
        
        if late_avg > early_avg + 0.5:
            return "increasing"
        elif late_avg < early_avg - 0.5:
            return "decreasing"
        else:
            return "stable"
    
    def detect_reactive_spiral(
        self,
        business_id: str,
        threshold_days: int = 30
    ) -> Optional[Dict[str, Any]]:
        """
        Detect if business is in a reactive spiral
        
        A reactive spiral is characterized by:
        - Frequent decisions (>1 per week)
        - High urgency dominance
        - Same competitor repeatedly
        - Decreasing confidence
        """
        recent = self.store.get_recent_decisions(business_id, limit=20)
        
        if len(recent) < 5:
            return None
        
        # Check frequency
        time_span = (
            datetime.fromisoformat(recent[0].timestamp) - 
            datetime.fromisoformat(recent[-1].timestamp)
        ).days
        
        if time_span == 0:
            return None
        
        decisions_per_week = (len(recent) / time_span) * 7
        
        # Check urgency
        high_urgency_count = sum(1 for d in recent if d.urgency == "high")
        
        # Check competitor focus
        competitor_counts = {}
        for d in recent:
            competitor_counts[d.competitor_name] = competitor_counts.get(d.competitor_name, 0) + 1
        
        max_competitor_focus = max(competitor_counts.values()) / len(recent)
        
        # Spiral detection
        is_spiral = (
            decisions_per_week > 1.5 and
            high_urgency_count / len(recent) > 0.6 and
            max_competitor_focus > 0.5
        )
        
        if is_spiral:
            return {
                "status": "spiral_detected",
                "severity": "high" if decisions_per_week > 3 else "moderate",
                "decisions_per_week": round(decisions_per_week, 2),
                "high_urgency_rate": round(high_urgency_count / len(recent), 2),
                "dominant_competitor": max(competitor_counts, key=competitor_counts.get),
                "recommendation": "Consider stepping back and reviewing overall strategy",
            }
        
        return None


# Singleton instance
memory_store = MemoryStore()
memory_insights = MemoryInsights(memory_store)