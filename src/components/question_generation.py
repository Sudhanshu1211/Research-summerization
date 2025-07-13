from typing import List, Dict
from config.settings import GEMINI_API_KEY
from src.Agent.gemini_agent import Gemini
import random
import json
import re

def generate_logic_challenges_dict(document_text: str, num_questions: int = 3) -> Dict[str, str]:
    """
    Generate logic-based challenge questions using Gemini agent. Return as a dictionary.
    Questions should test understanding and require reasoning, not just factual recall.
    """
    if not GEMINI_API_KEY:
        # Fallback: generate simple questions
        sentences = [s.strip() for s in document_text.split('.') if len(s.split()) > 6]
        random.shuffle(sentences)
        questions = []
        for sent in sentences[:num_questions]:
            questions.append(f"Based on the document, what is the implication of: '{sent[:60]}...'? Justify your reasoning.")
        while len(questions) < num_questions:
            questions.append("Explain a key concept from the document and justify your reasoning.")
        return {f"q{i+1}": q for i, q in enumerate(questions)}
    
    prompt = f"""Generate {num_questions} challenging logic-based questions that test deep understanding of the following document. 
    
    Requirements:
    - Questions should require critical thinking and reasoning, not just factual recall
    - Questions should ask for analysis, implications, or connections between concepts
    - Each question should require justification of the answer
    - Questions should be clear and specific
    
    Document:
    {document_text}
    
    Generate exactly {num_questions} questions. Format as a simple list, one question per line."""
    
    try:
        gemini = Gemini(api_key=GEMINI_API_KEY, id='gemini-1.5-flash-latest', temprature=0.1)
        response = gemini.generate(prompt)
        
        # Parse the response to extract questions
        lines = response.text.strip().split('\n')
        questions = []
        
        for line in lines:
            # Remove numbering, bullets, and extra whitespace
            cleaned = re.sub(r'^[\d\.\-\*\)\s]+', '', line.strip())
            if cleaned and len(cleaned) > 10:  # Ensure it's a substantial question
                questions.append(cleaned)
        
        # Ensure we have exactly num_questions
        while len(questions) < num_questions:
            questions.append("Analyze a key concept from the document and explain its significance with proper justification.")
        
        return {f"q{i+1}": questions[i] for i in range(num_questions)}
        
    except Exception as e:
        # Fallback on error
        print(f"Error generating questions: {e}")
        return generate_logic_challenges_dict(document_text, num_questions)  # Recursive fallback

def evaluate_challenge_answers(document_text: str, questions: Dict[str, str], user_answers: Dict[str, str]) -> Dict[str, str]:
    """
    Evaluate user answers against the questions using Gemini and return detailed feedback.
    Returns a dictionary with feedback for each question/answer pair and overall feedback.
    """
    if not GEMINI_API_KEY:
        # Fallback: provide basic feedback
        feedback = {}
        for k in questions:
            q = questions[k]
            a = user_answers.get(k, "")
            if a.strip():
                feedback[k] = f"Your answer: '{a[:100]}...'. No LLM evaluation available (API key missing)."
            else:
                feedback[k] = "No answer provided. Please provide a detailed response."
        feedback['overall'] = "LLM evaluation not available. Please provide detailed answers for better feedback."
        return feedback
    
    # Build the evaluation prompt
    qa_pairs = []
    for i in range(len(questions)):
        q_key = f"q{i+1}"
        if q_key in questions:
            q = questions[q_key]
            a = user_answers.get(q_key, "")
            qa_pairs.append(f"Question {i+1}: {q}\nAnswer {i+1}: {a}\n")
    
    qa_text = "\n".join(qa_pairs)
    
    prompt = f"""You are an expert evaluator. Evaluate the following question-answer pairs based strictly on the provided document.

Document:
{document_text}

Question-Answer Pairs:
{qa_text}

For each answer, provide:
1. A score from 0.0 to 1.0 (where 1.0 is excellent)
2. Specific feedback on what was good and what could be improved
3. Whether the answer demonstrates understanding of the document

Respond in this exact JSON format:
{{
    "q1": {{
        "score": 0.8,
        "feedback": "Your analysis shows good understanding of the concept. However, you could strengthen your argument by..."
    }},
    "q2": {{
        "score": 0.6,
        "feedback": "Your answer touches on the right points but lacks depth..."
    }},
    "q3": {{
        "score": 0.9,
        "feedback": "Excellent analysis with strong reasoning and good use of evidence..."
    }},
    "overall": {{
        "score": 0.77,
        "feedback": "Overall, you demonstrate good understanding of the document. Your strongest area is... Your weakest area is..."
    }}
}}

Be specific, constructive, and fair in your evaluation."""
    
    try:
        gemini = Gemini(api_key=GEMINI_API_KEY, id='gemini-1.5-flash-latest', temprature=0.1)
        response = gemini.generate(prompt)
        
        # Try to parse JSON response
        try:
            # Clean the response text to extract JSON
            text = response.text.strip()
            
            # Find JSON content (remove any markdown formatting)
            json_start = text.find('{')
            json_end = text.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_text = text[json_start:json_end]
                result = json.loads(json_text)
                
                # Ensure all expected keys exist
                expected_keys = [f'q{i+1}' for i in range(len(questions))] + ['overall']
                for key in expected_keys:
                    if key not in result:
                        result[key] = {"score": 0.0, "feedback": "No evaluation provided."}
                
                return result
            else:
                raise ValueError("No JSON found in response")
                
        except (json.JSONDecodeError, ValueError) as e:
            # Fallback: return structured feedback with raw response
            feedback = {}
            for i in range(len(questions)):
                q_key = f"q{i+1}"
                feedback[q_key] = {
                    "score": 0.5,
                    "feedback": f"Evaluation error. Raw response: {response.text[:200]}..."
                }
            feedback['overall'] = {
                "score": 0.5,
                "feedback": "Evaluation completed with errors. Please review your answers."
            }
            return feedback
            
    except Exception as e:
        # Final fallback
        print(f"Error in evaluation: {e}")
        feedback = {}
        for i in range(len(questions)):
            q_key = f"q{i+1}"
            a = user_answers.get(q_key, "")
            feedback[q_key] = {
                "score": 0.0,
                "feedback": f"Evaluation failed. Your answer: '{a[:100]}...'"
            }
        feedback['overall'] = {
            "score": 0.0,
            "feedback": "Evaluation system error. Please try again."
        }
        return feedback


def generate_logic_challenges(document_text: str, num_questions: int = 3) -> List[str]:
    """
    Generate logic-based challenge questions and return as a list.
    This is a wrapper function for compatibility with existing routes.
    """
    questions_dict = generate_logic_challenges_dict(document_text, num_questions)
    return [questions_dict[f"q{i+1}"] for i in range(num_questions)]
