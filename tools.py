# tools.py

import os
import re
import json
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from crewai_tools import SerperDevTool
from crewai.tools.base_tool import BaseTool

load_dotenv()

# -----------------------------------------------
# Search Tool using Serper (no wrapping needed)
# -----------------------------------------------
search_tool = SerperDevTool()


# -----------------------------------------------
# Blood Report Reader Tool
# -----------------------------------------------
class ReadBloodReportTool(BaseTool):
    name: str = "read_blood_report"
    description: str = "Reads and returns the content of a blood test PDF report."

    def _run(self, path='data/sample.pdf') -> str:
        docs = PyPDFLoader(file_path=path).load()
        full_report = ""
        for data in docs:
            content = data.page_content
            while "\n\n" in content:
                content = content.replace("\n\n", "\n")
            full_report += content + "\n"
        return full_report


# -----------------------------------------------
# Nutrition Analysis Tool
# -----------------------------------------------
class NutritionTool(BaseTool):
    name: str = "extract_nutrition_data"
    description: str = "Extracts nutrition-related values from a blood test report."

    def _run(self, full_report_text: str) -> str:
        data = {
            "glucose": "N/A",
            "cholesterol_total": "N/A",
            "hba1c": "N/A",
            "vitamin_d": "N/A",
            "abnormalities": []
        }

        lines = full_report_text.split('\n')

        for line in lines:
            line = line.strip()

            if "Glucose Fasting" in line:
                val = self._find_number(line, "Glucose Fasting")
                data["glucose"] = val
                if val != "N/A" and not (70 <= val <= 100):
                    data["abnormalities"].append("Abnormal Glucose")

            if "Cholesterol, Total" in line:
                val = self._find_number(line, "Cholesterol, Total")
                data["cholesterol_total"] = val
                if val != "N/A" and val > 200:
                    data["abnormalities"].append("High Cholesterol")

            if "HbA1c" in line and "%" in line:
                val = self._find_number(line, "HbA1c", "%")
                data["hba1c"] = val
                if val != "N/A" and not (4.0 <= val <= 5.6):
                    data["abnormalities"].append("Abnormal HbA1c")

            if "VITAMIN D, 25 HYDROXY, SERUM" in line:
                val = self._find_number(line)
                data["vitamin_d"] = val
                if val != "N/A" and not (75.0 <= val <= 250.0):
                    data["abnormalities"].append("Abnormal Vitamin D")

        return json.dumps(data, indent=2)

    def _find_number(self, text: str, keyword: str = "", unit: str = "") -> "float | str":
        if keyword:
            match = re.search(re.escape(keyword) + r'\s*[:\-]?\s*(\d+\.?\d*)\s*' + re.escape(unit), text)
        else:
            match = re.search(r'(\d+\.?\d*)\s*(nmol/L|ng/mL)', text)

        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return "N/A"
        return "N/A"


# -----------------------------------------------
# Exercise Planning Tool
# -----------------------------------------------
class ExerciseTool(BaseTool):
    name: str = "extract_exercise_data"
    description: str = "Extracts exercise-related values from a blood test report."

    def _run(self, full_report_text: str) -> str:
        data = {
            "hemoglobin": "N/A",
            "wbc": "N/A",
            "platelet_count": "N/A",
            "abnormalities": []
        }

        lines = full_report_text.split('\n')

        for line in lines:
            line = line.strip()

            if "Hemoglobin" in line and "g/dL" in line:
                val = self._find_number(line, "Hemoglobin", "g/dL")
                data["hemoglobin"] = val
                if val != "N/A" and not (13 <= val <= 17):
                    data["abnormalities"].append("Abnormal Hemoglobin")

            if "WBC Count" in line or "Total Leukocyte Count" in line:
                val = self._find_number(line, "WBC Count")
                data["wbc"] = val
                if val != "N/A" and not (4 <= val <= 11):
                    data["abnormalities"].append("Abnormal WBC Count")

            if "Platelet Count" in line and "thou/mm3" in line:
                val = self._find_number(line, "Platelet Count", "thou/mm3")
                data["platelet_count"] = val
                if val != "N/A" and not (150 <= val <= 450):
                    data["abnormalities"].append("Abnormal Platelet Count")

        return json.dumps(data, indent=2)

    def _find_number(self, text: str, keyword: str = "", unit: str = "") -> "float | str":
        if keyword:
            match = re.search(re.escape(keyword) + r'\s*[:\-]?\s*(\d+\.?\d*)\s*' + re.escape(unit), text)
        else:
            match = re.search(r'(\d+\.?\d*)', text)

        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return "N/A"
        return "N/A"
