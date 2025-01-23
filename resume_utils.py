import fitz
import re

def extract_text_from_pdf(file):
    """
    Extract text from a PDF file (uploaded via Streamlit).
    Using PyMuPDF (fitz).
    """
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        text = []
        for page in doc:
            text.append(page.get_text())
        return " ".join(text)

def clean_text(text):
    # Simple cleaning: remove extra spaces, line breaks, etc.
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_skills_dynamic(text):
    """
    Basic example: look for known skill keywords in text.
    Expand as needed or use a more advanced approach.
    """
    skills_list = [
        "Python", "SQL", "Tableau", "Power BI", "C", "Java", "Excel",
        "Big Query", "Google Cloud Platform", "Alteryx", "Slack", 
        "Looker", "Data Modeling", "Microsoft Excel", "MS PowerPoint", 
        "Jira", "Pandas", "NumPy", "Matplotlib", "MS Word", "Outlook"
    ]
    found_skills = []
    for skill in skills_list:
        if skill.lower() in text.lower():
            found_skills.append(skill)
    return found_skills
