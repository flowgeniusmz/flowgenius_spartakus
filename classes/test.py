# import streamlit as st
# from openai import OpenAI
# from tavily import TavilyClient
# import json
# import time

# def tavily_search(query):
#     client = TavilyClient(api_key=st.secrets.tavily.api_key)
#     response = client.search(query=query, max_results=10, search_depth="advanced", include_raw_content=True, include_answer=True)
#     return response

# assistant_id = st.secrets.openai.assistant_id
# client = OpenAI(api_key=st.secrets.openai.api_key)
# vstore = client.beta.vector_stores.create(name="SpartakusAI - Carlos Nolasko")
# vstoreid = vstore.id
# thread = client.beta.threads.create(tool_resources={"file_search": {"vector_store_ids": [vstoreid]}})
# threadid = thread.id

# initial_message_template = """Here is the user that I will be assisting:
# First Name: {firstname}
# Last Name: {lastname}
# Businses Name: {businessname}

# I will do as much research as I can to learn about this person and the business. I will summarize as much content as possible so that I can reference in the future."""

# firstname = "Carlos"
# lastname = "Nolasko"
# businessname = "Nolasko Insurance Advisors PLLC"

# initial_message_content = initial_message_template.format(firstname=firstname, lastname=lastname, businessname=businessname)

# initial_message = client.beta.threads.messages.create(thread_id=threadid, role="user", content=initial_message_content)

# initial_run = client.beta.threads.runs.create(assistant_id=assistant_id, thread_id=threadid, additional_instructions="Use search_tavily() function to research the users business. Return and summarize as much data as you can - this is for me to learn about the user and the business.", tool_choice={"type": "function", "function": {"name": "search_tavily"}})
# print(initial_run.id)
# while initial_run.status != "completed":
#     time.sleep(2)
#     initial_run = client.beta.threads.runs.retrieve(run_id=initial_run.id, thread_id=threadid)
#     if initial_run.status == "completed":
#         messages = client.beta.threads.messages.list(thread_id=threadid, run_id=initial_run.id)
#         print(messages)
#         for message in messages:
#             if message.role == "assistant" and message.run_id == initial_run.id:
#                 print(message.content[0].text.value)
#                 break
    
#     elif initial_run.status == "requires_action":
#         tooloutputs = []
#         print(initial_run)
#         toolcalls = initial_run.required_action.submit_tool_outputs.tool_calls
#         print(toolcalls)
#         for toolcall in toolcalls:
#             toolname = toolcall.function.name
#             toolargs = json.loads(toolcall.function.arguments)
#             toolid = toolcall.id
#             if toolname == "tavily_search":
#                 toolresponse = tavily_search(query=toolargs.get("query"))
#                 tooloutputs.append({"tool_call_id": toolid, "output": toolresponse})
#         if tooloutputs:
#             initial_run = client.beta.threads.runs.submit_tool_outputs(thread_id=threadid, run_id=initial_run.id, tool_outputs=tooloutputs)

#             if initial_run.status == "completed":
#                 messages = client.beta.threads.messages.list(thread_id=threadid, run_id=initial_run.id)
#                 for message in messages:
#                     if message.role == "assistant" and message.run_id == initial_run.id:
#                         print(message.content[0].text.value)
#                         break