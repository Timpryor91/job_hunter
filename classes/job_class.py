# -*- coding: utf-8 -*-
"""

@author: timpr
"""

class Job(object):
    """
    A job object, relating to a job found during scraping 

    """
    def __init__(self, job_title, city, company, salary, summary, url, easily_apply):
        """
        Initialize a job object
        
        Parameters:
            job_title (string): the name of the job e.g. "Senior Manager - Strategy"
            city (string): the city that the job is located in e.g. "Los Angeles"
            company (string): the company offering the job
            summary (string): additional detail about what the job entails
            url (string): a url link to the job posting
            easily_apply (boolean): true if job has easily apply option, false otherwise
        """
        self.job_title = job_title
        self.city = city
        self.company = company
        self.salary = salary
        self.summary = summary
        self.url = url
        self.easily_apply = easily_apply
        
    def get_job_title(self):
        return(self.job_title)

    def get_city(self):
        return(self.city)
    
    def get_company(self):
        return(self.company)    

    def get_salary(self):
        return(self.salary)
        
    def get_summary(self):
        return(self.summary)
    
    def get_url(self):
        return(self.url)

    def get_easily_apply(self):
        return(self.easily_apply)