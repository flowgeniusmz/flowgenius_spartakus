from openai import OpenAI
import streamlit as st
from yelpapi import YelpAPI
from tavily import TavilyClient

yelpClient = YelpAPI(api_key=st.secrets.yelp.api_key)
client = OpenAI(api_key=st.secrets.openai.api_key)
threadid = "thread_rtUmonQC9BwwkAy4KZth90cl"
messages = client.beta.threads.messages.list(thread_id=threadid)
print(messages)
run = "run_gRl7tK7BQO6tSyNsh6gcUyFX"

client.beta.threads.runs.cancel(run_id=run, thread_id=threadid)

# def yelp_query_search(query: str, zipcode: str):
#         """
#         Performs a search query using Yelp to find businesses based on term and location, useful for insurance research.
        
#         Parameters:
#             query (str): The search query describing the type of business.
#             zipcode (str): The zipcode of the business location.
        
#         Returns:
#             list: A list of businesses with basic information.
#         """
#         response = yelpClient.search_query(term=query, location=zipcode)
#         businesses = response['businesses']
#         return businesses
# a = yelp_query_search(query="FlowGenius", zipcode=60124)
# print(a)

query = "FlowGenius Elgin IL 60124"

def tavily_search(query: str):
        """
        Performs an advanced search using the Tavily client to gather comprehensive information about a business.
        
        Parameters:
            query (str): The search query describing the business or related information.
        
        Returns:
            dict: The search results including raw content and answers.
        """
        response = TavilyClient(api_key=st.secrets.tavily.api_key).search(query=query, search_depth="advanced", include_raw_content=True, include_answer=True, max_results=7)
        return response

a = tavily_search(query=query)
print(a)