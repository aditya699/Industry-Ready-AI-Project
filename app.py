'''
Author -Aditya Bhatt 11:50 AM 30-08-2024

TODO:Create a simple chating system with gemini llm
'''

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env file
load_dotenv()

# Access environment variables

os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

messages = [
    (
        "system",
        "You are a helpful assistant that translates English to Hindi and Tamil. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]
ai_msg = llm.invoke(messages)
print(ai_msg.content)