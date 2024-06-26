import streamlit as st
from streamlit.components.v1 import html
from classes import clsPageSetup as ps, clsSessionState as ss, clsUtilities as ut
from datetime import datetime
from supabase import create_client
from openai import OpenAI

client = OpenAI(api_key=st.secrets.openai.api_key)
supa = create_client(supabase_key=st.secrets.supabase.api_key_admin, supabase_url=st.secrets.supabase.url)

# 1 = Select user type 2 = New User Info 3 = Payment 4 = Authentication
class UserState:
    def __init__(self):
        self.userstate = st.session_state.userstate
        self.userstatecomplete = st.session_state.userstatecomplete
        self.authenticated = st.session_state.authenticated
        self.acknowledged = st.session_state.acknowledged
        self.background = ps.PageUtilities.display_background_page(type="main", style="background_page")
        self.header = ps.PageUtilities.get_title_app(div=True)
        self.userstate_window = ps.PageUtilities.get_styled_container()
        with self.userstate_window:
            self.userstate_container = st.container(border=False)
            with self.userstate_container:
                self.content_placeholder = st.empty()
        if self.userstatecomplete:
            self.bypass()
        else:
            self.get()
    
    def get(self):
        if self.userstate==1: #landing
            self.userstate1()
        elif self.userstate ==2: #userinfo
            self.userstate2()
        elif self.userstate == 3: #payment
            self.userstate3()
        elif self.userstate == 4: #authentication
            self.userstate4()
        elif self.userstate == 5: #welcome
            self.userstate5()
        else:
            self.userstate1()
    
    def bypass(self):
        self.userstate5()

    def callback(self, next_userstate):
        st.session_state.userstate = next_userstate
        st.rerun()

    def userstate1(self):
        with self.content_placeholder.container(border=False):
            cols = st.columns([1,20,1,20,1])
            with cols[1]:
                newuserbutton = st.button(label="Create New Account", use_container_width=True, type="primary")
                if newuserbutton:
                    st.session_state.usertype = "new"
                    self.callback(next_userstate=2)

            with cols[3]:
                existuserbutton = st.button(label="Sign In", type="primary", use_container_width=True)
                if existuserbutton:
                    st.session_state.usertype = "existing"
                    self.callback(next_userstate=4)
    
    def userstate2(self):
        with self.content_placeholder.container(border=False):
            ps.PageUtilities.get_header(type="blue", text="New Account Information")
            st.session_state.firstname = st.text_input(label="First Name", key="_firstname", type="default")
            st.session_state.lastname = st.text_input(label="Last Name", key="_lastname", type="default")
            st.session_state.email = st.text_input(label="Email Address", key="_email", type="default")
            st.session_state.businessname = st.text_input(label="Business Name", key="_businsesname", type="default")
            st.session_state.businessaddress = st.text_input(label="Business Address / Location", key="_businessaddress", type="default", help="Please provide city, state, and zip code at a minimum.")
            st.session_state.userrole = st.radio(label="User Role", key="_userrole", options=st.secrets.lists.userroles, index=None, horizontal=True)
            submitbutton = st.button(label="Submit", key="_newusersubmit", type="secondary")
            if submitbutton:
                if st.session_state.firstname is not None and st.session_state.lastname is not None and st.session_state.email is not None and st.session_state.businessname is not None and st.session_state.businessaddress is not None and st.session_state.userrole is not None:
                    st.session_state.fullname = f"{st.session_state.firstname} {st.session_state.lastname}"
                    st.session_state.createddate = datetime.now().isoformat()
                    self.callback(next_userstate=3)
                else:
                    errormessage = st.error("Please complete all fields and try again.")
    
    def userstate3(self):
        with self.content_placeholder.container(border=False):
            #ps.PageUtilities.get_header(type="blue", text="Terms and Payment")
            terms_container = st.container(border=False)
            payment_placeholder = st.empty()
            with terms_container:
                termsheader = ps.PageUtilities.get_header(type="blue", text="Terms and Conditions")
                acknowledged = st.checkbox(label="Please check this box to acknowledge and accept the SpartakusAI terms and conditions before proceeding to payment.", value=False, key="_termstype")
                terms_popover = st.popover(label="View Terms and Conditions")
                with terms_popover:
                    st.markdown(st.session_state.termscontent)
                if acknowledged:
                    st.session_state.acknowledged = True
                    st.session_state.termstype = "acknowledged"
                    with payment_placeholder.container(border=False):
                        payheader = ps.PageUtilities.get_header(type="blue", text="Proceed to Payment")
                        payproceed = html(st.secrets.stripe.stripejs.format(st.secrets.stripe.stripejs.format(buy_button_id=st.secrets.stripe.buy_btn_dev, publisher_key=st.secrets.stripe.pub_key_dev, client_reference_id=st.session_state.fullname, customer_email=st.session_state.email)))
    
    def userstate4(self):
        with self.content_placeholder.container(border=False):
            ps.PageUtilities.get_header(type="blue", text="Account Login")
            st.session_state.username = st.text_input(label="Username", key="_username", type="default")
            st.session_state.password = st.text_input(label="Password", key="_password", type="password" )
            loginbutton = st.button(label="Login", key="loginbutton", type="secondary")
            if loginbutton:
                if st.session_state.username is not None and st.session_state.password is not None:
                    auth = UserStateUtilities.authenticate_user()
                    if auth:
                        self.callback(next_userstate=5)
                    else:
                        st.error("Invalid login. Please try again")
    
    def userstate5(self):
        st.session_state.userstatecomplete = True
        st.switch_page(page=st.secrets.pages.paths[0])

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