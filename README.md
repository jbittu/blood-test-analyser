#  Blood Test Report Analyser (AI-Based)

An AI-powered humorous simulation system that analyzes blood test reports with exaggerated, fictional medical and lifestyle recommendations using CrewAI agents.

> ⚠️ This project is intentionally exaggerated, dramatized, and satirical—**not meant for real medical use**.

---

##  Features

- 🤖 Multi-agent system using `CrewAI` with agents:
  - Doctor (diagnoses everything dramatically)
  - Nutritionist (pushes weird superfoods and supplements)
  - Exercise Coach (forces intense CrossFit routines)
  - Verifier (blindly approves all documents as blood reports)
- 📄 PDF blood test report ingestion
- 🧠 Custom LLM integration using Google Gemini (`gemini-2.0-flash`)
- 🧰 Tools for nutrition, exercise, internet search, and blood report parsing
- 📦 REST API using FastAPI
- 📤 Saves analysis results to output directory

---

##  Tech Stack

| Component         | Tool/Library                     |
|------------------|----------------------------------|
| Backend API      | FastAPI                          |
| Agents Framework | CrewAI                           |
| LLM              | Google Gemini (`gemini-2.0-flash`) via LangChain |
| PDF Parsing      | `langchain_community.PyPDFLoader` |
| Tools Integration| Custom classes + CrewAI tools    |
| Async Handling   | Python asyncio                   |
| Deployment       | Uvicorn                          |

---

##  Folder Structure

```
blood-test-analyser/
├── agents.py # CrewAI agents (Doctor, Verifier, etc.)
├── main.py # FastAPI application entrypoint
├── task.py # Task definitions assigned to agents
├── tools.py # Custom tool classes for blood, nutrition, exercise
├── data/ # Uploaded blood report PDFs
├── output/ # JSON outputs of analyses
├── requirements.txt # Dependencies
└── .env # API keys and CrewAI settings

```

## ⚙️ Setup Instructions

### 1. Clone the Repo

```
git clone https://github.com/jbittu/blood-test-analyser.git
cd blood-test-analyser
```
### 2. Create and Activate Virtual Environment

```
python -m venv venv
source venv\Scripts\activate
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```
### 4. Setup .env
Create a .env file in the root directory:

```
GOOGLE_API_KEY=your_google_api_key_here
CREWAI_LLM_BACKEND=langchain
```
### 5. Run Server
```
uvicorn main:app --reload
```
API will be available at: http://127.0.0.1:8000

###  API Usage
Endpoint: /analyze
POST blood test report and query:

```
curl -X 'POST' \
  'http://127.0.0.1:8000/analyze' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@blood_test_report.pdf;type=application/pdf' \
  -F 'query=Summarise my Blood Test Report'
  ```
### Response
```json

{
  "status": "success",
  "query": "Summarise my Blood Test Report",
  "analysis": " Doctor recommends... 🧘 Nutritionist says... ",
  "file_processed": "blood_test_report.pdf",
  "output_saved_to": "output/analysis_result_<uuid>.json"
}
```

##  Design Decisions
LLM Backend: We use LangChain with ChatGoogleGenerativeAI (Gemini) for full control and compatibility.

CrewAI: Chosen for ease of agent/task orchestration and tool integration.

Tasks are intentionally funny and illogical to showcase prompt design + multi-agent dynamics.

Tools are modular (ReadBloodReportTool, NutritionTool, ExerciseTool) for extensibility.

## Disclaimer
This app is not a medical tool. It's a demo project meant for learning AI agent systems with humor and creativity. Never use it for real health decisions.

## 📄 License
MIT License - feel free to use and modify.

