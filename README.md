# 🧪 Blood Test Report Analyser (AI-Based)

An AI-powered **humorous simulation system** that analyzes blood test reports with exaggerated, fictional medical and lifestyle recommendations using **CrewAI agents** + **FastAPI backend** + **Streamlit frontend**.

> ⚠️ **Disclaimer**: This project is intentionally exaggerated, dramatized, and satirical — **not meant for real medical use**.

---

## ✨ Features

- 🤖 **Multi-agent system** using `CrewAI`:
  - 🩺 **Doctor** → diagnoses everything dramatically
  - 🥦 **Nutritionist** → pushes weird superfoods & supplements
  - 🏋️ **Exercise Coach** → forces intense CrossFit routines
  - ✅ **Verifier** → blindly approves all documents as blood reports
- 📄 **PDF ingestion** (blood test reports)
- 🧠 **LLM integration** using Google Gemini (`gemini-2.0-flash`)
- 🧰 Tools for **nutrition, exercise, internet search, blood parsing**
- 📦 **REST API** using FastAPI
- 🖥️ **Frontend UI** with Streamlit
- 📤 Saves analysis results to `output/` directory

---

## 🛠 Tech Stack

| Component         | Tool/Library                     |
|-------------------|----------------------------------|
| Backend API       | FastAPI                          |
| Frontend UI       | Streamlit                        |
| Agents Framework  | CrewAI                           |
| LLM               | Google Gemini (`gemini-2.0-flash`) |
| PDF Parsing       | `langchain_community.PyPDFLoader` |
| Tools Integration | Custom CrewAI tools              |
| Async Handling    | Python asyncio                   |
| Deployment        | Uvicorn                          |


## 📂 Folder Structure

blood-test-analyser/
├── agents.py        # CrewAI agents
├── main.py          # FastAPI application entrypoint
├── task.py          # Task definitions assigned to agents
├── tools.py         # Custom tool classes for blood, nutrition, exercise
├── data/            # Uploaded blood report PDFs
├── output/          # JSON outputs of analyses
├── frontend/
│   └── app.py       # Streamlit frontend
├── requirements.txt # Dependencies
├── .env             # API keys and config

---

## ⚙️ Setup Instructions

### 1. Clone the Repo
git clone https://github.com/jbittu/blood-test-analyser.git
cd blood-test-analyser

### 2. Create and Activate Virtual Environment
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Setup Environment Variables
Create a `.env` file in the root directory:
GOOGLE_API_KEY=your_google_api_key_here
CREWAI_LLM_BACKEND=langchain


## 🚀 Running the Project

### 1. Start Backend (FastAPI)
uvicorn main:app --reload
# Backend runs at: http://127.0.0.1:8000

### 2. Start Frontend (Streamlit)
# From project root:
streamlit run frontend/app.py
# Frontend runs at: http://localhost:8501

---

## 🔗 API Usage

### Endpoint
POST /analyze

### Example cURL
curl -X 'POST' \
  'http://127.0.0.1:8000/analyze' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@blood_test_report.pdf;type=application/pdf' \
  -F 'query=Summarise my Blood Test Report'

### Example Response
{
  "status": "success",
  "query": "Summarise my Blood Test Report",
  "analysis": " Doctor recommends... 🧘 Nutritionist says... ",
  "file_processed": "blood_test_report.pdf",
  "output_saved_to": "output/analysis_result_<uuid>.json"
}


## 🧩 Design Decisions

- **LLM Backend**: Uses LangChain with Gemini for compatibility.  
- **CrewAI**: Chosen for agent orchestration & tool integration.  
- **Agents**: Intentionally funny & illogical → demonstrates multi-agent coordination.  
- **Tools**: Modular (ReadBloodReportTool, NutritionTool, ExerciseTool) → easily extensible.  

---

## ⚠️ Disclaimer
This app is **not a medical tool**.  
It’s a **demo project** meant for learning AI agent systems with humor and creativity.  
👉 **Never use it for real health decisions.**

---

## 📄 License
MIT License – feel free to use, share, and modify.
