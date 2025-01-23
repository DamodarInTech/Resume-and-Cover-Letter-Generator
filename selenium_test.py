from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time

# Path to ChromeDriver executable
CHROMEDRIVER_PATH = "D:/LLM/Resume Parser/chromedriver-win64/chromedriver.exe"

# Configure Selenium options
options = Options()
options.add_argument("--headless")  # Run in headless mode (no browser window)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# Test URL
url = "https://jobs.nike.com/job/R-48596?from=job%20search%20funnel"

try:
    # Open the URL
    print(f"Fetching data from: {url}")
    driver.get(url)
    time.sleep(5)  # Wait for the page to load

    # Fetch the page source
    page_source = driver.page_source

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Extract specific fields
    job_title = soup.find('h1').get_text(strip=True) if soup.find('h1') else "Not Available"
    location = soup.find('div', class_='job-location').get_text(strip=True) if soup.find('div', class_='job-location') else "Not Available"
    job_description = soup.find('div', class_='job-description').get_text(strip=True) if soup.find('div', class_='job-description') else "Not Available"
    company_info = soup.find('div', class_='about-company').get_text(strip=True) if soup.find('div', class_='about-company') else "Not Available"

    # Structure the data
    job_data = {
        "Job Title": job_title,
        "Location": location,
        "Job Description": job_description[:500],  # Truncate if too long
        "Company Info": company_info[:500],  # Truncate if too long
    }

    # Print the extracted data
    print("Extracted Job Details (JSON):")
    print(json.dumps(job_data, indent=4))

    # Save to JSON file
    with open("job_data.json", "w", encoding="utf-8") as json_file:
        json.dump(job_data, json_file, indent=4)
        print("Extracted job data saved to 'job_data.json'.")

finally:
    # Close the WebDriver
    driver.quit()
