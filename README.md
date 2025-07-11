
````markdown
# 🧠 GenAI Document Assistant

An intelligent AI backend built with **FastAPI** that reads, understands, and reasons through uploaded PDF or TXT documents. Designed to:
- Comprehend content
- Answer free-form questions
- Generate logic-based challenges
- Justify every response with references from the document

---

## 📐 Project Structure

```bash
genai_backend/
├── main.py                     # FastAPI entry point
├── requirements.txt            # Project dependencies
├── Dockerfile                  # Containerization config
├── setup.py                    # Package metadata (optional)
├── README.md                   # Project documentation
├── params.yaml                 # Configurable model and pipeline parameters

├── config/
│   └── settings.py             # Global settings and API key config

├── data/
│   └── uploads/                # Uploaded documents go here
│       └── .gitkeep

├── .github/
│   └── workflows/
│       └── .gitkeep            # Placeholder for CI/CD workflows

├── api/
│   └── routes.py               # FastAPI route definitions (upload, ask, challenge)

├── models/
│   └── schemas.py              # Pydantic request/response models

├── research/
│   └── dev_trials.ipynb        # Prototyping and experimentation notebooks

├── src/
│   ├── __init__.py
│
│   ├── components/             # Core logic modules
│   │   ├── document_service.py     # PDF/TXT parsing and cleaning
│   │   ├── summarizer.py           # Document summarization logic
│   │   ├── question_answering.py   # QA via retrieval-based LLM (Ask Anything)
│   │   ├── question_generation.py  # Logic-based question generator
│   │   └── evaluation.py           # Answer evaluation + feedback logic
│
│   ├── pipeline/               # End-to-end orchestrators
│   │   ├── document_pipeline.py    # Upload → Parse → Chunk → Embed
│   │   └── interaction_pipeline.py # Manages Ask & Challenge user flow
│
│   ├── utils/                  # Common utility modules
│   │   ├── file_utils.py           # File reading, saving, and MIME handling
│   │   ├── chunk_utils.py          # Text splitting, cleaning, metadata tagging
│   │   └── llm_utils.py            # Wrapper for LLM interaction and prompt control
│
│   └── Agent/                  # LLM provider wrappers
│       ├── openai_agent.py         # OpenAI GPT API abstraction
│       └── gemini_agent.py         # Gemini API abstraction
````

---

## 🚀 Features

* ✅ Upload PDF/TXT files
* ✅ Auto-summary in ≤150 words
* ✅ Ask Anything — free-form Q\&A with justifications
* ✅ Challenge Me — generates and evaluates logical questions
* ✅ Uses OpenAI or Gemini LLMs
* ✅ Clean modular backend architecture

---

## 🛠 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/genai-document-assistant.git
cd genai-document-assistant
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> ✅ Use the minimal `requirements.txt` below to avoid bloat:

```txt
fastapi>=0.103.0
uvicorn>=0.23.2
python-dotenv>=1.0.0
pydantic>=2.3.0
python-multipart>=0.0.6
openai
google-generativeai>=0.3.0
PyPDF2>=3.0.0
unstructured>=0.5.0
```

### 4. Set API Keys

Create a `.env` file or configure `config/settings.py`:

```python
OPENAI_API_KEY = "your-openai-api-key"
GEMINI_API_KEY = "your-gemini-api-key"
DOC_UPLOAD_DIR = "./data/uploads/"
```

### 5. Run the API Server

```bash
uvicorn main:app --reload
```

Then open your browser at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📡 API Endpoints

| Route                     | Method | Description                           |
| ------------------------- | ------ | ------------------------------------- |
| `/upload`                 | POST   | Upload a document (PDF/TXT)           |
| `/summary/{session_id}`   | GET    | Retrieve the document summary         |
| `/ask`                    | POST   | Ask a contextual question             |
| `/challenge/{session_id}` | GET    | Get 3 logic-based questions           |
| `/evaluate`               | POST   | Evaluate answers against the document |

---

## 🧱 Component Breakdown

### 📁 `src/components/`

Handles document parsing, summarization, question answering, challenge generation, and evaluation logic.

### 📁 `src/pipeline/`

Coordinates multi-step workflows such as uploading, chunking, and inference.

### 📁 `src/Agent/`

Abstracts LLM providers like OpenAI and Gemini — easily switchable via config.

### 📁 `api/routes.py`

Contains all FastAPI endpoint routes.

### 📁 `models/schemas.py`

Holds Pydantic request and response models for type-safe API interaction.

---

## 🐳 Docker Support (Optional)

### Build the Docker image

```bash
docker build -t genai-backend .
```

### Run the container

```bash
docker run -p 8000:8000 genai-backend
```

---

## 🧪 Future Enhancements

* ⏳ LangChain memory/context support
* ⏳ Snippet highlighting for answers
* ⏳ MongoDB or vector DB for long-term memory
* ⏳ Role-based access control (user/admin)

---

## 👨‍💻 Author

Sudhanshu1211

---

## 📄 License

This project is licensed under the MIT License.



