from selenium import webdriver

search_url = "https://jobmine.ccol.uwaterloo.ca/psc/SS/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBSRCH" 
login_url = "https://jobmine.ccol.uwaterloo.ca/psp/SS/EMPLOYEE/WORK/"
job_url = "https://jobmine.ccol.uwaterloo.ca/psc/SS_2/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBDTLS.GBL?UW_CO_JOB_ID="

class JobmineQuery(object):
    def __init__(self, term = 1165, employer_name = "", job_title = "", disciplines = ["ENG-Software", "MATH-Computer Science", "MATH-Computing & Financial Management"], levels = ['junior', 'intermdiate', 'senior']):
        self.term = term
        self.employer_name = employer_name
        self.job_title = job_title
        self.disciplines = disciplines
        self.levels = levels

class Jobmine(object):
    def __init__(self, username, password, sleep_delay = 0):
        self.username = username
        self.password = password
        self.sleep_delay = sleep_delay
        self.last_query = None

        self.browser = webdriver.Firefox()

        self._login()


    def find_jobs(self, query):
        # save query in case they wanna redo the search
        self.last_query = query

        # inject search parameters into page
        self._set_disciplines(query)
        self._set_text_search_params(query)
        self._set_levels(query)

        self.browser.find_element_by_id("UW_CO_JOBSRCHDW_UW_CO_DW_SRCHBTN").click()

        self._sleep(4)

        job_ids = self.get_job_ids()

        jobs = [scrape_job(job_id) for job_id in job_ids]

        
    def get_job_ids(self):
        soup = bs4.BeautifulSoup(browser.page_source)
        job_spans = soup.findAll('span', id=lambda x: x and x.startswith('UW_CO_JOBRES_VW_UW_CO_JOB_ID'))

        return [span.text for span in job_spans]


    def scrape_job(self, job_id):
        browser.get(job_url + job_id)
        
        self._sleep(2)

        soup = bs4.BeautifulSoup(browser.page_source)

        job_data = {
            'job_id': job_id
            'posting open date': soup.find(id = "UW_CO_JOBDTL_VW_UW_CO_CHAR_EDATE").text,
            'last day to apply': soup.find(id = "UW_CO_JOBDTL_VW_UW_CO_CHAR_DATE").text,
            'emp job #': soup.find(id = "UW_CO_JOBDTL_VW_UW_CO_EMPOWN_JOBNO").text,
            'employer': soup.find(id = "UW_CO_JOBDTL_DW_UW_CO_EMPUNITDIV").text,
            'job title': soup.find(id = "UW_CO_JOBDTL_VW_UW_CO_JOB_TITLE").text,
            'work location': soup.find(id = "UW_CO_JOBDTL_VW_UW_CO_WORK_LOCATN").text,
            'grades': soup.find(id = "UW_CO_JOBDTL_DW_UW_CO_MARKS_DRVD").text,
            'available openings': intsoup.find(id = "_VW_UW_CO_AVAIL_OPENGS").text,
            'disciplines': soup.find(id = "UW_CO_JOBDTL_DW_UW_CO_DESCR").text,
            'disciplines1': soup.find(id = "UW_CO_JOBDTL_DW_UW_CO_DESCR100").text,
            'levels': soup.find(id = "UW_CO_JOBDTL_DW_UW_CO_DESCR_100").text,
            'hiring process support': soup.find(id = "UW_CO_OD_DV2_UW_CO_NAME").text,
            'work term support': soup.find(id = "UW_CO_OD_DV2_UW_CO_NAME2").text,
            'comments': soup.find(id = "UW_CO_JOBDTL_VW_UW_CO_JOB_SUMMARY").text,
            'job description': soup.find(id = "UW_CO_JOBDTL_VW_UW_CO_JOB_DESCR").text
        }

        return job_data


    def _set_text_search_params(self, query):
        payload = {
            'UW_CO_JOBSRCH_UW_CO_WT_SESSION': query.term,
            'UW_CO_JOBSRCH_UW_CO_EMPLYR_NAME': query.employer_name,
            'UW_CO_JOBSRCH_UW_CO_JOB_TITLE': query.job_title
        }
        self.find_eles_by_id_and_send(payload)


    def _set_disciplines(self, query):
        discip_xpath = "//select[@name='UW_CO_JOBSRCH_UW_CO_ADV_DISCP%d']/option[text()='%s']"
        
        for i in range(len(query.disciplines)):
            self.browser.find_element_by_xpath(discip_xpath % (i + 1, query.disciplines[i])).click()


    def _set_levels(self, query):
        level_elements = {
            'junior': browser.find_element_by_id("UW_CO_JOBSRCH_UW_CO_COOP_JR")
            'intermdiate': browser.find_element_by_id("UW_CO_JOBSRCH_UW_CO_COOP_INT")
            'senior': browser.find_element_by_id("UW_CO_JOBSRCH_UW_CO_COOP_SR")
        }

        for name, ele in level_elements.iteritems():
            if (name in query.disciplines and not ele.is_selected()) or \
               (name not in query.disciplines and ele.is_selected()):
               ele.click()


    def _login(self):
        self.browser.get(login_url)
        self._sleep(2)

        payload = {'user_id': self.user_id, 'pwd': self.password}
        self.find_eles_by_id_and_send(payload)

        browser.find_element_by_id("login").find_element_by_xpath("//input[@type='submit'][@name='submit']").submit()


    def find_eles_by_id_and_send(self, payload):
        for id, key in payload.iteritems():
            self.browser.find_element_by_id(data[id]).send_keys(data[key])


    def _sleep(t):
        time.sleep(self.sleep_delay + t)
