import streamlit as st
from config import pagesetup as ps
from chathistory import ChatHistory





page_number = 2
ps.master_page_display_styled_popmenu_pop(varPageNumber=page_number)
ChatHistory()

# def get_dataframe(threadmessages):
#     messages = []
#     for threadmessage in threadmessages:
#         new_row = {
#             "messageid": threadmessage.id,
#             "runid": threadmessage.run_id,
#             "role": threadmessage.role,
#             "content": threadmessage.content[0].text.value
#         }
#         messages.append(new_row)
#     df = pd.DataFrame(messages)
#     df_grouped = df.groupby('runid')
#     return df


# assistantid = st.secrets.openai.assistant_id
# threadid = st.session_state.threadid
# vectorid = st.session_state.vectorstoreid
# client = OpenAI(api_key=st.secrets.openai.api_key)
# threadmessages = client.beta.threads.messages.list(thread_id=threadid)
# df_messages = get_dataframe(threadmessages=threadmessages)
# user_messages = df_messages[df_messages['role'] == 'user']['content'].tolist()
# assistant_messages = df_messages[df_messages['role'] == 'assistant']['content'].tolist()
# print(df_messages)
# historycontainer = st.container(border=False) #ps.userflow_styled_container2()
# with historycontainer:
#     for user_msg, asst_msg in zip(user_messages, assistant_messages):
#         runcontainer = ps.userflow_styled_container2()
#         with runcontainer:
#             historycols = st.columns([10,1,10])
#             with historycols[0]:
#                 umessage = st.popover(label="User Messages", use_container_width=True, disabled=False)
#                 with umessage:
#                     st.markdown(user_msg)

#             with historycols[2]:
#                 amessage = st.popover(label="Assistant Messages", use_container_width=True, disabled=False)
#                 with amessage:
#                     st.markdown(asst_msg)


# # chatcontainer = ps.userflow_styled_container2(height=400)
# # with chatcontainer:
# #     for message in st.session_state.messages:
# #         with st.chat_message(message['role']):
# #             st.markdown(message['content'])

# # if prompt := st.chat_input(placeholder="Enter your question or request here..."):
# #     st.session_state.messages.append({"role": "user", "content": prompt})
# #     promptmessage = client.beta.threads.messages.create(thread_id=threadid, role="user", content=prompt)
# #     with chatcontainer:
# #         with st.chat_message("user"):
# #             st.markdown(prompt)
# #         status = st.status(label="Running assistant...please wait.", expanded=False, state="running")
# #         with status:
# #             st.markdown(f"Initializing....messageid: {promptmessage.id}")
    
# #     run = client.beta.threads.runs.create(thread_id=threadid, assistant_id=assistantid)
# #     while run.status == "queued" or run.status == "in_progress":
# #         time.sleep(2)
# #         st.toast("processing")
# #         run = client.beta.threads.runs.retrieve(run_id=run.id, thread_id=threadid)
# #         if run.status == "completed":
# #             st.toast("Completed")
# #             status.update(label="Completed", state="complete", expanded=False)
# #             threadmessages = client.beta.threads.messages.list(thread_id=threadid)
# #             for threadmessage in threadmessages:
# #                 if threadmessage.role == "assistant" and threadmessage.run_id == run.id:
# #                     st.session_state.messages.append({"role": "assistant", "content": threadmessage.content[0].text.value})
# #                     with chatcontainer:
# #                         with st.chat_message("assistant"):
# #                             st.markdown(threadmessage.content[0].text.value)
# #             break
# #         elif run.status == "requires_action":
# #             tool_outputs = []
# #             tool_calls = run.required_action.submit_tool_outputs.tool_calls
# #             with status:
# #                 st.markdown(tool_calls)
# #                 print(tool_calls)
# #             for tool_call in tool_calls:
# #                 tool_call_id = tool_call.id
# #                 tool_call_name = tool_call.function.name
# #                 tool_call_args = json.loads(tool_call.function.arguments)
# #                 tool_call_output = getattr(Tools, tool_call_name)(**tool_call_args)
# #                 tool_outputs.append({"tool_call_id": tool_call_id, "output": f"{tool_call_output}"})
# #             run = client.beta.threads.runs.submit_tool_outputs(run_id=run.id, thread_id=threadid, tool_outputs=tool_outputs)


        
           
# # class Run:
# #     def __init__(self, prompt):
# #         self.prompt = prompt    
# #         self.role = "user"
# #         self.initialize_attributes()
# #         self.create_message()
# #         self.create_run()

# #     def initialize_attributes(self):    
# #         self.assistantid = st.secrets.openai.assistant_id
# #         self.client = OpenAI(api_key=st.secrets.openai.api_key)
# #         self.threadid = st.session_state.threadid
# #         self.vectorstoreid = st.session_state.vectorstoreid

# #     def create_message(self):
# #         self.message = self.client.beta.threads.messages.create(thread_id=self.threadid, content=self.prompt, role=self.role)

# #     def create_run(self):
# #         self.run = self.client.beta.threads.runs.create(thread_id=self.threadid, assistant_id=self.assistantid)
# #         self.wait_on_run()
    
# #     def retrieve_run(self):
# #         self.run = self.client.beta.threads.runs.retrieve(thread_id=self.threadid, run_id=self.run.id)
    
# #     def append_message(self, role, content):
# #         st.session_state.messages.append({"role": role, "content": content})

# #     def wait_on_run(self):
# #         while self.run.status == "queued" or self.run.status == "in_progress":
# #             time.sleep(2)
# #             self.retrieve_run()
# #         if self.run.status == "completed":
# #             self.handle_run_completed()
# #         elif self.run.status == "requires_action":
# #             self.handle_run_requiresaction()
            
# #     def handle_run_completed(self):        
# #         self.response_messages = self.client.beta.threads.messages.list(thread_id=self.threadid)
# #         for response_message in self.response_messages:
# #             if response_message.role == "assistant" and response_message.run_id == self.run.id:
# #                 self.append_message(role="assistant", content=response_message.content[0].text.value)

# #     def handle_run_requiresaction(self):
# #         self.tool_outputs = []
# #         self.tool_calls = self.run.required_action.submit_tool_outputs.tool_calls
# #         for tool_call in self.tool_calls:
# #             tool_call_id = tool_call.id
# #             tool_call_name = tool_call.function.name
# #             tool_call_args = json.loads(tool_call.function.arguments)
# #             tool_call_output = getattr(Tools, tool_call_name)(**tool_call_args)
# #             self.tool_outputs.append({"tool_call_id": tool_call_id, "output": f"{tool_call_output}"})
# #         self.run = self.client.beta.threads.runs.submit_tool_outputs(thread_id=self.threadid, run_id=self.run.id, tool_outputs=self.tool_outputs)
# #         self.wait_on_run()




    