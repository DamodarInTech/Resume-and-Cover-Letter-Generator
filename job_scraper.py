import requests
from bs4 import BeautifulSoup

def scrape_job_data(job_url):
    """
    Scrapes job information from the given job URL.

    Args:
        job_url (str): URL of the job posting.

    Returns:
        dict: A dictionary containing the job's key information.
    """
    try:
        # Make a GET request to the job URL
        response = requests.get(job_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract key information (adjust selectors based on the website's structure)
        job_title = soup.find("h1").text.strip() if soup.find("h1") else "N/A"
        location = soup.find("div", {"class": "job-location"}).text.strip() if soup.find("div", {"class": "job-location"}) else "N/A"
        about_company = soup.find("div", {"class": "about-company"}).text.strip() if soup.find("div", {"class": "about-company"}) else "N/A"
        job_description = soup.find("div", {"class": "job-description"}).text.strip() if soup.find("div", {"class": "job-description"}) else "N/A"

        # Assume job requirements are in a list under a specific class
        job_requirements = soup.find("ul", {"class": "job-requirements"})
        requirements = [li.text.strip() for li in job_requirements.find_all("li")] if job_requirements else []

        # Structure the data in a dictionary
        job_data = {
            "Job Title": job_title,
            "Location": location,
            "About Company": about_company,
            "Job Description": job_description,
            "Job Requirements": requirements,
        }

        return job_data

    except Exception as e:
        print(f"Error scraping job data: {e}")
        return {}
