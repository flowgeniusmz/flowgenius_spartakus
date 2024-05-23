import streamlit as st
from streamlit_extras.stylable_container import stylable_container as sc

class Styles:
    def __init__(self):
        self.get_styles_html()
        self.get_styles_css()

    def get_styles_html(self):
        self.style_html_title_subtitle_1 = """<span style="font-weight: bold; font-size: 2em; color:#4A90E2;">{title} </span> <span style="font-weight: bold; color:#333333; font-size:1.3em;">{subtitle}</span>"""
        self.style_html_title_subtitle_2 = """<span style="font-weight: bold; font-size: 2em; color:#4A90E2;">{title} </span> <span style="font-weight: bold; color:#FFFFFF; font-size:1.3em;">{subtitle}</span>"""
        self.style_html_header = """<span style="font-weight: bold; color:#4A90E2; font-size:1.3em;">{header}</span>"""
        self.style_html_header_blue = """<span style="font-weight: bold; color:#4A90E2; font-size:1.3em;">{varText}</span>"""
        self.style_html_header_gray = """<span style="font-weight: bold; color:#333333; font-size:1.3em;">{varText}</span>"""
        self.style_html_header_green = """<span style="font-weight: bold; color:#00b084; font-size:1.3em;">{varText}</span>"""
        self.style_html_background_image_1 = "<style>.stApp {{ background-image: linear-gradient(rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.90)), url({background_image}); background-size: cover; }}</style>"
        self.style_html_background_image_2 = "<style>.stApp {{ background-image: linear-gradient(to bottom, rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.9)), url(\'{background_image}\'); background-size: cover; background-attachment: fixed; }}</style>"

    def get_styles_css(self):
        self.style_css_styled_container_1 = "{border: 1px solid rgba(34, 163, 97); background-color: rgba(40, 94, 159, 0.5); border-radius: 0.5rem; padding: calc(1em - 1px); overflow: hidden; /* Prevents the content from overflowing */ box-sizing: border-box;}"
        self.style_css_styled_container_2 = "{border: 2px solid rgba(0, 0, 0, 0.2); background-color: rgba(40, 94, 159, 0.75); border-radius: 0.5rem; padding: 1em; overflow: hidden; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2); transition: 0.3s; box-sizing: border-box;}"
        self.style_css_styled_container_3 = "{border: 2px solid rgba(40, 94, 159, 0.75); background-color: rgba(255, 255, 255, 0.75); border-radius: 0.5rem; padding: 1em; overflow: hidden; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2); transition: 0.3s; box-sizing: border-box;}"
        self.style_css_styled_container_4 = "{border: 2px solid rgba(0, 0, 0, 0.2); background-color: rgba(255, 255, 255, 0.75); border-radius: 0.5rem; padding: 1em; overflow: hidden; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2); transition: 0.3s; box-sizing: border-box;}"
        self.style_css_styled_container_5 = "{border: 2px solid rgba(0, 0, 0, 0.2); background-color: rgba(40, 94, 159, 0.75); border-radius: 0.5rem; padding: 1em; overflow: hidden; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2); transition: 0.3s; box-sizing: border-box;}"
        self.style_css_styled_container_6 = "{border: 2px solid rgba(40, 94, 159, 0.75); background-color: rgba(255, 255, 255, 0.75); border-radius: 0.5rem; padding: 1em; overflow: hidden; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2); transition: 0.3s; box-sizing: border-box;}"
    
    def get_master_styling(self):
        self.master_page_style = f"<style>{open("config/style.css").read()}</style>"

    def create_markdown(self, html_style):
        st.markdown(body=html_style, unsafe_allow_html=True)

    def create_stylable_container(self, css_style):
        styledcontainer = sc(key=css_style, css_styles=css_style)
        return styledcontainer



