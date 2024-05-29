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
import base64
import json
from tools import Tools

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

def create_first_message(thread_id: str, userdata):
    client = OpenAI(api_key=st.secrets.openai.api_key)
    message = st.secrets.messageconfig.message_1
    content = message.format(user_data=f"{userdata}")
    threadmessage = client.beta.threads.messages.create(thread_id=thread_id, role="user", content=content)
    message1 = st.secrets.messageconfig.message_4
    content1 = message1.format(fullname=st.session_state.fullname, businessname = st.session_state.businessname, businessaddress=st.session_state.businessaddress)
    threadmessage1 = client.beta.threads.messages.create(thread_id=thread_id, role="assistant", content=content1)
    toolchoice = [{"type": "function", "function": {"name": "tavily_search"}}, {"type": "function", "function": {"name": "google_places_search"}}]
    st.toast("Please wait while your account is created")
    run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=st.secrets.openai.assistant_id, additional_instructions="Run tavily_search and google_places_search asynchronously. Respond with 'Welcome to SpartakusAI - how may I help you?' only.")
    while run.status == "in_progress" or run.status == "queued":
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(run_id=run.id, thread_id=thread_id)
        if run.status == "requires_action":
            tool_outputs = []
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            for tool_call in tool_calls:
                tool_id = tool_call.id
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                tool_output = getattr(Tools, tool_name)(**tool_args)
                tool_outputs.append({"tool_call_id": tool_id, "output": f"{tool_output}"})
            run = client.beta.threads.runs.submit_tool_outputs(run_id=run.id, thread_id=thread_id, tool_outputs=tool_outputs)
        elif run.status == "completed":
            st.toast("Account created!")
            break

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
    st.session_state.businessname = userdata["businessname"]
    st.session_state.businessaddress = userdata["businessaddress"]
    st.session_state.f36 = userdata["form_036"]
    st.session_state.f125 = userdata["form_125"]
    st.session_state.f126 = userdata["form_126"]
    st.session_state.f127 = userdata["form_127"]
    st.session_state.f130 = userdata["form_130"]
    st.session_state.f133 = userdata["form_133"]
    st.session_state.f137 = userdata["form_137"]
    st.session_state.f140 = userdata["form_140"]
    
def user_login(username: str, password: str):
    client = create_client(supabase_key=st.secrets.supabase.api_key_admin, supabase_url=st.secrets.supabase.url)
    response = client.table("users").select("username", "password", "email", "firstname", "lastname", "fullname", "vectorstoreid", "threadid", "createddate", "userrole", "businessname", "businessaddress", "form_036", "form_125", "form_126", "form_127", "form_130", "form_133", "form_137", "form_140").eq("username", username).eq("password", password).execute()
    responsedata = response.data
    if responsedata:
        userdata = responsedata[0]
        st.session_state.authenticated = True
        add_userdata(userdata=userdata)
        return True
    else:
        st.session_state.authenticated = False
        return False

def user_create(username: str, password: str, email: str, businessname: str, businessaddress: str, firstname: str, lastname: str, userrole: Literal["Admin", "Client", "Carrier"]):
    client = create_client(supabase_key=st.secrets.supabase.api_key_admin, supabase_url=st.secrets.supabase.url)
    vectorstoreid = create_vectorstore(firstname=firstname, lastname=lastname)
    threadid = create_thread(vector_store_id=vectorstoreid)
    if userrole == "Admin":
        response = client.table("users").insert({"username": username, "password": password, "email": email, "firstname": firstname, "lastname": lastname, "fullname": get_fullname(firstname=firstname, lastname=lastname), "userrole": userrole, "createddate": get_current_datetime(), "threadid": threadid, "vectorstoreid": vectorstoreid, "businessname": businessname, "businessaddress": businessaddress, "form_036": True, "form_125": True, "form_126": True, "form_127": True, "form_130": True, "form_133": True, "form_137": True, "form_140": True }).execute()
    elif userrole == "Client" or userrole == "Carrier":
        response = client.table("users").insert({"username": username, "password": password, "email": email, "firstname": firstname, "lastname": lastname, "fullname": get_fullname(firstname=firstname, lastname=lastname), "userrole": userrole, "createddate": get_current_datetime(), "threadid": threadid, "vectorstoreid": vectorstoreid, "businessname": businessname, "businessaddress": businessaddress, "form_036": False, "form_125": True, "form_126": True, "form_127": False, "form_130": False, "form_133": False, "form_137": False, "form_140": False }).execute()
    responsedata = response.data
    if responsedata:
        userdata = responsedata[0]
        add_userdata(userdata=userdata)
        create_first_message(thread_id=threadid, userdata=userdata)
        #create_first_message(thread_id=threadid, userdata=userdata)
        st.session_state.authenticated = True
        return True
    else:
        st.session_state.authenticated = False
        return False

def append_chat_message(role: str, content: str):
    st.session_state.messages.append({"role": role, "content": content})


def convert_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
        return encoded_string
    
def encode_image(image_path: str):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return encoded_string
    
def get_base64_image_url(b64encoded_image):
    url = f"data:image/png;base64,{b64encoded_image}"
    return url

