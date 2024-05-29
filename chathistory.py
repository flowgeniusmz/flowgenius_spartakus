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