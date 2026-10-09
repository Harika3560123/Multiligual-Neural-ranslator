try:
    import truststore
    truststore.inject_into_ssl()
except Exception:
    pass

from flask import Flask, render_template, request
from translator import (
    translate_text,
    translate_image,
    translate_pdf,
    translate_speech,
    text_to_speech
)
import os
import time

# =====================================================
# FLASK APP
# =====================================================

app = Flask(__name__)

# =====================================================
# UPLOAD FOLDER
# =====================================================

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("static", exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# =====================================================
# HOME PAGE
# =====================================================

@app.route("/")
def home():
    return render_template("index.html")

# =====================================================
# TRANSLATION ROUTE
# =====================================================

@app.route("/translate", methods=["POST"])
def translate():
    translated = ""
    audio = None
    language = request.form.get("language")
    action = request.form.get("action")
    text = request.form.get("text")

    # ==========================================
    # TEXT TRANSLATION
    # ==========================================
    if text and action is None:
        translated = translate_text(text, language)

    # ==========================================
    # VOICE INPUT TRANSLATION
    # ==========================================
    elif action == "voice":
        translated = translate_speech(language)

    # ==========================================
    # PDF TRANSLATION
    # ==========================================
    elif action == "pdf":
        pdf = request.files.get("pdf")
        if pdf and pdf.filename:
            path = os.path.join(app.config["UPLOAD_FOLDER"], pdf.filename)
            pdf.save(path)
            translated = translate_pdf(path, language)

    # ==========================================
    # IMAGE TRANSLATION
    # ==========================================
    elif action == "image":
        image = request.files.get("image")
        if image and image.filename:
            path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
            image.save(path)
            translated = translate_image(path, language)

    # ==========================================
    # TEXT TO SPEECH
    # ==========================================
    if translated and not translated.startswith(("Translation Error", "Image Error", "PDF Error", "Speech Error", "Image Fallback Error")):
        language_codes = {
            "English": "en",
            "Telugu": "te",
            "Hindi": "hi",
            "Tamil": "ta",
            "French": "fr"
        }
        code = language_codes.get(language, "en")
        try:
            audio_path = text_to_speech(translated, code)
            if audio_path:
                # Add trailing timestamp to bypass browser cache
                audio = f"/{audio_path}?t={int(time.time())}"
        except Exception as e:
            print(f"Audio Error: {e}")
            audio = None

    # ==========================================
    # RETURN OUTPUT
    # ==========================================
    return render_template(
        "index.html",
        translated=translated,
        audio=audio
    )

# =====================================================
# RUN APPLICATION
# =====================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)); app.run(host="0.0.0.0", port=port, debug=False)
