from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)
# Construct the path to the .env file in the parent (main) directory
dotenv_path = os.path.join(os.path.dirname(current_dir), '.env')
print(dotenv_path)

# # Access environment variables
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vector = embeddings.embed_query("hello, world!")
print(vector[:5])