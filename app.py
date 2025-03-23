import os
import asyncio
import requests
from flask import Flask, request, jsonify
from chunkr_ai import Chunkr
from dotenv import load_dotenv

from flask_cors import CORS



# Load API keys from .env file
load_dotenv()

CHUNKR_API_KEY = os.getenv("CHUNKR_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Initialize Flask app
app = Flask(__name__)

CORS(app)

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



@app.route("/", methods=["GET"])
def home():
    return "AIPR Backend is Live!", 200



@app.route("/process", methods=["POST"])
async def process_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    pdf_file = request.files["file"]
    
    if pdf_file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    # Save uploaded file
    upload_path = os.path.join("uploads", pdf_file.filename)
    os.makedirs("uploads", exist_ok=True)  # Ensure the folder exists
    pdf_file.save(upload_path)
    
    # Process the document with Chunkr-AI and get OCR text
    result = await process_document(upload_path)

    # Separate extracted text and analysis
    ocr_text = result if isinstance(result, str) else result.get("ocr_text", "No text extracted")
    analysis = result if isinstance(result, str) else result.get("analysis", "No analysis available")

    return jsonify({
        "message": "File processed successfully",
        "extracted_text": ocr_text,  # ✅ OCR Extracted Text
        "analysis": analysis  # ✅ Legal Analysis
    }), 200




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)

