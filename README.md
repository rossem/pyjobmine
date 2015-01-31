# Jobmine-Scraper
Jobmine scraper written in Python 2.7 using Selenium and BeautifulSoap, by Rostislav Semenov.

#Dependencies
- Selenium
- BeautifulSoup 4

#How to run:
Clone the directory and in your terminal type:
```python
python scraper.py DICTIONARY
```
Where an example of DICTIONARY is:

```python
'{"term": "1155", "employer_name": "TD", "job_title": "analyst", "disciplines": ["ENG-Software", "MATH-Computer Science", "MATH-Computing & Financial Management"], "junior": true, "intermediate": true, "senior": false}'
```

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


This is a sample of a JSON that the scraper gets:

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
