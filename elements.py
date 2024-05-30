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
    

class Elements:
    def __init__(self):
        self.styles = Styles()

    def container1(self, height: int=None, border: bool=False):
        scouter = sc(key="container1outer", css_styles=self.styles.style_css_styled_container_5)
        with scouter:
            scinner = sc(key="container1inner", css_styles=self.styles.style_css_styled_container_3)
            with scinner:
                if height is not None:
                    container1 = st.container(height=height, border=border)
                else:
                    container1 = st.container(border=border)
        return container1
    

class HomePage:
    def __init__(self):
        self.elements = Elements()
        self.initialize_display() 

    def profile_section(self):
        self.profile_container = self.elements.container1(height=200, border=False)

    def nutrition_section(self):
        self.nutrition_container = self.elements.container1(height=400, border=True)

    def workout_section(self):
        self.workout_container = self.elements.container1(height=250, border=False)

    def initialize_display(self):
        container = st.container(border=True)
        with container:
            self.cols = st.columns([1, 20, 1, 20, 1, 20,1])
            with self.cols[1]:
                self.profile_section()
            with self.cols[3]:
                self.nutrition_section()
            with self.cols[5]:
                self.workout_section()



