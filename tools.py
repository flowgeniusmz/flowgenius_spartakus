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
from googlemaps import addressvalidation, places, geocoding, Client
import pandas as pd


tavClient = TavilyClient(api_key=st.secrets.tavily.api_key)
googleClient = Client(key=st.secrets.google.maps_api_key)
yelpClient = YelpAPI(api_key=st.secrets.yelp.api_key)

class Tools1:
    def business_research(query: str):
        tclient = TavilyClient(api_key=st.secrets.tavily.api_key)
        gclient = Client(key=st.secrets.google.maps_api_key)
        tresponse = tclient.search(query=query, search_depth="advanced", include_raw_content=True, include_answer=True, max_results=7)
        gresponse = places.places(client=gclient, query=query, region="US")
        response = f"Tavily Search: {tresponse}; Google Places Search: {gresponse}"
        print(response)
        return response

    def fill_form_125(form_data):
        supaClient = create_client(supabase_key=st.secrets.supabase.api_key_admin, supabase_url=st.secrets.supabase.url)
        table = "acord_form_125"
        response = supaClient.table(table_name=table).insert(json=form_data).execute()
        if response.data:
            formdata = response.data[0]
            return formdata
        else:
            print("error")

    def fill_form_125_required(form_data):
        supaClient = create_client(supabase_key=st.secrets.supabase.api_key_admin, supabase_url=st.secrets.supabase.url)
        table = "acord_form_125"
        response = supaClient.table(table_name=table).insert(json=form_data).execute()
        if response.data:
            formdata = response.data[0]
            return formdata
        else:
            print("error")

    def internet_search(query: str):
        client = TavilyClient(api_key=st.secrets.tavily.api_key)
        response = client.search(query=query, search_depth="advanced", include_answer=True, include_raw_content=True, max_results=7)
        return response
        


class Tools:
    def business_research(query: str):
        tclient = TavilyClient(api_key=st.secrets.tavily.api_key)
        gclient = Client(key=st.secrets.google.maps_api_key)
        tresponse = tclient.search(query=query, search_depth="advanced", include_raw_content=True, include_answer=True, max_results=7)
        gresponse = places.places(client=gclient, query=query, region="US")
        response = f"Tavily Search: {tresponse}; Google Places Search: {gresponse}"
        print(response)
        return response
    
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
    
    def google_places_search(query: str):
        """
        Searches for business information using Google Places to gather details on location, ratings, and more.
        
        Parameters:
            query (str): The search query describing the business.
        
        Returns:
            dict: The search results with detailed information about the business.
        """
        response = places.places(client=Client(key=st.secrets.google.maps_api_key), query=query, region="US")
        return response
    
    def google_address_validation(address_lines: list):
        """
        Validates business addresses using Google Address Validation to ensure accuracy for insurance documentation.
        
        Parameters:
            address_lines (list): The address lines to be validated.
        
        Returns:
            dict: The validation results including any corrections or standardizations.
        """
        response = addressvalidation.addressvalidation(client=Client(key=st.secrets.google.maps_api_key), addressLines=address_lines, regionCode="US", enableUspsCass=True)
        return response

    def google_geocode(address_lines: list):
        """
        Geocodes business addresses using Google Geocoding to obtain latitude and longitude for location verification.
        
        Parameters:
            address_lines (list): The address lines to be geocoded.
        
        Returns:
            dict: The geocoding results with latitude and longitude coordinates.
        """
        response = geocoding.geocode(client=Client(key=st.secrets.google.maps_api_key), address=address_lines, region="US")
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
        response = YelpAPI(api_key=st.secrets.yelp.api_key).search_query(term=query, location=zipcode)
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
        response = YelpAPI(api_key=st.secrets.yelp.api_key).business_query(id=business_id)
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
        businesses = YelpAPI(api_key=st.secrets.yelp.api_key).search_query(term=query, location=zipcode)['businesses']
        
        for business in businesses:
            business_id = business.get('id')
            detailed_info = YelpAPI(api_key=st.secrets.yelp.api_key).business_query(id=business_id)
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



