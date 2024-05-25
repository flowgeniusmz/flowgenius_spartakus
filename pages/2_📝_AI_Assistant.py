import streamlit as st
from config import pagesetup as ps
from openai import OpenAI
from classes import class_assistant

page_number = 1
ps.master_page_display_styled_popmenu_pop(varPageNumber=page_number)
st.write(st.session_state.threadid)

assistant = class_assistant.Assistant() 

    