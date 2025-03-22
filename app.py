import os
import asyncio
import requests
from flask import Flask, request, jsonify
from chunkr_ai import Chunkr
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()

CHUNKR_API_KEY = os.getenv("CHUNKR_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Initialize Flask app
app = Flask(__name__)

# Initialize Chunkr-AI
chunkr = Chunkr(api_key=CHUNKR_API_KEY)

# DeepSeek API details
URL = "https://openrouter.ai/api/v1/chat/completions"

async def process_document(file_path):
    try:
        # Upload document and get OCR text
        task = await chunkr.upload(file_path)
        ocr_text = task.content() if callable(task.content) else task.content

        # Analyze legal text
        result = analyze_legal_text(ocr_text)
        return result

    finally:
        await chunkr.close()

def analyze_legal_text(ocr_text):
    # Prepare prompt
    prompt = f"""
    You are a legal expert. Review this document and provide structured feedback like this:
    - Identify errors and inconsistencies.
    - Assign a risk score.
    - Suggest corrections.
    
    Here is the document:
    {ocr_text}
    """

    # API request data
    data = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [
            {"role": "system", "content": "You are an expert legal proofreader."},
            {"role": "user", "content": prompt}
        ]
    }

    # Send request
    response = requests.post(URL, headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"}, json=data)
    result = response.json()

    # Extract response
    reasoning = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
    return reasoning

@app.route("/process", methods=["POST"])
def process():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files["file"]
    file_path = f"./uploads/{file.filename}"
    file.save(file_path)

    # Run async function in event loop
    result = asyncio.run(process_document(file_path))

    return jsonify({"analysis": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
