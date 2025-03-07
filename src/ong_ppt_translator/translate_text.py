from typing import Literal

from pydantic import BaseModel, Field

from ong_ppt_translator import MODEL, client, logger
import os

from tenacity import retry, stop_after_attempt, wait_fixed

@retry(wait=wait_fixed(1), reraise=True, stop=stop_after_attempt(3))
def _translate(text, source_lang, target_lang, extra_context):
    retval = text
    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": f"You are a professional translator from {source_lang} to {target_lang}. "
                           f"Translate the entire HTML text precisely preserving its original meaning, nuance "
                           f"and original HTML format. Do not provide explanations, just translation. "
                           "NEVER add any HTML tag that is not present in the original text. "
                           f"Do not translate numbers. "
                           f"If the text is already in {target_lang} do not translate and return the original text. "
                           f"Never translate back from {target_lang} to {source_lang}. "
                           f"{extra_context}"
            },
            {
                "role": "user",
                "content": f"Translate the following text from {source_lang} to {target_lang}. "
                           f"If already in {target_lang} do not translate it back:\n\n{text}"
            }
        ],
        temperature=0.001,
        max_tokens=1024,
        response_format=Translation,
    )

    response = completion.choices[0].message
    if response.parsed:
 #       #print(response.parsed)
 #       if response.parsed.original_language == target_lang:
 #           # force no translation if original language was detected as english
 #           retval = text
 #       else:
            retval = response.parsed.translated_text
    elif response.refusal:
        logger.error(response.refusal)
    logger.info(f"Translated '{text}' -> '{retval}'")
    return retval


def translate_text_with_openai(text: str) -> str:
    source_lang = os.getenv("SOURCE_LANG") or "spanish"
    target_lang = os.getenv("TARGET_LANG") or "english"
    extra_context = os.getenv("EXTRA_CONTEXT") or ""
    retval = text
    if not text or text.isspace():
        return retval
    try:
        return _translate(text, source_lang=source_lang, target_lang=target_lang, extra_context=extra_context)
    except Exception as e:
        logger.exception(e)
        logger.error(f"Could not translate '{text}'")
        return text


class Translation(BaseModel):
    translated_text: str = Field(description="Translation of the original text without explanations")
#    original_language: Literal['english', 'spanish', 'other']

if __name__ == '__main__':
    translate_text_with_openai("España")
