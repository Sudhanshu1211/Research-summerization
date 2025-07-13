from config.settings import GEMINI_API_KEY
from src.Agent.gemini_agent import Gemini

def generate_summary(text: str, max_words: int = 150) -> str:
    """
    Generate a concise summary (≤150 words) using Gemini agent.
    """
    if not GEMINI_API_KEY:
        # Fallback: first N words
        import re
        words = re.findall(r'\w+|[.,!?;]', text)
        summary = ' '.join(words[:max_words])
        return summary
    prompt = (
        f"Summarize the following document in no more than {max_words} words.\n\nDocument:\n{text}\n\nSummary:"
    )
    gemini = Gemini(api_key=GEMINI_API_KEY, id='gemini-1.5-flash-latest', temprature=0.1)
    response = gemini.generate(prompt)
    return response.text.strip()
