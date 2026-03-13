<<<<<<< HEAD
# ai-onboarding-agent
=======
# 🤖 Enterprise Onboarding Agent (Gemini 3.1)

A professional AI Agent designed to streamline the employee onboarding experience. This agent uses **RAG** (Retrieval-Augmented Generation) to answer policy questions from PDFs and **Function Calling** to retrieve teammate details from Excel.

## 🚀 The 6-Phase Workflow
This project was built using a structured AI-Architect methodology:
1. **Brainstorming:** Defining project scope and data requirements with Gemini.
2. **Architecture:** Mapping the flow between Unstructured (PDF) and Structured (Excel) data.
3. **Environment:** Setting up a stable Python Virtual Environment.
4. **Ingestion:** Converting PDFs into searchable semantic embeddings via ChromaDB.
5. **The Agent:** Building a ReAct-based agent using Gemini 3.1 Flash Lite.
6. **Interface:** Deploying a professional Web UI using Streamlit.

## 🛠️ Tech Stack
- **LLM:** Google Gemini 3.1 Flash Lite
- **Framework:** LangChain (Modular 2026 version)
- **Vector DB:** ChromaDB
- **UI:** Streamlit
- **Data:** Pandas & OpenPyXL

## 📂 Project Structure
- `agent.py`: The reasoning "Brain" of the assistant.
- `app.py`: The Streamlit web interface.
- `ingest.py`: The document processing script.
- `data/`: Sample company policies and team directories.
>>>>>>> cadc9ea (First build)
