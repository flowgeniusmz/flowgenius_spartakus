import streamlit as st
from classes_helper import class_clients, class_utils
import pandas as pd
from googlemaps import addressvalidation, places, geocoding

class Tools:
    def __init__(self):
        self.clients = class_clients.Clients()
        self.utils = class_utils.Utils()

    def yelp_query_search(self, query, zipcode):
        self.yelp_search_response = self.clients.yelp_client.search_query(term=query, location=zipcode)
        self.businesses = self.yelp_search_response['businesses']

    def yelp_business_search(self, business_id):
        self.yelp_business_search_response = self.clients.yelp_client.business_query(id=business_id)
        self.detailed_info = self.yelp_business_search_response

    def yelp_search(self, query: str, zipcode: str):
        self.business_records = []
        self.yelp_query_search(query=query, zipcode=zipcode)
        business_records = []
        # query_search_response = self.yelp_client.search_query(term=query, location=zipcode)
        # businesses = query_search_response['businesses']
        for business in self.businesses:
            business_id = business.get('id')
            self.yelp_business_search(business_id=business_id)
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
                'is_claimed': self.detailed_info.get('is_claimed'),
                'cross_streets': self.detailed_info['location'].get('cross_streets') if self.detailed_info.get('location') else None,
                'photos': ", ".join(self.detailed_info.get('photos', [])),
                'hours': self.detailed_info.get('hours', [{}])[0].get('open', []),
                'is_open_now': self.detailed_info.get('hours', [{}])[0].get('is_open_now'),
                'transactions': ", ".join(self.detailed_info.get('transactions', []))
            }
            
            # Add categories to the record
            categories = business.get('categories', [])
            category_aliases = [cat['alias'] for cat in categories]
            category_titles = [cat['title'] for cat in categories]
            business_record['categories_alias'] = ", ".join(category_aliases)
            business_record['categories_title'] = ", ".join(category_titles)

            self.business_records.append(business_record)
        self.yelp_business_records_df = pd.DataFrame(self.business_records)

    def tavily_search(self, query):
        self.tavily_search_response = self.tavily_client.search(query=query, search_depth="advanced", include_raw_content=True, include_answer=True, max_results=10)
        self.tavily_search_results = self.tavily_search_response['results']    

    def validate_address(self, address_lines):
        self.address_validation_response = addressvalidation.addressvalidation(client=self.clients.google_client, addressLines=address_lines, regionCode="US", enableUspsCass=True)
        # print(self.addvalidate)
        # ['1840 Coralito Ln', 'Elgin, IL 60124']
    
    def get_geocode(self, address_lines):
        self.address_geocode_response = geocoding.geocode(client=self.clients.google_client, address=address_lines, region="US")

    def places_search(self, query):
        self.places_search_response = places.places(client=self.clients.google_client, query=query, region="US")