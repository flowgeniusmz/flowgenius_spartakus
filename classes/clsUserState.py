import streamlit as st
from streamlit.components.v1 import html
from classes import clsPageSetup as ps, clsUtilities as ut
import base64
from openai import OpenAI
from supabase import create_client

supa = create_client(supabase_key=st.secrets.supabase.api_key_admin, supabase_url=st.secrets.supabase.url)
client = OpenAI(api_key=st.secrets.openai.api_key)

class UserState:
    def __init__(self):
        self._initialize_attributes()
        self._initialize_background()
        self._initialize_userstate()

    def _initialize_attributes(self):
        self.userstate = st.session_state.userstate
        self.userstatecomplete = st.session_state.userstatecomplete

    def _initialize_background(self):
        self.background = ps.PageUtilities.display_background_page(type="main", style="background_page")
        self.header = ps.PageUtilities.get_title_app(div=True)

    def _initialize_userstate(self):
        if self.userstatecomplete:
            self.bypass()
        else:
            self.get()

    def get(self):
        if self.userstate == 1:
            self._userstate1()
        elif self.userstate == 2:
            self._userstate2()
        elif self.userstate == 3:
            self._userstate3()
        elif self.userstate == 4:
            self._userstate4()
        elif self.userstate == 5:
            self._userstate5()
        else:
            self._userstate1()
    
    def bypass(self):
        self._userstate5()

    
    def _userstate1(self):
        main_container = st.container(border=False)
        with main_container:
            buttoncontainer = ps.PageUtilities.get_styled_container1()
            with buttoncontainer:
                cols = st.columns(2)
                with cols[0]:
                    newbtn = st.button("Create New Account", use_container_width=True, type="primary")
                with cols[1]:
                    existbtn = st.button("Sign In to Existing Account", use_container_width=True,  type="primary")
            # st.divider()
            # chatcontainer = ps.PageUtilities.get_styled_container1()
            # with chatcontainer:
            #     dispcont = st.container(border=False, height=300)
            #     with dispcont:
            #         with st.chat_message("assistant"):
            #             st.markdown("Welcome to WrestleAI. Type below to try it out!")
            # pcont = st.container(border=False, height=100)
            # with pcont:
            #     guestprompt = st.chat_input(placeholder="Type here to try the assistant!")
            # st.divider()
                
        if newbtn:
            st.session_state.usertype = "new"
            self._userstate_callback(next_userstate=2)
        if existbtn:
            st.session_state.usertype = "existing"
            self._userstate_callback(next_userstate=4)

    @st.experimental_dialog(title="New Account Information", width="large")
    def _userstate2(self):
        ps.PageUtilities.display_background_dialog(type="dialog1", style="background_dialog")
        infoheader = ps.PageUtilities.get_header(type="blue", text="Please Complete Account Information Below")
        st.session_state.firstname = st.text_input(label="First Name", key="_firstname", type="default")
        st.session_state.lastname = st.text_input(label="Last Name", key="_lastname", type="default")
        st.session_state.email = st.text_input(label="Email Address", key="_email", type="default")
        st.session_state.userrole = st.radio(label="User Role", key="_userrole", options=st.secrets.lists.userroles, index=None, horizontal=True)
        create_button = st.button(label="Create Account", key="createbutton", type="primary")
        if create_button:
            st.session_state.fullname = f"{st.session_state.firstname} {st.session_state.lastname}"
            st.session_state.createddate = ut.Utilities.get_datetime()
            self._userstate_callback(next_userstate=3)
    
    @st.experimental_dialog(title="Terms, Conditions, and Payment", width="large")
    def _userstate3(self):
        ps.PageUtilities.display_background_dialog(type="dialog2", style="background_dialog")
        terms_container = st.container(border=False)
        payment_placeholder = st.empty()
        with terms_container:
            termsheader = ps.PageUtilities.get_header(type="blue", text="Terms and Conditions")
            terms_agree = st.checkbox(label="Please check this box to acknowledge and accept the WrestleAI terms and conditions before proceeding to payment.", value=False, key="_termstype")
            terms_pop = st.popover(label="View Terms and Conditions")
            with terms_pop:
                st.markdown(st.session_state.termscontent)
            if terms_agree:
                st.session_state.termstype = "acknowledged"
                with payment_placeholder.container(border=False):
                    payheader = ps.PageUtilities.get_header(type="blue", text="Proceed to Payment")
                    payproceed = html(st.secrets.stripe.stripejs.format(buy_button_id=st.secrets.stripe.buy_btn_dev, publisher_key=st.secrets.stripe.pub_key_dev, client_reference_id="testtest", customer_email="test@test.com"))

    @st.experimental_dialog(title="User Login", width="large")
    def _userstate4(self):
        ps.PageUtilities.display_background_dialog(type="dialog3", style="background_dialog")
        ps.PageUtilities.get_header(type="blue", text="Sign In to Your Account")
        st.session_state.username = st.text_input(label="Username", key="_username", type="default")
        st.session_state.password = st.text_input(label="Password", key="_password", type="password" )
        loginbutton = st.button(label="Login", key="loginbutton", type="primary")
        if loginbutton:
            st.session_state.logintype = "authenticated"
            self._userstate_callback(next_userstate=5)

    def _userstate5(self):
        st.session_state.userstatecomplete = True
        st.switch_page(page=st.secrets.pages.paths[0])

    def _userstate_callback(self, next_userstate):
        st.session_state.userstate = next_userstate
        st.rerun()



class UserStateUtilities:
    @staticmethod
    def create_user():
        UserStateUtilities.user_thread_vector_ids()
        payload = {"username": st.session_state.username, "password": st.session_state.password, "email": st.session_state.email, "businessname": st.session_state.businessname, "businessaddress": st.session_state.businessaddress, "createddate": st.session_state.createddate, "userrole": st.session_state.userrole, "firstname": st.session_state.firstname, "lastname": st.session_state.lastname, "fullname": st.session_state.fullname, "threadid": st.session_state.threadid, "vectorid": st.session_state.vectorid}
        response = supa.table("users").insert(payload).execute()
        responsedata = response.data
        if responsedata:
            userdata = responsedata[0]
            st.session_state.userdata = userdata
            st.session_state.email = userdata.get("email")
            st.session_state.businessname = userdata.get("businessname")
            st.session_state.businessaddress = userdata.get("businessaddress")
            st.session_state.firstname = userdata.get("firstname")
            st.session_state.lastname = userdata.get("lastname")
            st.session_state.fullname = userdata.get("fullname")
            st.session_state.threadid = userdata.get("threadid")
            st.session_state.vectorid = userdata.get("vectorid")
            st.session_state.userrole = userdata.get("userrole")
            st.session_state.createddate = userdata.get("createddate")
            return True
        else:
            return False
        
    @staticmethod
    def authenticate_user():
        response = client.table(table_name="users").select("*").eq(column="username", value=st.session_state.username).eq(column="password", value=st.session_state.password).execute()
        responsedata = response.data
        if response.data:
            userdata = responsedata[0]
            st.session_state.authenticated = True
            st.session_state.userdata = userdata
            return True
        else:
            st.session_state.authenticated = False
            return False
    
    @staticmethod
    def create_user_thread():
        if st.session_state.threadid is None:
            st.session_state.threadid = client.beta.threads.create().id
        
        
    @staticmethod
    def create_user_vector():
        if st.session_state.vectorid is None:
            st.session_state.vectorid = client.beta.vector_stores.create(name=f"SpartakusAI - {st.session_state.fullname}").id
    
    @staticmethod
    def user_thread_vector_ids():
        UserStateUtilities.create_user_thread()
        UserStateUtilities.create_user_vector()