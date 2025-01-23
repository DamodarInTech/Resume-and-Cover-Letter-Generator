import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables from .env
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY", "")

llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama3-70b-8192",  # my model
    temperature=0,
)

def extract_data_with_llm(text, skills):
    """
    Use LLM to parse resume text into structured JSON (dict).
    """
    prompt = f"""
    Parse the following resume text into structured JSON with these fields:
    1. Skills: (already known) => {skills}
    2. Education: Extract degree, university, and years attended.
    3. Work Experience: job title, company, duration, responsibilities.
    4. Projects: title and description.

    Resume Text:
    {text}
    """
    response = llm.invoke([{"role": "user", "content": prompt}])
    content = response.content

    # Try to parse the response as JSON
    try:
        parsed_data = json.loads(content)
    except json.JSONDecodeError:
        # Fallback if the LLM doesn't return valid JSON
        parsed_data = {
            "Skills": skills,
            "Education": [],
            "Work Experience": [],
            "Projects": [],
            "raw_llm_output": content,
        }
    return parsed_data

def extract_job_details_with_llm(job_text):
    """
    Use LLM to parse job posting text into structured JSON.
    """
    prompt = f"""
    Extract the following details from the job posting text in JSON format:
    - Job Title
    - Location
    - Job Requirements
    - Company Info

    Job Posting Text:
    {job_text}
    """
    response = llm.invoke([{"role": "user", "content": prompt}])
    content = response.content

    try:
        parsed_data = json.loads(content)
    except json.JSONDecodeError:
        parsed_data = {
            "Job Title": "",
            "Location": "",
            "Job Requirements": [],
            "Company Info": "",
            "raw_llm_output": content,
        }
    return parsed_data
