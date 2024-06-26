import streamlit as st
from openai import OpenAI
from classes import clsPageSetup as ps, clsSessionState as ss, clsTools as t, clsUtilities as u, clsAssistant as asst

# Set session state
sessionstate = ss.SessionState.get()

# Set Main Containers
chat_container = ps.PageUtilities.get_styled_container()
suggestion_container = st.popover(label="Suggested Prompts", use_container_width=True, disabled=False)
prompt_container = st.container(border=False, height=100)

def get_buttons():
    suggestions = st.session_state.suggestions
    # Create a 2-column layout
    col1, col2 = st.columns(2)

    # Iterate over items and assign them to columns based on even or odd index
    for index, (key, value) in enumerate(suggestions.items()):
        # Select the column based on even or odd index
        col = col1 if index % 2 == 0 else col2
        # Place a button in the selected column
        col.button(label=value, use_container_width=True, key=f"_{key}")
 
# Add to main containers
with chat_container:
    message_container = st.container(border=False, height=400)
    with message_container:
        for message in st.session_state.messages:
            with st.chat_message(name=message['role']):
                st.markdown(body=message['content'])
    
with suggestion_container:
    # suggestionpop = st.popover(label="Suggested Prompts", use_container_width=True)
    # with suggestionpop:
    suggestion_cols = st.columns(2)
    with suggestion_cols[0]:
        suggested_prompt_1 = st.button(label=st.session_state.suggestion1, use_container_width=True, type="primary")
        suggested_prompt_3 = st.button(label=st.session_state.suggestion3, use_container_width=True, type="primary")
    with suggestion_cols[1]:
        suggested_prompt_2 = st.button(label=st.session_state.suggestion2, use_container_width=True, type="primary")
        suggested_prompt_4 = st.button(label=st.session_state.suggestion4, use_container_width=True, type="primary")




with prompt_container:
    user_prompt = st.chat_input(placeholder=sessionstate.get_value(key="placeholder1"))

if user_prompt or suggested_prompt_1 or suggested_prompt_2 or suggested_prompt_3 or suggested_prompt_4:
    suggestion_container.empty()
    if user_prompt:
        prompt = user_prompt
    elif suggested_prompt_1:
        prompt=sessionstate.get_value(key="suggestion1")
    elif suggested_prompt_2:
        prompt=sessionstate.get_value(key="suggestion2")
    elif suggested_prompt_3:
        prompt=sessionstate.get_value(key="suggestion3")
    elif suggested_prompt_4:
        prompt=sessionstate.get_value(key="suggestion4")
    
    sessionstate.update(prompt=prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    

    with message_container:
        with st.chat_message("user"):
            st.markdown(prompt)
        asst.Assistant(type="guest").run_assistant()
        with st.chat_message("assistant"):
            st.markdown(st.session_state.response)
    

