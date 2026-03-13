import os
import google.generativeai as genai
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

# Configuration
GOOGLE_API_KEY = "YOUR GOOGLE API KEY"

# Configure the underlying Google library to check models
genai.configure(api_key=GOOGLE_API_KEY)

def ingest_pdf():
    # --- MODEL CHECKER ---
    print("Checking available embedding models...")
    available_models = [m.name for m in genai.list_models() if 'embedContent' in m.supported_generation_methods]
    print(f"Your API key has access to: {available_models}")

    # We will try to use text-embedding-004, or fall back to whatever is first in your list
    chosen_model = "models/gemini-embedding-001" 
    if chosen_model not in available_models and len(available_models) > 0:
        chosen_model = available_models[0]
    
    print(f"--- Using model: {chosen_model} ---")

    # --- REST OF THE SCRIPT ---
    base_dir = os.path.dirname(__file__)
    pdf_path = os.path.join(base_dir, "data", "welcome_guide.pdf")
    db_path = os.path.join(base_dir, "chroma_db")

    loader = PyPDFLoader(pdf_path)
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(data)

    embeddings = GoogleGenerativeAIEmbeddings(
        model=chosen_model, 
        google_api_key=GOOGLE_API_KEY
    )

    print("--- Embedding and storing in ChromaDB ---")
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=db_path
    )
    print("Done! Check your project folder for the 'chroma_db' folder.")

if __name__ == "__main__":
    ingest_pdf()