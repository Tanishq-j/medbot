# MedBot — Multi-Agent Medical Assistant 🩺

**MedBot** is an educational, multi-agent clinical guidance and medical reference assistant designed for undergraduate GenAI & ML DevOps coursework. It leverages **FastAPI**, **Agno framework** multi-agent teams, and the **Google Gemini / Groq API** (running fast models such as Gemini 3.8 Flash or open-weight models) with a modern HTML/CSS/JavaScript interface and a Streamlit dashboard.

---

## 🏛️ Multi-Agent Architecture

MedBot coordinates exactly **three collaborating agents** via Agno's `Team` framework (`TeamMode.coordinate`):

```
                       +-------------------------+
                       |  User Clinical Inquiry  |
                       +------------+------------+
                                    |
                                    v
            +-----------------------------------------------+
            |               Agno Medical Team               |
            |                                               |
            |  1. Medical Query Analyzer                    |
            |     - Classifies clinical specialty           |
            |     - Extracts patient vitals & chronology    |
            |     - Formulates targeted medical issues      |
            |                        |                      |
            |                        v                      |
            |  2. Medical Research Agent                    |
            |     - Invokes `search_medical_library` tool   |
            |     - Grounded in clinical guidelines & ICMR  |
            |     - Cites dosage limits, metrics & protocols|
            |                        |                      |
            |                        v                      |
            |  3. Medical Answer Reviewer                   |
            |     - Cross-examines all clinical claims      |
            |     - Strips ungrounded/unsafe assertions     |
            |     - Synthesizes final structured guidance   |
            +-----------------------+-----------------------+
                                    |
                                    v
                     +------------------------------+
                     | Final Reviewed Advisory Memo |
                     | + Consulted Guidelines       |
                     | + Mandatory Medical Alert    |
                     +------------------------------+
```

1. **Medical Query Analyzer**: Breaks down user inquiries into distinct clinical specialties (e.g., Cardiology, Endocrinology, Pulmonology, Pharmacology, Emergency Medicine) and frames precise research questions.
2. **Medical Research Agent**: Calls the `search_medical_library` tool to investigate clinical practice standards, target metrics, dosage thresholds, and contraindications to ground the findings.
3. **Medical Answer Reviewer**: Audits claims against available evidence, eliminates speculative assertions, ensures safe clinical phrasing, highlights emergency red flags, and formats the verified guidance.

---

## 📁 Project Structure

```
MedBot/
├── .dockerignore            # Excludes caches, venv, and secrets from container image
├── Dockerfile               # Production container definition for FastAPI & Streamlit
├── .env.example             # Template for environment configuration
├── .gitignore               # Git ignore rules (prevents committing secrets)
├── requirements.txt         # Python project dependencies
├── README.md                # Project documentation and student guide
├── DOCKER_LAB_GUIDE.md      # Containerization lab manual
├── streamlit_app.py         # Streamlit web UI with image/prescription upload
├── app/
│   ├── __init__.py
│   ├── config.py            # Environment variable loading & secret sanitization
│   ├── main.py              # FastAPI application (GET /, POST /ask, GET /health)
│   ├── schemas.py           # Pydantic models for request & response validation
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── medical_team.py  # Agno Team definition and multi-agent coordination
│   │   ├── legal_team.py    # Backward compatibility re-export
│   │   └── tools.py         # Clinical reference search tool for Research Agent
│   ├── data/
│   │   ├── __init__.py
│   │   └── sample_documents.py # Grounding clinical guidelines (Cardio, Diabetes, Respiratory, Pharma, Emergency)
│   └── static/
│       ├── index.html       # Clean single-page user interface
│       ├── style.css        # Responsive styling & layout
│       └── app.js           # Frontend client logic & pipeline animation
└── tests/
    ├── __init__.py
    ├── test_health.py       # Tests for /health and / endpoints
    ├── test_validation.py   # Tests for input validation and error handling
    └── test_agents.py       # Tests for Agno medical agents, Team, and search tool
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10, 3.11, 3.12, 3.13, or 3.14
- A free Google Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey) OR a free Groq API key from [Groq Console](https://console.groq.com/keys)

### 2. Setup Virtual Environment

On macOS / Linux:
```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

On Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Open `.env` in any text editor and paste your API key:
```ini
MODEL_PROVIDER=google
GEMINI_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini-3.8-flash

GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-20b

HOST=127.0.0.1
PORT=8000
REQUEST_TIMEOUT=90
```

---

## 💻 Running the Application

### Option A: Streamlit Frontend (Recommended UI)
Run the clean, dark-themed Streamlit web interface with prescription/report image upload:
```bash
streamlit run streamlit_app.py
```
Open your browser at **[http://localhost:8501](http://localhost:8501)**.

### Option B: FastAPI Backend & API Endpoints
Run the FastAPI application:
```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
- **Web UI & Redirect:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Interactive API Docs (Swagger):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Health Check Endpoint:** [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

---

## 🐳 Docker Deployment

Build and run using the optimized Docker setup:

```bash
# 1. Build the Docker container image
docker build -t medbot:latest .

# 2. Run the FastAPI application container
docker run -d --name medbot-app -p 8000:8000 --env-file .env medbot:latest

# Or run the Streamlit dashboard container
docker run -d --name medbot-streamlit -p 8501:8501 --env-file .env medbot:latest streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0
```

---

## 🧪 Running Automated Tests

Run the test suite using `pytest`:
```bash
pytest -v
```

All automated tests verify:
- Health endpoint status and medical agent registration
- Input validation (empty, whitespace, or short questions)
- Graceful 503 error handling when API key is not configured
- Agno Team creation, member roles, and tool attachments
- Clinical reference library search accuracy and source tracking

---

## 🔌 API Endpoints

### 1. `GET /`
Serves the responsive single-page web application.

### 2. `GET /health`
Returns system health, active model, and agent registration status without leaking secrets:
```json
{
  "status": "healthy",
  "app_name": "MedBot — Multi-Agent Medical Assistant",
  "groq_configured": true,
  "model": "Google (gemini-3.8-flash)",
  "agents": [
    "Medical Query Analyzer",
    "Medical Research Agent",
    "Medical Answer Reviewer"
  ]
}
```

### 3. `POST /ask`
Submits a query to the multi-agent team.

**Request Body:**
```json
{
  "question": "What are the recommended first-line lifestyle modifications and blood pressure targets for Stage 1 Hypertension?"
}
```

**Response Body:**
```json
{
  "status": "success",
  "question": "What are the recommended first-line lifestyle modifications and blood pressure targets for Stage 1 Hypertension?",
  "answer": "### Clinical Domain & Assessment Summary\n...",
  "sources": [
    "Cardiovascular Health & Hypertension Clinical Guidelines"
  ],
  "disclaimer": "Disclaimer: MedBot provides educational and informational medical guidance based on established clinical guidelines..."
}
```

---

## 🎓 Note for Students: Assignment Scope

This starter project contains the functional application layer. **As part of your GenAI & ML DevOps assignment, you will independently implement:**
1. **Containerization:** Create an optimized `Dockerfile` for the FastAPI/Streamlit service.
2. **Local Multi-Container Orchestration:** Build a `docker-compose.yml` (or `compose.yaml`) with volume mounts, environment isolation, and healthchecks.
3. **Cloud-Native Deployment:** Author Kubernetes manifests (Deployments, Services, ConfigMaps, Secrets, Ingress, and Resource Limits) or Helm charts.
4. **CI/CD Pipeline:** Configure automated testing and container image building workflows.

---

## 🩺 Medical Disclaimer

*MedBot is built exclusively for educational and demonstrative purposes. It provides generalized informational summaries and does not constitute medical diagnosis, treatment, prescription, or a physician-patient relationship. Always consult a licensed healthcare professional for medical concerns or emergency services for acute medical situations.*
