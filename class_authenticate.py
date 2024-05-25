import streamlit as st
from typing import Literal
from datetime import datetime
from openai import OpenAI
from supabase import create_client as supabase_client
from config import pagesetup as ps

oaiClient = OpenAI(api_key=st.secrets.openai.api_key)
supaClient = supabase_client(supabase_key=st.secrets.supabase.api_key_admin, supabase_url=st.secrets.supabase.url)

class Sessionstate:
    def __init__(self):
        self.check_sessionstate()

    def check_sessionstate(self):
        if "initialized" not in st.session_state:
            st.session_state.initialized = False
            self.initialize_sessionstate()
        elif not st.session_state.initialized:
            self.initialize_sessionstate()
        else:
            print(st.session_state)
           
    def initialize_sessionstate(self):    
        st.session_state.user = None
        st.session_state.userrole = None
        st.session_state.username = None
        st.session_state.password = None
        st.session_state.email = None
        st.session_state.firstname = None
        st.session_state.lastname = None
        st.session_state.fullname = None
        st.session_state.businessid = None
        st.session_state.threadid = None
        st.session_state.vectorstoreid = None
        st.session_state.createddate = None
        st.session_state.userdata = None
        st.session_state.response = None
        st.session_state.authenticated = False
        st.session_state.userflow_complete = False
        st.session_state.usertype = None
        st.session_state.businessname = None
        st.session_state.request_headers = {'Accept': 'application/json', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36', 'Accept-Language': 'en-US,en;q=0.9','Accept-Encoding': 'gzip, deflate, br'}
        st.session_state.initialized = True



class Userflow:
    def __init__(self):
        self.initialize_attributes()
        self.display_userflow()
    
    def initialize_attributes(self):
        self.authenticator = Authentication()
        self.authenticated = st.session_state.authenticated
        self.userflow_complete = st.session_state.userflow_complete
        self.usertype = st.session_state.usertype

    def display_userflow(self):
        if not st.session_state.authenticated:
            self.userflow_display_1()
        else:
            self.switch_homepage()

    def userflow_display_1(self):
        self.maincontainer = ps.userflow_styled_container2(border=False)
        with self.maincontainer:
            self.maincols = st.columns([1, 20, 1, 20, 1])
            with self.maincols[1]:
                self.exist_button = st.button(label="Existing User Login", key="exist_button", type="primary", use_container_width=True)
                if self.exist_button:
                    self.usertype = "existing"
                    self.userflow_display_2()
            with self.maincols[3]:
                self.new_button = st.button(label="New User Registration", key="new_button", type="primary", use_container_width=True)
                if self.new_button:
                    self.usertype = "new"
                    self.userflow_display_2()

    @st.experimental_dialog(title="User Login / Registration", width="large")
    def userflow_display_2(self):
        self.username = st.text_input(label="Username", key=f"username")
        self.password = st.text_input(label="Password", key=f"password", type="password")
        if self.usertype == "new":
            self.firstname = st.text_input(label="First Name", key="firstname")
            self.lastname = st.text_input(label="Last Name", key="lastname")
            self.business_name = st.text_input(label="Business Name", key="business_name")
            self.email = st.text_input(label="Email", key="email")
            self.createddate = datetime.now().isoformat()
            self.userrole = st.radio(label="User Role", options=["Admin", "Client", "Carrier"], index=None, horizontal=True)
        self.userflow_submit = st.button(label="Submit", key="userflow_submitted", type="primary")
        if self.userflow_submit:
            if self.usertype == "new":
                try:
                    self.authenticator.new_user(username=self.username, password=self.password, email=self.email, firstname=self.firstname, lastname=self.lastname, userrole=self.userrole, businessname=self.business_name)
                    st.rerun()
                except Exception as e:
                    print(e)
                    st.error("ERROR: There was an error please try again")


    def switch_homepage(self):
        path = "1_🏠_Home.py"
        st.switch_page(page=path)


class Authentication:
    def __init__(self):
        self.initialize_authentication_attributes()

    def initialize_authentication_attributes(self):
        #self.userdata =  {st.secrets.supabase.column_username: None, st.secrets.supabase.column_password: None, st.secrets.supabase.column_vectorstoreid: None, st.secrets.supabase.column_threadid: None, st.secrets.supabase.column_email: None, st.secrets.supabase.column_userrole: None, st.secrets.supabase.column_firstname: None, st.secrets.supabase.column_lastname: None, st.secrets.supabase.column_fullname: None, st.secrets.supabase.column_createddate: None, st.secrets.supabase.column_businessid: None}
        self.select_string = f"{st.secrets.supabase.column_username}, {st.secrets.supabase.column_password}, {st.secrets.supabase.column_vectorstoreid}, {st.secrets.supabase.column_threadid}, {st.secrets.supabase.column_email}, {st.secrets.supabase.column_userrole}, {st.secrets.supabase.column_firstname}, {st.secrets.supabase.column_lastname}, {st.secrets.supabase.column_fullname}, {st.secrets.supabase.column_createddate}, {st.secrets.supabase.column_businessid}"
        self.table = "users"
        self.userdata = None
        

    def new_user(self, username: str, password: str, email: str, firstname: str, lastname: str, userrole: Literal["Admin", "Client", "Carrier"], businessname: str):
        self.usertype = "new"
        self.businessname = businessname
        vectorid = oaiClient.beta.vector_stores.create(name=f"SpartakusAI - {firstname} {lastname}").id
        threadid = oaiClient.beta.threads.create(tool_resources={"file_search": {"vector_store_ids": [vectorid]}}).id
        self.response = supaClient.table("users").insert({"username": username, "password": password, "email": email, "firstname": firstname, "lastname": lastname, "fullname": f"{firstname} {lastname}", "createddate": datetime.now().isoformat(), "userrole": userrole, "threadid": threadid, "vectorstoreid": vectorid}).execute()
        print(self.response)
        self.manage_response()

    def existing_user(self, username: str, password: str):
        self.usertype = "existing"
        #self.check_user(username=username, password=password)
        self.response = supaClient.table("users").select(self.select_string).eq("username", username).eq("password", password).execute()
        print(self.response)
        self.manage_response()

    def manage_response(self):
        if self.response.data:
            self.userdata = self.response.data[0]
            print(self.userdata)
            self.set_sessionstate()
        else: 
            self.userdata = None

    def set_sessionstate(self):
        st.session_state.usertype = self.usertype
        st.session_state.userdata = self.userdata
        st.session_state.username = self.userdata['username']
        st.session_state.password = self.userdata['password']
        st.session_state.email = self.userdata['email']
        st.session_state.firstname = self.userdata['firstname']
        st.session_state.lastname = self.userdata['lastname']      
        st.session_state.fullname = self.userdata['fullname']
        st.session_state.businessname = self.businessname
        st.session_state.userrole = self.userdata['userrole']
        st.session_state.createddate = self.userdata['createddate']
        st.session_state.vectorid = self.userdata['vectorstoreid']
        st.session_state.threadid = self.userdata['threadid']
        st.session_state.authenticated = True
        st.session_state.userflow_complete = True
        print(st.session_state)
