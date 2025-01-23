# job_utils.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# ──────────────────────────────────────────────────────────
# Specify the FULL PATH to your ChromeDriver executable here.
# Example:
CHROMEDRIVER_PATH = "D:\LLM\Resume Parser\chromedriver-win64\chromedriver.exe.exe"
# ──────────────────────────────────────────────────────────

def fetch_job_html_with_selenium(url):
    """
    Fetch job posting page using headless Chrome + Selenium.
    Return the raw text from the page.
    """
    # Set Chrome to run in headless mode (without opening a browser window)
    options = Options()
    options.add_argument("--headless")

    # Initialize the driver service with the full ChromeDriver path
    driver_service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=driver_service, options=options)
    
    try:
        # Navigate to the specified URL
        driver.get(url)
        # Allow time for the page to load (increase if needed for slower pages)
        time.sleep(5)
        
        # Parse the page HTML with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # Return the text content of the page
        return soup.get_text()
    finally:
        # Always quit the browser, even if there's an error
        driver.quit()
