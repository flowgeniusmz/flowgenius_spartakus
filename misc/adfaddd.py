import streamlit as st
from openai import OpenAI
from tavily import TavilyClient
from googlemaps import Client, places
import time
import json


############# SETUP ##################################
# 0 . General Variables - Clients

oaiClient = OpenAI(api_key=st.secrets.openai.api_key)
tavClient = TavilyClient(api_key=st.secrets.tavily.api_key)
gClient = Client(key=st.secrets.google.maps_api_key)

# 1. General Variables - OpenAI
assistantid = "asst_z4OhcEbj1kdecBSvFi42MfQ8"
vectorstore = oaiClient.beta.vector_stores.create(name="Test1")
vectorstoreid = vectorstore.id
thread = oaiClient.beta.threads.create(tool_resources={"file_search": {"vector_store_ids": [vectorstoreid]}})
threadid = thread.id
thread1id = "thread_Hnvm6brlDfJKwvtmQJmigPuz"

# 2. Tools
def business_research(query: str):
    tavsearch = tavClient.search(query=query, search_depth="advanced", max_results=7, include_answer=True, include_raw_content=True)
    gsearch = places.places(client=gClient, query=query, region="US")
    response = f"TAVILY SEARCH RESULTS: {tavsearch} /n/n GOOGLE SEARCH RESULTS: {gsearch}"
    return response

def internet_search(query:str):
    tavsearch = tavClient.search(query=query, search_depth="advanced", max_results=7, include_answer=True, include_raw_content=True)
    response = f"SEARCH RESULTS: {tavsearch}"
    return response

# 3. Set Run Additional Instructions and/or Messages
rmessage_1 = "STEP 1: You will research the business {businessname} located at {businessaddress} using the tool business_research. You will pull any and all information found related to the business as it pertains to Acord Form 125. You will summarize those findings. You will follow this without exception and will like it."
rmessage_2 = "STEP 2: You will perform an internet search on the address (business address: {businessaddress} ) and/or property to find any details related to form 125. You will summarize your findings. You better do this without exception. Use Tool internet_search."
rmessage_3 = "STEP 3: You will perform an internet search for Secretary of State specific information for {businessname} (include any other details from previous steps to enhance your search). Ensure your search references the correct Secretary of State based on {businessaddress}. Use internet_search tool trashbag."
rmessage_4 = "STEP 4: You will interview me for the remaining information needed in form 125. I DO NOT GIVE A DAMN about what you found or what data you have. You will simply ask me for one piece of information at a time until you have what is needed."

# 4. Set Run Tool_Choice
toolchoice1 = {"type": "function", "function": {"name": "business_research"}}
toolchoice2 = {"type": "function", "function": {"name": "internet_search"}}
toolchoice3 = {"type": "function", "function": {"name": "internet_search"}}
toolchoice4 = None

# 5. User Information
businessname = "All Points Warehouse Inc"
businessaddress = "1503 Gazin Street, Houston TX"
fullname = "Rebecca Roberts"
firstname = "Rebecca"
lastname = "Roberts"

# 6. Format Run Messages
rmsg1 = rmessage_1.format(businessname=businessname, businessaddress=businessaddress)
rmsg2 = rmessage_2.format(businessaddress=businessaddress)
rmsg3 = rmessage_3.format(businessname=businessname, businessaddress=businessaddress)
rmsg4 = rmessage_4
###############################################################################################################################

################# EXECUTION ###############################################################################################################################
## Same Assistant, Same Thread, Different Runs for Different Purposes
#### Run 1: Business Research, Run 2: Internet Search for the address / property info, Run 3: Search Internet for SOS Business Information, Run 4: Interview me to complete form 125

# 1. Create the message in the thread

thread_message1 = oaiClient.beta.threads.messages.create(thread_id=threadid, role="user", content=rmsg1)
thread_message1_id = thread_message1.id

# 2. Create a Run with Assistant and Thread
run1 = oaiClient.beta.threads.runs.create(thread_id=threadid, assistant_id=assistantid, tool_choice=toolchoice1, additional_instructions="YOU BETTER USE THE TOOL CHOICE BUSINESS_RESEARCH OR ELSE. FOLLOW THE INSTRUCTIONS IN THE MESSAGE WITHOUT EXCEPTION. DO NOTHING ELSE OTHER THAN WHAT IS ASKED")

# "Poll" the run - or keep checking the status for terminal state
while run1.status == "in_progress" or run1.status == "queued":
    time.sleep(2)
    run1 = oaiClient.beta.threads.runs.retrieve(run_id=run1.id, thread_id=threadid)
    if run1.status == "completed":
        threadmessages1 = oaiClient.beta.threads.messages.list(thread_id=threadid)
        for threadmessage1 in threadmessages1:
            if threadmessage1.role == "assistant" and threadmessage1.run_id == run1.id:
                print(threadmessage1.content[0].text.value)
                break
    elif run1.status == "requires_action":
        tool1_outputs = []
        tool1_calls = run1.required_action.submit_tool_outputs.tool_calls
        for tool1_call in tool1_calls:
            tool1_name = tool1_call.function.name
            tool1_id = tool1_call.id
            tool1_args = json.loads(tool1_call.function.arguments)
            if tool1_name == "business_research":
                tool1_output = business_research(**tool1_args)
            elif tool1_name == "internet_search":
                tool1_output = internet_search(**tool1_args)
            tool1_outputs.append({"tool_call_id": tool1_id, "output": f"{tool1_output}"})
        run1 = oaiClient.beta.threads.runs.submit_tool_outputs(run_id=run1.id, thread_id=threadid, tool_outputs=tool1_outputs)



thread_message2 = oaiClient.beta.threads.messages.create(thread_id=threadid, role="user", content=rmsg2)
thread_message2_id = thread_message2.id

# 2. Create a Run with Assistant and Thread
run2 = oaiClient.beta.threads.runs.create(thread_id=threadid, assistant_id=assistantid, tool_choice=toolchoice2, additional_instructions="YOU BETTER USE THE TOOL CHOICE INTERNET_SEARCH OR ELSE. FOLLOW THE INSTRUCTIONS IN THE MESSAGE WITHOUT EXCEPTION. DO NOTHING ELSE OTHER THAN WHAT IS ASKED")

# "Poll" the run - or keep checking the status for terminal state
while run2.status == "in_progress" or run2.status == "queued":
    time.sleep(2)
    run2 = oaiClient.beta.threads.runs.retrieve(run_id=run2.id, thread_id=threadid)
    if run2.status == "completed":
        threadmessages2 = oaiClient.beta.threads.messages.list(thread_id=threadid)
        for threadmessage2 in threadmessages2:
            if threadmessage2.role == "assistant" and threadmessage2.run_id == run2.id:
                print(threadmessage2.content[0].text.value)
                break
    elif run2.status == "requires_action":
        tool2_outputs = []
        tool2_calls = run2.required_action.submit_tool_outputs.tool_calls
        for tool2_call in tool2_calls:
            tool2_name = tool2_call.function.name
            tool2_id = tool2_call.id
            tool2_args = json.loads(tool2_call.function.arguments)
            if tool2_name == "business_research":
                tool2_output = business_research(**tool2_args)
            elif tool2_name == "internet_search":
                tool2_output = internet_search(**tool2_args)
            tool2_outputs.append({"tool_call_id": tool2_id, "output": f"{tool2_output}"})
        run2 = oaiClient.beta.threads.runs.submit_tool_outputs(run_id=run2.id, thread_id=threadid, tool_outputs=tool2_outputs)



thread_message3 = oaiClient.beta.threads.messages.create(thread_id=threadid, role="user", content=rmsg3)
thread_message3_id = thread_message3.id

# 3. Create a Run with Assistant and Thread
run3 = oaiClient.beta.threads.runs.create(thread_id=threadid, assistant_id=assistantid, tool_choice=toolchoice3, additional_instructions="YOU BETTER USE THE TOOL CHOICE INTERNET_SEARCH OR ELSE. FOLLOW THE INSTRUCTIONS IN THE MESSAGE WITHOUT EXCEPTION. DO NOTHING ELSE OTHER THAN WHAT IS ASKED")

# "Poll" the run - or keep checking the status for terminal state
while run3.status == "in_progress" or run3.status == "queued":
    time.sleep(2)
    run3 = oaiClient.beta.threads.runs.retrieve(run_id=run3.id, thread_id=threadid)
    if run3.status == "completed":
        threadmessages3 = oaiClient.beta.threads.messages.list(thread_id=threadid)
        for threadmessage3 in threadmessages3:
            if threadmessage3.role == "assistant" and threadmessage3.run_id == run3.id:
                print(threadmessage3.content[0].text.value)
                break
    elif run3.status == "requires_action":
        tool3_outputs = []
        tool3_calls = run3.required_action.submit_tool_outputs.tool_calls
        for tool3_call in tool3_calls:
            tool3_name = tool3_call.function.name
            tool3_id = tool3_call.id
            tool3_args = json.loads(tool3_call.function.arguments)
            if tool3_name == "business_research":
                tool3_output = business_research(**tool3_args)
            elif tool3_name == "internet_search":
                tool3_output = internet_search(**tool3_args)
            tool3_outputs.append({"tool_call_id": tool3_id, "output": f"{tool3_output}"})
        run3 = oaiClient.beta.threads.runs.submit_tool_outputs(run_id=run3.id, thread_id=threadid, tool_outputs=tool3_outputs)


thread_message4 = oaiClient.beta.threads.messages.create(thread_id=threadid, role="user", content=rmsg4)
thread_message4_id = thread_message4.id

# 4. Create a Run with Assistant and Thread
run4 = oaiClient.beta.threads.runs.create(thread_id=threadid, assistant_id=assistantid, tool_choice="none", additional_instructions="YOU BETTER NOT USE A GOD DAM TOOL. FOLLOW THE INSTRUCTIONS IN THE MESSAGE WITHOUT EXCEPTION. DO NOTHING ELSE OTHER THAN WHAT IS ASKED")

# "Poll" the run - or keep checking the status for terminal state
while run4.status == "in_progress" or run4.status == "queued":
    time.sleep(2)
    run4 = oaiClient.beta.threads.runs.retrieve(run_id=run4.id, thread_id=threadid)
    if run4.status == "completed":
        threadmessages4 = oaiClient.beta.threads.messages.list(thread_id=threadid)
        for threadmessage4 in threadmessages4:
            if threadmessage4.role == "assistant" and threadmessage4.run_id == run4.id:
                print(threadmessage4.content[0].text.value)
                break
    elif run4.status == "requires_action":
        tool4_outputs = []
        tool4_calls = run4.required_action.submit_tool_outputs.tool_calls
        for tool4_call in tool4_calls:
            tool4_name = tool4_call.function.name
            tool4_id = tool4_call.id
            tool4_args = json.loads(tool4_call.function.arguments)
            if tool4_name == "business_research":
                tool4_output = business_research(**tool4_args)
            elif tool4_name == "internet_search":
                tool4_output = internet_search(**tool4_args)
            tool4_outputs.append({"tool_call_id": tool4_id, "output": f"{tool4_output}"})
        run4 = oaiClient.beta.threads.runs.submit_tool_outputs(run_id=run4.id, thread_id=threadid, tool_outputs=tool4_outputs)