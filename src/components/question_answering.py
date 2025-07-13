from typing import Dict
import re
from config.settings import GEMINI_API_KEY
from src.Agent.gemini_agent import Gemini

def extract_relevant_context(question: str, document_text: str, top_k: int = 3) -> str:
    # Simple heuristic: pick top_k sentences with most keyword overlap
    sentences = re.split(r'(?<=[.!?]) +', document_text)
    q_words = set(re.findall(r'\w+', question.lower()))
    ranked = sorted(
        sentences,
        key=lambda sent: len(q_words & set(re.findall(r'\w+', sent.lower()))),
        reverse=True
    )
    return " ".join(ranked[:top_k])

def answer_question(question: str, document_text: str) -> Dict:
    """
    Uses Gemini agent for context-grounded Q&A. Falls back to keyword matching if no key.
    """
    if not GEMINI_API_KEY:
        # fallback to keyword matching
        # fallback to keyword matching
        sentences = re.split(r'(?<=[.!?]) +', document_text)
        q_words = set(re.findall(r'\w+', question.lower()))
        best = ('', 0)
        for sent in sentences:
            overlap = len(q_words & set(re.findall(r'\w+', sent.lower())))
            if overlap > best[1]:
                best = (sent, overlap)
        answer = best[0] if best[0] else "Sorry, I couldn't find an answer in the document."
        return {'answer': answer, 'reference_snippet': answer}

    context = extract_relevant_context(question, document_text)
    prompt = (
        "You are a research document assistant. Answer the question strictly using the provided context. "
        "If the answer is not present in the context, say so.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    )
    gemini = Gemini(api_key=GEMINI_API_KEY, id='gemini-1.5-flash-latest', temprature=0.1)
    response = gemini.generate(prompt)
    answer = response.text.strip()
    return {
        'answer': answer,
        'reference_snippet': context
    }