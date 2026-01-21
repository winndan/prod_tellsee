"""
Guardrails System

Prevents harmful, unethical, or dangerous decisions.
Validates inputs and outputs at every phase.

Design Principles:
- Fail-safe: Block harmful actions, never break pipeline
- Transparent: Log all guardrail violations
- Configurable: Easy to add new rules
- Privacy-first: No PII in logs
"""

import re
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class GuardrailViolation:
    """
    Records a guardrail violation
    """
    violation_type: str
    severity: str  # low, medium, high, critical
    message: str
    timestamp: str
    context: Dict[str, Any]


class GuardrailResult:
    """
    Result of guardrail check
    """
    def __init__(self):
        self.passed = True
        self.violations: List[GuardrailViolation] = []
        self.warnings: List[str] = []
    
    def add_violation(
        self,
        violation_type: str,
        severity: str,
        message: str,
        context: Optional[Dict] = None
    ):
        self.passed = False
        self.violations.append(
            GuardrailViolation(
                violation_type=violation_type,
                severity=severity,
                message=message,
                timestamp=datetime.utcnow().isoformat(),
                context=context or {}
            )
        )
    
    def add_warning(self, message: str):
        self.warnings.append(message)


class InputGuardrails:
    """
    Phase 0: Validate inputs before processing
    """
    
    # Patterns to detect harmful content
    SENSITIVE_PATTERNS = [
        r"hack\s+competitor",
        r"ddos",
        r"sabotage",
        r"illegal\s+activity",
        r"steal\s+(data|information|secrets)",
        r"bribe",
        r"blackmail",
    ]
    
    # PII patterns
    PII_PATTERNS = [
        r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
        r"\b\d{16}\b",  # Credit card
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",  # Email
    ]
    
    def __init__(self):
        self.max_length = 3000
        self.min_length = 10
    
    def validate(self, raw_text: str) -> GuardrailResult:
        """
        Validate raw input text
        """
        result = GuardrailResult()
        
        # 1. Length checks
        if not raw_text or len(raw_text.strip()) < self.min_length:
            result.add_violation(
                "input_too_short",
                "medium",
                f"Input must be at least {self.min_length} characters",
                {"length": len(raw_text) if raw_text else 0}
            )
            return result
        
        if len(raw_text) > self.max_length:
            result.add_violation(
                "input_too_long",
                "medium",
                f"Input exceeds {self.max_length} character limit",
                {"length": len(raw_text)}
            )
            return result
        
        # 2. Harmful content detection
        text_lower = raw_text.lower()
        for pattern in self.SENSITIVE_PATTERNS:
            if re.search(pattern, text_lower):
                result.add_violation(
                    "harmful_intent_detected",
                    "critical",
                    "Input contains potentially harmful or unethical intent",
                    {"pattern": pattern}
                )
                return result
        
        # 3. PII detection (warning only)
        for pattern in self.PII_PATTERNS:
            if re.search(pattern, raw_text):
                result.add_warning(
                    "Input may contain personally identifiable information (PII). "
                    "Consider removing sensitive data."
                )
        
        # 4. Spam detection
        if self._is_spam(raw_text):
            result.add_violation(
                "spam_detected",
                "low",
                "Input appears to be spam or gibberish",
                {}
            )
        
        return result
    
    def _is_spam(self, text: str) -> bool:
        """
        Basic spam detection
        """
        # Check for excessive repetition
        words = text.split()
        if len(words) > 5:
            unique_ratio = len(set(words)) / len(words)
            if unique_ratio < 0.3:
                return True
        
        # Check for keyboard smashing
        if re.search(r"[a-z]{20,}", text.lower()):
            return True
        
        return False


class OutputGuardrails:
    """
    Phase 6: Validate outputs before returning to user
    """
    
    # Forbidden strategy patterns
    FORBIDDEN_STRATEGIES = [
        "price_war",
        "race_to_bottom",
        "aggressive_undercutting",
        "feature_copying",
        "direct_attack",
    ]
    
    def __init__(self):
        pass
    
    def validate_strategy(
        self,
        strategy_decision: Dict[str, Any]
    ) -> GuardrailResult:
        """
        Validate strategy decision is safe and ethical
        """
        result = GuardrailResult()
        
        # 1. Check for forbidden strategies
        focus = strategy_decision.get("focus", "").lower()
        for forbidden in self.FORBIDDEN_STRATEGIES:
            if forbidden in focus:
                result.add_violation(
                    "forbidden_strategy",
                    "high",
                    f"Strategy focus contains forbidden pattern: {forbidden}",
                    {"focus": focus}
                )
        
        # 2. Validate urgency makes sense
        urgency = strategy_decision.get("urgency", "")
        strategy_type = strategy_decision.get("best_move", "")
        
        if strategy_type == "wait_and_observe" and urgency == "high":
            result.add_violation(
                "inconsistent_urgency",
                "medium",
                "Wait strategy should not have high urgency",
                {"strategy": strategy_type, "urgency": urgency}
            )
        
        # 3. Check advice tone
        advice = strategy_decision.get("advice", "")
        if self._is_aggressive_tone(advice):
            result.add_warning(
                "Advice tone may be too aggressive. Consider softer language."
            )
        
        return result
    
    def _is_aggressive_tone(self, text: str) -> bool:
        """
        Detect aggressive or hostile language
        """
        aggressive_words = [
            "destroy",
            "crush",
            "annihilate",
            "attack",
            "dominate",
            "kill",
        ]
        
        text_lower = text.lower()
        return any(word in text_lower for word in aggressive_words)


class RateLimitGuardrail:
    """
    Prevent abuse through rate limiting
    """
    
    def __init__(self):
        self.request_history: Dict[str, List[datetime]] = {}
        
        # Limits
        self.max_per_minute = 10
        self.max_per_hour = 100
        self.max_per_day = 500
    
    def check_rate_limit(
        self,
        business_id: str
    ) -> GuardrailResult:
        """
        Check if business exceeds rate limits
        """
        result = GuardrailResult()
        now = datetime.utcnow()
        
        # Initialize history
        if business_id not in self.request_history:
            self.request_history[business_id] = []
        
        history = self.request_history[business_id]
        
        # Clean old entries
        history = [
            ts for ts in history
            if now - ts < timedelta(days=1)
        ]
        self.request_history[business_id] = history
        
        # Count recent requests
        minute_ago = now - timedelta(minutes=1)
        hour_ago = now - timedelta(hours=1)
        day_ago = now - timedelta(days=1)
        
        requests_per_minute = sum(1 for ts in history if ts > minute_ago)
        requests_per_hour = sum(1 for ts in history if ts > hour_ago)
        requests_per_day = sum(1 for ts in history if ts > day_ago)
        
        # Check limits
        if requests_per_minute > self.max_per_minute:
            result.add_violation(
                "rate_limit_exceeded",
                "high",
                f"Exceeded {self.max_per_minute} requests per minute",
                {"requests": requests_per_minute}
            )
        elif requests_per_hour > self.max_per_hour:
            result.add_violation(
                "rate_limit_exceeded",
                "high",
                f"Exceeded {self.max_per_hour} requests per hour",
                {"requests": requests_per_hour}
            )
        elif requests_per_day > self.max_per_day:
            result.add_violation(
                "rate_limit_exceeded",
                "high",
                f"Exceeded {self.max_per_day} requests per day",
                {"requests": requests_per_day}
            )
        
        # Record this request
        if result.passed:
            self.request_history[business_id].append(now)
        
        return result


class BusinessContextGuardrail:
    """
    Validate business context and permissions
    """
    
    def __init__(self):
        pass
    
    def validate_business_access(
        self,
        business_id: str,
        user_id: Optional[str] = None
    ) -> GuardrailResult:
        """
        Validate business exists and user has access
        """
        result = GuardrailResult()
        
        # TODO: Implement actual business validation
        # This would check Supabase for:
        # - Business exists
        # - User has permission
        # - Business account is active
        # - No outstanding violations
        
        if not business_id:
            result.add_violation(
                "invalid_business",
                "critical",
                "Business ID is required",
                {}
            )
        
        return result


class CompetitorDataGuardrail:
    """
    Ensure competitor data is ethically sourced
    """
    
    FORBIDDEN_SOURCES = [
        "leaked",
        "hacked",
        "stolen",
        "confidential",
        "internal document",
        "employee said",
    ]
    
    def validate_data_source(self, raw_text: str) -> GuardrailResult:
        """
        Check if competitor data might be from unethical sources
        """
        result = GuardrailResult()
        
        text_lower = raw_text.lower()
        for source in self.FORBIDDEN_SOURCES:
            if source in text_lower:
                result.add_violation(
                    "unethical_data_source",
                    "critical",
                    f"Competitor data may be from unethical source: {source}",
                    {"source": source}
                )
                return result
        
        return result


class GuardrailOrchestrator:
    """
    Main guardrail system - coordinates all checks
    """
    
    def __init__(self):
        self.input_guardrails = InputGuardrails()
        self.output_guardrails = OutputGuardrails()
        self.rate_limiter = RateLimitGuardrail()
        self.business_guardrail = BusinessContextGuardrail()
        self.data_guardrail = CompetitorDataGuardrail()
    
    def validate_input(
        self,
        raw_text: str,
        business_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> GuardrailResult:
        """
        Run all input validations
        """
        # Combine all checks
        checks = [
            self.input_guardrails.validate(raw_text),
            self.data_guardrail.validate_data_source(raw_text),
        ]
        
        # Rate limiting (if business_id provided)
        if business_id:
            checks.append(self.rate_limiter.check_rate_limit(business_id))
            checks.append(self.business_guardrail.validate_business_access(business_id, user_id))
        
        # Aggregate results
        result = GuardrailResult()
        for check in checks:
            if not check.passed:
                result.passed = False
                result.violations.extend(check.violations)
            result.warnings.extend(check.warnings)
        
        return result
    
    def validate_output(
        self,
        strategy_decision: Dict[str, Any]
    ) -> GuardrailResult:
        """
        Run all output validations
        """
        return self.output_guardrails.validate_strategy(strategy_decision)
    
    def log_violation(self, violation: GuardrailViolation):
        """
        Log guardrail violation for monitoring
        
        In production, this would:
        - Send to logging service
        - Alert on critical violations
        - Track patterns of abuse
        """
        print(f"GUARDRAIL VIOLATION: [{violation.severity}] {violation.violation_type}")
        print(f"  Message: {violation.message}")
        print(f"  Time: {violation.timestamp}")


# Singleton instance
guardrails = GuardrailOrchestrator()