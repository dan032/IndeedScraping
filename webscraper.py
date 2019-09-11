import requests
from bs4 import BeautifulSoup
import smtplib

class Webscraper():

    def __init__(self):
        self._headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.3"}
        self._jobDict = {}
        self._email = "Enter your email here"
        self._password = "Enter your App password for Google here"

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
        msg = self.create_email_message()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(self._email, self._password)
        server.sendmail(self._email, self._email, msg)
        server.quit()

    def create_email_message(self):
        """
        Creates the email message that is to be sent to
        the specified email, and populates it
        with the info from the jobDict dictionary
        """
        message_body = ''
        count = 0
        for job_tuple in self._jobDict.values():
            message_body += f'Title: {job_tuple[0]}\n'
            message_body += f'Company: {job_tuple[1]}\n'
            message_body += f'Description: {job_tuple[2]}\n'
            message_body += f'URL: {job_tuple[3]}\n\n'
            count += 1
            if count == 5:
                break

        subject = 'Job list!'
        body = message_body.encode('ascii', 'ignore').decode('ascii')
        msg = f"Subject: {subject}\n\n{body}"
        return msg