import streamlit as st
from openai import OpenAI 
from supabase import create_client
from yelpapi import YelpAPI
from googlemaps import Client
from tavily import TavilyClient
from simple_salesforce import Salesforce
from typing import Literal
import time
from datetime import datetime
from tempfile import NamedTemporaryFile

class Utilities:
    def get_client(client_type: Literal["openai", "supabase", "salesforce", "googlemaps", "yelp", "tavily"]):
        if client_type == "openai":
            client = OpenAI(api_key=st.secrets.openai.api_key)
        elif client_type == "googlemaps":
            client = Client(key=st.secrets.google.maps_api_key)
        elif client_type == "salesforce":
            client = Salesforce(username=st.secrets.salesforce.username, password=st.secrets.salesforce.password, security_token=st.secrets.salesforce.security_token)
        elif client_type == "supabase":
            client = create_client(supabase_key=st.secrets.supabase.api_key_admin, supabase_url=st.secrets.supabase.url)
        elif client_type == "yelp":
            client = YelpAPI(api_key=st.secrets.yelp.api_key)
        elif client_type == "tavily":
            client = TavilyClient(api_key=st.secrets.tavily.api_key)
        return client
    
    def get_current_datetime():
        current_datetime = datetime.now().isoformat()
        return current_datetime
    
    def get_fullname(firstname: str, lastname: str):
        fullname = f"{firstname} {lastname}"
        return fullname
    
    def create_vectorstore(firstname: str=None, lastname: str=None):
        if firstname is not None and lastname is not None:
            vname = f"SpartakusAI - {firstname} {lastname}"
        else:
            vname = f"SpartakusAI"
        vectorstoreid = OpenAI(api_key=st.secrets.openai.api_key).beta.vector_stores.create(name=vname).id
        return vectorstoreid
    
    def create_thread(vector_store_id: str=None):
        if vector_store_id is not None:
            tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}}
            threadid = OpenAI(api_key=st.secrets.openai.api_key).beta.threads.create(tool_resources=tool_resources).id
        else:
            threadid = OpenAI(api_key=st.secrets.openai.api_key).beta.threads.create().id
        return threadid
    
    def create_tempfile(suffix: Literal[".txt", ".log", ".dat", ".tmp", ".csv", ".json", ".xml", ".html", ".xlsx", ".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".mp3", ".wav", ".ogg", ".flac", ".mp4", ".avi", ".mov", ".mkv", ".zip", ".tar", ".gz", ".bz2", ".7z", ".rar", ".py", ".java", ".c", ".cpp", ".js", ".html", ".css"]):
        with NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file_path = temp_file.name
            return temp_file_path
        

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

    

