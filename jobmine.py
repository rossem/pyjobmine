import time
import bs4
import urls
import ids

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class JobMineQuery(object):

    def __init__(self, term, employer_name, job_title, disciplines, levels):
        self.term = term
        self.employer_name = employer_name
        self.job_title = job_title
        self.disciplines = disciplines
        self.levels = levels


class JobMine(object):

    def __init__(self, username, password, sleep_delay = 0):
        self.username = username
        self.password = password
        self.sleep_delay = sleep_delay

        self.last_query = None
        self.last_results = {}

        self.browser = webdriver.PhantomJS()

        self._login()


    def _login(self):
        self.browser.get(urls.LOGIN)
        self._sleep(2)

        data = {'userid': self.username, 'pwd': self.password}
        self._find_eles_by_id_and_send(data)

        self.browser.find_element_by_id("login").find_element_by_xpath("//input[@type='submit'][@name='submit']").submit()

    
    def close(self):
        self.browser.close()
        self.browser = None


    def find_jobs_with_last_query(self, query):
        if self.last_query is not None:
            self.find_jobs_with_query(self.last_query)
        else:
            print('You have not made a job query yet.')


    def find_jobs(self, term = 1165, employer_name = "", job_title = "",
                  disciplines = ["ENG-Software", "MATH-Computer Science", "MATH-Computing & Financial Mgm"],
                  levels = ['junior', 'intermdiate', 'senior']):
        self.find_jobs_with_query(JobMineQuery(term, employer_name, job_title, disciplines, levels))


    def find_jobs_with_query(self, query):
        self.browser.get(urls.SEARCH)

        self._sleep(2)

        # save query in case they wanna redo the search
        self.last_query = query

        # inject search parameters into page
        self._set_disciplines(query)
        self._set_text_search_params(query)
        self._set_levels(query)

        self._sleep(0.5)

        self.browser.find_element_by_id(ids.SEARCH_BUTTON).click()

        self._sleep(2)

        job_ids = self.get_job_ids()
        jobs = [self.scrape_job(job_id) for job_id in job_ids]
        self.last_results = jobs

        return jobs

        
    def get_job_ids(self):
        job_ids = []
        no_pages_left = False

        while not no_pages_left:
            soup = bs4.BeautifulSoup(self.browser.page_source)
            job_spans = soup.findAll('span', id=lambda x: x and x.startswith(ids.JOB_ID_GENERIC))
            job_ids.extend([span.text for span in job_spans])

            # check if we are on the last page of search results 
            try:
                self.browser.find_element_by_id(ids.NEXT_PAGE_BUTTON).click()
                self._sleep(0.1)
            except NoSuchElementException:
                no_pages_left = True

        # if no results, there is still one row in the table which we can filter out
        if job_ids == ['\xa0']:
            return []

        return job_ids


    def scrape_job(self, job_id):
        self.browser.get(urls.JOB_PROFILE + job_id)
        
        self._sleep(2)

        soup = bs4.BeautifulSoup(self.browser.page_source)

        job_data = {
            'job_id':                 job_id,
            'posting_open_date':      soup.find(id = ids.POSTING_OPEN_DATE).text,
            'last_day_to_apply':      soup.find(id = ids.LAST_DAY_TO_APPLY).text,
            'employer_job_number':    soup.find(id = ids.EMPLOYER_JOB_NUMBER).text,
            'employer':               soup.find(id = ids.EMPLOYER).text,
            'job_title':              soup.find(id = ids.JOB_TITLE).text,
            'work_location':          soup.find(id = ids.WORK_LOCATION).text,
            'grades':                 soup.find(id = ids.GRADES).text,
            'available_openings':     int(soup.find(id = ids.AVAILABLE_OPENINGS).text),
            'disciplines':            soup.find(id = ids.DISCIPLINES).text,
            'disciplines_more':       soup.find(id = ids.DISCIPLINES_MORE).text,
            'levels':                 soup.find(id = ids.LEVELS).text,
            'hiring_process_support': soup.find(id = ids.HIRING_PROCESS_SUPPORT).text,
            'work_term_support':      soup.find(id = ids.WORK_TERM_SUPPORT).text,
            'comments':               soup.find(id = ids.COMMENTS).text,
            'job_description':        soup.find(id = ids.JOB_DESCRIPTION).text
        }

        return job_data


    def _set_text_search_params(self, query):
        data = {
            'UW_CO_JOBSRCH_UW_CO_WT_SESSION': query.term,
            'UW_CO_JOBSRCH_UW_CO_EMPLYR_NAME': query.employer_name,
            'UW_CO_JOBSRCH_UW_CO_JOB_TITLE': query.job_title
        }
        self._find_eles_by_id_and_send(data)


    def _set_disciplines(self, query):
        discip_xpath = "//select[@name='UW_CO_JOBSRCH_UW_CO_ADV_DISCP%d']/option[text()='%s']"
        
        for i in range(len(query.disciplines)):
            self.browser.find_element_by_xpath(discip_xpath % (i + 1, query.disciplines[i])).click()


    def _set_levels(self, query):
        level_elements = {
            'junior': self.browser.find_element_by_id("UW_CO_JOBSRCH_UW_CO_COOP_JR"),
            'intermdiate': self.browser.find_element_by_id("UW_CO_JOBSRCH_UW_CO_COOP_INT"),
            'senior': self.browser.find_element_by_id("UW_CO_JOBSRCH_UW_CO_COOP_SR")
        }

        for name, ele in level_elements.items():
            if (name in query.disciplines and not ele.is_selected()) or \
               (name not in query.disciplines and ele.is_selected()):
               ele.click()


    def _find_eles_by_id_and_send(self, data):
        for id in data:
            ele = self.browser.find_element_by_id(id)

            ele.clear()
            ele.send_keys(data[id])


    def _sleep(self, t):
        time.sleep(self.sleep_delay + t)

