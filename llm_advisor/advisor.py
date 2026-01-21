import os
import json
from dotenv import load_dotenv

from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

from llm_advisor.prompts import ADVISOR_SYSTEM_PROMPT
from llm_advisor.schema import AdvisorInputSchema, AdvisorOutputSchema

# ----------------------------
# ENV SETUP
# ----------------------------
load_dotenv()

google_api_key = os.getenv("GEMINI_API_KEY")
if not google_api_key:
    raise RuntimeError("GEMINI_API_KEY not set")

# ----------------------------
# MODEL + PROVIDER
# ----------------------------
model = GoogleModel(
    "gemini-2.5-flash",
    provider=GoogleProvider(api_key=google_api_key),
)

# ----------------------------
# AGENT (ADVISOR)
# ----------------------------
advisor_agent = Agent(
    model=model,
    system_prompt=ADVISOR_SYSTEM_PROMPT,
)

# ----------------------------
# HELPERS
# ----------------------------
def extract_json_block(text: str) -> str:
    """
    Removes ``` wrappers if present.
    """
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        return "\n".join(lines).strip()
    return text


def force_json(text: str) -> dict:
    """
    Ensures JSON parsing even if the model adds extra text.
    """
    text = text.strip()

    # Strip leading prose if present
    if not text.startswith("{"):
        idx = text.find("{")
        if idx != -1:
            text = text[idx:]
    
    # Strip trailing prose if present
    if not text.endswith("}"):
        idx = text.rfind("}")
        if idx != -1:
            text = text[:idx + 1]

    return json.loads(text)

# ----------------------------
# MAIN ENTRY
# ----------------------------
def explain_strategy(payload: dict) -> AdvisorOutputSchema:
    """
    Phase 3 - Advisor LLM

    Explains a FINAL strategy decision.
    Does NOT invent strategy.
    Does NOT modify decisions.
    """

    # 1. Validate input schema
    validated_input = AdvisorInputSchema(**payload)

    # 2. Send structured JSON AS TEXT (CRITICAL)
    result = advisor_agent.run_sync(
        json.dumps(validated_input.model_dump(), indent=2)
    )

    raw_output = result.output
    clean_output = extract_json_block(raw_output)

    # 3. Enforce JSON-only output
    try:
        parsed = force_json(clean_output)
    except Exception as e:
        raise ValueError(
            f"Advisor LLM did not return valid JSON.\nRaw output:\n{raw_output}\nError: {e}"
        )

    # 4. Validate output schema
    try:
        validated_output = AdvisorOutputSchema(**parsed)
    except Exception as e:
        raise ValueError(f"Advisor output failed validation: {e}\nParsed data: {parsed}")

    return validated_output