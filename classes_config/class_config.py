import streamlit as st


class Config:
    def __init__(self):
        self.initialize_app_config()
        self.initialize_page_config()
        self.initialize_status_config()

    def initialize_app_config(self):
        self.app_name = st.secrets.appconfig.app_name
        self.app_icon = st.secrets.appconfig.app_icon
        self.app_layout = st.secrets.appconfig.app_layout
        self.app_initial_sidebar = st.secrets.appconfig.app_initial_sidebar
        self.app_background_image = st.secrets.appconfig.app_background_image
    
    def initialize_page_config(self):
        self.page_icons = st.secrets.pageconfig.page_icons
        self.page_titles = st.secrets.pageconfig.page_titles
        self.page_subtitles = st.secrets.pageconfig.page_subtitles
        self.page_descriptions = st.secrets.pageconfig.page_descriptions
        self.page_headers = st.secrets.pageconfig.page_headers
        self.page_paths = st.secrets.pageconfig.page_paths
        self.page_abouts = st.secrets.pageconfig.page_abouts
        self.page_count = len(self.page_paths)

    def initialize_status_config(self):
        self.error_icon = "⚠️"
        self.waiting_icon = "⏳"
        self.success_icon = "✅"

    def get_pageconfig_item(self, pagenumber, pageconfig_element):
        """
        Retrieves configuration data for a given page number and configuration type from an array within Streamlit secrets.

        Args:
        - varPageNumber: int, the page number for which to retrieve the configuration.
        - varPageConfigType: str, the type of configuration to retrieve ('title', 'subtitle', 'description', 'header', 'icon', 'path', 'about').

        Returns:
        - str, the configuration data for the given page number and configuration type from the specified array.
        """

        if pageconfig_element == "icon" :
            value = self.page_icons[pagenumber]
        elif pageconfig_element == "title":
            value = self.page_titles[pagenumber]
        elif pageconfig_element == "subtitle":
            value = self.page_subtitles[pagenumber]
        elif pageconfig_element == "path":
            value = self.page_paths[pagenumber]
        elif pageconfig_element == "header":
            value = self.page_headers[pagenumber]
        elif pageconfig_element == "description":
            value = self.page_descriptions[pagenumber]
        elif pageconfig_element == "about":
            value = self.page_abouts[pagenumber]
        else:
            value = "error"

        return value