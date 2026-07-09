"""
Module 3: Intent Detection Agent

Classifies a customer query into one or more of:
Billing, Refund, Product, Technical, Complaint, FAQ

Supports MULTI-LABEL classification, so a query like
"I paid yesterday but Premium is still locked" correctly
triggers both Billing and Technical -- matching the spec's example.
"""
import json
import re
from backend.agents.llm_client import chat_completion

VALID_INTENTS = {"Billing", "Refund", "Product", "Technical", "Complaint", "FAQ"}

SYSTEM_PROMPT = """You are an intent classification system for a customer support platform.
Classify the customer's message into one or more of these categories:
- Billing: payments, subscriptions, invoices
- Refund: refund requests, return status
- Product: product features, pricing, comparisons, availability
- Technical: login issues, password reset, installation, bugs, errors
- Complaint: dissatisfaction, escalation requests, complaints
- FAQ: general company policy or informational questions

Respond ONLY with a JSON object in this exact format, no other text:
{"intents": ["Category1", "Category2"], "confidence": 0.0-1.0}

Include multiple categories if the query genuinely spans more than one domain.
Confidence reflects how certain you are about the classification overall."""


def detect_intent(query: str) -> dict:
    """Returns {'intents': [...], 'confidence': float}. Falls back to
    ['FAQ'] with low confidence if the LLM output can't be parsed, so the
    router always has something safe to route to."""
    raw = chat_completion(SYSTEM_PROMPT, query, temperature=0.0)

    # Be defensive: strip markdown fences if the model adds them anyway
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        return {"intents": ["FAQ"], "confidence": 0.3}

    try:
        parsed = json.loads(match.group(0))
        intents = [i for i in parsed.get("intents", []) if i in VALID_INTENTS]
        confidence = float(parsed.get("confidence", 0.5))
        if not intents:
            intents = ["FAQ"]
        return {"intents": intents, "confidence": confidence}
    except (json.JSONDecodeError, ValueError, TypeError):
        return {"intents": ["FAQ"], "confidence": 0.3}
