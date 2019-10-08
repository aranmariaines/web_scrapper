#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import libraries
import os
import pathlib
path = pathlib.Path.home().joinpath('Documents','Upwork','web_scrapping','web_scrapper')
os.chdir(path)
from google_search_functions import google_search,create_dataframe,save_dataframe_to_excel

# Import keys
from config import my_api_key,my_cse_id

# Credentials
my_api_key = my_api_key
my_cse_id = my_cse_id

# Search parameters
search_term = "restaurants in coventry"
pages_to_retrieve = 2
output_file_name = 'restaurants_in_coventry.csv'

# Get results
result = google_search(search_term, my_api_key, my_cse_id, pages=pages_to_retrieve)

# Dataframe from results
df = create_dataframe(result)
    
# Save as CSV
save_dataframe_to_excel(df,path,output_file_name)
 


