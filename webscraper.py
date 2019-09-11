import requests
from bs4 import BeautifulSoup


class Webscraper():

    def __init__(self):
        self._headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.3"}
        self._jobDict = {}


    def get_jobs(self):
        """
        Sends an HTTP Get Request to specified URL
        and returns all jobs listed on webpage
        """
        url = self.create_url()
        r = requests.get(url, headers=self._headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        jobs = soup.find_all("div", class_='jobsearch-SerpJobCard')
        return jobs

    def create_url(self):
        """
        Asks the user for their search terms and location and concatanates
        them into the proper URL string for indeed.ca
        """
        search_terms = input("\nWhat are your search parameters: ")
        search_term = search_terms.replace(" ", "+")
        location = input("\nWhere do you live: ")
        url = f'https://www.indeed.ca/jobs?q={search_term}&l={location}'
        return url
    
    def populate_jobs_dictionary(self, jobs):
        """
        Populates the jobDict dictionary, where the
        keys are ascending ID's made locally, and
        the values are a tuple containing the job title,
        company, description and URL for the ad
        """
        job_id = 0
        for job in jobs:
            job_id += 1

            title = job.find("div", class_="title").find("a", class_="jobtitle").text.strip()
            title_url = job.find("div", class_="title").find("a", class_="jobtitle")['href']
            job_url = f'indeed.ca{title_url}'
            company = job.find("div", class_="sjcl").find("span").text.strip()
            description = job.find("div", class_="summary").text.strip()
            self._jobDict[job_id] = (title, company, description, job_url)

    def send_jobs_email(self):
        """
        Sets up the SMTP connection to allow an email
        to be sent, sends the email, and terminates the connection
        """
        pass

  