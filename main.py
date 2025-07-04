# main.py
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import asyncio
import json
from crewai import Crew, Process
# Import the new consolidator agent
from agents import doctor, verifier, nutritionist, exercise_specialist
# Import the new consolidate_results task
from task import help_patients, nutrition_analysis, exercise_planning, verification
from tools import ReadBloodReportTool

app = FastAPI(title="Blood Test Report Analyser")

# Create shared tool instance (if ReadBloodReportTool is used by multiple agents directly)
# Note: For tasks, tools are typically passed to the Task constructor, not here.
# read_tool = ReadBloodReportTool() # This line might not be strictly necessary here if tools are passed to tasks/agents.

# Async wrapper for crew execution
async def run_crew_async(query: str, file_path: str = "data/sample.pdf"):
    def run_sync():
        crew = Crew(
            agents=[doctor, verifier, nutritionist, exercise_specialist], # Add the new agent
            tasks=[verification, help_patients, nutrition_analysis, exercise_planning], # Add the new consolidation task last
            process=Process.sequential,
            verbose=True # Keep verbose for debugging if needed
        )
        # Pass file_path to ALL tasks that might need it
        inputs = {"query": query, "file_path": file_path}
        return crew.kickoff(inputs=inputs)
    
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
    """Analyze blood test report and provide health recommendations, structured by specialist."""
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
        # The result here should now be the JSON string from consolidate_results
        analysis_raw_string = await run_crew_async(query=query, file_path=data_file_path)

        # Attempt to parse the analysis result as JSON
        try:
            analysis_structured = json.loads(analysis_raw_string)
        except json.JSONDecodeError:
            # If the LLM didn't produce perfect JSON, handle it gracefully
            analysis_structured = {"error": "Failed to parse analysis as JSON", "raw_output": analysis_raw_string}

        # Save to output file
        output_data = {
            "query": query,
            "file_processed": file.filename,
            "analysis": analysis_structured # Save the structured data
        }
        with open(output_file_path, "w", encoding="utf-8") as f_out:
            json.dump(output_data, f_out, indent=2)

        return {
            "status": "success",
            "query": query,
            "analysis": analysis_structured, # Return the structured data
            "file_processed": file.filename,
            "output_saved_to": output_file_path
        }

    except Exception as e:
        import traceback
        traceback.print_exc() # For debugging
        raise HTTPException(status_code=500, detail=f"Error processing report: {str(e)}")

    finally:
        if os.path.exists(data_file_path):
            try:
                os.remove(data_file_path)
            except Exception:
                pass # Ignore cleanup errors