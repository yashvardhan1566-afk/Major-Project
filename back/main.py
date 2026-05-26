from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types

# Import database
from database import conn, cursor

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os
# Gemini API Key
REAL_API_KEY = os.getenv("GEMINI_API_KEY")
if not REAL_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing in environment variables")
# Gemini client
client = genai.Client(api_key=REAL_API_KEY)

# Request model
class StudyRequest(BaseModel):
    exam: str
    weak: str
    strong: str
    days: int
    hours: int

# Generate Study Plan API
@app.post("/generate-plan")
def generate_plan(req: StudyRequest):

    try:

        prompt = f"""
        You are an expert academic coach.

        Create a structured study plan.

        Exam: {req.exam}

        Weak subjects: {req.weak}

        Strong subjects: {req.strong}

        Days Left: {req.days} days

        Daily Study Capacity: {req.hours} hours per day
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if not response.text:
            raise Exception("Gemini returned empty response")

        # Save into SQLite database
        cursor.execute(
            """
            INSERT INTO study_plans
            (exam, weak, strong, days, hours, plan)

            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                req.exam,
                req.weak,
                req.strong,
                req.days,
                req.hours,
                response.text
            )
        )

        conn.commit()

        return {
            "plan": response.text
        }

    except Exception as e:

        print(f"ERROR: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# View saved plans
@app.get("/plans")
def get_plans():

    cursor.execute("SELECT * FROM study_plans")

    data = cursor.fetchall()

    return {
        "saved_plans": data
    }