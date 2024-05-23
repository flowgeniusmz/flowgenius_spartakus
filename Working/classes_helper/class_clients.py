import streamlit as st
from openai import OpenAI as oaiClient
from simple_salesforce import Salesforce as sfdcClient
from supabase import create_client as supaClient
from tavily import TavilyClient as tavClient
from yelpapi import YelpAPI as yelpClient
from googlemaps import Client as gClient

class Clients:
    def __init__(self):
        self.openai_client = self.get_client_openai()
        self.supabase_client = self.get_client_supabase()
        self.salesforce_client = self.get_client_salesforce()
        self.yelp_client = self.get_client_yelp()
        self.google_client = self.get_client_google()
        self.tavily_client = self.get_client_tavily()

    def get_client_openai(self):
        return oaiClient(api_key=st.secrets.openai.api_key)
    
    def get_client_supabase(self):
        return supaClient(supabase_key=st.secrets.supabase.api_key_admin, supabase_url=st.secrets.supabase.url)
    
    def get_client_salesforce(self):
        return sfdcClient(username=st.secrets.salesforce.username, password=st.secrets.salesforce.password, security_token=st.secrets.salesforce.security_token)
    
    def get_client_tavily(self):
        return tavClient(api_key=st.secrets.tavily.api_key)
    
    def get_client_yelp(self):
        return yelpClient(api_key=st.secrets.yelp.api_key)
    
    def get_client_google(self):
        return gClient(key=st.secrets.google.api_key)
    
