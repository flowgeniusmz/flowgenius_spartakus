import streamlit as st
import base64
from datetime import datetime
from supabase import create_client
from simple_salesforce import Salesforce
from typing import Literal

supaClient = create_client(supabase_key=st.secrets.supabase.api_key_admin, supabase_url=st.secrets.supabase.url)
sfdcClient = Salesforce(username=st.secrets.salesforce.username, password=st.secrets.salesforce.password, security_token=st.secrets.salesforce.security_token)


class Utilities:
    @staticmethod
    def encode_image(image_path: str):
        with open(file=image_path, mode="rb") as image_file:
            encoded_image = base64.b64encode(s=image_file.read()).decode()
        return encoded_image
    
    @staticmethod
    def get_file_content(file_path: str):
        with open(file=file_path, mode="rb") as file:
            content = file.read()
        return content
    
    @staticmethod
    def get_datetime():
        value = datetime.now().isoformat()
        return value
    
    @staticmethod
    def authenticate_user():
        client = create_client(supabase_key=st.secrets.supabase.api_key_admin, supabase_url=st.secrets.supabase.url)
        response = client.table(table_name="users").select("*").eq(column="username", value=st.session_state.username).eq(column="password", value=st.session_state.password).execute()
        responsedata = response.data
        if response.data:
            userdata = responsedata[0]
            st.session_state.authenticated = True
            st.session_state.userdata = userdata
            Utilities.callback_userdata()
            return True
        else:
            st.session_state.authenticated = False
            return False
            

    @staticmethod
    def callback_userdata():
        userdata = st.session_state.userdata
        st.session_state.firstname = userdata["firstname"]
        st.session_state.lastname = userdata["lastname"]
        st.session_state.fullname = userdata["fullname"]
        st.session_state.salesforceid = userdata["salesforceid"]
        st.session_state.threadid = userdata["threadid"]
        st.session_state.vectorid = userdata["vectorstoreid"]
        st.session_state.subsidiary = userdata["subsidiary"]
        st.session_state.isactive = userdata["isactive"]
        st.session_state.email = userdata["email"]

class SalesforceUtilities:
    @staticmethod
    def get_soql_query(type: Literal["tasks", "leads", "accounts", "opportunities"]):
        queries = dict(st.secrets.soql)
        default = st.secrets.soql.leads
        query_template = queries.get(type, default)
        query = query_template.format(          )
        response = sfdcClient.query(query=query)
        records = response['records']     
        return records
    

