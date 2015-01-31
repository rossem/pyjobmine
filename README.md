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
- posting open date
- last day to apply
- emp job #
- job id
- employer
- job title
- work location
- grades
- available 
- disciplines
- disciplines1 (more disciplines)
- levels
- hiring process support
- work term support
- comments
- job description


Enjoy!
