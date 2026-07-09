from backend.agents.base_agent import run_agent

SYSTEM_PROMPT = """You are the FAQ Agent for TechMart Electronics.
You handle: general company policy questions, contact information, and
informational queries that don't fit billing, technical, product, or complaint
categories. Keep responses concise and friendly."""


def handle(query: str) -> dict:
    return run_agent("FAQ Agent", SYSTEM_PROMPT, query)
