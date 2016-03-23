# WHY IS JOBMINE DOWN AT NIGHT????!?!?!?!?!?!? ugh
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

#-----------------------------------------------------------

#userid = sys.argv[1]
#pwd = sys.argv[2]
userid = raw_input("Username: ")
pwd = getpass.getpass("Password: ")
_settings = sys.argv[1]
settings = json.loads(_settings)

search_url = "https://jobmine.ccol.uwaterloo.ca/psc/SS/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBSRCH" 
login_url = "https://jobmine.ccol.uwaterloo.ca/psp/SS/EMPLOYEE/WORK/"
job_url = "https://jobmine.ccol.uwaterloo.ca/psc/SS_2/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBDTLS.GBL?UW_CO_JOB_ID="

browser = webdriver.Firefox()
job_data_list = []

#-----------------------------------------------------------

def login_jobmine():
    browser.get(login_url)
    time.sleep(2)
    old_url = browser.current_url
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

def search_jobs():
    browser.get(search_url)
    xpath = "//select[@name='UW_CO_JOBSRCH_UW_CO_ADV_DISCP%s']/option[text()='%s']"

    if len(settings['disciplines']) > 2:
        browser.find_element_by_xpath(xpath % ("3", settings['disciplines'][2])).click()
    if len(settings['disciplines']) > 1:
        browser.find_element_by_xpath(xpath % ("2", settings['disciplines'][1])).click()
    if len(settings['disciplines']) > 0:
        browser.find_element_by_xpath(xpath % ("1", settings['disciplines'][0])).click()


    browser.find_element_by_id("UW_CO_JOBSRCH_UW_CO_WT_SESSION").send_keys(settings['term'])

    employer_name = browser.find_element_by_id("UW_CO_JOBSRCH_UW_CO_EMPLYR_NAME")
    job_title = browser.find_element_by_id("UW_CO_JOBSRCH_UW_CO_JOB_TITLE")
    jr = browser.find_element_by_id("UW_CO_JOBSRCH_UW_CO_COOP_JR")
    inter = browser.find_element_by_id("UW_CO_JOBSRCH_UW_CO_COOP_INT")
    sr = browser.find_element_by_id("UW_CO_JOBSRCH_UW_CO_COOP_SR")

    if (not jr.is_selected() and settings['junior']):
        jr.click()

    if (not inter.is_selected() and settings['intermediate']):
        inter.click()

    if (not sr.is_selected() and settings['senior']):
        sr.click()

    if (len(settings['employer_name']) > 0):
        employer_name.send_keys(settings['employer_name'])
    
    if (len(settings['job_title']) > 0):
        job_title.send_keys(settings['job_title'])



    browser.find_element_by_id("UW_CO_JOBSRCHDW_UW_CO_DW_SRCHBTN").click()
    time.sleep(4)


def get_jobs():
    job_list = []
    soup = bs4.BeautifulSoup(browser.page_source)
    job_spans = soup.findAll('span', id=lambda x: x and x.startswith('UW_CO_JOBRES_VW_UW_CO_JOB_ID'))

    for x in job_spans:
        job_list.append(x.text)

    return job_list


def scrape_job(job_id):
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

    print "Done job: " + job_id
    print "-------------------------"


def main():
    login_jobmine()
    search_jobs()
    joblist = get_jobs()

    for job in joblist:
        scrape_job(job)

    with open('job_data_json', 'w') as outfile:
        json.dump(job_data_list, outfile, indent=4)

    browser.quit()


main()

