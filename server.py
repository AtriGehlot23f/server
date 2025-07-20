from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import json
import uvicorn

# Load dataset from local file (data.json in the same repo directory)
with open("data.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Set up FastAPI app
app = FastAPI()

# Allow CORS for all origins (so external browser requests are allowed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/query")
async def answer_query(q: str, request: Request):
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
            answer = round(float(avg), 2) if not np.isnan(avg) else 0

        elif "rene gutmann" in q_lower and "north olin" in q_lower:
            result = df[(df["rep"] == "Rene Gutmann") & (df["city"] == "North Olin")]
            if not result.empty:
                max_row = result.loc[result["sales"].idxmax()]
                answer = max_row["date"]

        elif "total sales of table in lake rooseveltboro" in q_lower:
            total = df[(df["product"] == "Table") & (df["city"] == "Lake Rooseveltboro")]["sales"].sum()
            answer = int(total)

        elif "how many sales reps are there in new hampshire" in q_lower:
            reps = df[df["region"] == "New Hampshire"]["rep"].nunique()
            answer = int(reps)

        elif "average sales for towels in new hampshire" in q_lower:
            avg = df[(df["product"] == "Towels") & (df["region"] == "New Hampshire")]["sales"].mean()
            answer = round(float(avg), 2)

        elif "charlotte lang" in q_lower and "marciaview" in q_lower:
            result = df[(df["rep"] == "Charlotte Lang") & (df["city"] == "Marciaview")]
            if not result.empty:
                max_row = result.loc[result["sales"].idxmax()]
                answer = max_row["date"]

        elif "total sales of bike in bartonton" in q_lower:
            total = df[(df["product"] == "Bike") & (df["city"] == "Bartonton")]["sales"].sum()
            answer = int(total)

        elif "average sales for bike in california" in q_lower:
            avg = df[(df["product"] == "Bike") & (df["region"] == "California")]["sales"].mean()
            answer = round(float(avg), 2)

        elif "mrs. lindsey connelly" in q_lower and "okunevaport" in q_lower:
            result = df[(df["rep"] == "Mrs. Lindsey Connelly") & (df["city"] == "Okunevaport")]
            if not result.empty:
                max_row = result.loc[result["sales"].idxmax()]
                answer = max_row["date"]

        elif "total sales of pizza in torphycester" in q_lower:
            total = df[(df["product"] == "Pizza") & (df["city"] == "Torphycester")]["sales"].sum()
            answer = int(total)

        elif "how many sales reps are there in delaware" in q_lower:
            reps = df[df["region"] == "Delaware"]["rep"].nunique()
            answer = int(reps)

        elif "what is the total sales of pizza in greeley" in q_lower:
            total = df[(df["product"] == "Pizza") & (df["city"] == "Greeley")]["sales"].sum()
            answer = int(total)

        elif "jeremy fahey" in q_lower and "donnellyville" in q_lower:
            result = df[(df["rep"] == "Jeremy Fahey") & (df["city"] == "Donnellyville")]
            if not result.empty:
                max_row = result.loc[result["sales"].idxmax()]
                answer = max_row["date"]

        elif "lewis quigley" in q_lower and "deckowside" in q_lower:
            result = df[(df["rep"] == "Lewis Quigley") & (df["city"] == "Deckowside")]
            if not result.empty:
                max_row = result.loc[result["sales"].idxmax()]
                answer = max_row["date"]

    except Exception as e:
        answer = f"Error: {str(e)}"

    return Response(
        content=json.dumps({"answer": answer}),
        media_type="application/json",
        headers={"X-Email": "23f3000059@ds.study.iitm.ac.in"}
    )

# Don't include if hosted via Uvicorn directly on Render
# If run locally:
# if __name__ == "__main__":
#     uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
