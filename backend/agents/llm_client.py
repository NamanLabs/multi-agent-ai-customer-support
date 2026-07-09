"""
Thin wrapper around the Groq API (Llama 3) used by all agents.
Set GROQ_API_KEY as an environment variable before running.
Get a free key at: https://console.groq.com/keys
"""
import os
from groq import Groq

_client = None
MODEL_NAME = "llama-3.3-70b-versatile"


def get_client() -> Groq:
    global _client
    if _client is None:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "GROQ_API_KEY not set. Get a free key at https://console.groq.com/keys "
                "and set it: export GROQ_API_KEY=your_key_here"
            )
        _client = Groq(api_key=api_key)
    return _client


def chat_completion(system_prompt: str, user_prompt: str, temperature: float = 0.3) -> str:
    """Single-turn completion: system prompt + user prompt -> text response."""
    client = get_client()
    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content.strip()
