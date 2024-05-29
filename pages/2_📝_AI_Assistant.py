import streamlit as st
from config import pagesetup as ps
from openai import OpenAI
from assistant import Assistant, Tools
import time
import json

page_number = 1
ps.master_page_display_styled_popmenu_pop(varPageNumber=page_number)
#st.write(st.session_state.threadid)

assistantid = st.secrets.openai.assistant_id
threadid = st.session_state.threadid
vectorid = st.session_state.vectorstoreid
client = OpenAI(api_key=st.secrets.openai.api_key)
threadmessages = client.beta.threads.messages.list(thread_id=threadid)



chatcontainer = ps.userflow_styled_container2(height=400)
with chatcontainer:
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

if prompt := st.chat_input(placeholder="Enter your question or request here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    promptmessage = client.beta.threads.messages.create(thread_id=threadid, role="user", content=prompt)
    with chatcontainer:
        with st.chat_message("user"):
            st.markdown(prompt)
        status = st.status(label="Running assistant...please wait.", expanded=False, state="running")
        with status:
            st.markdown(f"Initializing....messageid: {promptmessage.id}")
    
    run = client.beta.threads.runs.create(thread_id=threadid, assistant_id=assistantid)
    while run.status == "queued" or run.status == "in_progress":
        time.sleep(2)
        st.toast("processing")
        run = client.beta.threads.runs.retrieve(run_id=run.id, thread_id=threadid)
        if run.status == "completed":
            st.toast("Completed")
            status.update(label="Completed", state="complete", expanded=False)
            threadmessages = client.beta.threads.messages.list(thread_id=threadid)
            for threadmessage in threadmessages:
                if threadmessage.role == "assistant" and threadmessage.run_id == run.id:
                    st.session_state.messages.append({"role": "assistant", "content": threadmessage.content[0].text.value})
                    with chatcontainer:
                        with st.chat_message("assistant"):
                            st.markdown(threadmessage.content[0].text.value)
            break
        elif run.status == "requires_action":
            tool_outputs = []
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            with status:
                st.markdown(tool_calls)
                print(tool_calls)
            for tool_call in tool_calls:
                tool_call_id = tool_call.id
                tool_call_name = tool_call.function.name
                tool_call_args = json.loads(tool_call.function.arguments)
                tool_call_output = getattr(Tools, tool_call_name)(**tool_call_args)
                tool_outputs.append({"tool_call_id": tool_call_id, "output": f"{tool_call_output}"})
            run = client.beta.threads.runs.submit_tool_outputs(run_id=run.id, thread_id=threadid, tool_outputs=tool_outputs)


