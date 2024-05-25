# import streamlit as st
# from openai import OpenAI as oaiClient
# from simple_salesforce import Salesforce as sfdcClient
# from supabase import create_client as supaClient
# from tavily import TavilyClient as tavClient
# from yelpapi import YelpAPI as yelpClient
# from googlemaps import Client as gClient

# class Clients:
#     def __init__(self):
#         self.openai_client = self.get_client_openai()
#         self.supabase_client = self.get_client_supabase()
#         self.salesforce_client = self.get_client_salesforce()
#         self.yelp_client = self.get_client_yelp()
#         self.google_client = self.get_client_google()
#         self.tavily_client = self.get_client_tavily()

#     def get_client_openai(self):
#         return oaiClient(api_key=st.secrets.openai.api_key)
    
#     def get_client_supabase(self):
#         self.column_username = st.secrets.supabase.username_column
#         self.column_password = st.secrets.supabase.password_column
#         self.column_vectorstoreid = st.secrets.supabase.vstoreid_column
#         self.column_threadid = st.secrets.supabase.threadid_column
#         self.column_email = st.secrets.supabase.email_column
#         self.column_userrole = st.secrets.supabase.userrole_column
#         self.column_firstname = st.secrets.supabase.firstname_column
#         self.column_lastname = st.secrets.supabase.lastname_column
#         self.column_fullname = st.secrets.supabase.fullname_column
#         self.column_createddate = st.secrets.supabase.createddate_column
#         self.column_businessid = st.secrets.supabase.businessid_column
#         # Tables
#         self.table_users = st.secrets.supabase.users_table
#         # Query Items
#         self.user_select_string = f"{self.column_username}, {self.column_password}, {self.column_vectorstoreid}, {self.column_threadid}, {self.column_email}, {self.column_userrole}, {self.column_firstname}, {self.column_lastname}, {self.column_fullname}, {self.column_createddate}, {self.column_businessid}"
#         # New User Data
#         self.new_user_data_template = {self.column_username: None, self.column_password: None, self.column_vectorstoreid: None, self.column_threadid: None, self.column_email: None, self.column_userrole: None, self.column_firstname: None, self.column_lastname: None, self.column_fullname: None, self.column_createddate: None, self.column_businessid: None}
    
#         return supaClient(st.secrets.supabase.url, st.secrets.supabase.api_key_admin)
    
#     def get_client_salesforce(self):
#         return sfdcClient(username=st.secrets.salesforce.username, password=st.secrets.salesforce.password, security_token=st.secrets.salesforce.security_token)
    
#     def get_client_tavily(self):
#         return tavClient(api_key=st.secrets.tavily.api_key)
    
#     def get_client_yelp(self):
#         return yelpClient(api_key=st.secrets.yelp.api_key)
    
#     def get_client_google(self):
#         return gClient(key=st.secrets.google.maps_api_key)
    
# class SupabaseClient:
#     def __init__(self):
#         clients = Clients()
#         self.supaClient = clients.supabase_client
#         self.oaiClient = clients.openai_client
#         self.initialize_static_values()
        
#     def initialize_static_values(self):
#         # Columns
#         self.column_username = st.secrets.supabase.username_column
#         self.column_password = st.secrets.supabase.password_column
#         self.column_vectorstoreid = st.secrets.supabase.vstoreid_column
#         self.column_threadid = st.secrets.supabase.threadid_column
#         self.column_email = st.secrets.supabase.email_column
#         self.column_userrole = st.secrets.supabase.userrole_column
#         self.column_firstname = st.secrets.supabase.firstname_column
#         self.column_lastname = st.secrets.supabase.lastname_column
#         self.column_fullname = st.secrets.supabase.fullname_column
#         self.column_createddate = st.secrets.supabase.createddate_column
#         self.column_businessid = st.secrets.supabase.businessid_column
#         # Tables
#         self.table_users = st.secrets.supabase.users_table
#         # Query Items
#         self.user_select_string = f"{self.column_username}, {self.column_password}, {self.column_vectorstoreid}, {self.column_threadid}, {self.column_email}, {self.column_userrole}, {self.column_firstname}, {self.column_lastname}, {self.column_fullname}, {self.column_createddate}, {self.column_businessid}"
#         # New User Data
#         self.new_user_data_template = {self.column_username: None, self.column_password: None, self.column_vectorstoreid: None, self.column_threadid: None, self.column_email: None, self.column_userrole: None, self.column_firstname: None, self.column_lastname: None, self.column_fullname: None, self.column_createddate: None, self.column_businessid: None}
    
#     def user_authentication(self, username: str, password: str):
#         response = self.supaClient.table(self.table_users).select(self.user_select_string).eq(self.column_username, username).eq(self.column_password, password).execute()
#         if response.data:
#             user_data = response.data[0]
#             st.session_state.email = user_data[self.column_email]
#             st.session_state.firstname = user_data[self.column_firstname]
#             st.session_state.lastname = user_data[self.column_lastname]
#             st.session_state.fullname = user_data[self.column_fullname]
#             st.session_state.createddate = user_data[self.column_createddate]
#             st.session_state.threadid = user_data[self.column_threadid]
#             st.session_state.vectorstoreid = user_data[self.column_vectorstoreid]
#             st.session_state.businessid = user_data[self.column_businessid]
#             print(st.session_state.threadid)
#             return user_data
#         else:
#             return None
        
#     def user_addition(self, username: str, password: str, email: str, firstname: str, lastname: str, fullname: str, createddate: str,  userrole: str):
#         #vstore = self.oaiClient.beta.vector_stores.create().id
#         #threadid = self.oaiClient.beta.threads.create(tool_resources={"file_search": {"vector_store_ids": [vstore]}}).id
        
#         new_user_data = self.new_user_data_template.copy()
#         new_user_data[self.column_username] = username
#         new_user_data[self.column_password] = password
#         new_user_data[self.column_email] = email
#         new_user_data[self.column_firstname] = firstname
#         new_user_data[self.column_lastname] = lastname
#         new_user_data[self.column_fullname] = fullname
#         new_user_data[self.column_createddate] = createddate
#         new_user_data[self.column_threadid] = st.session_state.threadid
#         new_user_data[self.column_vectorstoreid] = st.session_state.vectorstoreid
#         new_user_data[self.column_userrole] = userrole
#         self.new_user_data = new_user_data
#         response = self.supaClient.table(self.table_users).insert(new_user_data).execute()
#         if response.data:
#             st.session_state.email = email
#             st.session_state.firstname = firstname
#             st.session_state.lastname = lastname
#             st.session_state.fullname = fullname
#             st.session_state.createddate = createddate
#             st.session_state.userrole = userrole
#             return response.data[0]
#         else:
#             return None


