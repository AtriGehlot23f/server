from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
import json

# Load data.json which must be in the same directory
with open("data.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Create FastAPI app
app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/query")
def answer_query(q: str):
    q_lower = q.lower()
    answer = "Question not supported."

    try:
        if "total sales of table in beierburgh" in q_lower:
            total = df[(df["product"] == "Table") & (df["city"] == "Beierburgh")]["sales"].sum()
            answer = int(total)

        elif "how many sales reps are there in south dakota" in q_lower:
            reps = df[df["region"] == "South Dakota"]["rep"].nunique()
            answer = int(reps)

        elif "average sales for soap in utah" in q_lower:
            avg = df[(df["product"] == "Soap") & (df["region"] == "Utah")]["sales"].mean()
            answer = round(float(avg), 2)

        elif "rene gutmann" in q_lower and "north olin" in q_lower:
            result = df[(df["rep"] == "Rene Gutmann") & (df["city"] == "North Olin")]
            if not result.empty:
                answer = result.loc[result["sales"].idxmax()]["date"]
            else:
                answer = "No record found"

    except Exception as e:
        answer = f"Error: {str(e)}"

    return JSONResponse(
        status_code=200,
        content={"answer": answer},
        headers={"X-Email": "23f3000059@ds.study.iitm.ac.in"}
    )
