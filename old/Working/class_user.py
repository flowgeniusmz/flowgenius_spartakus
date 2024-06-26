# import streamlit as st
# from classes import class_clients

# class User:
#     def __init__(self):
#         self.initialize_list_attributes()
#         self.initialize_user_attributes()
    
#     def initialize_user_attributes(self):
#         self.user_role = None
#         self.username = None
#         self.password = None
#         self.thread_id = None
#         self.vectorstore_id = None
#         self.email = None
#         self.business_name = None
#         self.business_id = None
#         self.firstname = None
#         self.lastname = None
#         self.fullname = None
#         self.datecreated = None

#     def initialize_userflow_attributes(self):
#         self.user_initialized = False
#         self.user_authenticated = False
#         self.user_type = None
#         self.user_flow_complete = False

#     def initialize_list_attributes(self):
#         self.user_roles = ["Admin", "Client", "Carrier"]
#         self.user_types = ["New", "Existing"]

#     def initialize_utils(self):
#         self.clients = class_clients.Clients()
#         self.openai_client = self.clients.openai_client
#         self.supabase_client = self.clients.supabase_client