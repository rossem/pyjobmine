# WHY IS JOBMINE DOWN AT NIGHT????!?!?!?!?!?!? ugh
import requests
import json

import bs4

import mechanize

import selenium


search_url = "https://jobmine.ccol.uwaterloo.ca/psc/SS/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBSRCH" #find this
login_url = "https://jobmine.ccol.uwaterloo.ca/psp/SS/?cmd=login"
job_url = "https://jobmine.ccol.uwaterloo.ca/psp/SS_2/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBDTLS.GBL?UW_CO_JOB_ID="

"""
br = mechanize.Browser()
br.set_handle_refresh(False)


def login_jobmine(userid, pwd): #dis works
    br.open(login_url)          #i think
    br.select_form('login')
    br.form['userid'] = userid
    br.form['pwd'] = pwd
    br.submit()
    return br.response()

print login_jobmine("", "")


def search_jobs(search_url):
    job_urls = []
    br.open(search_url)
    br.select_form(nr=0)
    form = br.form

    form['UW_CO_JOBSRCH_UW_CO_WT_SESSION'] = '1155'
    form['UW_CO_JOBSRCH_UW_CO_ADV_DISCP1'] = ["45"] #sets discipline to softeng
    #discipline = br.find_control(name="UW_CO_JOBSRCH_UW_CO_ADV_DISCP1")
    form['UW_CO_JOBSRCH_UW_CO_ADV_DISCP2'] = ["45"]
    form['UW_CO_JOBSRCH_UW_CO_ADV_DISCP3'] = ["45"]
    form['UW_CO_JOBSRCH_UW_CO_COOP_JR'] = ['Y']
    form['UW_CO_JOBSRCH_UW_CO_COOP_INT'] = ['Y']
    form['UW_CO_JOBSRCH_UW_CO_COOP_SR'] = ['Y']
    form['TYPE_COOP'] = ['1']
    form['UW_CO_JOBSRCH_UW_CO_JS_JOBSTATUS'] = ['POST'] #dog

    response = br.submit()
    soup = bs4.BeautifulSoup(response.read())

    

def get_joblist(list_url):
    response = requests.get(list_url)
    soup = bs4.BeautifulSoup(response.text)
    return [a.attrs.get('href') for a in soup.select('')] #find url to each job
    
def get_job_data(job_url):
    job_data = {}
    response = requests.get(root_url + job_url)
    soup = bs4.BeautifulSoup(response.text)
    #do things to soup and put in job_data

    return job_data 

def main():
    status_code = login_jobmine(userid, pwd)

    if status_code = requests.codes.ok:
        job_urls = get_joblist(list_url)

        for job_url in job_urls:
            get_job_data(job_url)


if __name__ == '__main__':
    #gaycat
    main()

"""

profile = webdriver.firefox.firefox_profile.FirefoxProfile()
browser = webdriver.Firefox(firefox_profile=profile)


def login_jobmine():
    browser.get(login_url)
    browser.find_element_by_id("userid").send_keys(userid)
    browser.find_element_by_id("pwd").send_keys(pwd)
    browser.find_element_by_id("login").find_element_by_xpath("//input[@type='submit'][@name='submit']").submit()

    if 'invalid' or 'required' in browser.page_source:
        "Please try again."
        login_jobmine()

    return

def search_jobs():
    browser.get(search_url)
    xpath = "//select[@name='UW_CO_JOBSRCH_UW_CO_ADV_DISCP%s']/option[text()='%s']"
    browser.find_element_by_xpath(xpath % ('1', 'ENG-Software')).click()#do dis
    browser.find_element_by_id("UW_CO_JOBSRCH_UW_CO_WT_SESSION").send_keys('1155')
    browser.find_element_by_id("UW_CO_JOBSRCH_UW_CO_COOP_JR").click()
    browser.find_element_by_id("UW_CO_JOBSRCH_UW_CO_COOP_INT").click()
    browser.find_element_by_id("UW_CO_JOBSRCH_UW_CO_COOP_SR").click()
    driver.find_element_by_id("UW_CO_JOBSRCHDW_UW_CO_DW_SRCHBTN").click()

    return driver.page_source

def get_jobs(html):
    job_list = []
    soup = bs4.BeautifulSoup(html)
    job_spans = soup.findAll('span', id=lambda x: x and x.startswith('UW_CO_JOBRES_VW_UW_CO_JOB_ID'))

    for x in job_spans:
        job_list.append(x.text)

    return job_list


def scrape_job(job_id):
    browser.get(job_url + job_id)


def get_joblist()
    html_source = browser.page_source
    soup = bs4.BeautifulSoup(html_source)

