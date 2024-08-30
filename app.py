# app.py
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env file
load_dotenv()

# Access environment variables
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    messages = [
        (
            "system",
            "You are a helpful assistant that translates English to 10 Indian languages(pick up random 10 languages). Translate the user sentence.",
        ),
        ("human", user_message),
    ]
    ai_msg = llm.invoke(messages)
    return jsonify({'response': ai_msg.content})

if __name__ == '__main__':
    app.run(debug=True)