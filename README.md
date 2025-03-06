# ONG_PPT_TRANSLATOR

Tool to translate a **whole** ppt from a language to another while keeping (_mostly_) current formatting using a LLM (chatgpt...)

Still work in progress! There are some failures with color and with complex bolds and italics.

Tested with ollama and llama3.1:latest

## Usage
Create a .env file with the following variables:
```bash
# openai compatible endpoint. Leave it empty for openai, use it endend in /v1 for ollama
BASE_URL=
# API Key. Use any string for ollama in local development
API_KEY=
# Model Name
MODEL=
# Any extra information to be passed to the LLM for better understanding of the document and for fine tune translation
EXTRA_CONTEXT=
# Original language to translate
SOURCE_LANG=spanish
# Target language to translate
TARGET_LANG=english
```
Then run process with
`python -m ong_ppt_translator --input_file "Ejemplo.pptx" --output_file "Ejemplo (traducido).pptx"`
