from typing import Literal

import openai
from pydantic import BaseModel, Field

from ong_ppt_translator import MODEL, client
import os


def translate_text_with_openai(text: str) -> str:
    source_lang = os.getenv("SOURCE_LANG") or "spanish"
    target_lang = os.getenv("TARGET_LANG") or "english"
    extra_context = os.getenv("EXTRA_CONTEXT") or ""
    retval = ""
    if not text or text.isspace():
        return retval
    try:
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
            #print(response.parsed)
            if response.parsed.original_language == target_lang:
                # force no translation if original language was detected as english
                retval = text
            else:
                retval = response.parsed.translated_text
            if "Renfe" in retval:
                pass
            # Remove extra \n if original text did not have it
            if retval.startswith("\n") and not text.startswith("\n"):
                retval = retval[1:]
        elif response.refusal:
            print(response.refusal)
    except Exception as e:
        if type(e) == openai.LengthFinishReasonError:
            print("Too many tokens: ", e)
            pass
        else:
            print(e)
            pass

    # response = client.chat(
    #     model=os.getenv("MODEL"),
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant that translates text while preserving formatting."},
    #         {"role": "user", "content": f"Translate the following text to {target_language} while preserving formatting:\n\n{text}"}
    #     ],
    #     format=Translation.model_json_schema()
    # )
    # retval = Translation.model_validate_json(response.message.content).translated_text
    print(f"Translated '{text}' -> '{retval}'")
    return retval


class Translation(BaseModel):
    translated_text: str = Field(description="Translation of the original text without explanations")
    original_language: Literal['english', 'spanish', 'other']

