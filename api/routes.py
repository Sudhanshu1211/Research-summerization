from fastapi import APIRouter, UploadFile, File, HTTPException
from models.schemas import UploadResponse, AskRequest, AskResponse, ChallengeResponse, EvaluateRequest, EvaluateResponse, SummaryResponse
from src.components.document_service import save_and_parse_document, get_summary, get_document_text
from src.components.question_answering import answer_question
from src.components.question_generation import generate_logic_challenges_dict, evaluate_challenge_answers
from src.components.evaluation import evaluate_answer
from src.utils.session_store import session_store

router = APIRouter()

# Batch challenge question/answer workflow
from models.schemas import ChallengeDictResponse, ChallengeAnswersRequest, ChallengeBatchFeedbackResponse

@router.get('/challenge-dict/{session_id}', response_model=ChallengeDictResponse)
def get_challenge_dict(session_id: str):
    if not session_store.session_exists(session_id):
        raise HTTPException(status_code=404, detail='Session not found')
    doc_text = get_document_text(session_id)
    questions = generate_logic_challenges_dict(doc_text)
    session_store.update_session(session_id, {'challenges_dict': questions})
    return ChallengeDictResponse(session_id=session_id, questions=questions)

@router.post('/challenge/submit', response_model=ChallengeAnswersRequest)
def submit_challenge_answers(request: ChallengeAnswersRequest):
    if not session_store.session_exists(request.session_id):
        raise HTTPException(status_code=404, detail='Session not found')
    session_store.update_session(request.session_id, {'challenge_answers': request.answers})
    return request

@router.post('/challenge/evaluate_batch', response_model=ChallengeBatchFeedbackResponse)
def evaluate_challenge_batch(request: ChallengeAnswersRequest):
    if not session_store.session_exists(request.session_id):
        raise HTTPException(status_code=404, detail='Session not found')
    doc_text = get_document_text(request.session_id)
    questions = session_store.get_session(request.session_id).get('challenges_dict', {})
    answers = session_store.get_session(request.session_id).get('challenge_answers', {})
    # If answers are provided in request, use them (for stateless clients)
    if request.answers:
        answers = request.answers
    feedback = evaluate_challenge_answers(doc_text, questions, answers)
    return ChallengeBatchFeedbackResponse(session_id=request.session_id, feedback=feedback)

@router.post('/upload', response_model=UploadResponse)
def upload_document(file: UploadFile = File(...)):
    if not (file.filename.endswith('.pdf') or file.filename.endswith('.txt')):
        raise HTTPException(status_code=400, detail='Only PDF and TXT files are supported.')
    file_bytes = file.file.read()
    session_id, summary = save_and_parse_document(file_bytes, file.filename)
    return UploadResponse(session_id=session_id, summary=summary)

@router.get('/summary/{session_id}', response_model=SummaryResponse)
def get_document_summary(session_id: str):
    if not session_store.session_exists(session_id):
        raise HTTPException(status_code=404, detail='Session not found')
    summary = get_summary(session_id)
    return SummaryResponse(session_id=session_id, summary=summary)

@router.post('/ask', response_model=AskResponse)
def ask_anything(request: AskRequest):
    if not session_store.session_exists(request.session_id):
        raise HTTPException(status_code=404, detail='Session not found')
    doc_text = get_document_text(request.session_id)
    result = answer_question(request.question, doc_text)
    return AskResponse(**result)

@router.get('/challenge/{session_id}', response_model=ChallengeResponse)
def get_challenge(session_id: str):
    if not session_store.session_exists(session_id):
        raise HTTPException(status_code=404, detail='Session not found')
    doc_text = get_document_text(session_id)
    questions = generate_logic_challenges(doc_text)
    session_store.update_session(session_id, {'challenges': questions})
    return ChallengeResponse(session_id=session_id, questions=questions)

@router.post('/evaluate', response_model=EvaluateResponse)
def evaluate_user_answer(request: EvaluateRequest):
    if not session_store.session_exists(request.session_id):
        raise HTTPException(status_code=404, detail='Session not found')
    doc_text = get_document_text(request.session_id)
    result = evaluate_answer(request.question, request.user_answer, doc_text)
    return EvaluateResponse(**result)
