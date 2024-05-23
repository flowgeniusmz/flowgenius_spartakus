import streamlit as st
from classes import user_class

class SessionState:
    def __init__(self):
        self.initialize_user()
        self.initialize_requests()
    
    def initialize_user(self):
        if "user_initialized" not in st.session_state:
            st.session_state.user = user_class.User()
            st.session_state.user_initailized = False
            st.session_state.user_authenticated = False
            st.session_state.user_type = None
            st.session_state.userflow_complete = False

    def initialize_requests(self):
        self.request_headers = {'Accept': 'application/json', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36', 'Accept-Language': 'en-US,en;q=0.9','Accept-Encoding': 'gzip, deflate, br'}
