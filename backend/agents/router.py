"""
Module 4: Agent Router + Response Aggregator

Routes a query to one or more specialized agents based on detected intent(s),
and aggregates their responses into a single final answer. Also runs
escalation logic (part of the Objective: "Escalate unresolved issues").
"""
from backend.agents.intent_detector import detect_intent
from backend.agents import billing, technical, product, complaint, faq

# Maps each possible intent label to the agent module that handles it.
# Refund maps to Billing per the spec (Billing Agent handles Refunds).
INTENT_TO_AGENT = {
    "Billing": billing,
    "Refund": billing,
    "Technical": technical,
    "Product": product,
    "Complaint": complaint,
    "FAQ": faq,
}

CONFIDENCE_ESCALATION_THRESHOLD = 0.45
COMPLAINT_KEYWORDS = {"angry", "furious", "unacceptable", "worst", "scam", "sue", "lawsuit"}


def should_escalate(query: str, intents: list[str], confidence: float) -> bool:
    """Escalation triggers (beyond spec minimum): low intent-detection
    confidence, explicit Complaint intent, or strong negative-sentiment
    keywords in the raw query."""
    if confidence < CONFIDENCE_ESCALATION_THRESHOLD:
        return True
    if "Complaint" in intents:
        return True
    lowered = query.lower()
    if any(kw in lowered for kw in COMPLAINT_KEYWORDS):
        return True
    return False


def route_query(query: str) -> dict:
    """Main entry point used by the API layer. Detects intent, dispatches
    to the relevant agent(s), aggregates their answers, and flags escalation."""
    detection = detect_intent(query)
    intents = detection["intents"]
    confidence = detection["confidence"]

    # Deduplicate agents (e.g. Billing + Refund both map to the billing agent)
    agents_to_call = []
    seen_modules = set()
    for intent in intents:
        module = INTENT_TO_AGENT.get(intent)
        if module and module not in seen_modules:
            agents_to_call.append((intent, module))
            seen_modules.add(module)

    if not agents_to_call:
        agents_to_call = [("FAQ", faq)]

    agent_responses = [module.handle(query) for _, module in agents_to_call]

    aggregated_answer = _aggregate(agent_responses)
    escalate = should_escalate(query, intents, confidence)

    return {
        "query": query,
        "detected_intents": intents,
        "confidence": confidence,
        "agents_invoked": [r["agent"] for r in agent_responses],
        "agent_responses": agent_responses,
        "final_response": aggregated_answer,
        "escalated": escalate,
    }


def _aggregate(agent_responses: list[dict]) -> str:
    """Module: Response Aggregator. If only one agent responded, use its
    answer directly. If multiple agents responded (multi-agent routing),
    combine them into one coherent reply with light labeling."""
    if len(agent_responses) == 1:
        return agent_responses[0]["answer"]

    parts = []
    for r in agent_responses:
        parts.append(f"{r['answer']}")
    return "\n\n".join(parts)
