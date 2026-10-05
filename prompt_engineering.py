def create_advanced_prompt(text, language):

    prompt = f"""
Act as an expert AI multilingual translator.

Translate the given content into {language}.

Requirements:
- Preserve meaning
- Preserve emotions
- Preserve slang
- Preserve idioms
- Preserve cultural understanding
- Detect sentence tone
- Translate naturally
- Avoid robotic translation
- Avoid literal translation

If slang appears:
Convert slang meaning correctly.

If idioms appear:
Translate the actual meaning.

Return only translated text.

Content:
{text}
"""

    return prompt