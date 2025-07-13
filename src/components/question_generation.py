from typing import List
from config.settings import GEMINI_API_KEY
from typing import Dict, List
from config.settings import GEMINI_API_KEY
from src.Agent.gemini_agent import Gemini
import random

# Generate 3 challenge questions and return as a dictionary {q1: ..., q2: ..., q3: ...}
def generate_logic_challenges_dict(document_text: str, num_questions: int = 3) -> Dict[str, str]:
    """
    Generate logic-based challenge questions using Gemini agent. Return as a dictionary.
    """
    if not GEMINI_API_KEY:
        sentences = [s.strip() for s in document_text.split('.') if len(s.split()) > 6]
        random.shuffle(sentences)
        questions = []
        for sent in sentences[:num_questions]:
            questions.append(f"Based on the document, what is the implication of: '{sent[:60]}...'? Justify.")
        while len(questions) < num_questions:
            questions.append("Explain a key point from the document and justify your reasoning.")
        return {f"q{i+1}": q for i, q in enumerate(questions)}
    prompt = (
        f"Generate {num_questions} logic-based, reasoning challenge questions that test a reader's understanding of the following document. Each question should require the user to justify their answer. Respond as a numbered list.\n\nDocument:\n{document_text}\n\nQuestions:"
    )
    gemini = Gemini(api_key=GEMINI_API_KEY, id='gemini-1.5-flash-latest', temprature=0.1)
    response = gemini.generate(prompt)
    questions = [q.strip('- ').strip() for q in response.text.strip().split('\n') if q.strip()]
    return {f"q{i+1}": q for i, q in enumerate(questions[:num_questions])}

# Evaluate all user answers (dict) against the questions using Gemini and return feedback
def evaluate_challenge_answers(document_text: str, questions: Dict[str, str], user_answers: Dict[str, str]) -> Dict[str, str]:
    """
    Combine the 3 questions and user answers, ask Gemini to evaluate and provide feedback for each.
    Returns a dictionary with feedback for each question/answer pair and overall feedback.
    """
    if not GEMINI_API_KEY:
        # Fallback: heuristic feedback
        feedback = {}
        for k in questions:
            q = questions[k]
            a = user_answers.get(k, "")
            feedback[k] = f"Your answer: '{a}'. No LLM feedback (API key missing)."
        feedback['overall'] = "LLM feedback not available."
        return feedback
    # Build prompt
    qa_pairs = "\n".join([
        f"Q{i+1}: {questions[f'q{i+1}']}\nA{i+1}: {user_answers.get(f'q{i+1}', '')}" for i in range(3)
    ])
    prompt = (
        f"You are an expert evaluator. Evaluate the following 3 question-answer pairs based strictly on the provided document. For each, provide specific feedback and a score (0-1). Then give overall feedback. Respond in JSON as: {{'q1': feedback1, 'q2': feedback2, 'q3': feedback3, 'overall': overall_feedback}}.\n\nDocument:\n{document_text}\n\n{qa_pairs}\n\nFeedback:"
    )
    gemini = Gemini(api_key=GEMINI_API_KEY, id='gemini-1.5-flash-latest', temprature=0.1)
    response = gemini.generate(prompt)
    import json
    try:
        result = json.loads(response.text)
        for k in ['q1', 'q2', 'q3', 'overall']:
            if k not in result:
                result[k] = ''
        return result
    except Exception:
        # Fallback: return raw text
        return {'q1': '', 'q2': '', 'q3': '', 'overall': response.text.strip()}
