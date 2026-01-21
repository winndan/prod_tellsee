# Memory & Guardrails System

Complete documentation for the Agent Memory and Safety Guardrails systems.

---

## 🧠 Memory System

### Overview

The Memory System tracks all strategic decisions over time, enabling:
- Pattern detection (reactive tendencies, price war risks)
- Competitor-specific history
- Learning from past decisions
- Spiral detection (warning when over-reacting)

### Design Principles

✅ **Read-only for decisions** - Memory NEVER influences strategy decisions  
✅ **Write-only for analytics** - Used for insights and learning  
✅ **Fail-safe** - Memory failures never block the pipeline  
✅ **Privacy-aware** - Business-scoped, no cross-contamination  

---

## 📊 Memory Components

### 1. DecisionMemory
Records individual decisions with full context:
```python
@dataclass
class DecisionMemory:
    decision_id: str
    business_id: str
    timestamp: str
    competitor_name: str
    extracted_signals: Dict
    strategy_type: str
    focus: str
    urgency: str
    avoid: List[str]
    confidence: str
    context_hash: str
    cache_hit: bool
```

### 2. BusinessMemoryProfile
Aggregated patterns for a business:
```python
@dataclass
class BusinessMemoryProfile:
    business_id: str
    total_decisions: int
    decision_frequency: Dict[str, int]
    common_competitors: List[str]
    avg_urgency: str
    last_decision_date: str
    patterns: Dict[str, Any]
```

### 3. MemoryStore
Core storage interface:
```python
# Save decision
memory_store.save_decision(
    decision_id="...",
    business_id="...",
    competitor_name="...",
    extracted_signals={...},
    strategy_decision={...},
    advisor_output={...},
    context_hash="...",
    cache_hit=False
)

# Retrieve recent
recent = memory_store.get_recent_decisions(business_id, limit=10)

# Build profile
profile = memory_store.build_business_profile(business_id, days=90)
```

---

## 🔍 Memory Insights

### Pattern Detection

The system automatically detects:

1. **Reactivity Level**
   - High: >50% high-urgency decisions
   - Moderate: 25-50% high-urgency
   - Low: <25% high-urgency

2. **Wait Tendency**
   - High: >60% wait decisions (analysis paralysis)
   - Moderate: 30-60% wait decisions
   - Low: <30% wait decisions

3. **Price War Risk**
   - High: >40% pricing responses
   - Moderate: 20-40% pricing responses
   - Low: <20% pricing responses

4. **Competitor Diversity**
   - High: >5 unique competitors analyzed
   - Moderate: 2-5 competitors
   - Low: 1-2 competitors (obsession risk)

### Reactive Spiral Detection

Identifies when a business is over-reacting:
```python
spiral = memory_insights.detect_reactive_spiral(business_id)

if spiral:
    # {
    #   "status": "spiral_detected",
    #   "severity": "high",
    #   "decisions_per_week": 4.5,
    #   "high_urgency_rate": 0.75,
    #   "dominant_competitor": "Competitor X",
    #   "recommendation": "Consider stepping back..."
    # }
```

**Spiral Criteria:**
- >1.5 decisions per week
- >60% high-urgency decisions
- >50% focused on single competitor

### Competitor Trends

Track how responses evolve over time:
```python
trend = memory_insights.get_competitor_trend(
    business_id,
    competitor_name
)

# {
#   "total_analyses": 12,
#   "first_seen": "2025-01-01",
#   "last_seen": "2025-01-21",
#   "most_common_response": "positioning_response",
#   "urgency_trend": "increasing"  # or "decreasing", "stable"
# }
```

---

## 🛡️ Guardrails System

### Overview

Multi-layer safety system that:
- Validates inputs before processing
- Blocks harmful or unethical requests
- Enforces rate limits
- Validates outputs before delivery
- Ensures ethical data sourcing

### Design Principles

✅ **Fail-safe** - Block harmful actions, never break pipeline  
✅ **Transparent** - Log all violations for monitoring  
✅ **Configurable** - Easy to add new rules  
✅ **Privacy-first** - No PII in logs  

---

## 🚧 Guardrail Layers

### Layer 1: Input Guardrails

**Checks:**
- Length validation (10-3000 characters)
- Harmful intent detection
- PII detection (warnings only)
- Spam detection

**Blocked Patterns:**
```python
SENSITIVE_PATTERNS = [
    r"hack\s+competitor",
    r"ddos",
    r"sabotage",
    r"steal\s+(data|secrets)",
    r"bribe",
    r"blackmail",
]
```

**Example:**
```python
result = guardrails.validate_input(
    "Let's hack competitor's website",
    business_id="..."
)

if not result.passed:
    # Request blocked
    # violations: [GuardrailViolation(...)]
```

### Layer 2: Data Source Validation

Ensures competitor data is ethically sourced:

**Blocked Sources:**
- Leaked documents
- Hacked information
- Stolen data
- Confidential materials
- Insider information

**Example:**
```python
result = guardrails.data_guardrail.validate_data_source(
    "From leaked internal document..."
)
# blocked: True
```

### Layer 3: Rate Limiting

Prevents abuse:
- **10 requests/minute**
- **100 requests/hour**
- **500 requests/day**

```python
result = guardrails.rate_limiter.check_rate_limit(business_id)

if not result.passed:
    # Rate limit exceeded
    # violations: [{type: "rate_limit_exceeded"}]
```

### Layer 4: Business Access Validation

Verifies:
- Business exists
- User has permission
- Account is active
- No outstanding violations

### Layer 5: Output Guardrails

Validates strategy decisions:

**Forbidden Strategies:**
- price_war
- race_to_bottom
- aggressive_undercutting
- feature_copying
- direct_attack

**Consistency Checks:**
- Wait strategy should not have high urgency
- Pricing response should avoid race-to-bottom

**Tone Validation:**
- Flags aggressive language
- Warns about hostile tone

---

## 🔄 Integration with Pipeline

### Enhanced Orchestrator Flow

```
1. Input Validation (Guardrails)
   ↓
2. Extract Signals (Phase 2)
   ↓
3. Cache Lookup
   ↓
4. Decide Strategy (Phase 1)
   ↓
5. Explain Strategy (Phase 3)
   ↓
6. Output Validation (Guardrails)
   ↓
7. Cache Result
   ↓
8. Store in Memory (async, non-blocking)
```

### Usage Examples

**Basic Usage:**
```python
from controller.orchestrator import handle_request

decision = handle_request(
    raw_text="Competitor dropped prices",
    business_id="business-123",
    user_id="user-456",
    enable_memory=True  # Track decision
)
```

**With Error Handling:**
```python
from controller.orchestrator import (
    handle_request,
    GuardrailException
)

try:
    decision = handle_request(text, business_id)
except GuardrailException as e:
    print(f"Request blocked: {e}")
except Exception as e:
    print(f"Processing error: {e}")
```

**Get Insights:**
```python
from controller.orchestrator import (
    get_business_insights,
    get_competitor_history
)

# Business-level insights
insights = get_business_insights("business-123")
print(insights['profile'])
print(insights['spiral_warning'])

# Competitor-specific history
history = get_competitor_history(
    "business-123",
    "Competitor X"
)
print(history['trend'])
print(history['decisions'])
```

---

## 💾 Database Schema

### Required Tables

**decision_memory**
- Stores all historical decisions
- Indexed on business_id, timestamp, competitor

**guardrail_violations**
- Logs all security events
- Tracks severity and resolution

**business_patterns**
- Caches aggregated patterns
- Auto-updated via triggers

**rate_limits**
- Tracks request frequency
- Auto-cleanup after 24 hours

See `memory_schema.sql` for complete schema.

---

## 📈 Analytics Queries

### Recent Decisions
```sql
SELECT * FROM recent_decisions
WHERE business_id = 'your-business-id'
LIMIT 10;
```

### Strategy Distribution
```sql
SELECT * FROM strategy_distribution
WHERE business_id = 'your-business-id';
```

### Competitor Focus
```sql
SELECT * FROM competitor_focus
WHERE business_id = 'your-business-id'
ORDER BY analysis_count DESC;
```

### High-Risk Patterns
```sql
SELECT * FROM high_risk_patterns
WHERE business_id = 'your-business-id';
```

### Check Reactive Spiral
```sql
SELECT check_reactive_spiral('your-business-id');
```

---

## 🔧 Configuration

### Environment Variables

```env
# Memory System
ENABLE_MEMORY=true
MEMORY_RETENTION_DAYS=90

# Guardrails
RATE_LIMIT_PER_MINUTE=10
RATE_LIMIT_PER_HOUR=100
RATE_LIMIT_PER_DAY=500
```

### Custom Guardrail Rules

Add new patterns to `guardrails.py`:

```python
# In InputGuardrails class
SENSITIVE_PATTERNS = [
    r"your_custom_pattern",
    # ...
]

# In OutputGuardrails class
FORBIDDEN_STRATEGIES = [
    "your_forbidden_strategy",
    # ...
]
```

---

## 🧪 Testing

Run complete test suite:
```bash
python test_memory_guardrails.py
```

Tests verify:
- ✅ Memory storage and retrieval
- ✅ Pattern detection accuracy
- ✅ Guardrail blocking behavior
- ✅ Rate limiting enforcement
- ✅ PII detection
- ✅ Integration with orchestrator

---

## 🚨 Monitoring

### Key Metrics

**Memory System:**
- Total decisions stored
- Cache hit rate
- Pattern detection accuracy
- Spiral detection rate

**Guardrails:**
- Violation rate by type
- False positive rate
- Rate limit hit rate
- Output fallback rate

### Alerts

Set up alerts for:
- High violation rates (>5% of requests)
- Critical violations (harmful intent)
- Reactive spirals detected
- Rate limit abuse patterns

---

## 🎯 Best Practices

### Memory System

1. **Enable memory for production** - Insights are valuable
2. **Review patterns monthly** - Catch reactive tendencies early
3. **Monitor spiral warnings** - Intervene when detected
4. **Clean old data** - Keep last 180 days

### Guardrails

1. **Log all violations** - Track patterns
2. **Review false positives** - Tune patterns
3. **Update forbidden lists** - Add new harmful patterns
4. **Test new rules** - Before deploying

### Integration

1. **Never skip guardrails** - Even for trusted users
2. **Handle failures gracefully** - Show clear error messages
3. **Respect rate limits** - Don't bypass for "VIP" users
4. **Audit regularly** - Review violation logs

---

## 🔐 Security Considerations

1. **No PII in memory** - Strip before storage
2. **Business isolation** - Row-level security (RLS)
3. **Encrypted storage** - Use Supabase encryption
4. **Access logging** - Track who views what
5. **Data retention** - Auto-delete after 180 days

---

## 📚 API Reference

### Memory Functions

```python
# Save decision
memory_store.save_decision(...)

# Get recent
memory_store.get_recent_decisions(business_id, limit)

# Get by competitor
memory_store.get_decisions_by_competitor(business_id, name, days)

# Build profile
memory_store.build_business_profile(business_id, days)
```

### Insight Functions

```python
# Detect spiral
memory_insights.detect_reactive_spiral(business_id, threshold_days)

# Competitor trend
memory_insights.get_competitor_trend(business_id, name)
```

### Guardrail Functions

```python
# Validate input
guardrails.validate_input(text, business_id, user_id)

# Validate output
guardrails.validate_output(decision)

# Check rate limit
guardrails.rate_limiter.check_rate_limit(business_id)

# Validate data source
guardrails.data_guardrail.validate_data_source(text)
```

---

## 🤝 Contributing

When adding new features:
1. Add tests to `test_memory_guardrails.py`
2. Update schema if needed
3. Document new patterns/rules
4. Run full test suite

---

## 📝 License

MIT

---

## 💡 Philosophy

> "The system helps businesses avoid losing by reacting badly."

Memory and guardrails embody this by:
- **Preventing hasty decisions** (spiral detection)
- **Blocking harmful actions** (guardrails)
- **Learning from patterns** (memory insights)
- **Encouraging patience** (wait is a first-class strategy)

The goal is **thoughtful restraint**, not aggressive reaction.