
# AI Proofreader - Backend (Flask)

This is the backend for the **AI Proofreader (AIPR)** system. It performs OCR on uploaded PDF legal documents, runs legal NLP analysis, and returns key insights, summaries, and risk assessments.

⚙️ Frontend Repo: [AIPR_Frontend](https://github.com/Shashwat-Balodhi/AIPR_Frontend)

🌐 Deployed on: [Render](https://render.com/) backend server is offline right now...

---

## 🧠 Technologies Used

- Python + Flask
- `pdf2image` + `pytesseract` for OCR
- HuggingFace Transformers (`legal-bert-small-uncased`)
- Docker (for containerization)
- Render.com (for deployment)

---

## 🚀 How to Run Locally

1. Clone the repo:
   ```bash
   git clone https://github.com/Shashwat-Balodhi/AIPR_Backend.git
   cd AIPR_Backend
   ```

2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # or venv\Scripts\activate on Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask app:
   ```bash
   python app.py
   ```

---

## 📦 API Endpoint

### `POST /process`

Accepts PDF files and returns a JSON response with:
- Extracted text
- Named entities (e.g., seller, buyer, document number)
- Legal summary
- Risk insights

#### Example curl request:
```bash
curl -X POST -F "file=@example.pdf" https://proofreader-backend.onrender.com/process
```

---

## 🐳 Deployment with Docker

```bash
docker build -t aiprb .
docker run -p 5000:5000 aiprb
```

---

## 📁 Project Structure

```
AIPR_Backend/
├── app.py                # Flask app
├── model/                # NLP and OCR logic
├── utils/                # Helper functions
├── requirements.txt
└── Dockerfile
```

---

## 🔐 API Security

- CORS enabled for frontend access
- File size and extension checks
- Can add API keys/token auth if needed

---

## 📜 License

MIT License © 2025 Shashwat Balodhi
