import streamlit as st


class SessionState:
    def __init__(self):
        self.initialize_user()
        self.initialize_requests()
        self.initialize_userflow()
    
    def initialize_user(self):
        if "user_initialized" not in st.session_state:
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


    def initialize_userflow(self):
        if "userflow_initialized" not in st.session_state:
            st.session_state.userflow_initialized = False
            st.session_state.userflow_complete = False
            st.session_state.userflow_authenticated = False
            st.session_state.usertype = None

    def initialize_requests(self):
        self.request_headers = {'Accept': 'application/json', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36', 'Accept-Language': 'en-US,en;q=0.9','Accept-Encoding': 'gzip, deflate, br'}
