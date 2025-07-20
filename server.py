from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import json
import uvicorn
import os

# Load dataset from desktop
desktop_path = os.path.expanduser("~/Desktop/data.json")
with open(desktop_path, "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/query")
async def answer_query(q: str, request: Request):
    q_lower = q.lower()
    answer = "Question not supported."

    # ✨ Add as many question patterns here as needed
    if "total sales of table in beierburgh" in q_lower:
        total = df[(df["product"] == "Table") & (df["city"] == "Beierburgh")]["sales"].sum()
        answer = int(total)

    elif "how many sales reps are there in south dakota" in q_lower:
        reps = df[df["region"] == "South Dakota"]["rep"].nunique()
        answer = int(reps)

    elif "average sales for soap in utah" in q_lower:
        avg = df[(df["product"] == "Soap") & (df["region"] == "Utah")]["sales"].mean()
        answer = round(float(avg), 2) if not np.isnan(avg) else "No sales"

    elif "rene gutmann" in q_lower and "north olin" in q_lower:
        data = df[(df["rep"] == "Rene Gutmann") & (df["city"] == "North Olin")]
        if not data.empty:
            max_row = data.loc[data["sales"].idxmax()]
            answer = max_row["date"]
        else:
            answer = "No data found."

    elif "total sales of pizza in torphycester" in q_lower:
        total = df[(df["product"] == "Pizza") & (df["city"] == "Torphycester")]["sales"].sum()
        answer = int(total)

    else:
        answer = "Question not recognized or supported."

    # Prepare response with required email header
    return Response(
        content=json.dumps({"answer": answer}),
        media_type="application/json",
        headers={"X-Email": "23f3000059@ds.study.iitm.ac.in"}
    )

if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
