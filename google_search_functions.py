#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Functions to retrieve data from Google Search API. 

# Google search output

# a Dictionary with these keys:
# Kind: Customsearch
# URL: Full address of search (good to check how to parameterizase it)
# Queries: 
# 'context' : google
#'searchInformation': search performance
#'items' : actual results. It is a list. 

# Inside each element of the list there is a dict:
# 'kind': customsearch
# 'title': title of the search
# 'htmlTitle': Title in html format
# 'link': link of the webpage 
# 'displayLink': short name of the url that is displayed under the search title
# 'snippet': short description that appears under the title of the webpage
# 'htmlSnippet': idem below but html
# 'cacheId': code
# 'formattedUrl':  Url of webpage
# 'htmlFormattedUrl': idem below html
# 'pagemap': a dictionary of metatags: referrer , origin

# Libraries
from googleapiclient.discovery import build
import pandas as pd

# Define function to retrieve google search results
def google_search(search_term, api_key, cse_id, pages, **kwargs):
    """
    Get google results
    Parameters
    ---------
    search_term : string
        Words/numbers to look up in Google
    api_key: string
        Key provided by Google to use the API: https://developers.google.com/custom-search/
    cse_id: string
        Id of the search enginee that you created in Google CSE web
    pages: int
        Quantity of pages to retrieve. Usually < 5. 
    kwargs: string
        Arguments that can be added with more specifications on the search such as country or language(check documentation)
        
    Returns
    ------
        result : list of dictionaries
    Each element in the list contains 10 items resulted from search.
    """
    result = []
    service = build("customsearch", "v1", developerKey=api_key)
    if pages == 1:
        res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
        result.append(res)
    else:
        res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
        result.append(res)
        for i in range(pages):
            res = service.cse().list(q=search_term, cx=cse_id, 
                             start=res['queries']['nextPage'][0]['startIndex'],
                             **kwargs).execute()
            result.append(res)
    return result


def create_dataframe(result):
    """
    Build a dataframe with data retrieved from google search
    Parameters
    ----------
        result : list of dictionaries
            each element is a result page
    Return
    ------
    Dataframe with columns that specify name,snippet and url
    """
    # List of elements in the search result
    names = []
    snippet = []
    url = []
    
    # Append search results to list
    for j,item in enumerate(result):
        for i,element in enumerate(result[j]['items']):
            names.append(result[j]['items'][i]['title'])
            snippet.append(result[j]['items'][i]['snippet'])
            url.append(result[j]['items'][i]['link'])
  
    # Create a dataframe
    df = pd.DataFrame(list(zip(names, snippet,url)), 
                   columns =['name', 'snippet','url']) 
    
    return df

def save_dataframe_to_excel(df,path,filename):
    """"
    Saves Google search results in CSV file delimited by ';'
    Parameters
    ----------
    df: dataframe
        dataframe with results from google search
    path: PosixPath object
        path where the file should be saved. Built with pathlib
    filename: string
        name of output file, should end '.csv'
    Return
    ------
        csv file 
    """
    
    path_and_file_name = path.joinpath('output',filename)
    df.to_csv(path_or_buf = path_and_file_name, sep=';',index=False)