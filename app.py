# app.py
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, session
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# Load environment variables from .env file
load_dotenv()

# Access environment variables
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set a secret key for session management

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Load and index the PDF
loader = PyPDFLoader("Data/Raw/Prompt-Eng.pdf")
pages = loader.load_and_split()
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vector_store = FAISS.from_documents(pages, embeddings)

# Create a retriever
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

@app.route('/')
def index():
    # Initialize or reset the conversation memory when loading the main page
    session['memory'] = []
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    
    # Retrieve the conversation memory from the session
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key='answer'
    )
    for entry in session.get('memory', []):
        memory.chat_memory.add_user_message(entry['human'])
        memory.chat_memory.add_ai_message(entry['ai'])

    # Create the conversational chain with memory
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        verbose=True
    )
    
    # Get the response from the chain
    response = qa_chain({"question": user_message})
    
    # Extract the answer and source documents
    answer = response['answer']
    source_docs = response['source_documents']
    
    # Update the session memory
    session['memory'] = session.get('memory', []) + [{'human': user_message, 'ai': answer}]
    
    # Prepare the response
    response_data = {
        'response': answer,
        'sources': [{"page": doc.metadata['page'], "content": doc.page_content[:300]} for doc in source_docs]
    }
    
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)