from flask import Flask, request
from scraper import *

import time
import requests
import json
import sys
import getpass

import bs4
import mechanize

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

app = Flask(__name__)
global browser
#browser = webdriver.Firefox()

key_list = ['userid', 'pwd' , 'term', 'employer_name', 'job_title', 'discipline1', 'discipline2', 'discipline3', 'junior', 'intermediate', 'senior']

search_url = "https://jobmine.ccol.uwaterloo.ca/psc/SS/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBSRCH" 
login_url = "https://jobmine.ccol.uwaterloo.ca/psp/SS/EMPLOYEE/WORK/"
job_url = "https://jobmine.ccol.uwaterloo.ca/psc/SS_2/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBDTLS.GBL?UW_CO_JOB_ID="



def login_jobmine(userid, pwd, browser):
    browser.get(login_url)
    time.sleep(2)
    browser.find_element_by_id("userid").send_keys(userid)
    browser.find_element_by_id("pwd").send_keys(pwd)
    browser.find_element_by_id("login").find_element_by_xpath("//input[@type='submit'][@name='submit']").submit()

    """
    Doesnt work :(
    if old_url == browser.current_url:
        print "Your username/password are invalid. Please try again."
        browser.quit()
        sys.exit(0)

    """

def search_jobs(term, employer_name, job_title, junior, intermediate, senior, browser, discipline1, discipline2, discipline3):
    browser.get(search_url)
    time.sleep(5)
    xpath = "//select[@name='UW_CO_JOBSRCH_UW_CO_ADV_DISCP%s']/option[text()='%s']"

    #job_title = browser.find_element_by_id("UW_CO_JOBSRCH_UW_CO_JOB_TITLE").send_keys("lol")

    print discipline1, discipline2, discipline3

    if len(discipline3) > 0:
        browser.find_element_by_xpath(xpath % ("3", discipline3)).click()
    if len(discipline2) > 0:
        browser.find_element_by_xpath(xpath % ("2", discipline2)).click()
    if len(discipline1) > 0:
        browser.find_element_by_xpath(xpath % ("1", discipline1)).click()

    print "done discp"
    


    browser.find_element_by_id("UW_CO_JOBSRCH_UW_CO_WT_SESSION").send_keys(term)
    print "done term"

    browser.find_element_by_id("UW_CO_JOBSRCH_UW_CO_EMPLYR_NAME").send_keys(Keys.BACKSPACE*50 + employer_name)
    print "done employer"

    browser.find_element_by_id("UW_CO_JOBSRCH_UW_CO_JOB_TITLE").send_keys(Keys.BACKSPACE*50 + job_title)
    print "dont job title"

    jr = browser.find_element_by_id("UW_CO_JOBSRCH_UW_CO_COOP_JR")
    inter = browser.find_element_by_id("UW_CO_JOBSRCH_UW_CO_COOP_INT")
    sr = browser.find_element_by_id("UW_CO_JOBSRCH_UW_CO_COOP_SR")

    
    if (not jr.is_selected() and junior == "True"):
        jr.click()

    if (not inter.is_selected() and intermediate == "True"):
        inter.click()

    if (not sr.is_selected() and senior == "True"):
        sr.click()

    browser.find_element_by_id("UW_CO_JOBSRCHDW_UW_CO_DW_SRCHBTN").click()
    time.sleep(4)


def get_jobs(browser):
    job_list = []
    soup = bs4.BeautifulSoup(browser.page_source)
    job_spans = soup.findAll('span', id=lambda x: x and x.startswith('UW_CO_JOBRES_VW_UW_CO_JOB_ID'))

    for x in job_spans:
        job_list.append(x.text)

    return job_list


def scrape_job(job_id, job_data_list, browser):
    job_data = {}
    browser.get(job_url + job_id)
    time.sleep(2)

    soup = bs4.BeautifulSoup(browser.page_source)

    job_data['posting open date'] = soup.find(id = "UW_CO_JOBDTL_VW_UW_CO_CHAR_EDATE").text
    job_data['last day to apply'] = soup.find(id = "UW_CO_JOBDTL_VW_UW_CO_CHAR_DATE").text
    job_data['emp job #'] = soup.find(id = "UW_CO_JOBDTL_VW_UW_CO_EMPOWN_JOBNO").text
    job_data['job id'] = job_id
    job_data['employer'] = soup.find(id = "UW_CO_JOBDTL_DW_UW_CO_EMPUNITDIV").text
    job_data['job title'] = soup.find(id = "UW_CO_JOBDTL_VW_UW_CO_JOB_TITLE").text
    job_data['work location'] = soup.find(id = "UW_CO_JOBDTL_VW_UW_CO_WORK_LOCATN").text
    job_data['grades'] = soup.find(id = "UW_CO_JOBDTL_DW_UW_CO_MARKS_DRVD").text
    job_data['available openings'] = int(soup.find(id = "UW_CO_JOBDTL_VW_UW_CO_AVAIL_OPENGS").text)
    job_data['disciplines'] = soup.find(id = "UW_CO_JOBDTL_DW_UW_CO_DESCR").text
    job_data['disciplines1'] = soup.find(id = "UW_CO_JOBDTL_DW_UW_CO_DESCR100").text
    job_data['levels'] = soup.find(id = "UW_CO_JOBDTL_DW_UW_CO_DESCR_100").text
    job_data['hiring process support'] = soup.find(id = "UW_CO_OD_DV2_UW_CO_NAME").text
    job_data['work term support'] = soup.find(id = "UW_CO_OD_DV2_UW_CO_NAME2").text
    job_data['comments'] = soup.find(id = "UW_CO_JOBDTL_VW_UW_CO_JOB_SUMMARY").text
    job_data['job description'] = soup.find(id = "UW_CO_JOBDTL_VW_UW_CO_JOB_DESCR").text

    job_data_list.append(job_data)


@app.route('/')
def api_jobmine():
    data = {}

    for argument in key_list:
        if argument not in request.args:
            data[argument] = ''
        else:
            data[argument] = request.args[argument]

    print data

    search_url = "https://jobmine.ccol.uwaterloo.ca/psc/SS/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBSRCH" 
    login_url = "https://jobmine.ccol.uwaterloo.ca/psp/SS/EMPLOYEE/WORK/"
    job_url = "https://jobmine.ccol.uwaterloo.ca/psc/SS_2/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBDTLS.GBL?UW_CO_JOB_ID="
    profile = webdriver.firefox.firefox_profile.FirefoxProfile()
    profile.set_preference("browser.cache.disk.enable", False);
    profile.set_preference("browser.cache.memory.enable", False);
    profile.set_preference("browser.cache.offline.enable", False);
    profile.set_preference("network.http.use-cache", False);
    browser = webdriver.Firefox(firefox_profile=profile)
    job_data_list = []

    login_jobmine(data['userid'], data['pwd'], browser)

    search_jobs(data['term'], data['employer_name'], data['job_title'], data['junior'], data['intermediate'], data['senior'], browser, data['discipline1'], data['discipline2'], data['discipline3'])

    joblist = get_jobs(browser)

    for job in joblist:
        scrape_job(job, job_data_list, browser)

    #with open('job_data_json', 'w') as outfile:
        #json.dump(job_data_list, outfile, indent=4)

    browser.quit()
    return json.dumps(job_data_list, indent=4)

if __name__ == "__main__":
    app.run()
