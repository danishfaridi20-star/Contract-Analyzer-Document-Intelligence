from flask import request, jsonify, Blueprint
from app.extensions import db
from tandc.models.tc_models import Term_conditions
import fitz
import os
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
import requests
import json
import pymupdf
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

tc_bp = Blueprint('tandc', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    fileext = filename.split('.')[-1].lower()
    if fileext in ALLOWED_EXTENSIONS:
        return fileext
    return "unsupported"


def summerise(text):
    prompt = """
Analyze the following Terms and Conditions and return a strictly valid JSON object with these exact fields:

- risky_clauses
- data_privacy_issues
- cancellation_and_refund_policy
- user_obligations_and_restrictions
- governing_law_and_jurisdiction
- ambiguous_language
- summary

Each field must be a dictionary with:
- explanation
- quote

Return only raw JSON.
"""

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
            "messages": [
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        }
    )

    response_json = response.json()
    print(response_json)

    return response_json["choices"][0]["message"]["content"]


def extract_text_from_file(file_path, ext):
    text = ""

    if ext == 'pdf':
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
        doc.close()

    elif ext in ['png', 'jpg', 'jpeg']:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)

    else:
        raise ValueError("Unsupported file format")

    return text


@tc_bp.route('/fileupload', methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file found"})

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"})

    ext = allowed_file(file.filename)

    if ext == "unsupported":
        return jsonify({"error": "File type not allowed"})

    filename = secure_filename(file.filename)
    saved_path = os.path.join(UPLOAD_FOLDER, filename)

    file.save(saved_path)

    try:
        text = extract_text_from_file(saved_path, ext)
        summary = summerise(text)

        return jsonify({
            "filename": filename,
            "extracted_text": text,
            "summary": summary
        })

    except Exception as e:
        return jsonify({"error": str(e)})