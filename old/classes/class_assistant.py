import streamlit as st
from openai import OpenAI
import googlemaps.addressvalidation
import googlemaps.geocoding
from simple_salesforce import Salesforce
from tavily import TavilyClient
import pandas as pd
import json
import time
import requests
from googlemaps import Client as gClient, addressvalidation, places, geocoding, geolocation
from classes import class_clients
from config import pagesetup as ps
from yelpapi import YelpAPI


# 0. SET CLIENTS
clients = class_clients.Clients()
oaiClient = clients.openai_client
googleClient = clients.google_client
yelpClient = clients.yelp_client
tavClient = clients.tavily_client
sfdcClient = clients.salesforce_client


# CLASS 1: Assistant
class Assistant:
    def __init__(self):
        self.initialize_attributes()
        self.initialize_display()

    def initialize_attributes(self):  
        print(st.session_state.threadid)
        self.assistant_id = st.secrets.openai.assistant_id
        self.assistant_vstoreid = st.secrets.openai.vectorstore_id
        self.assistant = oaiClient.beta.assistants.retrieve(assistant_id=self.assistant_id)
        self.threadid = st.session_state.threadid
        self.vstoreid = st.session_state.vectorstoreid
        self.run = None
        self.message = None
        self.thread_messages = oaiClient.beta.threads.messages.list(thread_id=self.threadid)

    def initialize_display(self):
        self.chat_container = ps.userflow_styled_container2(height=400, border = False)
        with self.chat_container:
            for thread_message in self.thread_messages:
                with st.chat_message(name=thread_message.role):
                    st.markdown(body=thread_message.content[0].text.value)
        self.prompt_container = ps.userflow_styled_container2(height=100, border=False)
        with self.prompt_container:
            self.prompt = st.chat_input(placeholder="Enter question or request here...")
            if self.prompt:
                with self.chat_container:
                    with st.chat_message(name="user"):
                        st.markdown(body=self.prompt)
                self.initialize_status(label="Running...please wait.")
                self.create_message_and_run(content=self.prompt, role="user")

    def initialize_status(self, label):
        self.status = st.status(label=label, expanded=False, state="running")

    def wait_on_run(self):
        while self.run.status == "queued" or self.run.status == "in progress":
            st.toast("Processing...please wait.")
            self.run = oaiClient.beta.threads.runs.retrieve(run_id=self.run.id, thread_id=self.threadid)
            time.sleep(1)
        if self.run.status =="requires_action":
            st.toast("Requires action")
            self.tool_outputs = []
            self.tool_calls = self.run.required_action.submit_tool_outputs.tool_calls
            for tool_call in self.tool_calls:
                tool_call_id = tool_call.id
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                with self.status:
                    st.write(f"Running {tool_call_id} {tool_name} with args {tool_args}")
                st.toast(f"Tool call {tool_name}")
                tool_output = getattr(Tools, tool_name)(**tool_args)
                st.toast(f"Tool call complete {tool_name}")
                with self.status:
                    st.write(f"Tool call {tool_name} results: {tool_output}")
                self.tool_outputs.append({"tool_call_id"})
            self.run = oaiClient.beta.threads.runs.submit_tool_outputs(run_id=self.run.id, thread_id=self.threadid, tool_outputs=self.tool_outputs)
            self.wait_on_run()
        else:
            # get messages added after last user message
            self.new_messages = oaiClient.beta.threads.messages.list(thread_id=self.threadid, order="asc", after=self.message.id)
            with self.status:
                st.markdown(self.new_messages)
            self.status.update(label="Run completed!", expanded=False, state="complete")
            st.toast("Run completed")
            for new_message in self.new_messages:
                with self.chat_container:
                    with st.chat_message(name=new_message.role):
                        st.markdown(body=new_message.content[0].text.value)
        
    def create_message_and_run(self, content, role):
        self.message = oaiClient.beta.threads.messages.create(thread_id=self.threadid, content=content, role=role)
        self.messageid = self.messageid
        self.run = oaiClient.beta.threads.runs.create(thread_id=self.threadid, assistant_id=self.assistant_id)
        self.wait_on_run()

    
        

class Tools:
    def tavily_search(query: str):
        """
        Performs an advanced search using the Tavily client to gather comprehensive information about a business.
        
        Parameters:
            query (str): The search query describing the business or related information.
        
        Returns:
            dict: The search results including raw content and answers.
        """
        response = tavClient.search(query=query, search_depth="advanced", include_raw_content=True, include_answer=True, max_results=7)
        return response
    
    def google_places_search(query: str):
        """
        Searches for business information using Google Places to gather details on location, ratings, and more.
        
        Parameters:
            query (str): The search query describing the business.
        
        Returns:
            dict: The search results with detailed information about the business.
        """
        response = places.places(client=googleClient, query=query, region="US")
        return response
    
    def google_address_validation(address_lines: list):
        """
        Validates business addresses using Google Address Validation to ensure accuracy for insurance documentation.
        
        Parameters:
            address_lines (list): The address lines to be validated.
        
        Returns:
            dict: The validation results including any corrections or standardizations.
        """
        response = addressvalidation.addressvalidation(client=googleClient, addressLines=address_lines, regionCode="US", enableUspsCass=True)
        return response

    def google_geocode(address_lines: list):
        """
        Geocodes business addresses using Google Geocoding to obtain latitude and longitude for location verification.
        
        Parameters:
            address_lines (list): The address lines to be geocoded.
        
        Returns:
            dict: The geocoding results with latitude and longitude coordinates.
        """
        response = geocoding.geocode(client=googleClient, address=address_lines, region="US")
        return response
    
    def yelp_query_search(query: str, zipcode: str):
        """
        Performs a search query using Yelp to find businesses based on term and location, useful for insurance research.
        
        Parameters:
            query (str): The search query describing the type of business.
            zipcode (str): The zipcode of the business location.
        
        Returns:
            list: A list of businesses with basic information.
        """
        response = yelpClient.search_query(term=query, location=zipcode)
        businesses = response['businesses']
        return businesses

    def yelp_business_search(business_id: str):
        """
        Searches for detailed information about a business using its Yelp ID to gather in-depth data for insurance purposes.
        
        Parameters:
            business_id (str): The Yelp ID of the business.
        
        Returns:
            dict: The detailed information about the business.
        """
        response = yelpClient.business_query(id=business_id)
        return response

    def yelp_search(query: str, zipcode: str):
        """
        Performs a search query using Yelp and retrieves detailed information for each business, aggregating useful data for insurance analysis.
        
        Parameters:
            query (str): The search query describing the type of business.
            zipcode (str): The zipcode of the business location.
        
        Returns:
            pd.DataFrame: A DataFrame containing detailed information about the businesses.
        """
        business_records = []
        businesses = yelpClient.search_query(term=query, location=zipcode)['businesses']
        
        for business in businesses:
            business_id = business.get('id')
            detailed_info = yelpClient.business_query(id=business_id)
            business_record = {
                'id': business.get('id'),
                'alias': business.get('alias'),
                'name': business.get('name'),
                'image_url': business.get('image_url'),
                'is_closed': business.get('is_closed'),
                'url': business.get('url'),
                'review_count': business.get('review_count'),
                'rating': business.get('rating'),
                'latitude': business['coordinates'].get('latitude') if business.get('coordinates') else None,
                'longitude': business['coordinates'].get('longitude') if business.get('coordinates') else None,
                'phone': business.get('phone'),
                'display_phone': business.get('display_phone'),
                'distance': business.get('distance'),
                'address1': business['location'].get('address1') if business.get('location') else None,
                'address2': business['location'].get('address2') if business.get('location') else None,
                'address3': business['location'].get('address3') if business.get('location') else None,
                'city': business['location'].get('city') if business.get('location') else None,
                'zip_code': business['location'].get('zip_code') if business.get('location') else None,
                'country': business['location'].get('country') if business.get('location') else None,
                'state': business['location'].get('state') if business.get('location') else None,
                'display_address': ", ".join(business['location'].get('display_address', [])) if business.get('location') else None,
                'is_claimed': detailed_info.get('is_claimed'),
                'cross_streets': detailed_info['location'].get('cross_streets') if detailed_info.get('location') else None,
                'photos': ", ".join(detailed_info.get('photos', [])),
                'hours': detailed_info.get('hours', [{}])[0].get('open', []),
                'is_open_now': detailed_info.get('hours', [{}])[0].get('is_open_now'),
                'transactions': ", ".join(detailed_info.get('transactions', []))
            }
            
            # Add categories to the record
            categories = business.get('categories', [])
            category_aliases = [cat['alias'] for cat in categories]
            category_titles = [cat['title'] for cat in categories]
            business_record['categories_alias'] = ", ".join(category_aliases)
            business_record['categories_title'] = ", ".join(category_titles)

            business_records.append(business_record)
        yelp_business_records_df = pd.DataFrame(business_records)
        return yelp_business_records_df

    

