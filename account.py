import streamlit as st
from config import pagesetup as ps

class BasicUserInformation:
    def __init__(self):
        self.initialize_attributes()
        self.initialize_display()
    def initialize_attributes(self):
        self.username = st.session_state.username
        self.password = st.session_state.password
        self.firstname = st.session_state.firstname
        self.lastname = st.session_state.lastname
        self.fullname = st.session_state.fullname
        self.email = st.session_state.email
        self.businessname = st.session_state.businessname
        self.businessaddress = st.session_state.businessaddress
        self.threadid = st.session_state.threadid
        self.vectorstoreid = st.session_state.vectorstoreid
        self.createddate = st.session_state.createddate
        self.userrole = st.session_state.userrole

    def initialize_display(self):
        self.basicinfo_container = st.container(height=300, border=False)
        with self.basicinfo_container:
            ps.get_gray_header(varText="User Basic Information")
            self.basicinfocols = st.columns([1,20,1,20,1])
            with self.basicinfocols[1]:
                st.text_input(label="First Name", disabled=True, value=self.firstname)
                st.text_input(label="Email Address", disabled=True, value=self.email)
                st.text_input(label="Business Name", disabled=True, value=self.businessname)
            with self.basicinfocols[3]:
                st.text_input(label="Last Name", disabled=True, value=self.lastname)
                st.text_input(label="Username", disabled=True, value=self.username)
                st.text_input(label="Business Address", disabled=True, value=self.businessaddress)

