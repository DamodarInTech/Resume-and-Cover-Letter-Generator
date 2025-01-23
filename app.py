import streamlit as st
import json

# Local imports
from resume_utils import extract_text_from_pdf, clean_text, extract_skills_dynamic
from llm_utils import extract_data_with_llm, extract_job_details_with_llm, llm
from job_utils import fetch_job_html_with_selenium
from db_utils import save_to_chromadb, fetch_from_chromadb, reset_collection

# LangChain / LLM imports
from langchain.schema import HumanMessage

# ───────────────────────────────────────────────────────────
# Welcome & Intro
# ───────────────────────────────────────────────────────────
st.title("AI Resume & Job Description Parser")

st.write(
    """
    **Welcome!** This tool helps you generate custom professional communications 
    (cover letter, semi-formal email, and short LinkedIn/WhatsApp message) 
    in **under 30 seconds** based on your resume and a job posting.
    
    **Tech Used**:
    - **Llama Model** for text generation
    - **ChromaDB** for storing your data
    - **Streamlit** for this UI
    """
)

# Optional Reset Button (remove if not needed)
if st.button("Reset ChromaDB"):
    try:
        reset_collection("resume_data")
        reset_collection("job_data")
        st.success("ChromaDB collections reset successfully.")
    except Exception as e:
        st.error(f"Error resetting collections: {e}")

# ───────────────────────────────────────────────────────────
# Section: Upload Resume
# ───────────────────────────────────────────────────────────
st.subheader("Step 1: Upload Your Resume (PDF)")

uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

if uploaded_file is not None:
    try:
        raw_text = extract_text_from_pdf(uploaded_file)
        cleaned_text = clean_text(raw_text)
        extracted_skills = extract_skills_dynamic(cleaned_text)
        resume_data = extract_data_with_llm(cleaned_text, extracted_skills)
        save_to_chromadb("resume_data", resume_data)
        st.success("Resume successfully uploaded!")
    except Exception as e:
        st.error(f"Error processing the resume: {e}")

# ───────────────────────────────────────────────────────────
# Section: Enter Job Posting URL
# ───────────────────────────────────────────────────────────
st.subheader("Step 2: Enter Job Posting URL")

job_url = st.text_input("Paste the job posting URL here...")

if job_url:
    try:
        page_text = fetch_job_html_with_selenium(job_url)
        job_data = extract_job_details_with_llm(page_text)
        save_to_chromadb("job_data", job_data)
        st.success("Job link successfully uploaded!")
    except Exception as e:
        st.error(f"Error processing job details: {e}")

# ───────────────────────────────────────────────────────────
# Section: Generate Outputs
# ───────────────────────────────────────────────────────────
st.subheader("Step 3: Generate Cover Letter, Email & LinkedIn Msg")

if st.button("Generate All"):
    try:
        # Fetch the data from ChromaDB
        resume_docs = fetch_from_chromadb("resume_data")
        job_docs = fetch_from_chromadb("job_data")

        # Ensure we have at least 1 doc in each
        if not resume_docs["documents"] or not job_docs["documents"]:
            st.warning(
                "No resume or job data found in ChromaDB. "
                "Please upload your resume and job link first."
            )
        else:
            # Always pick the LAST document from each (the newest uploaded)
            resume_data = resume_docs["documents"][-1]
            job_data = job_docs["documents"][-1]

            # Single prompt generating multiple outputs
            prompt = f"""
            Using the following details:

            Resume Details:
            {json.dumps(resume_data, indent=2)}

            Job Description Details:
            {json.dumps(job_data, indent=2)}

            Generate the following outputs:

            1) A Professional Cover Letter (~400 words)
               - Start with "Dear Hiring Manager"
               - End with "Sincerely, [Your Name]".
            
            2) A Semi-Formal Email (~250 words) describing interest in the job.
            
            3) A short LinkedIn/WhatsApp message (~300 characters total) 
               explaining why you're interested in the position.

            Clearly separate each output with headings or labels.
            """

            message = HumanMessage(content=prompt)
            llm_response = llm.invoke([message])
            generated_text = llm_response.content.strip()

            # Display the result
            st.subheader("Generated Cover Letter, Email & LinkedIn Message")
            st.write(generated_text)

            # Optional: Save to a file
            with open("generated_content.txt", "w", encoding="utf-8") as file:
                file.write(generated_text)

            st.success("Content generated and saved to 'generated_content.txt'!")
    except Exception as e:
        st.error(f"Error generating content: {e}")

# ───────────────────────────────────────────────────────────
# Footer / Credits
# ───────────────────────────────────────────────────────────
st.write("---")
st.markdown(
    """
    **© 2025 @Damodar Prabhu**  
    **LinkedIn**: [Damodar Prabhu](https://www.linkedin.com/in/damodar-prabhu-b9207715a)  
    **Email**: [damodarprabhuwork@gmail.com](mailto:damodarprabhuwork@gmail.com)
    """
)
