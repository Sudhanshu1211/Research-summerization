from pydantic import BaseModel
from typing import List, Optional

class UploadResponse(BaseModel):
    session_id: str
    summary: str

class AskRequest(BaseModel):
    session_id: str
    question: str

class AskResponse(BaseModel):
    answer: str
    reference_snippet: str

class ChallengeDictResponse(BaseModel):
    session_id: str
    questions: dict

class ChallengeAnswersRequest(BaseModel):
    session_id: str
    answers: dict

class ChallengeBatchFeedbackResponse(BaseModel):
    session_id: str
    feedback: dict

class ChallengeResponse(BaseModel):
    session_id: str
    questions: List[str]

class EvaluateRequest(BaseModel):
    session_id: str
    question: str
    user_answer: str

class EvaluateResponse(BaseModel):
    score: float
    justification: str
    reference_snippet: str

class SummaryResponse(BaseModel):
    session_id: str
    summary: str
