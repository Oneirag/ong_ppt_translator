from dotenv import load_dotenv

load_dotenv()
import os
from openai import OpenAI
import httpx
import ssl


if not os.getenv("MODEL") or not os.getenv("BASE_URL") or not os.getenv("API_KEY"):
    raise Exception("Missing environment variables. You must set the following: MODEL, BASE_URL, API_KEY")

MODEL = os.getenv("MODEL")
client = OpenAI(base_url=os.getenv("BASE_URL"), api_key=os.getenv("API_KEY"),
                http_client=httpx.Client(verify=ssl.create_default_context()))

if __name__ == '__main__':
    res = client.chat.completions.create(messages=[{"role": "user", "content": "hola"}], model=MODEL)
    print(res.choices[0].message.content)
