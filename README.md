Header & Badges: Python, Flask, Google Gemini 2.5 Flash, LangChain & FAISS, and license badges.
Project Overview: An introduction explaining the multimodal neural translation pipeline powered by Gemini 2.5 Flash and RAG.
Key Features:
🧠 Context & Idiom-Aware Translation (RAG): LangChain + FAISS + sentence-transformers for disambiguating idioms and metaphors.
🗣️ Speech Recognition: Voice-to-text input via Google Speech Recognition.
🖼️ OCR Extraction: Image text recognition via Tesseract OCR and Pillow.
📄 PDF Translation: Document extraction via PyPDF2.
🔊 Voice Synthesis (TTS): Audio playback using gTTS.
🎨 Modern Glassmorphic UI: Responsive dark theme with gradients and interactive controls.
Architecture Diagram: A Mermaid workflow diagram showing the end-to-end data flow from input modalities through extraction, RAG semantic retrieval, Gemini translation, and audio output.
Supported Languages Table: Complete list of 25+ Indian and international languages, plus audio playback language code mappings.
Project Directory Tree: File-by-file breakdown (app.py, translator.py, rag_engine.py, prompt_engineering.py, etc.).
Prerequisites & System Dependencies: Steps for Python, Tesseract OCR (Windows/macOS/Linux), PortAudio / PyAudio, and Gemini API keys.
Installation & Running: Step-by-step setup commands and .env configuration notes.
Troubleshooting Guide: Solutions for common issues (Tesseract path errors, PyAudio installation, audio caching, and API keys).
