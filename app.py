import streamlit as st
from config import pagesetup as ps, sessionstates as ss
from typing import Literal
from openai import OpenAI
from datetime import datetime
from supabase import create_client


st.set_page_config(page_title=st.secrets.appconfig.app_name, page_icon=st.secrets.appconfig.app_icon, layout=st.secrets.appconfig.app_layout, initial_sidebar_state=st.secrets.appconfig.app_initial_sidebar)
# ss.initialize_session_state()
# class_userflow.UserFlow()
ps.display_background_image_stretch()

def submit_callback(usertype: Literal["existing", "new"], username: str, password: str, email: str, businessname: str, firstname: str, lastname: str, userrole: Literal["Admin", "Client", "Carrier"]):
    supaClient = create_client(supabase_key=st.secrets.supabase.api_key_admin, supabase_url=st.secrets.supabase.url)
    oaiClient = OpenAI(api_key=st.secrets.openai.api_key)
    if usertype == "new":
        vectorid = oaiClient.beta.vector_stores.create(name=f"SpartakusAI - {firstname} {lastname}").id
        threadid = oaiClient.beta.threads.create(tool_resources={"file_search": {"vector_store_ids": [vectorid]}})
        userdatasubmitted = {"username": username, "password": password, "email": email, "firstname": firstname, "lastname": lastname, "fullname": f"{firstname} {lastname}", "userrole": userrole, "createddate": datetime.now().isoformat(), "threadid": threadid, "vectorstoreid": vectorid}
        print(userdatasubmitted)
        response = supaClient.table("users").insert(userdatasubmitted).execute()
        if response.data:
            userdata = response.data[0]
            print(userdata)
            st.session_state.userdata = userdata
            st.session_state.authenticated = True
            st.switch_page("1_🏠_Home.py")
        else:
            st.error("ERROR")
            print(response)
    else:
        response = supaClient.table("users").select("username", "password", "email", "firstname", "lastname", "fullname", "threadid", "vectorstoreid", "createddate", "userrole").eq(column="username", value=username).eq(column="password", value=password).execute()
        if response.data:
            userdata = response.data[0]
            print(userdata)
            st.session_state.userdata = userdata
            st.session_state.authenticated = True
            st.switch_page("1_🏠_Home.py")
        else:
            st.error("ERROR")
            print(response)



@st.experimental_dialog(title="Existing User Sign In / New User Registration", width="large")
def display_userflow(usertype: Literal["new", "existing"]):
    username = st.text_input(label="Username", key="username")
    password = st.text_input(label="Password", key="password", type="password")
    if usertype == "new":
        email = st.text_input(label="Email Address", key="email")
        businessname = st.text_input(label="Business Name", key="businessname")
        firstname = st.text_input(label="First Name", key="firstname")
        lastname = st.text_input(label="Last Name", key="lastname")
        userrole = st.radio(label="User Role", options=["Admin", "Client", "Carrier"], horizontal=True, index=None, key="userrole")
    else:
        email = None
        businessname = None
        firstname = None
        lastname = None
        userrole = "Admin"

    submit = st.button(label="Submit", key="submit", type="primary")#, #on_click=submit_callback, args=[usertype,username, password, email, businessname, firstname, lastname, userrole])
    if submit:
        submit_callback(usertype=usertype, username=username, password=password, email=email, businessname=businessname, firstname=firstname, lastname=lastname, userrole=userrole)                 

def maindisplay():
    ps.set_title_manual(varTitle="SpartakusAI", varSubtitle="User Login / Registration")
    maincontainer = ps.userflow_styled_container2()
    with maincontainer:
        maincols = st.columns([1,20,1,20,1])
        with maincols[1]:
            btnExisting = st.button(label="Existing User Login", key="existinguser", use_container_width=True, type="primary", on_click=display_userflow, args=["existing"])
        with maincols[3]:
            btnNew = st.button(label="New User Registration", key="new_submit", on_click=display_userflow, args=["new"], type="primary", use_container_width=True)




if "initialized" not in st.session_state:
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


if not st.session_state.authenticated:
    maindisplay()
else:
    st.switch_page("1_🏠_Home.py")