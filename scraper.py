# WHY IS JOBMINE DOWN AT NIGHT????!?!?!?!?!?!? ugh
import requests
import json

import bs4


root_url = '' #find this
login_url = "https://jobmine.ccol.uwaterloo.ca/psp/SS/?cmd=login"
list_url = "" #find this


def login_jobmine(userid, pwd):
    payload = {'userid': userid, 'pwd': pwd}
    response = requests.post(login_url, data=payload)
    return response.status_code


print login_jobmine("", "")


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
    main()
