from webscraper import Webscraper
import time

class Application:

    def __init__(self):
        self._webscraper = Webscraper()
    
    def main(self):
        while True:
            jobs = self._webscraper.get_jobs()
            self._webscraper.populate_jobs_dictionary(jobs)
            self._webscraper.send_jobs_email()
            time.sleep(86400)
