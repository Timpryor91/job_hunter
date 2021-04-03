# -*- coding: utf-8 -*-
"""

@author: timpr
"""

from classes.rolesearch_class import IndeedRoleSearch
import pandas as pd

if __name__ == "__main__":
    
    # Define target job roles
    job_role_list = ["Program Manager",
                     "Operations Manager",
                     "Strategy Manager",
                     "Project Manager"
                     ]
    
    # Define job location
    location = "Los Angeles"
    
    # Define experience level for job (entry_level, mid_level, senior_level)
    exp_level = "mid_level"
    
    # Define target salary
    target_salary = "$120,000"
    
    # Set omit words (if any of these words found in job title, job will be ignored)
    omit_words = ["construction",
                  "manufacturing",
                  "scrum",
                  "developer",
                  "junior",
                  "jr",
                  "software",
                  "technical",
                  "intern"
                  ]
    
    # Set maximum number of jobs to return for each role search
    max_num_jobs = 100
    
    # Compile all jobs into single dataframe
    role_dfs = []
    for role in job_role_list:
        search = IndeedRoleSearch(role,
                                  location,
                                  max_num_jobs,
                                  omit_words,
                                  exp_level,
                                  target_salary
                                  )
        search_df = search.get_job_list_dataframe()
        role_dfs.append(search_df)
    combined_job_df = pd.concat(role_dfs)
    
    # Remove duplicate listings from dataframe (different role searches may yield the same job)
    combined_job_df.drop_duplicates(inplace = True)
    
    # Sort and filter dataframe
    combined_job_df.sort_values("easily_apply?", ascending = False, inplace = True)
    
    # print(combined_job_df)
    combined_job_df.to_csv("job_database.csv")