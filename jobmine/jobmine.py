import time
import json

from jobmine import urls
from jobmine import ids
from jobmine.exceptions import LoginFailed

from unidecode import unidecode
from bs4 import BeautifulSoup
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.common.exceptions import NoSuchElementException


HTML_PARSER = 'html.parser'


class JobMineQuery(object):

    def __init__(self, term, employer_name, job_title, disciplines, levels):
        self.term = term
        self.employer_name = employer_name
        self.job_title = job_title
        self.disciplines = disciplines
        self.levels = levels


class JobMineDriver(webdriver.PhantomJS):

    def _find_eles_by_id_and_send(self, data):
        for _id in data:
            ele = self.find_element_by_id(_id)

            ele.clear()
            ele.send_keys(data[_id])

    @contextmanager
    def wait_for_page_load(self, timeout=10):
        old_page = self.find_element_by_tag_name('html')
        yield
        WebDriverWait(self, timeout).until(staleness_of(old_page))

    @contextmanager
    def wait_for_element_stale(self, element_id, timeout=10):
        element = self.find_element_by_id(element_id)
        yield
        WebDriverWait(self, timeout).until(staleness_of(element))


class Job(object):

    def __init__(self, browser, data):
        self.browser = browser
        self.id = data['id']
        self.data = data

    @classmethod
    def from_row(cls, browser, row):
        """used to construct Job from row in search results"""
        col_names = ['id', 'title', 'employer', 'unit', 'location', 'num_openings', 'app_status', 'num_apps', 'app_deadline']
        return cls(browser, dict(zip(col_names, row)))

    def __repr__(self):
        return json.dumps(self.data)

    def get_detailed_info(self):
        with self.browser.wait_for_page_load():
            self.browser.get(urls.JOB_PROFILE + self.id)

        soup = BeautifulSoup(self.browser.page_source, HTML_PARSER)

        detailed_data = {
            'posting_open_date':      soup.find(id = ids.POSTING_OPEN_DATE).text,
            'last_day_to_apply':      soup.find(id = ids.LAST_DAY_TO_APPLY).text,
            'employer_job_number':    soup.find(id = ids.EMPLOYER_JOB_NUMBER).text,
            'employer':               soup.find(id = ids.EMPLOYER).text,
            'job_title':              soup.find(id = ids.JOB_TITLE).text,
            'work_location':          soup.find(id = ids.WORK_LOCATION).text,
            'available_openings':     soup.find(id = ids.AVAILABLE_OPENINGS).text,
            'hiring_process_support': soup.find(id = ids.HIRING_PROCESS_SUPPORT).text,
            'work_term_support':      soup.find(id = ids.WORK_TERM_SUPPORT).text,
            'comments':               soup.find(id = ids.COMMENTS).text,
            'job_description':        soup.find(id = ids.JOB_DESCRIPTION).text
        }

        disciplines = soup.find(id = ids.DISCIPLINES).text
        disciplines_more = soup.find(id = ids.DISCIPLINES_MORE).text
        detailed_data['disciplines'] = (disciplines + ', ' + disciplines_more).split(', ')

        detailed_data['levels'] = soup.find(id = ids.LEVELS).text.split(', ')
        detailed_data['grades_required'] = soup.find(id = ids.GRADES).text == 'Required'

        self.data.update(detailed_data)

        return self.data


class JobMine(object):

    def __init__(self, username, password):
        self.last_query = None
        self.last_results = []

        self.browser = JobMineDriver('phantomjs')

        self.authorized = False
        self.login(username, password) # on success sets authorized to True

    def __del__(self):
        self.browser.quit()

    def login(self, username, password):
        with self.browser.wait_for_page_load():
            self.browser.get(urls.LOGIN)

        data = {'userid': username, 'pwd': password}
        self.browser._find_eles_by_id_and_send(data)

        with self.browser.wait_for_page_load():
            self.browser \
                .find_element_by_id(ids.LOGIN) \
                .find_element_by_xpath('//input[@type=\'submit\'][@name=\'submit\']') \
                .submit()

        try:
            login_err = self.browser.find_element_by_class_name('PSERRORTEXT').text
            raise LoginFailed(login_err)
        except NoSuchElementException:
            self.authorized = True

    def get_num_apps_remaining(self):
        if not hasattr(self, 'num_apps_remaining'):
            self.browser.get(urls.SEARCH)
            self.num_apps_remaining = int(self.browser.find_element_by_id(ids.NUM_APPS_REMAINING).text)

        return self.num_apps_remaining

    def find_jobs(self, term=1165, employer_name='', job_title='',
                  disciplines=['ENG-Software', 'MATH-Computer Science', 'MATH-Computing & Financial Mgm'],
                  levels=['junior', 'intermediate', 'senior']):
        jmquery = JobMineQuery(term, employer_name, job_title, disciplines, levels)
        return self.find_jobs_with_query(jmquery)

    def find_jobs_with_query(self, query):
        with self.browser.wait_for_page_load():
            self.browser.get(urls.SEARCH)

        # inject search parameters into page
        self._set_disciplines(query.disciplines)
        self._set_text_search_params(query.term, query.employer_name, query.job_title)
        self._set_levels(query.levels)

        time.sleep(0.5) # TODO: figure out a better solution

        # basically wait until search has been executed and
        # jobmine has reload the first job component
        with self.browser.wait_for_element_stale(element_id=ids.FIRST_JOB):
            self.browser.find_element_by_id(ids.SEARCH_BUTTON).click()
            #time.sleep(2)

        jobs = self._scrape_jobs()

        # cache last query and results
        self.last_results = jobs
        self.last_query = query

        return jobs

    def _scrape_jobs(self):
        jobs = []

        while True:
            soup = BeautifulSoup(self.browser.page_source, HTML_PARSER)

            ungrouped_jobs = []
            for ele_id in ids.JOB_LISTING_COLUMNS:
                spans = soup.findAll('span', id=lambda x: x and x.startswith(ele_id))
                ungrouped_jobs.append([unidecode(span.text).strip() for span in spans])

            grouped_jobs = list(zip(*ungrouped_jobs))

            # check if first job id is invalid incase no matches found
            if grouped_jobs[0][0] == '':
                return []

            jobs.extend([Job.from_row(self.browser, row) for row in grouped_jobs])

            # check if we are on the last page of search results
            try:
                with self.browser.wait_for_element_stale(element_id=ids.FIRST_JOB):
                    self.browser.find_element_by_id(ids.NEXT_PAGE_BUTTON).click()
            except NoSuchElementException:
                break

        return jobs

    def _set_text_search_params(self, term, employer_name, job_title):
        data = {
            'UW_CO_JOBSRCH_UW_CO_WT_SESSION': term,
            'UW_CO_JOBSRCH_UW_CO_EMPLYR_NAME': employer_name,
            'UW_CO_JOBSRCH_UW_CO_JOB_TITLE': job_title
        }
        self.browser._find_eles_by_id_and_send(data)

    def _set_disciplines(self, disciplines):
        discip_xpath = "//select[@name='UW_CO_JOBSRCH_UW_CO_ADV_DISCP%d']/option[text()='%s']"

        for i in range(len(disciplines)):
            self.browser.find_element_by_xpath(discip_xpath % (i + 1, disciplines[i])).click()

    def _set_levels(self, levels):
        level_elements = {
            'junior': self.browser.find_element_by_id(ids.LEVEL_JUNIOR),
            'intermediate': self.browser.find_element_by_id(ids.LEVEL_INTERMEDIATE),
            'senior': self.browser.find_element_by_id(ids.LEVEL_SENIOR),
            'bachelor': self.browser.find_element_by_id(ids.LEVEL_BACHELOR),
            'masters': self.browser.find_element_by_id(ids.LEVEL_MASTERS),
            'phd': self.browser.find_element_by_id(ids.LEVEL_PHD)
        }

        for name, ele in level_elements.items():
            if (name in levels and not ele.is_selected()) or \
               (name not in levels and ele.is_selected()):
                ele.click()

