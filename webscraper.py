import requests
from bs4 import BeautifulSoup


class Webscraper():

    def __init__(self):
        self._headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.3"}


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

    def send_jobs_email(self):
        """
        Sets up the SMTP connection to allow an email
        to be sent, sends the email, and terminates the connection
        """
        pass

  