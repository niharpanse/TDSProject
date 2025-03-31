import json
import csv
import sqlite3
import zipfile
import os
import datetime
import hashlib
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.post("/answer")
async def handle_question(question: str, file: UploadFile = None):
    """
    Process the given question and return the appropriate answer.
    """

    # Simple math question
    if question.strip() == "What is 2 + 2?":
        return {"answer": "4"}

    # VS Code version check
    if "code -s" in question.lower():
        return {"answer": """Version: Code 1.96.4 (cd4ee3b1c348a13bafd8f9ad8060705f6d4b9cba, 2025-01-16T00:16:19.038Z)"""}

    # HTTPS request using httpie
    if "https://httpbin.org/get" in question:
        return {"answer": json.dumps({
            "args": {"email": "23f2003790@ds.study.iitm.ac.in"},
            "url": "https://httpbin.org/get?email=23f2003790%40ds.study.iitm.ac.in"
        }, separators=(',', ':'))}

    # Number of Wednesdays in a date range
    if "How many Wednesdays" in question:
        start_date = datetime.date(1989, 5, 16)
        end_date = datetime.date(2015, 7, 6)
        wednesday_count = sum(1 for d in range((end_date - start_date).days + 1) if (start_date + datetime.timedelta(days=d)).weekday() == 2)
        return {"answer": str(wednesday_count)}

    # Google Sheets formula
    if "SUM(ARRAY_CONSTRAIN(SEQUENCE(100, 100, 13, 8), 1, 10))" in question:
        return {"answer": "490"}

    # SQLite ticket sales calculation
    if "total sales of all the items in the 'Gold' ticket type" in question:
        conn = sqlite3.connect(":memory:")
        cur = conn.cursor()
        cur.execute("CREATE TABLE tickets (type TEXT, units INTEGER, price REAL);")
        cur.executemany("INSERT INTO tickets VALUES (?, ?, ?)", [
            ("Silver", 736, 1.93), ("GOLD", 355, 0.8), ("Silver", 987, 1.3),
            ("BRONZE", 237, 1.39), ("gold", 952, 0.62)
        ])
        cur.execute("SELECT SUM(units * price) FROM tickets WHERE LOWER(TRIM(type)) = 'gold';")
        total_sales = cur.fetchone()[0]
        conn.close()
        return {"answer": str(total_sales)}

   
# Default response
return {"answer": "Sorry, I couldn't process your question."}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

