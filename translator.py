from rag_engine import retrieve_context

from google import genai

from dotenv import load_dotenv

from PIL import Image

from PyPDF2 import PdfReader

from gtts import gTTS

import speech_recognition as sr

import pytesseract

import os


# =====================================================
# LOAD API KEY
# =====================================================

load_dotenv()

j = os.getenv("jyo")


# =====================================================
# GEMINI CLIENT
# =====================================================

client = genai.Client(api_key=j)

# =====================================================
# OCR IMAGE TO TEXT
# =====================================================

def extract_text_from_image(image_path):

    try:

        img = Image.open(image_path)

        text = pytesseract.image_to_string(img)

        return text

    except Exception as e:

        return f"Image Error: {e}"


# =====================================================
# PDF TO TEXT
# =====================================================

def extract_text_from_pdf(pdf_path):

    try:

        reader = PdfReader(pdf_path)

        text = ""

        for page in reader.pages:

            extracted = page.extract_text()

            if extracted:

                text += extracted + "\n"

        return text

    except Exception as e:

        return f"PDF Error: {e}"


# =====================================================
# SPEECH TO TEXT
# =====================================================

def speech_to_text():

    recognizer = sr.Recognizer()

    try:

        with sr.Microphone() as source:

            print("Speak Now...")

            recognizer.adjust_for_ambient_noise(source)

            audio = recognizer.listen(source)

        text = recognizer.recognize_google(audio)

        return text

    except Exception as e:

        return f"Speech Error: {e}"


# =====================================================
# TRANSLATION FUNCTION
# =====================================================

def translate_text(text, language):

    try:

        context = retrieve_context(text)

        prompt = f"""
You are an advanced multilingual neural translator.

Context:
{context}

Translate the following text into {language}.

Rules:
1. Understand context
2. Understand idioms
3. Preserve meaning
4. Return only translated text

Text:
{text}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"Translation Error: {e}"


# =====================================================
# IMAGE TRANSLATION
# =====================================================

def translate_image(image_path, language):

    text = extract_text_from_image(image_path)

    translated = translate_text(
        text,
        language
    )

    return translated


# =====================================================
# PDF TRANSLATION
# =====================================================

def translate_pdf(pdf_path, language):

    text = extract_text_from_pdf(pdf_path)

    translated = translate_text(
        text,
        language
    )

    return translated


# =====================================================
# VOICE TRANSLATION
# =====================================================

def translate_speech(language):

    speech = speech_to_text()

    translated = translate_text(
        speech,
        language
    )

    return translated


# =====================================================
# TEXT TO SPEECH
# =====================================================

def text_to_speech(text, language_code):

    try:

        tts = gTTS(
            text=text,
            lang=language_code
        )

        audio_file = "static/output.mp3"

        tts.save(audio_file)

        return audio_file

    except Exception as e:

        print(f"TTS Error: {e}")

        return None