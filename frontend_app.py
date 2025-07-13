import streamlit as st
import requests
import json
import time
from typing import Dict, Any

# Configuration
API_BASE_URL = "http://localhost:8000"

def main():
    st.set_page_config(
        page_title="Document Analysis & Challenge System",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 1rem;
        padding: 0.5rem;
        background-color: #ecf0f1;
        border-radius: 5px;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
        color: #155724 !important;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
        color: #0c5460 !important;
    }
    .question-box {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
        color: #000000 !important;
    }
    .question-box strong {
        color: #000000 !important;
    }
    .question-box span {
        color: #000000 !important;
    }
    .feedback-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
        color: #856404 !important;
    }
    .evaluation-box {
        background-color: #ffffff;
        border: 2px solid #e9ecef;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #000000 !important;
    }
    .score-box {
        background-color: #f8f9fa;
        border: 2px solid #dee2e6;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
        color: #000000 !important;
    }
    .score-excellent {
        background-color: #d4edda !important;
        border-color: #c3e6cb !important;
        color: #155724 !important;
    }
    .score-good {
        background-color: #fff3cd !important;
        border-color: #ffeaa7 !important;
        color: #856404 !important;
    }
    .score-needs-improvement {
        background-color: #f8d7da !important;
        border-color: #f5c6cb !important;
        color: #721c24 !important;
    }
    .question-feedback {
        background-color: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
        color: #000000 !important;
    }
    .question-feedback h4 {
        color: #000000 !important;
        margin-bottom: 0.5rem;
    }
    .question-feedback p {
        color: #000000 !important;
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown('<h1 class="main-header">📚 Document Analysis & Challenge System</h1>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'session_id' not in st.session_state:
        st.session_state.session_id = None
    if 'document_uploaded' not in st.session_state:
        st.session_state.document_uploaded = False
    if 'summary' not in st.session_state:
        st.session_state.summary = None
    if 'questions' not in st.session_state:
        st.session_state.questions = None
    if 'interaction_mode' not in st.session_state:
        st.session_state.interaction_mode = None
    
    # Sidebar for navigation
    with st.sidebar:
        st.markdown("## 🧭 Navigation")
        
        if st.session_state.document_uploaded:
            st.success("✅ Document uploaded successfully!")
            st.info(f"Session ID: {st.session_state.session_id}")
            
            st.markdown("### 📋 Document Summary")
            if st.session_state.summary:
                st.text_area("Summary", st.session_state.summary, height=200, disabled=True)
            
            st.markdown("### 🔄 Reset Session")
            if st.button("🔄 Upload New Document"):
                reset_session()
        else:
            st.info("📤 Please upload a document to get started")
    
    # Main content area
    if not st.session_state.document_uploaded:
        upload_section()
    else:
        interaction_section()

def upload_section():
    """Handle document upload and initial processing"""
    st.markdown('<h2 class="section-header">📤 Upload Document</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose a document file",
            type=['pdf', 'txt'],
            help="Upload a PDF or TXT file to analyze"
        )
        
        if uploaded_file is not None:
            st.info(f"📄 File: {uploaded_file.name}")
            st.info(f"📏 Size: {uploaded_file.size} bytes")
    
    with col2:
        st.markdown("### 📋 Supported Formats")
        st.markdown("- PDF files")
        st.markdown("- Text files")
        st.markdown("- Max size: 10MB")
    
    if uploaded_file is not None:
        if st.button("🚀 Upload & Analyze", type="primary"):
            with st.spinner("Uploading and analyzing document..."):
                try:
                    # Upload file
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                    response = requests.post(f"{API_BASE_URL}/upload", files=files)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state.session_id = result["session_id"]
                        st.session_state.summary = result["summary"]
                        st.session_state.document_uploaded = True
                        
                        st.success("✅ Document uploaded and analyzed successfully!")
                        st.rerun()
                    else:
                        st.error(f"❌ Upload failed: {response.text}")
                        
                except Exception as e:
                    st.error(f"❌ Error during upload: {str(e)}")

def interaction_section():
    """Handle user interaction modes after document upload"""
    st.markdown('<h2 class="section-header">🎯 Choose Interaction Mode</h2>', unsafe_allow_html=True)
    
    # Mode selection
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("❓ Ask Me Anything", use_container_width=True, type="primary"):
            st.session_state.interaction_mode = "ask"
            st.rerun()
    
    with col2:
        if st.button("🎯 Take Challenge", use_container_width=True, type="primary"):
            st.session_state.interaction_mode = "challenge"
            st.rerun()
    
    # Handle selected mode
    if st.session_state.interaction_mode == "ask":
        ask_anything_mode()
    elif st.session_state.interaction_mode == "challenge":
        challenge_mode()

def ask_anything_mode():
    """Handle ask anything mode"""
    st.markdown('<h3 class="section-header">❓ Ask Me Anything</h3>', unsafe_allow_html=True)
    
    # Question input
    question = st.text_area(
        "Ask any question about the document:",
        placeholder="Enter your question here...",
        height=100
    )
    
    if st.button("🔍 Get Answer", type="primary"):
        if question.strip():
            with st.spinner("Analyzing your question..."):
                try:
                    response = requests.post(f"{API_BASE_URL}/ask", json={
                        "session_id": st.session_state.session_id,
                        "question": question
                    })
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Display answer
                        st.markdown("### 💡 Answer")
                        st.markdown(f'<div class="success-box">{result["answer"]}</div>', unsafe_allow_html=True)
                        
                        # Display reference
                        if result.get("reference_snippet"):
                            st.markdown("### 📖 Reference from Document")
                            st.markdown(f'<div class="info-box">{result["reference_snippet"]}</div>', unsafe_allow_html=True)
                    else:
                        st.error(f"❌ Error: {response.text}")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Please enter a question")
    
    # Back button
    if st.button("⬅️ Back to Mode Selection"):
        st.session_state.interaction_mode = None
        st.rerun()

def challenge_mode():
    """Handle challenge mode"""
    st.markdown('<h3 class="section-header">🎯 Document Challenge</h3>', unsafe_allow_html=True)
    
    # Generate questions if not already done
    if st.session_state.questions is None:
        with st.spinner("Generating challenge questions..."):
            try:
                response = requests.get(f"{API_BASE_URL}/challenge-dict/{st.session_state.session_id}")
                
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.questions = result["questions"]
                else:
                    st.error(f"❌ Error generating questions: {response.text}")
                    return
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                return
    
    # Display questions
    st.markdown("### 📝 Challenge Questions")
    st.markdown("Please answer the following questions based on the document:")
    
    # Create form for answers
    with st.form("challenge_form"):
        answers = {}
        
        for i, (q_key, question) in enumerate(st.session_state.questions.items(), 1):
            st.markdown(f'<div class="question-box"><strong style="color: #000000;">Question {i}:</strong> <span style="color: #000000;">{question}</span></div>', unsafe_allow_html=True)
            answer = st.text_area(
                f"Your answer to question {i}:",
                key=f"answer_{i}",
                height=120,
                placeholder="Enter your detailed answer here..."
            )
            answers[q_key] = answer
        
        submitted = st.form_submit_button("🎯 Submit Answers & Get Evaluation", type="primary")
        
        if submitted:
            # Check if all answers are provided
            empty_answers = [key for key, value in answers.items() if not value.strip()]
            
            if empty_answers:
                st.warning(f"⚠️ Please provide answers for all questions: {', '.join(empty_answers)}")
            else:
                with st.spinner("Evaluating your answers..."):
                    try:
                        response = requests.post(f"{API_BASE_URL}/challenge/submit", json={
                            "session_id": st.session_state.session_id,
                            "answers": answers
                        })
                        
                        if response.status_code == 200:
                            result = response.json()
                            display_evaluation_results(result["feedback"])
                        else:
                            st.error(f"❌ Error evaluating answers: {response.text}")
                            
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    # Back button
    if st.button("⬅️ Back to Mode Selection"):
        st.session_state.interaction_mode = None
        st.session_state.questions = None
        st.rerun()

def display_evaluation_results(feedback: Dict[str, Any]):
    """Display evaluation results in a structured format"""
    st.markdown("### 🎯 Evaluation Results")
    
    # Calculate overall score
    overall_score = 0
    if 'overall' in feedback and isinstance(feedback['overall'], dict):
        overall_score = feedback['overall'].get('score', 0)
    
    # Determine score class
    if overall_score >= 0.8:
        score_class = "score-excellent"
        score_label = "Excellent!"
    elif overall_score >= 0.6:
        score_class = "score-good"
        score_label = "Good!"
    else:
        score_class = "score-needs-improvement"
        score_label = "Needs improvement"
    
    # Overall score display
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div class="score-box {score_class}">
            <h3>Overall Score</h3>
            <h2>{overall_score:.1%}</h2>
            <p>{score_label}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Individual question feedback
    st.markdown("### 📊 Detailed Feedback")
    
    for i, (q_key, result) in enumerate(feedback.items(), 1):
        if q_key == 'overall':
            continue
            
        if isinstance(result, dict):
            score = result.get('score', 0)
            feedback_text = result.get('feedback', 'No feedback provided')
            
            # Determine question score class
            if score >= 0.7:
                question_class = "score-excellent"
            elif score >= 0.5:
                question_class = "score-good"
            else:
                question_class = "score-needs-improvement"
            
            st.markdown(f"""
            <div class="question-feedback {question_class}">
                <h4>Question {i} - Score: {score:.1%}</h4>
                <p><strong>Feedback:</strong> {feedback_text}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Fallback for string feedback
            st.markdown(f"""
            <div class="question-feedback">
                <h4>Question {i}</h4>
                <p>{result}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Overall feedback
    if 'overall' in feedback and isinstance(feedback['overall'], dict):
        overall_feedback = feedback['overall'].get('feedback', 'No overall feedback provided')
        st.markdown(f"""
        <div class="evaluation-box">
            <h4>Overall Assessment</h4>
            <p>{overall_feedback}</p>
        </div>
        """, unsafe_allow_html=True)

def reset_session():
    """Reset the session state"""
    st.session_state.session_id = None
    st.session_state.document_uploaded = False
    st.session_state.summary = None
    st.session_state.questions = None
    st.session_state.interaction_mode = None
    st.rerun()

if __name__ == "__main__":
    main() 