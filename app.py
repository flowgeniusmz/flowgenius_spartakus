import streamlit as st
from config import pagesetup as ps, sessionstates as ss
from classes_config import class_pagesetup

st.set_page_config(page_title=st.secrets.appconfig.app_name, page_icon=st.secrets.appconfig.app_icon, layout=st.secrets.appconfig.app_layout, initial_sidebar_state=st.secrets.appconfig.app_initial_sidebar)

ps.get_page_styling()
ps.display_background_image()

ss.initialize_session_states()

ps.set_title_manual(varTitle="SpartakusAI", varSubtitle="Login / Registration", varDiv=True)
