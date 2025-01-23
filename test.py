from langchain.schema import HumanMessage  # Correct import path
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize LLM
llm = ChatGroq(
    temperature=0,
    groq_api_key=os.getenv("groq_api_key"),
    model_name="llama3-70b-8192"
)

# Create a HumanMessage object
prompt = "Hello! Can you extract structured data from this text?"
message = HumanMessage(content=prompt)

# Send the prompt to the LLM
try:
    response = llm.invoke([message])  # Use the invoke method
    print("LLM Response:", response.content)
except Exception as e:
    print(f"Error: {e}")
