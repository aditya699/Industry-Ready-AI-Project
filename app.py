# app.py
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, session
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# Load environment variables from .env file
load_dotenv()

# Set up Google API key for accessing AI models
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set a secret key for session management

# Define the path to the PDF file
file_path = "Data/Raw/Prompt-Eng.pdf"

# Initialize the PyPDFLoader to load the PDF file
loader = PyPDFLoader(file_path)

# Load the PDF content and split it into pages
pages = loader.load_and_split()

# Initialize the RecursiveCharacterTextSplitter for chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
)

# Split the documents into chunks
splits = text_splitter.split_documents(pages)

# Create embeddings using Google's AI model
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Create a FAISS index from the document chunks
faiss_index = FAISS.from_documents(splits, embeddings)

# Set up the retriever with the FAISS index
retriever = faiss_index.as_retriever(search_kwargs={"k": 2})

# Set up the language model for generating responses
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)

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