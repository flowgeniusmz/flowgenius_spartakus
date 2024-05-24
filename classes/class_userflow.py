import streamlit as st
from typing import Literal
from classes import class_clients, class_user
from datetime import datetime
from config import pagesetup as ps




class UserFlow:
    def __init__(self):
        self.initialize_userflow_attributes()
        self.initialize_sessionstate()
        self.userflow_render()

    def initialize_sessionstate(self):
        if "userflow_initialized" not in st.session_state:
            st.session_state.userflow_initialized = True
            st.session_state.userflow_complete = False
            st.session_state.userflow_authenticated = False

    def initialize_userflow_attributes(self):
        self.supabase_client = class_clients.SupabaseClient()
        self.userflow_complete = st.session_state.userflow_complete
        self.userflow_authenticated = st.session_state.userflow_authenticated

    def userflow_render(self):
        if self.userflow_complete:
            self.switch_to_homepage()
        else:
            self.userflow_display_1()

    def userflow_display_1(self):
        title_display = ps.set_title_manual(varTitle="SpartakusAI", varSubtitle="User Login / Registration")
        selection_container = ps.userflow_styled_container()
        with selection_container:
            usertype_cols = st.columns([1,20,1,20,1])
            with usertype_cols[1]:
                self.usertype_button_new = st.button(label="New User", key="new", type="primary", use_container_width=True)
                if self.usertype_button_new:
                    self.userflow_display(usertype="new")
            with usertype_cols[3]:
                self.usertype_button_exist = st.button(label="Existing User", key="existing", type="primary", use_container_width=True)
                if self.usertype_button_exist:
                    self.userflow_display(usertype="existing")


    @st.experimental_dialog(title="User Login / Registration", width="large")
    def userflow_display(self, usertype: Literal["new", "existing"]):
        self.usertype = usertype
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
                self.fullname = f"{self.firstname} {self.lastname}"
                self.user_data = self.supabase_client.user_addition(username=self.username, password=self.password, email=self.email, firstname=self.firstname, lastname=self.lastname, fullname=self.fullname, createddate=self.createddate, userrole=self.userrole)
            elif self.usertype == "existing":
                self.user_data = self.supabase_client.user_authentication(username=self.username, password=self.password)
            else: 
                self.user_data = None
            
            if self.user_data is not None:
                st.session_state.userflow_complete = True
                st.session_state.userflow_authenticated = True
                st.session_state.usertype = self.usertype
                st.session_state.user  = class_user.User()
                self.user = st.session_state.user
                self.userflow_complete = True
                self.userflow_authenticated = True
                self.userdata = self.user_data
                st.session_state.userdata = self.userdata
                st.rerun()
            else:
                st.error("Try again")
    
    def switch_to_homepage(self):
        path = st.secrets.pageconfig.page_paths[0]
        st.switch_page(page="1_🏠_Home.py")
