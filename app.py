from flask import Flask, request, jsonify
from PIL import Image
import base64
from io import BytesIO

# Import custom modules
from ocr_translate.ocr import run_ocr
from deep_translator.google_translator import GoogleTranslator

app = Flask(__name__)

@app.route("/ocr-translate", methods=["POST"])
def ocr_translate():
    data = request.get_json()
    image_base64 = data.get("image_base64")

    if not image_base64:
        return jsonify({"error": "No image provided"}), 400

    try:
        image_data = base64.b64decode(image_base64.split(',')[-1])
        image = Image.open(BytesIO(image_data))
    except Exception as e:
        return jsonify({"error": "Invalid image", "details": str(e)}), 400

    try:
        text = run_ocr(image)
    except Exception as e:
        return jsonify({"error": "OCR failed", "details": str(e)}), 500

    try:
        translated = GoogleTranslator(source='auto', target='en').translate(text)
    except Exception as e:
        return jsonify({"error": "Translation failed", "details": str(e)}), 500

    return jsonify({
        "original": text,
        "translated": translated
    })

if __name__ == "__main__":
    app.run(debug=True)
