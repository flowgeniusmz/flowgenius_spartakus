import streamlit as st
from config import pagesetup as ps

page_number = 3
ps.master_page_display_styled_popmenu_pop(varPageNumber=page_number)

maincontainer = ps.userflow_styled_container2()
with maincontainer:
    userinfocontainer = st.container(height=300, border=False)
    with userinfocontainer:
        cols = st.columns([1, 20, 1, 20, 1])
        with cols[1]:
            st.text_input(label="First Name", value=st.session_state.firstname, disabled=True)
        with cols[3]:
            st.text_input(label="Last Name", value=st.session_state.lastname, disabled=True)
    detailscontainer = st.container(height=400)
    with detailscontainer:
        tabnames = ["Chat History", "Forms", "Other"]
        tab1, tab2, tab3 = st.tabs(tabs=tabnames)
