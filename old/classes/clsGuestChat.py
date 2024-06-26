# import streamlit as st
# from openai import OpenAI
# from classes import clsSessionState as ss, clsTools as t, clsPageSetup as ps, clsUtilities as ut
# import time
# import json
# from tavily import TavilyClient
# from googlemaps import places, geocoding, addressvalidation
# from googlesearch import search

# class GuestChat:
#     def __init__(self):
#         self.assistantid = "asst_zyz5pyaA9frv3EJ29gl919xJ"
#         self.client = OpenAI(api_key=st.secrets.openai.api_key)
#         self.threadid = self.client.beta.threads.create(messages=[{"role": "user", "content": {"type": "text", "text": st.secrets.openai.guest_initial}}])
#         self.displaymessages = [{"role": "assistant", "content": st.secrets.openai.guest_initial}]
#         self.prompt = None
#         self.response = None
#         self.threadmessages = None
#         self.suggestions = st.session_state.suggestions
#         self.sug1 = st.session_state.sug1
#         self.sug2 = st.session_state.sug2
#         self.sug3 = st.session_state.sug3
#         self.sug4 = st.session_state.sug4

#     def display(self):
#         self.window = st.container(border=False)
#         with self.window:
#             self.chat_container = ps.PageUtilities.get_styled_container()
#             with self.chat_container:
#                 self.message_container = st.container(height=400, border=False)
#                 self.suggestion_container = st.empty()
#             self.prompt_container = st.container(border=False, height=100)
#             with self.prompt_container:
#                 self.prompt_input = st.chat_input(placeholder="Type your response or question here! (Ex: Yes I would like to buy insurance)")
        
#         with self.message_container:
#             for msg in self.displaymessages:
#                 with st.chat_message(msg['role']):
#                     st.markdown(msg['content'])
        
#         if self.suggestions is not None:
            
        
#     def runchat(self):
#         self.run = self.client.beta.threads.runs.create(assistant_id=self.assistantid, thread_id=self.threadid)
#         self.runid = self.run.id
#         self.runstatus = self.run.status
#         while self.runstatus !="completed":



# window = st.container(border=False)
# with window:
#     chat_container = ps.PageUtilities.get_styled_container()
#     with chat_container:
#         message_container = st.container(height=400, border=False)
#         suggestion_container = st.empty()
#     prompt_container = st.container(border=False, height=100)

