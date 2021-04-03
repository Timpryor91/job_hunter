# -*- coding: utf-8 -*-
"""
@author: timpr

Class utilizes some similar logic to that described 
in https://medium.com/@msalmon00/web-scraping-job-postings-from-indeed-96bd588dcb4b
"""

import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

from classes.job_class import Job

class IndeedRoleSearch(object):
    """
    A job search object, relating to a scraping search on indeed.com for a particular job role  

    """
    def __init__(self, job_role, city, num_jobs, omit_words, exp_level, target_salary):
        """
        Initialize an IndeedRoleSearch object
        
        Parameters:
            job_role (string): a job role title e.g. "Program Manager"
            city (string): the city to search for jobs in e.g. "Los Angeles"
            num_jobs (integer): the number of jobs results to search for, multiple of 10
            omit_words (List<string>): a list of lowercase keywords, any job role containing any of these will
                                       be ignored
            exp_level (string): the job experience level to search for
            target_salary (string): the target salary to search for, expressed as a string with a $ sign
        """  
        self.job_role = job_role.replace(" ", "+")
        self.city = city.replace(" ", "+")
        self.num_jobs = num_jobs
        self.omit_words = omit_words
        self.exp_level = exp_level
        self.target_salary = target_salary
        
        self.search_jobs = []
        
        self.base_url = "https://www.indeed.com/jobs?q=" + self.job_role + self.target_salary + \
                        "&l=" + self.city + "&jt=fulltime&explvl=" + self.exp_level
        
        for start in range(0, self.num_jobs, 10):
            # Build page url to scrape, each page contains 10 job listings
            self.url = self.base_url + "&start=" + str(start)
            self.page_search = rq.get(self.url)
            time.sleep(1)
            self.soup = bs(self.page_search.text, "lxml", from_encoding = "utf-8")
            
            # Each div with a class of row corresponds to an individual job posting
            for div in self.soup.find_all(name = "div", attrs = {"class" : "row"}):
                # Extract job title from posting and url to page with application link
                self.title = div.find_all(name = "a", attrs = {"data-tn-element": "jobTitle"})[0]["title"]
                self.job_link = self.url + div.find_all(name = "a", attrs = {"data-tn-element": "jobTitle"})[0]["href"]
                
                # Check job title for omit terms
                self.title_lowercase = self.title.lower()
                self.valid_job = True
                for word in self.omit_words:
                    if word in self.title_lowercase:
                        self.valid_job = False
    
                if self.valid_job == False:
                    continue
                
                # Extract company from job posting
                for item in div.find_all(attrs = {"class": "company"})[0]:
                    if len(str(item.string).strip()) > 0:
                        self.company = str(item.string).strip()
                
                # Extract salary information from the posting, if it is provided
                self.salary = "N/A"
                for item in div.find_all(attrs = {"class": "salaryText"}):
                    if len(item.text.strip()) > 0:
                        self.salary = item.text.strip()
                
                # Extract brief description of role
                self.summaries = div.find_all(attrs = {"class": "summary"})
                for summary in self.summaries:
                    self.summary = summary.text.strip()
                
                # Determine is role is available for easy apply on Indeed
                self.easily_apply_check = div.find_all(attrs = {"class": "iaLabel iaIconActive"})
                if len(self.easily_apply_check) > 0: 
                    self.easily_apply = True
                else:
                    self.easily_apply = False
                
                self.search_jobs.append(Job(self.title,
                                            city,
                                            self.company,
                                            self.salary,
                                            self.summary,
                                            self.job_link,
                                            self.easily_apply))

    def get_job_list_dataframe(self):
        """
        Obtain a dataframe with all the details of job listings from the search
        
        Returns:
            job_dataframe (Dataframe): dataframe containing job listing info
        
        """
        self.job_entry_list = []

        for job in self.search_jobs:
            self.job_entry_list.append([job.get_job_title(),
                                        job.get_company(),
                                        job.get_city(),
                                        job.get_salary(),
                                        job.get_summary(),
                                        job.get_url(),
                                        job.get_easily_apply()])

        self.job_dataframe = pd.DataFrame(data = self.job_entry_list,
                                          columns = ["job_title",
                                                     "company",
                                                     "location",
                                                     "salary",
                                                     "summary",
                                                     "url",
                                                     "easily_apply?"])
        return(self.job_dataframe)     