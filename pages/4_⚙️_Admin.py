import streamlit as st
from config import pagesetup as ps
from chathistory import ChatHistory
from account import BasicUserInformation

page_number = 3
ps.master_page_display_styled_popmenu_pop(varPageNumber=page_number)

maincontainer = ps.userflow_styled_container2()
with maincontainer:
    BasicUserInformation()
    detailscontainer = st.container(height=400)
    with detailscontainer:
        ps.get_gray_header(varText="User Detailed Information")
        tabnames = ["Chat History", "Forms", "Other"]
        tab1, tab2, tab3 = st.tabs(tabs=tabnames)
        with tab1:
            chathist = ChatHistory()

