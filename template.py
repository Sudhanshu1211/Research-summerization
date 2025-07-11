import os
from pathlib import Path
import logging

# Setup logging format
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

# Define your project name
project_name = "genai-document-assistant"

# List of all required files and directories
list_of_files = [
    # CI/CD
    ".github/workflows/.gitkeep",

    # Core project files
    "main.py",
    "requirements.txt",
    "Dockerfile",
    "setup.py",
    "README.md",
    "params.yaml",

    # Config
    "config/settings.py",

    # Data storage
    "data/uploads/.gitkeep",

    # API
    "api/routes.py",  # ✅ Combined all routes here

    # Pydantic models
    "models/schemas.py",

    # Research notebooks
    "research/dev_trials.ipynb",

    # src package
    "src/_init_.py",

    # Components
    "src/components/_init_.py",
    "src/components/document_service.py",
    "src/components/summarizer.py",
    "src/components/question_answering.py",
    "src/components/question_generation.py",
    "src/components/evaluation.py",

    # Pipeline
    "src/pipeline/_init_.py",
    "src/pipeline/document_pipeline.py",
    "src/pipeline/interaction_pipeline.py",

    # Utilities
    "src/utils/_init_.py",
    "src/utils/file_utils.py",
    "src/utils/chunk_utils.py",
    "src/utils/llm_utils.py",

    # LLM Agents
    "src/Agent/_init_.py",
    "src/Agent/openai_agent.py",
    "src/Agent/gemini_agent.py",
]

# Create each file and its directory if not already present
for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for file: {filename}")

    if not filepath.exists() or filepath.stat().st_size == 0:
        with open(filepath, "w") as f:
            pass  # create an empty file
        logging.info(f"Created empty file: {filepath}")
    else:
        logging.info(f"File already exists: {filepath}")