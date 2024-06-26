import streamlit as st
from classes import clsPageSetup as ps, clsTools as t
from typing import Literal
from openai import OpenAI
import time
import json

pagenumber = 0
pagesetup = ps.PageSetup(page_number=pagenumber)

## Variables
client = OpenAI(api_key=st.secrets.openai.api_key)
assistantid = st.secrets.openai.main_assistant
threadid = st.session_state.threadid

# Container
chat_container = st.container(border=False)

## Functions
def append_and_display(role, content):
    message = {"role": role, "content": content}
    st.session_state.messages.append(message)
    with chat_container:
        with st.chat_message(role):
            st.markdown(content)

def run_assistant(content: str):
    #create message
    promptmessage = client.beta.threads.messages.create(role="user", thread_id=threadid, content=content)
    promptmessageid = promptmessage.id
    #create run
    statusmessage = st.toast("Initializing...")
    with chat_container:
        statusbox = st.status(label="Initializing...", expanded=False, state="running")
    run = client.beta.threads.runs.create(thread_id=threadid, assistant_id=assistantid)
    while run.status == "in_progress" or run.status == "queued":
        statusmessage = st.toast("Running...")
        time.sleep(2)
        run = client.beta.threads.runs.retrieve(run_id=run.id, thread_id=threadid)
        if run.status == "requires_action":
            statusmessage = st.toast("Running tools")
            statusbox.update(label="Running tools", expanded=False, state="running")
            tooloutputs = []
            toolcalls = run.required_action.submit_tool_outputs.tool_calls
            for call in toolcalls:
                tid = call.id
                tname = call.function.name
                targs = json.loads(call.function.arguments)
                toutput = getattr(t.Tools, tname)(**targs)
                tooloutputs.append({"tool_call_id": tid, "output": toutput})
            run = client.beta.threads.runs.submit_tool_outputs(run_id=run.id, thread_id=threadid, tool_outputs=tooloutputs)
            statusmessage = st.toast("Tools complete")
            statusbox.markdown(f"ToolCalls: {toolcalls} /n/nToolOutputs: {tooloutputs}")
        elif run.status == "completed":
            statusmessage = st.toast("Completed")
            statusbox.update(label="Completed", expanded=False, state="complete")
            threadmessages = client.beta.threads.messages.list(thread_id=threadid)
            for threadmessage in threadmessages:
                if threadmessage.role == "assistant" and threadmessage.run_id == run.id:
                    responsemessage = threadmessage.content[0].text.value
                    st.session_state.response = responsemessage
                    statusbox.markdown(responsemessage)
                    append_and_display(role="assistant", content=responsemessage)
            
            break



# 1. Display Chat Messages
for message in st.session_state.messages:
    append_and_display(role=message['role'], content=message['content'])

# 2. Add Chat Prompt
if prompt := st.chat_input(placeholder=st.session_state.placeholder1):
    append_and_display(role="user", content=prompt)
    st.session_state.prompt = prompt
    run_assistant(content=prompt)
    



