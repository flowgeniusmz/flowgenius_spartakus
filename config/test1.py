import streamlit as st
from tavily import TavilyClient

client = TavilyClient(api_key=st.secrets.tavily.api_key)
search = client.search(query="Nolasko Insurance Advisors PLLC", max_results=10, search_depth="advanced", include_raw_content=True, include_answer=True)
print(search)