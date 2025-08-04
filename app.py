from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import base64
from io import BytesIO
from deep_translator import GoogleTranslator

app = Flask(__name__)

@app.route("/ocr-translate", methods=["POST"])
def ocr_translate():
    data = request.get_json()
    image_base64 = data.get("image_base64")

    if not image_base64:
        return jsonify({"error": "No image provided"}), 400

    # Decode base64 image
    try:
        image_data = base64.b64decode(image_base64.split(',')[-1])
        image = Image.open(BytesIO(image_data))
    except Exception as e:
        return jsonify({"error": "Invalid image", "details": str(e)}), 400

    # OCR
    try:
        text = pytesseract.image_to_string(image, lang='jpn')
    except Exception as e:
        return jsonify({"error": "OCR failed", "details": str(e)}), 500

    # Translate
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
