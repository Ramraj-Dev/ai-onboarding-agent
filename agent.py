import os
import pandas as pd
import time

# --- 2026 MODULAR IMPORTS ---
# We use 'langchain_classic' for the stable ReAct agent logic
from langchain_classic.agents import AgentExecutor, create_react_agent
# 'langchain_core' for the base structures (Tools & Prompt Templates)
from langchain_core.tools import Tool
from langchain_core.prompts import PromptTemplate
# Official Google-LangChain bridge
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
# Local vector database connector
from langchain_chroma import Chroma

# --- CONFIGURATION ---
GOOGLE_API_KEY = "YOUR GOOGLE API KEY"

# --- STEP 1: CONNECT TO THE PDF "SEMANTIC MEMORY" ---
# Uses the same embedding model from your ingest.py script
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001", 
    google_api_key=GOOGLE_API_KEY
)

# Connects to the 'chroma_db' folder you created earlier
vector_db = Chroma(
    persist_directory="./chroma_db", 
    embedding_function=embeddings
)

def search_pdf(query):
    """Searches the PDF for policy details (WiFi, Friday rules, etc.)"""
    # Pulls the 2 most relevant text chunks from the database
    docs = vector_db.similarity_search(query, k=2)
    return "\n".join([d.page_content for d in docs])

# --- STEP 2: CONNECT TO THE EXCEL "STRUCTURED DIRECTORY" ---
def get_team_info(name_query):
    """Searches Excel for colleague details (Role, Dept, Fun Fact)."""
    try:
        # Load your data/team_list.xlsx file
        df = pd.read_excel("data/team_list.xlsx")
        
        # Look for the name in the 'Full Name' column (case-insensitive)
        result = df[df['Full Name'].str.contains(name_query, case=False, na=False)]
        
        if not result.empty:
            data = result.iloc[0].to_dict()
            return (f"Found: {data['Full Name']}. Role: {data['Role']}. "
                    f"Dept: {data['Department']}. Email: {data['Email']}. "
                    f"Fun Fact: {data['Fun Fact']}")
        return "Teammate not found in the Excel list."
    except Exception as e:
        return f"Error reading Excel sheet: {e}"

# --- STEP 3: ARMED WITH TOOLS ---
# We describe the tools so the AI knows 'why' and 'when' to use them
tools = [
    Tool(
        name="Policy_Search",
        func=search_pdf,
        description="Search this for policy info from the PDF like benefits or WiFi."
    ),
    Tool(
        name="Team_Directory",
        func=get_team_info,
        description="Search this for colleague details from Excel like Fun Facts or Roles."
    )
]

# --- STEP 4: DEFINE THE REASONING (PROMPT) ---
# This 'ReAct' template forces the AI to Think, Act, and Observe in a loop
template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)

# --- STEP 5: INITIALIZE THE BRAIN (2026 FLASH LITE) ---
# We use Flash Lite to avoid 'Quota Exhausted' errors on free tier accounts
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite-preview", 
    google_api_key=GOOGLE_API_KEY,
    temperature=0,
    max_retries=5, # Automatically retries if the server is busy
    timeout=120     # Wait up to 2 minutes for the AI to respond
)

# Build the agent and the executor
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True, # This lets us see the AI's 'thoughts' in the terminal
    handle_parsing_errors=True
)

# --- STEP 6: RUN THE AGENT ---
if __name__ == "__main__":
    query = (
        "I'm a new hire. Look up 'Arjun Mehra' in the team list and find their fun fact. "
        "Then check the PDF for the 'Friday' policy. "
        "Finally, write a 'Hi' email to Arjun Mehra mentioning their fun fact."
    )
    
    print("--- 🚀 AI Agent Starting Onboarding Task ---\n")
    
    try:
        result = agent_executor.invoke({"input": query})
        print("\n--- ✅ FINAL RESPONSE ---\n")
        print(result["output"])
    except Exception as e:
        if "429" in str(e):
            print("\n❌ QUOTA HIT: The agent is too fast for the free tier.")
            print("Action: Wait 60 seconds and run it again.")
        else:
            print(f"\n❌ UNEXPECTED ERROR: {e}")