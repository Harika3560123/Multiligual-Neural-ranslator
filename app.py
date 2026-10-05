from flask import Flask, render_template, request

from translator import (
    translate_text,
    translate_image,
    translate_pdf,
    translate_speech,
    text_to_speech
)

import os


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

        translated = translate_text(
            text,
            language
        )


    # ==========================================
    # VOICE INPUT TRANSLATION
    # ==========================================

    elif action == "voice":

        translated = translate_speech(
            language
        )


    # ==========================================
    # PDF TRANSLATION
    # ==========================================

    elif action == "pdf":

        pdf = request.files.get("pdf")

        if pdf:

            path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                pdf.filename
            )

            pdf.save(path)

            translated = translate_pdf(
                path,
                language
            )


    # ==========================================
    # IMAGE TRANSLATION
    # ==========================================

    elif action == "image":

        image = request.files.get("image")

        if image:

            path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                image.filename
            )

            image.save(path)

            translated = translate_image(
                path,
                language
            )


    # ==========================================
    # TEXT TO SPEECH
    # ==========================================

    if translated:

        language_codes = {

            "English": "en",

            "Telugu": "te",

            "Hindi": "hi",

            "Tamil": "ta",

            "French": "fr"

        }

        code = language_codes.get(
            language,
            "en"
        )

        try:

            audio = text_to_speech(
                translated,
                code
            )

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

    app.run(debug=True)