from typing import Dict
from config.settings import GEMINI_API_KEY
from src.Agent.gemini_agent import Gemini
import re

def evaluate_answer(question: str, user_answer: str, document_text: str) -> Dict:
    """
    Evaluate user answer using Gemini agent. Fallback to heuristic if no key.
    """
    if not GEMINI_API_KEY:
        q_words = set(re.findall(r'\w+', question.lower()))
        a_words = set(re.findall(r'\w+', user_answer.lower()))
        sentences = re.split(r'(?<=[.!?]) +', document_text)
        best = ('', 0)
        for sent in sentences:
            overlap = len(a_words & set(re.findall(r'\w+', sent.lower())))
            if overlap > best[1]:
                best = (sent, overlap)
        justification = f"Your answer overlaps with: '{best[0]}'" if best[0] else "No clear match found in document."
        score = min(1.0, best[1]/max(1, len(a_words)))
        return {
            'score': score,
            'justification': justification,
            'reference_snippet': best[0]
        }
    prompt = (
        f"Evaluate the following user's answer to the given question, strictly using the provided document.\n\nDocument:\n{document_text}\n\nQuestion: {question}\nUser Answer: {user_answer}\n\nGive a score between 0 and 1 (where 1 is perfect), a short justification, and a reference snippet from the document.\nRespond in JSON with keys: score, justification, reference_snippet."
    )
    gemini = Gemini(api_key=GEMINI_API_KEY, id='gemini-1.5-flash-latest', temprature=0.1)
    response = gemini.generate(prompt)
    import json
    # Try to parse Gemini's JSON response
    try:
        result = json.loads(response.text)
        # Ensure all required keys
        for key in ['score', 'justification', 'reference_snippet']:
            if key not in result:
                result[key] = ''
        return result
    except Exception:
        # Fallback: return raw text
        return {
            'score': 0.0,
            'justification': response.text.strip(),
            'reference_snippet': ''
        }
