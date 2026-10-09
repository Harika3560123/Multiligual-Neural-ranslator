try:
    import truststore
    truststore.inject_into_ssl()
except Exception:
    pass

from deep_translator import MyMemoryTranslator, GoogleTranslator
from PIL import Image
from PyPDF2 import PdfReader
from gtts import gTTS
import speech_recognition as sr
import pytesseract
import os

# =====================================================
# OCR IMAGE TO TEXT
# =====================================================

def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text.strip()
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
        return text.strip()
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
# TRANSLATION FUNCTION (NO API KEY)
# =====================================================

def translate_text(text, language):
    if not text or not text.strip():
        return ""
    try:
        lang_code = language.lower()
        try:
            translator = MyMemoryTranslator(source='english', target=lang_code)
            return translator.translate(text)
        except Exception:
            translator = GoogleTranslator(source='auto', target=lang_code)
            return translator.translate(text)
    except Exception as e:
        return f"Translation Error: {e}"

# =====================================================
# IMAGE TRANSLATION
# =====================================================

def translate_image(image_path, language):
    text = extract_text_from_image(image_path)
    
    if text.startswith("Image Error:") or not text:
        return "Image Error: Tesseract OCR is not installed or no text was found. (Multimodal fallback is disabled in no-key version)"

    return translate_text(text, language)

# =====================================================
# PDF TRANSLATION
# =====================================================

def translate_pdf(pdf_path, language):
    text = extract_text_from_pdf(pdf_path)
    if text.startswith("PDF Error:"):
        return text
    if not text:
        return "No text found in PDF."
    translated = translate_text(text, language)
    return translated

# =====================================================
# VOICE TRANSLATION
# =====================================================

def translate_speech(language):
    speech = speech_to_text()
    if speech.startswith("Speech Error:"):
        return speech
    if not speech:
        return "No speech detected."
    translated = translate_text(speech, language)
    return translated

# =====================================================
# TEXT TO SPEECH
# =====================================================

def text_to_speech(text, language_code):
    try:
        tts = gTTS(text=text, lang=language_code)
        audio_file = "static/output.mp3"
        tts.save(audio_file)
        return audio_file
    except Exception as e:
        print(f"TTS Error: {e}")
        return None