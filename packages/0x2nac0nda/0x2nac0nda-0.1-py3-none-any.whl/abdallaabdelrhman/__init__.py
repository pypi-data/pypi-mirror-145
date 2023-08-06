from serpapi import GoogleSearch
import requests
from termcolor import colored


def scrape():
    print (colored('0x2nac0nda', 'green'))
    q = input('Enter the text to search : ')
    api_key = input('Enter your api_key  : ')    

    params = {
        "q": {q},
        "google_domain": "google.com",
        "api_key": {api_key}
    }
   
    search = GoogleSearch(params)
    results = search.get_dict()
    knowledge_graph = results['knowledge_graph']
    print(f"Serching....")
    print(knowledge_graph)

scrape()