import streamlit as st


class SessionState:
    def __init__(self):
        self.set()
        self.initialize()

    def set(self):
        # Master call for all the _set methods
        self._set_initialstate()
        self._set_queryparams()
        self._set_userstate()
        self._set_termscontent()
        self._set_messages()

    def initialize(self):
        # Once initial state is set - this initializes each key/value pair to the session state
        for key, value in self.initial_state.items():
            if key not in st.session_state:
                st.session_state[key] = value

    @classmethod
    def get(cls):
        # Class method applies to the class as a whole every time it is called. It prevents a new instance of the class being created each time and instead returns the existing
        if 'session_state_instance' not in st.session_state:
            st.session_state.session_state_instance = cls()
        return st.session_state.session_state_instance
    
    def update(self, **kwargs):
        # Allows to update session state values using keyword arguemnts or KWARGS. Dynamic so that you can literally say update(username= value, ...)
        for key, value in kwargs.items():
            st.session_state[key] = value
    
    def get_value(self, key):
        # Retuns a single key value
        return st.session_state.get(key, None)

    def set_file_content(self, key, filepath):
        # Method that lets a file content be set to a variable
        try:
            with open(file=filepath, mode="r") as file:
                content = file.read()
            st.session_state[key] = content
        except FileNotFoundError:
            st.session_state[key] = "File Not Found"


    def _set_initialstate(self):
        # Sets the initial session state equal to the key/values listed in st.secrets
        self.initial_state = dict(st.secrets.sessionstate)

    def _set_queryparams(self):
        # Checks to see if there are query params in the URL and returns True/False using bool
        self.query_params = bool(st.query_params)
    
    def _set_userstate(self):
        # Sets initial userstate and usertype values based on if query parameters are present
        if not self.query_params:
            self.initial_state['userstate'] = 0
            self.initial_state['usertype'] = 'guest'
        else:
            if st.query_params.usertype == "new":
                self.initial_state['userstate'] = 2
                self.initial_state['usertype'] = "new"
            else:
                self.initial_state['userstate'] = 4
                self.initial_state['usertype'] = "existing"
        self.initial_state['userstatecomplete'] = False
    
    def _set_termscontent(self):
        # Sets terms content
        self.initial_state['termscontent'] = self.set_file_content(key="termscontent", filepath=st.secrets.paths.terms)

    def _set_messages(self):
        self.initial_state['messages'] = [{"role": "assistant", "content": "Welcome to SpartakusAI - Are you here to buy insurance?"}]




### EXAMPLE USAGE
# import streamlit as st
# from classes.class0_pagesetup import PageSetup
# from classes.class1_payment import Payment
# from session_state import SessionState  # Adjust the import path as needed

# 1. Set ST PAGE CONFIG
# st.set_page_config(
#     page_icon=st.secrets.app.icon,
#     page_title=st.secrets.app.title,
#     layout=st.secrets.app.layout,
#     initial_sidebar_state=st.secrets.app.sidebar
# )

# # 2. Initialize Session State with values from st.secrets.sessionstate
# initial_state = dict(st.secrets.sessionstate)
# query_params = st.experimental_get_query_params()
# initial_state['userstate'] = 0 if not query_params else 4

# session_state = SessionState.get(**initial_state)

# # 3. Set Page Setup
# PageSetup(pagenumber=session_state.get_value('userstate')).display_manual()

# c = st.checkbox("proceed")
# if c:
#     Payment().display_payment()
#     # Update session state if needed
#     session_state.update(userstate=1)  # Example update

    