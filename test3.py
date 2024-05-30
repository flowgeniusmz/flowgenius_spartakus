import streamlit as st
import stripe
import urllib.parse

def callbackpayinfo():
    st.session_state.payinfo=True

def stripetest():
    username = "mzozulia@flowgenius.com"
    password = "EverlyQuinn#7665"
    email = "mzozulia@flowgenius.com"
    businessname = "Alma Lasers Inc"
    businessaddress="485 Half Day Road"
    fullname = "Michael Zozulia"
    firstname = "Michael"
    lastname = "Zozulia"
    encoded_username = urllib.parse.quote(username)
    encoded_businessname = urllib.parse.quote(businessname)
    encoded_fullname = urllib.parse.quote(fullname)
    encoded_firstname = urllib.parse.quote(firstname)
    encoded_lastname = urllib.parse.quote(lastname)
    encoded_email = urllib.parse.quote(email)
    encoded_businessaddress = urllib.parse.quote(businessaddress)
    api_key_dev = "sk_test_51OEP9VDvYq7iSz1po6HfNfJHsmXKurfUKCfaOkqEEYWS8IXwPTWhNHGKDqQsKSCDxa3VGVBbmwEZozuwKdM5Zf8X00tBJw9cG0"
    api_key_prod = "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"
    price = "price_1PM0roDvYq7iSz1pUgrukCp5"
    price_dev = "price_1PM12oDvYq7iSz1pBSlPEh8L"
    prod = "prod_QCPhpDPt1qqxd8"
    prod_dev = "prod_QCPsE0piVOxc3H"
    #successurl = "http://chat.spartakusai.com/return.html?session_id={CHECKOUT_SESSION_ID}" + f"&username={username}&credential={password}"
    successurl = "http://chat.spartakusai.com/return.html?session_id={CHECKOUT_SESSION_ID}" + f"&username={encoded_username}&businessname={encoded_businessname}&fullname={encoded_fullname}&firstname={encoded_firstname}&lastname={encoded_lastname}&email={encoded_email}&businessaddress={encoded_businessaddress}"
    print(successurl)

    

    cancelurl = "http://chat.spartakusai.com"
    line_items=[{"price": price_dev, "quantity": 1}]
    ui_mode = "hosted"
    mode = "subscription" #"payment"


    if st.query_params:
        session = stripe.checkout.Session.retrieve(id=st.query_params.session_id)
        print(st.query_params)
        st.markdown(st.query_params)

    else:
        email1 = st.text_input("Email")
        payinfo = st.checkbox(label="You will be redirected to Stripe to process your payment. Once completed you will return to SpartakusAI. Click here to acknowledge.", key="_payinfo", on_change=callbackpayinfo, value=st.session_state.payinfo)
        if payinfo:
            session = stripe.checkout.Session.create(api_key=api_key_dev, ui_mode=ui_mode, mode=mode, line_items=line_items, customer_email=email, cancel_url=cancelurl, success_url=successurl)
            sessionurl = session.url
            btn = st.link_button(label="Payment", url=sessionurl)




class Payment:
    def __init__(self, dev_mode: bool=True):
        self.initialize_user_attributes()
        self.initialize_user_attributes_encoded()
        self.initialize_devmode_attributes()
        self.initialize_stripe_attributes()
        self.initialize_checkout_type()
        self.initialize_checkout_session()
        self.devmode = dev_mode

    def initialize_user_attributes(self):
        self.username = st.session_state.username
        self.password = st.session_state.password
        self.email = st.session_state.email
        self.businessaddress = st.session_state.businessaddress
        self.businessname = st.session_state.businessname
        self.fullname = st.session_state.fullname
        self.firstname = st.session_state.firstname
        self.lastname = st.session_state.lastname

    def initialize_user_attributes_encoded(self):
        self.encoded_username = urllib.parse.quote(self.username)
        self.encoded_password = urllib.parse.quote(self.password)
        self.encoded_email = urllib.parse.quote(self.email)
        self.encoded_businessaddress = urllib.parse.quote(self.businessaddress)
        self.encoded_businessname = urllib.parse.quote(self.businessname)
        self.encoded_fullname = urllib.parse.quote(self.fullname)
        self.encoded_firstname = urllib.parse.quote(self.firstname)
        self.encoded_lastname = urllib.parse.quote(self.lastname)

    def initialize_stripe_attributes(self):
        self.lineitems = [{"price": self.priceid, "quantity": self.quantity}]
        self.successurl = "http://chat.spartakusai.com/return.html?session_id={CHECKOUT_SESSION_ID}" + f"&username={self.encoded_username}&businessname={self.encoded_businessname}&fullname={self.encoded_fullname}&firstname={self.encoded_firstname}&lastname={self.encoded_lastname}&email={self.encoded_email}&businessaddress={self.encoded_businessaddress}"
        self.cancelurl = "http://chat.spartakusai.com/"
        self.mode = "subscription" #"payment"
        self.uimode = "hosted"
        self.quantity = 1
    
    def initialize_checkout_type(self):
        if st.query_params:
            self.checkouttype = "retrieve"
        else:
            self.checkouttype = "create"

    
    def initialize_devmode_attributes(self):
        if self.devmode:
            self.priceid = st.secrets.stripe.price_dev
            self.prodid = st.secrets.stripe.prod_dev
            self.key = st.secrets.stripe.api_key_dev
        else:
            self.priceid = st.secrets.stripe.price
            self.prodid = st.secrets.stripe.prod
            self.key = st.secrets.stripe.api_key_prod

    def initialize_checkout_session(self):
        if st.query_params:
            self.checkout_session_id = st.query_params.session_id
            self.checkout_session = stripe.checkout.Session.retrieve(api_key=self.key, id=st.query_params.session_id)
            self.checkout_session_url = None
        else:
            self.checkout_session = stripe.checkout.Session.create(api_key=self.key, ui_mode=self.uimode, mode=self.mode, line_items=self.lineitems, cancel_url=self.cancelurl, success_url=self.successurl, customer_email=self.email)
            self.checkout_session_id = self.checkout_session.id
            self.checkout_session_url = self.checkout_session.url
        self.update_session_state()

    def update_session_state(self):
        st.session_state.stripe_session = self.checkout_session
        st.session_state.stripe_session_id = self.checkout_session.id
        st.session_state.stripe_customer_email = self.checkout_session.customer_email
        st.session_state.customer_address_state = self.checkout_session.customer_details.address.state
        st.session_state.customer_address_zip = self.checkout_session.customer_details.address.postal_code
        st.session_state.stripe_customer_name = self.checkout_session.customer_details.name
        st.session_state.stripe_payment_status = self.checkout_session.payment_status
        st.session_state.stripe_payment_intent = self.checkout_session.payment_intent

    def display_button(self):
        if self.checkouttype == "create":
            button = st.link_button(label="Payment", url=self.checkout_session_url)
        elif self.checkouttype == "retrieve":
            button = st.button(label="Create User", type="primary")
        return button