from fastapi import FastAPI, File, UploadFile, Form
from openai import OpenAI
import csv
import zipfile
import io
import os
import uvicorn

# Initialize FastAPI app
app = FastAPI()

# Load OpenAI API key (ensure this is set as an environment variable)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

@app.post("/api/")
async def answer_question(question: str = Form(...), file: UploadFile = File(None)):
    extracted_text = ""
    
    # Process uploaded file if present
    if file:
        if file.filename.endswith(".zip"):
            with zipfile.ZipFile(io.BytesIO(await file.read()), "r") as zip_ref:
                for filename in zip_ref.namelist():
                    if filename.endswith(".csv"):  # Assuming CSV file inside ZIP
                        with zip_ref.open(filename) as csv_file:
                            reader = csv.DictReader(io.TextIOWrapper(csv_file))
                            for row in reader:
                                if "answer" in row:
                                    extracted_text = row["answer"]
                                    break  # Extract first answer found

    # Construct query for LLM
    full_prompt = question
    if extracted_text:
        full_prompt += f"\nExtracted data: {extracted_text}"

    # Get response from OpenAI
    response = client.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Answer questions accurately."},
                  {"role": "user", "content": full_prompt}]
    )
    
    answer = response["choices"][0]["message"]["content"]
    return {"answer": answer}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)