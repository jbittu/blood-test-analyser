from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import asyncio
import json
from crewai import Crew, Process
from agents import doctor, verifier, nutritionist, exercise_specialist
from task import help_patients, nutrition_analysis, exercise_planning, verification
from tools import ReadBloodReportTool

app = FastAPI(title="Blood Test Report Analyser")

# Create shared tool instance
read_tool = ReadBloodReportTool()


# Async wrapper for crew execution
async def run_crew_async(query: str, file_path: str = "data/sample.pdf"):
    def run_sync():
        crew = Crew(
            agents=[doctor, verifier, nutritionist, exercise_specialist],
            tasks=[verification, help_patients, nutrition_analysis, exercise_planning],
            process=Process.sequential,
        )
        return crew.kickoff(inputs={"query": query, "file_path": file_path})
    
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, run_sync)


@app.get("/")
async def root():
    return {"message": "Blood Test Report Analyser API is running"}


@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(...),
    query: str = Form(default="Summarise my Blood Test Report")
):
    """Analyze blood test report and provide health recommendations"""
    file_id = str(uuid.uuid4())
    data_file_path = f"data/blood_test_report_{file_id}.pdf"
    output_filename = f"analysis_result_{file_id}.json"
    output_file_path = os.path.join("output", output_filename)

    try:
        os.makedirs("data", exist_ok=True)
        os.makedirs("output", exist_ok=True)

        # Save file
        with open(data_file_path, "wb") as f:
            f.write(await file.read())

        query = query.strip() or "Summarise my Blood Test Report"

        # Kickoff analysis
        analysis_result = await run_crew_async(query=query, file_path=data_file_path)

        # Save to output file
        output_data = {
            "query": query,
            "file_processed": file.filename,
            "analysis_raw_output": str(analysis_result)
        }
        with open(output_file_path, "w", encoding="utf-8") as f_out:
            json.dump(output_data, f_out, indent=2)

        return {
            "status": "success",
            "query": query,
            "analysis": str(analysis_result),
            "file_processed": file.filename,
            "output_saved_to": output_file_path
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing report: {str(e)}")

    finally:
        if os.path.exists(data_file_path):
            try:
                os.remove(data_file_path)
            except Exception:
                pass
