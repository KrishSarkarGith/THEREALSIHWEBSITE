
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Union, List
import os, json
from models.recommender import CareerRecommender

app = FastAPI(title="SIH Career Advisor API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "models", "data", "careers.json")
reco = CareerRecommender(DATA_PATH)

class Assessment(BaseModel):
    name: str
    age: int
    education_level: str
    interests: List[str]
    strengths: List[str]
    preferred_languages: List[str]
    values: List[str] = []
    location: Union[str, None] = None

def _profile_to_text(a: Assessment) -> str:
    parts = [
        " ".join(a.interests),
        " ".join(a.strengths),
        " ".join(a.preferred_languages),
        " ".join(a.values),
        a.education_level or "",
        a.location or ""
    ]
    return " ".join(parts)

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.post("/api/assess")
def assess(a: Assessment):
    profile_text = _profile_to_text(a)
    results = reco.recommend(profile_text, top_k=3)
    # Build a lightweight plan
    plans = []
    for r in results:
        plans.append({
            "careerId": r["id"],
            "careerTitle": r["title"],
            "matchScore": r["match_score"],
            "why": f"Matches your interests/strengths in {', '.join(a.interests[:3])} and {', '.join(a.strengths[:3])}.",
            "skillGaps": [s for s in r["skills"] if s not in [*a.interests, *a.strengths]],
            "courses": r["courses"],
            "nextSteps": [
                "Enroll in 1 course from the list",
                "Find a mentor or alumni to review your plan",
                "Build 1 project and add to portfolio within 4 weeks"
            ]
        })
    return {"profile": a.dict(), "recommendations": plans}

@app.get("/api/careers")
def list_careers():
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
    return {"careers": data}
