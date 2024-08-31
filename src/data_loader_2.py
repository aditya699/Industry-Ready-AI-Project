from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set up Google API key for accessing AI models
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

# Define the path to the PDF file
file_path = "../Data/Raw/Prompt-Eng.pdf"

# Initialize the PyPDFLoader to load the PDF file
loader = PyPDFLoader(file_path)

# Load the PDF content and split it into pages
pages = loader.load_and_split()

# Initialize the RecursiveCharacterTextSplitter for chunking
# This splitter breaks text into smaller, overlapping chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # Maximum size of each chunk
    chunk_overlap=200,  # Overlap between chunks to maintain context
    length_function=len  # Function to measure chunk size
)

# Split the documents into chunks
# This is better than page-wise splitting for several reasons:
# 1. More granular content division: Chunks can cross page boundaries, capturing complete ideas.
# 2. Consistent size: Unlike pages, which can vary in length, chunks have a consistent size.
# 3. Improved context: Overlapping ensures that context is maintained between chunks.
# 4. Better for embeddings: Smaller, focused chunks lead to more accurate embeddings.
# 5. Flexible retrieval: Allows for retrieving specific, relevant portions rather than entire pages.
splits = text_splitter.split_documents(pages)

# Create embeddings using Google's AI model
# Embeddings convert text into numerical vectors, capturing semantic meaning
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Create a FAISS index from the document chunks
# FAISS is an efficient similarity search library for finding relevant text quickly
faiss_index = FAISS.from_documents(splits, embeddings)

# Set up the retriever with the FAISS index
# The retriever will find the most relevant chunks for a given query
retriever = faiss_index.as_retriever(search_kwargs={"k": 2})  # Retrieve top 5 most relevant chunks

# Set up the language model for generating responses
# Using a temperature of 0.3 for a balance between creativity and accuracy
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

# Create the RetrievalQA chain
# This chain combines the retriever and language model to answer questions
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # "stuff" method: input all relevant documents into the prompt
    retriever=retriever,
    return_source_documents=True  # Include source documents in the output
)

# Function to ask questions and display answers with sources
def ask_question(question):
    result = qa_chain({"query": question})
    print(f"Question: {question}")
    print(f"Answer: {result['result']}")
    print("\nSources:")
    for idx, doc in enumerate(result['source_documents'], 1):
        print(f"Source {idx}:")
        print(f"Page: {doc.metadata['page']}")
        print(f"Content: {doc.page_content[:300]}...\n")

# Example usage
ask_question("What is CHAIN-OF-KNOWLEDGE (COK)?")