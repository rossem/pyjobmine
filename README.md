# Jobmine Scraper and REST API.
Jobmine scraper and RESTful API written in Python 2.7 using Selenium and BeautifulSoap, by Rostislav Semenov.

===
#Using the REST API.

###Usage.
#####Send a GET request to `http://jomine.me:8080` ***(jomine, NOT jobmine)*** with the following parameters:
- `userid` -- JobMine username
- `pwd` -- JobMine password
- `term` -- coop term
- `employer_name` -- name of the employer -- optional
- `job_title` -- title of job -- optional
- `discipline1` -- first discipline (e.g. "ENG-Software") -- optional 
- `discipline2` -- second discipline -- optional
- `discipline3` -- third discipline -- optional
- `junior` -- junior level ("True" or "False") -- optional
- `intermediate` -- intermediate level ("True" or "False") -- optional
- `senior` -- senior level ("True" or "False") -- optional

Or simply call `http://jomine.me:8080/?term=1155...` in your browser.

*Note: it can take up to ~10 seconds to get the JSON.*
#Using the Web Scraper.


#Dependencies
- Selenium
- BeautifulSoup 4
- Pyvirtualdisplay

#How to run:
Clone the directory and in your terminal type:
```python
python scraper.py DICTIONARY
```
Where an example of DICTIONARY is:

```python
'{"term": "1155", "employer_name": "TD", "job_title": "analyst", "disciplines": ["ENG-Software", "MATH-Computer Science", "MATH-Computing & Financial Management"], "junior": true, "intermediate": true, "senior": false}'
```


===

##Currently the scraper gets these attributes for each job:
- Posting open date
- Last day to apply
- Employer job number
- Job id
- Employer
- Job title
- Work location
- If marks are required to apply
- Available openings 
- Disciplines applicable to the job
- Additional disciplines
- Level of the job
- Hiring process support staff
- Work term support staff
- Additional comments
- Job description



#This is a sample of a JSON that the scraper/api gets:

```json
{
        "disciplines": "ENG-Software, ENG-Systems Design, MATH-Computer Science", 
        "work term support": "Pasternak,Paul", 
        "available openings": 1, 
        "work location": "Toronto", 
        "job title": "Test Analyst", 
        "employer": "TD Bank Group, TD Securities", 
        "job description": "\"The group acts asCorporate Segment Technology Solutions Testing Shared Services (CSTS TSS) is the provider of testing services across the CSTS group. TSS is responsible for providing appropriate testing solutions and quality control for IT-owned projects by CSTS. The goal of the TSS is to create a best in class testing team, focused on leveraging industry best practices and processes for Quality Assurance and Quality Control\n\nTesting in following technologies\n1. ETL\n2. Data integration and Data mapping\n3. SQL scripting - medium to Advance level\n4. mainframe testing skills\nWriting of Test Cases from Requirements document\nExecution of test cases using HP Quality Center\nUse of HP Quality Center for Test Execution, Traceability matrix, and defects\"", 
        "emp job #": "BAKHTIAR", 
        "job id": "00254025", 
        "levels": "Junior, Intermediate", 
        "last day to apply": "25 JAN 2015", 
        "comments": "\u00a0", 
        "disciplines1": "ENG-Computer, MATH- (unspecified)", 
        "posting open date": "23 JAN 2015", 
        "grades": "Required", 
        "hiring process support": "Shin,Donna"
    }
```

Enjoy!
