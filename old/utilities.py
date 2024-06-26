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
import stripe
from urllib.parse import quote
import requests
import json

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
    run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=st.secrets.openai.assistant_id, tool_choice={"type": "function", "function": {"name": "business_research"}},additional_instructions="Run business_research asynchronously. Respond with 'Welcome to SpartakusAI - how may I help you?' only.")
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
        print(userdata)
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

def get_summary_message():
    client = OpenAI(api_key=st.secretse.openai.api_key)
    threadid = st.session_state.threadid
    assistantid = st.secrets.openai.assistant_id
    additional_instructions = "The user has just returned for more assistance. Refresh yourself on the user information. Then review the previous chat messages and provide a concise but comprehensive summary of all previous chats. Return only the summary."
    messagetext = "Please summarize all previous chats for me and provide a concise yet comprehensive recap to refresh my memory."
    tmessage = client.beta.threads.messages.create(thread_id=threadid, role="user", content=messagetext)
    run = client.beta.threads.runs.create(thread_id=threadid, assistant_id=assistantid, additional_instructions=additional_instructions, tool_choice="none")
    while run.status == "queued" or run.status =="in_progress":
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(run_id=run.id, thread_id=threadid)
        if run.status == "completed":
            tmessages = client.beta.threads.messages.list(thread_id=threadid)
            for msg in tmessages:
                if msg.role == "assistant" and msg.run_id == run.id:
                    st.session_state.welcomesummary = msg.content[0].text.value

def send_welcome_email(username, password, firstname, lastname, email, businessname, businessaddress, createddate):
    payload = {
    "username": username,
    "password":password,
    "firstname": firstname,
    "lastname": lastname,
    "email": email,
    "businessname": businessname,
    "businessaddress": businessaddress,
    "createddate": createddate
    }
    url = st.secrets.requests.welcome_email_url
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36','Accept-Language': 'en-US,en;q=0.9','Accept-Encoding': 'identity'}
    response = requests.post(url=url, headers=headers, json=payload)
    response_text = response.text
    response_json = response.json()
    return response_json



# get queues

# be mroe concise
#prompts

# ai asking it questions, ask it to interview to (1) find out the purpose (i.e. form 125) (2) fulfill that purpose
# use the form names, not numbers
# prompt instructions to limit the number of questions and make deductions / research
# dont ask questions that are knowable or researchable
# default question by question 1 at a time
# secratery of state - all the info
# dunn and bradstreet

## is  this your name, is this locatred here? - get them interested, would you like to save this information, last 4 of phone number is pw, create user interface

## subdirectory on spartakus

# abandoned chat

a = user_login(username="mzozulia@flowgenius.com", password="EverlyQuinn#7665")
print(a)
