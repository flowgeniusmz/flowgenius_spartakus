import streamlit as st
from config import pagesetup as ps
from openai import OpenAI
from assistant import Assistant, Tools
import time
import pandas as pd
import json


class ChatHistory:
    def __init__(self):
        self.initialize_attributes()
        self.get_thread_messages()
        self.get_thread_messages_dataframe()
        self.initialize_display()

    def initialize_attributes(self):
        self.client = OpenAI(api_key=st.secrets.openai.api_key)
        self.threadid = st.session_state.threadid
        self.assistantid = st.secrets.openai.assistant_id
        self.vectorid = st.session_state.vectorstoreid
    
    def get_thread_messages(self):
        self.thread_messages = self.client.beta.threads.messages.list(thread_id=self.threadid)
    
    def get_thread_messages_dataframe(self):
        self.df_messages = []
        for threadmessage in self.thread_messages:
            new_row = {
            "messageid": threadmessage.id,
            "runid": threadmessage.run_id,
            "role": threadmessage.role,
            "content": threadmessage.content[0].text.value
            }
            self.df_messages.append(new_row)
        self.df_thread_messages = pd.DataFrame(self.df_messages)
        self.user_messages = self.df_thread_messages[self.df_thread_messages['role'] == 'user']['content'].tolist()
        self.assistant_messages = self.df_thread_messages[self.df_thread_messages['role'] == 'assistant']['content'].tolist()

    def initialize_display(self):
        self.history_container = st.container(border=False)
        with self.history_container:
            for user_msg, asst_msg in zip(self.user_messages, self.assistant_messages):
                runcontainer = ps.userflow_styled_container2()
                with runcontainer:
                    runcols = st.columns([10,1,10])
                    with runcols[0]:
                        userpop = st.popover(label="User Message", use_container_width=True, disabled=False)
                        with userpop:
                            st.markdown(user_msg)
                    with runcols[2]:
                        asstpop = st.popover(label="Assistant Message", use_container_width=True, disabled=False)
                        with asstpop:
                            st.markdown(asst_msg)

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


class FormAccess:
    def __init__(self):
        self.initialize_attributes()
        self.initialize_display()

    def initialize_attributes(self):
        self.f36 = st.session_state.f36
        self.f125= st.session_state.f125
        self.f126 = st.session_state.f126
        self.f127 = st.session_state.f127
        self.f130 = st.session_state.f130
        self.f133 = st.session_state.f133
        self.f137 = st.session_state.f137
        self.f140 = st.session_state.f140
        self.forms = [{"form": "Form 36", "access": self.f36}, {"form": "Form 125", "access": self.f125},{"form": "Form 126", "access": self.f126},{"form": "Form 127", "access": self.f127}, {"form": "Form 130", "access": self.f130},{"form": "Form 133", "access": self.f133},{"form": "Form 137", "access": self.f137},{"form": "Form 140", "access": self.f140}]
    
    def initialize_display(self):
        self.formaccess_container = st.container(border=False)
        with self.formaccess_container:
            self.formaccesscols = st.columns([1,20,1])
            for form in self.forms:
                form_name = form['form']
                form_value = form['access']
                with self.formaccesscols[1]:
                    st.checkbox(label=form_name, value=form_value, disabled=True)