# --- THE CORRECT 2026 IMPORTS ---
from langchain_text_splitters import RecursiveCharacterTextSplitter # Fixed typo
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
import streamlit as st
import os
os.environ["GOOGLE_API_KEY"] = "YOUR GOOGLE API KEY"

# This brings in the Agent 'Brain' we built in the previous phase
from agent import agent_executor

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Onboarding Buddy", page_icon="🚀")
st.title("🚀 AI Onboarding Agent")
st.markdown("Build your team connection and learn policies in seconds.")

# --- 2. SIDEBAR FOR FILE UPLOADS ---
with st.sidebar:
    st.header("📁 Knowledge Base")
    uploaded_pdf = st.file_uploader("Upload Welcome PDF", type="pdf")
    uploaded_excel = st.file_uploader("Upload Team Excel", type="xlsx")
    
    if st.button("Build Agent Memory"):
        if uploaded_pdf and uploaded_excel:
            with st.spinner("Processing files..."):
                # Save files locally so our agent can read them
                with open("data/welcome_guide.pdf", "wb") as f:
                    f.write(uploaded_pdf.getbuffer())
                with open("data/team_list.xlsx", "wb") as f:
                    f.write(uploaded_excel.getbuffer())
                
                # Trigger the 'Ingest' logic (simplified for UI)
                loader = PyPDFLoader("data/welcome_guide.pdf")
                data = loader.load()
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
                chunks = text_splitter.split_documents(data)
                
                embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
                vector_db = Chroma.from_documents(
                    documents=chunks, 
                    embedding=embeddings, 
                    persist_directory="./chroma_db"
                )
                st.success("Memory Built Successfully!")
        else:
            st.error("Please upload both files first.")

# --- 3. CHAT INTERFACE ---
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask me about the team or policies..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # We call the same agent_executor from your agent.py!
                response = agent_executor.invoke({"input": prompt})
                full_response = response["output"]
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Error: {e}")