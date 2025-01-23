 AI Resume & Job Description Parser

This Streamlit application allows you to upload your resume and fetch job details from a URL. It then uses LLM (Llama model) to generate:

1. A Professional Cover Letter (~400 words)  
2. A SemiFormal Email (~250 words)  
3. A Short LinkedIn/WhatsApp Message (~300 characters)  

Everything is stored in ChromaDB for quick data retrieval.  

> Author: @Damodar Prabhu  
> LinkedIn: [Damodar Prabhu](https://www.linkedin.com/in/damodarprabhub9207715a)  
> Email: [damodarprabhuwork@gmail.com](mailto:damodarprabhuwork@gmail.com)  



 Table of Contents

1. [Tech Stack](techstack)  
2. [Features](features)  
3. [Prerequisites](prerequisites)  
4. [Installation](installation)  
5. [Project Structure](projectstructure)  
6. [Usage](usage)  
7. [License](license)  



 Tech Stack

 Python 3.9+  
 Streamlit (UI)  
 ChromaDB (Local storage for resume/job data)  
 Selenium + ChromeDriver (fetch job postings)  
 PyMuPDF (fitz) (extract text from PDF)  
 LangChain & langchain_groq (LLM prompt handling)  
 Llama model (via `ChatGroq`)  



 Features

 Upload Resume (PDF): Extract text, parse structured data (skills, education, work experience, projects) via an LLM.  
 Fetch Job Data from URL: Use Selenium + BeautifulSoup to grab the job posting text, then parse it via an LLM.  
 Generate Customized Writings:
   A 400word cover letter.  
   A 250word semiformal email.  
   A 300character LinkedIn/WhatsApp message.  
 ChromaDB Persistence: Resume and job data remain stored locally for reuse until reset.  



 Prerequisites

1. Python 3.9+  
2. Chrome Browser (matching version of ChromeDriver)  
3. A Groq API key (for ChatGroq LLM). Stored in a `.env` file as `GROQ_API_KEY=YOUR_KEY`.  



 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/airesumejobparser.git](https://github.com/DamodarInTech/Resume-and-Cover-Letter-Generator)
   cd airesumejobparser
   ```
2. Create a virtual environment (optional, but recommended):
   ```bash
   python m venv venv
   source venv/bin/activate   or venv\Scripts\activate on Windows
   ```
3. Install dependencies:
   ```bash
   pip install r requirements.txt
   ```
4. Set up `.env`:
   ```
    .env file
   GROQ_API_KEY=YOUR_GROQ_API_KEY
   ```
5. Configure ChromeDriver:
    Either place your `chromedriver.exe` in a known path, or
    Use the webdriver_manager approach, or
    Explicitly specify the full path in `job_utils.py`:
     ```python
     CHROMEDRIVER_PATH = "D:\\LLM\\Resume Parser\\chromedriverwin64\\chromedriver.exe"
     ```
   Make sure the ChromeDriver version matches your installed Chrome browser.



 Project Structure

```
.
├── app.py
├── db_utils.py
├── job_utils.py
├── llm_utils.py
├── resume_utils.py
├── requirements.txt
├── .env           Contains GROQ_API_KEY
└── chroma_storage/   Created automatically by ChromaDB
```

 app.py: Main Streamlit application.  
 db_utils.py: Utility functions for saving/fetching/deleting data in ChromaDB.  
 llm_utils.py: Functions to call the LLM (Llama model via ChatGroq) to parse resume/job data.  
 resume_utils.py: PDF text extraction and simple skill parsing.  
 job_utils.py: Seleniumbased function to fetch job posting text from a URL.  



 Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
2. Open your browser's provided local URL (usually `http://localhost:8501`).
3. Upload your resume (PDF only). 
    You’ll see “Resume successfully uploaded!”.
4. Paste a job posting URL. 
    You’ll see “Job link successfully uploaded!”.
5. Click “Generate All” to produce:
    A ~400word cover letter (formal, starts with “Dear Hiring Manager”)  
    A ~250word semiformal email  
    A ~300character LinkedIn/WhatsApp message  
6. Output is displayed onscreen and also saved to `generated_content.txt`.

Note: If you want to reset the entire database (remove stored resume/job data), click “Reset ChromaDB”.



 License

© 2025 [Damodar Prabhu](https://www.linkedin.com/in/damodarprabhub9207715a).  

Feel free to adapt or modify for personal use. For commercial use, please contact the author.
