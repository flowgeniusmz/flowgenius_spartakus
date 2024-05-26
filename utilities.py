import streamlit as st
from openai import OpenAI 
from supabase import create_client
from yelpapi import YelpAPI
from googlemaps import Client
from tavily import TavilyClient
from simple_salesforce import Salesforce
from typing import Literal
import time
from datetime import datetime
from tempfile import NamedTemporaryFile

def get_client(client_type: Literal["openai", "supabase", "salesforce", "googlemaps", "yelp", "tavily"]):
    if client_type == "openai":
        client = OpenAI(api_key=st.secrets.openai.api_key)
    elif client_type == "googlemaps":
        client = Client(key=st.secrets.google.maps_api_key)
    elif client_type == "salesforce":
        client = Salesforce(username=st.secrets.salesforce.username, password=st.secrets.salesforce.password, security_token=st.secrets.salesforce.security_token)
    elif client_type == "supabase":
        client = create_client(supabase_key=st.secrets.supabase.api_key_admin, supabase_url=st.secrets.supabase.url)
    elif client_type == "yelp":
        client = YelpAPI(api_key=st.secrets.yelp.api_key)
    elif client_type == "tavily":
        client = TavilyClient(api_key=st.secrets.tavily.api_key)
    return client

def get_current_datetime():
    current_datetime = datetime.now().isoformat()
    return current_datetime

def get_fullname(firstname: str, lastname: str):
    fullname = f"{firstname} {lastname}"
    return fullname

def create_vectorstore(firstname: str=None, lastname: str=None):
    if firstname is not None and lastname is not None:
        vname = f"SpartakusAI - {firstname} {lastname}"
    else:
        vname = f"SpartakusAI"
    vectorstoreid = OpenAI(api_key=st.secrets.openai.api_key).beta.vector_stores.create(name=vname).id
    return vectorstoreid

def create_thread(vector_store_id: str=None):
    if vector_store_id is not None:
        tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}}
        threadid = OpenAI(api_key=st.secrets.openai.api_key).beta.threads.create(tool_resources=tool_resources).id
    else:
        threadid = OpenAI(api_key=st.secrets.openai.api_key).beta.threads.create().id
    return threadid

def create_tempfile(suffix: Literal[".txt", ".log", ".dat", ".tmp", ".csv", ".json", ".xml", ".html", ".xlsx", ".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".mp3", ".wav", ".ogg", ".flac", ".mp4", ".avi", ".mov", ".mkv", ".zip", ".tar", ".gz", ".bz2", ".7z", ".rar", ".py", ".java", ".c", ".cpp", ".js", ".html", ".css"]):
    with NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file_path = temp_file.name
        return temp_file_path

def add_userdata(userdata):
    st.session_state.userdata = userdata
    st.session_state.username = userdata["username"]
    st.session_state.password = userdata["password"]
    st.session_state.email = userdata["email"]
    st.session_state.firstname = userdata["firstname"]
    st.session_state.lastname = userdata["lastname"]
    st.session_state.fullname = userdata["fullname"]
    st.session_state.vectorstoreid = userdata["vectorstoreid"]
    st.session_state.threadid = userdata["threadid"]
    st.session_state.createddate = userdata["createddate"]
    st.session_state.userrole = userdata["userrole"]
    
def user_login(username: str, password: str):
    client = create_client(supabase_key=st.secrets.supabase.api_key_admin, supabase_url=st.secrets.supabase.url)
    response = client.table("users").select("username", "password", "email", "firstname", "lastname", "fullname", "vectorstoreid", "threadid", "createddate", "userrole").eq("username", username).eq("password", password).execute()
    responsedata = response.data
    if responsedata:
        userdata = responsedata[0]
        st.session_state.authenticated = True
        add_userdata(userdata=userdata)
        return True
    else:
        st.session_state.authenticated = False
        return False

def user_create(username: str, password: str, email: str, businessname: str, firstname: str, lastname: str, userrole: Literal["Admin", "Client", "Carrier"]):
    client = create_client(supabase_key=st.secrets.supabase.api_key_admin, supabase_url=st.secrets.supabase.url)
    vectorstoreid = create_vectorstore(firstname=firstname, lastname=lastname)
    threadid = create_thread(vector_store_id=vectorstoreid)
    response = client.table("users").insert({"username": username, "password": password, "email": email, "firstname": firstname, "lastname": lastname, "fullname": get_fullname(firstname=firstname, lastname=lastname), "userrole": userrole, "createddate": get_current_datetime(), "threadid": threadid, "vectorstoreid": vectorstoreid}).execute()
    responsedata = response.data
    if responsedata:
        userdata = responsedata[0]
        add_userdata(userdata=userdata)
        st.session_state.authenticated = True
        return True
    else:
        st.session_state.authenticated = False
        return False

