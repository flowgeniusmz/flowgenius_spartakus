import streamlit as st
from config import pagesetup as ps, sessionstates as ss
from typing import Literal
import utilities as u
from classes import clsSessionState as ss, clsPageSetup as ps, clsUserState as us



# 1. Set App Config
st.set_page_config(page_title=st.secrets.appconfig.app_name, page_icon=st.secrets.appconfig.app_icon, layout=st.secrets.appconfig.app_layout, initial_sidebar_state=st.secrets.appconfig.app_initial_sidebar)

# 2. Set Session State Config
ss.sessionstate_controller()

@st.experimental_dialog("User Login / Registration", width="large")
def userflow_dialog(usertype: Literal["new", "existing"]):
    st.session_state.username = st.text_input(label="Username", key="_username")
    st.session_state.password = st.text_input(label="Password", key="_password", type="password")
    if usertype == "new":
        st.session_state.firstname = st.text_input(label="First Name", key="_firstname")
        st.session_state.lastname = st.text_input(label="Last Name", key="_lastname")
        st.session_state.email = st.text_input(label="Email Address", key="_email")
        st.session_state.businessname = st.text_input(label="Business Name", key="_businessname")
        st.session_state.businessaddress = st.text_input(label="Business Address", key="_businessaddress")
        st.session_state.userrole = st.radio(label="User Role", key="_userrole", options=["Admin", "Client", "Carrier"], horizontal=True, index=None)
    st.session_state.userflow_submitted = st.button(label="Submit", type="primary")
    if st.session_state.userflow_submitted:
        if usertype == "new":
            auth = u.user_create(username=st.session_state.username, password=st.session_state.password, email=st.session_state.email, businessname=st.session_state.businessname, businessaddress=st.session_state.businessaddress, firstname=st.session_state.firstname, lastname=st.session_state.lastname, userrole=st.session_state.userrole)
        elif usertype == "existing":
            auth = u.user_login(username=st.session_state.username, password=st.session_state.password)
        if auth:
            st.rerun()
        else:
            st.error("ERROR: Please try again")


if not st.session_state.userflow_submitted:
    # 3. Set Page Config
    maincontainer = ps.get_userflow_setup()
    with maincontainer:
        maincols = st.columns([1, 20, 1, 20, 1])
        with maincols[1]:
            btn_exist_user = st.button("Existing User Login", type="primary", use_container_width=True)
        with maincols[3]:
            btn_new_user = st.button("New User Registration", type="primary", use_container_width=True)

    


    
    # 4. Define Dialog
    
   

    if btn_exist_user:
        userflow_dialog(usertype="existing")
    elif btn_new_user:
        userflow_dialog(usertype="new")

  

else:
    st.switch_page("pages/1_🏠_Home.py")





