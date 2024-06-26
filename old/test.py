import streamlit as st
from tavily import TavilyClient

tavclient = TavilyClient(api_key=st.secrets.tavily.api_key)

querytemplate = "All information from Secratary of State for {businessname} located {businsesaddress}"

businessname = "All Points Warehouse"
businsesaddress = ""

