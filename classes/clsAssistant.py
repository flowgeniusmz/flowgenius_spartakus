import streamlit as st
from openai import OpenAI
from classes import clsPageSetup as ps, clsSessionState as ss, clsTools as t, clsStatus as stt, clsUtilities as u
from typing import Literal
import time
import json

sessionstate = ss.SessionState.get()

class Assistant:
    def __init__(self, type: Literal["main", "guest"]):
        self.client = OpenAI(api_key=st.secrets.openai.api_key)
        if type == "main": 
            self.assistant_id = st.secrets.openai.main_assistant
        elif type == "guest":
            self.assistant_id = st.secrets.openai.guest_assistant
            st.session_state.threadid = self.client.beta.threads.create(messages=[{"role": "user", "content": [{"type": "text", "text": sessionstate.get_value(key="placeholder3")}]}]).id
        self.thread_id = sessionstate.get_value(key="threadid")
        sessionstate.update(assistantid=self.assistant_id)
    
    def run_assistant(self):
        self.prompt = sessionstate.get_value(key="prompt")
        self.statusmessage = st.toast(body="Processing...please wait.", icon="⏳")
        self.statusbox = st.status(label="Initializing", expanded=False, state="running")
        self.create_message(role="user", content=self.prompt)
        self.create_run()
        self.wait_on_run()

    def wait_on_run(self):
        while self.run.status == "in_progress" or self.run.status == "queued":
            self.statusmessage = st.toast(body="Processing...please wait.", icon="⏳")
            self.statusbox.update(label="Running", expanded=False, state="running")
            time.sleep(2)
            self.retrieve_run()
            if self.run.status == "requires_action":
                self.statusmessage = st.toast(body="Running tools...")
                self.statusbox.update(label="Running tools", expanded=False, state="running")
                self.run_tools()
                self.statusbox.markdown(f"**Tool Calls**: {self.toolcalls} /n/n**Tool Outputs**: {self.tooloutputs}")
                self.submit_tools()
            elif self.run.status == "completed":
                self.get_response()
                self.statusmessage = st.toast("Completed")
                self.statusbox.update(label="Completed", expanded=False, state="complete")
                self.get_suggestions()
                break

    def create_message(self, role, content):
        self.message = self.client.beta.threads.messages.create(thread_id=self.thread_id, role=role, content=content)
        self.messageid = self.message.id

    def create_run(self):
        self.run = self.client.beta.threads.runs.create(thread_id=self.thread_id, assistant_id=self.assistant_id)
        self.runid = self.run.id
        self.runstatus = self.run.status
    
    def retrieve_run(self):
        self.run = self.client.beta.threads.runs.retrieve(run_id=self.runid, thread_id=self.thread_id)
        self.runid = self.run.id
        self.runstatus = self.run.status
    
    def run_tools(self):
        self.tooloutputs = []
        self.toolcalls = self.run.required_action.submit_tool_outputs.tool_calls
        for tc in self.toolcalls:
            tcid = tc.id
            tcname = tc.function.name
            tcargs = json.loads(tc.function.arguments)
            tcoutput = getattr(t.Tools, tcname)(**tcargs)
            self.tooloutputs.append({"tool_call_id": tcid, "output": f"{tcoutput}"})
    
    def submit_tools(self):
        self.run = self.client.beta.threads.runs.submit_tool_outputs(run_id=self.runid, thread_id=self.thread_id, tool_outputs=self.tooloutputs)
        self.runid = self.run.id
        self.runstatus = self.run.status
    
    def get_response(self):
        self.threadmessages = self.client.beta.threads.messages.list(thread_id=self.thread_id)
        for tm in self.threadmessages:
            if tm.role == "assistant" and tm.run_id==self.runid:
                self.response = tm.content[0].text.value
                sessionstate.update(response=self.response)
                st.session_state.messages.append({"role": "assistant", "content": self.response})
            

    def get_suggestions(self):
        self.suggestions = t.Tools.suggest_prompts(user_prompt=self.prompt, assistant_response=self.response)