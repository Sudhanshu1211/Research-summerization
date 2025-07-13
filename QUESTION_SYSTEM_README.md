# Question Generation and Evaluation System

This system provides a complete workflow for generating logical questions from documents and evaluating user answers with AI-powered feedback.

## Features

- **Question Generation**: Generate 3 logical, reasoning-based questions from any document
- **Answer Collection**: Collect user answers through API endpoints
- **AI Evaluation**: Evaluate answers using Gemini AI with detailed feedback and scores
- **Fallback Support**: Works without API key using basic fallback functionality

## API Endpoints

### 1. Generate Questions
```
GET /challenge-dict/{session_id}
```
Returns a dictionary of 3 logical questions based on the uploaded document.

**Response:**
```json
{
  "session_id": "abc123",
  "questions": {
    "q1": "Analyze the implications of AI in healthcare...",
    "q2": "Explain the relationship between machine learning and deep learning...",
    "q3": "Discuss the ethical considerations of AI implementation..."
  }
}
```

### 2. Submit Answers
```
POST /challenge/submit
```
Submit user answers for evaluation.

**Request:**
```json
{
  "session_id": "abc123",
  "answers": {
    "q1": "AI in healthcare can improve diagnosis accuracy...",
    "q2": "Deep learning is a subset of machine learning...",
    "q3": "Ethical considerations include privacy and bias..."
  }
}
```

### 3. Evaluate Answers
```
POST /challenge/evaluate_batch
```
Get detailed feedback and scores for submitted answers.

**Response:**
```json
{
  "session_id": "abc123",
  "feedback": {
    "q1": {
      "score": 0.85,
      "feedback": "Excellent analysis of AI implications in healthcare..."
    },
    "q2": {
      "score": 0.72,
      "feedback": "Good understanding of the relationship..."
    },
    "q3": {
      "score": 0.68,
      "feedback": "You touched on important points but could elaborate..."
    },
    "overall": {
      "score": 0.75,
      "feedback": "Overall, you demonstrate good understanding..."
    }
  }
}
```

## Complete Workflow Example

### Step 1: Upload Document
```bash
curl -X POST "http://localhost:8000/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"
```

### Step 2: Generate Questions
```bash
curl "http://localhost:8000/challenge-dict/{session_id}"
```

### Step 3: Submit Answers
```bash
curl -X POST "http://localhost:8000/challenge/submit" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "abc123",
    "answers": {
      "q1": "Your answer to question 1...",
      "q2": "Your answer to question 2...",
      "q3": "Your answer to question 3..."
    }
  }'
```

### Step 4: Get Evaluation
```bash
curl -X POST "http://localhost:8000/challenge/evaluate_batch" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "abc123",
    "answers": {
      "q1": "Your answer to question 1...",
      "q2": "Your answer to question 2...",
      "q3": "Your answer to question 3..."
    }
  }'
```

## Configuration

### API Key Setup
To use the full AI-powered features, set your Gemini API key:

1. Create a `.env` file in the project root:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```

2. Or set the environment variable:
```bash
export GOOGLE_API_KEY=your_gemini_api_key_here
```

### Without API Key
The system works without an API key using fallback functionality:
- Questions are generated using simple heuristics
- Basic feedback is provided without AI evaluation
- All core functionality remains available

## Question Types

The system generates questions that require:
- **Critical Thinking**: Analysis and reasoning beyond factual recall
- **Justification**: Users must explain their reasoning
- **Deep Understanding**: Questions test comprehension of concepts and relationships
- **Application**: Questions ask for implications and real-world connections

## Evaluation Criteria

When using AI evaluation, answers are scored on:
- **Accuracy**: Correctness of information
- **Completeness**: Coverage of the question requirements
- **Reasoning**: Quality of logical thinking
- **Evidence**: Use of document content to support answers
- **Clarity**: Clear and well-structured responses

## Testing

Run the test script to verify the system:
```bash
# Test with fallback (no API key)
python test_question_system_no_api.py

# Test with API key (requires valid key)
python test_question_system.py
```

## Error Handling

The system includes robust error handling:
- **API Failures**: Graceful fallback to basic functionality
- **Invalid Input**: Clear error messages for malformed requests
- **Missing Data**: Appropriate defaults and fallbacks
- **JSON Parsing**: Handles malformed AI responses

## File Structure

```
src/components/question_generation.py  # Core question generation and evaluation
api/routes.py                          # API endpoints
models/schemas.py                      # Request/response models
test_question_system.py                # Full system test
test_question_system_no_api.py         # Fallback test
```

## Dependencies

- `google-generativeai`: For AI-powered question generation and evaluation
- `fastapi`: Web framework for API endpoints
- `pydantic`: Data validation and serialization
- `python-dotenv`: Environment variable management

## Troubleshooting

### Common Issues

1. **API Key Not Working**
   - Verify the key is valid and has proper permissions
   - Check environment variable name (`GOOGLE_API_KEY`)
   - Ensure the key is for Gemini API

2. **Questions Not Generating**
   - Check if document text is being extracted properly
   - Verify the document format is supported
   - Check for API rate limits

3. **Evaluation Errors**
   - Ensure answers are provided for all questions
   - Check that session exists and contains questions
   - Verify document text is available for context

### Debug Mode

Enable debug logging by setting:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Future Enhancements

- Support for different question types (multiple choice, true/false)
- Customizable evaluation criteria
- Question difficulty levels
- Batch processing for multiple documents
- Export evaluation results to various formats 