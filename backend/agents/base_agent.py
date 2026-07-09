"""
Shared logic used by every specialized agent (billing, technical, product,
complaint, faq). Each agent module just defines its own SYSTEM_PROMPT and
calls run_agent().
"""
from backend.agents.llm_client import chat_completion
from backend.rag.retrieve import retrieve, format_context


def run_agent(agent_name: str, system_prompt: str, query: str, top_k: int = 4) -> dict:
    """Retrieves relevant KB context and generates a grounded response.
    Returns a dict so the Response Aggregator can combine multiple agents'
    outputs and cite which sources were used (useful for the report/demo)."""
    chunks = retrieve(query, top_k=top_k)
    context = format_context(chunks)

    full_prompt = (
        f"Company knowledge base context:\n{context}\n\n"
        f"Customer query: {query}\n\n"
        f"Answer using only the context above. If the context doesn't cover "
        f"the question, say you don't have that information and offer to "
        f"escalate to a human agent."
    )
    answer = chat_completion(system_prompt, full_prompt, temperature=0.3)

    return {
        "agent": agent_name,
        "answer": answer,
        "sources": sorted(set(c["source"] for c in chunks)),
    }
