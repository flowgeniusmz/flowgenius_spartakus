import streamlit as st
from streamlit_extras import stylable_container as sc
from classes_config import class_config, class_styles



class PageSetup:
    def __init__(self):
        self.styles = class_styles.Styles()
        self.config = class_config.Config()

    def get_page_title_section(self, pagenumber, include_divider: bool=True):
        title = self.config.get_pageconfig_item(pageconfig_element="title", pagenumber=pagenumber)
        subtitle = self.config.get_pageconfig_item(pageconfig_element="subtitle", pagenumber=pagenumber)
        style = self.styles.style_html_title_subtitle_1.format(title=title, subtitle=subtitle)
        self.styles.create_markdown(html_style=style)
        if include_divider:
            st.divider()
    
    def get_page_overview_section(self, pagenumber, include_divider: bool=True):
        header = self.config.get_pageconfig_item(pageconfig_element="header", pagenumber=pagenumber)
        description = self.config.get_pageconfig_item(pageconfig_element="description", pagenumber=pagenumber)
        header_style = self.styles.style_html_header.format(header=header)
        self.styles.create_markdown(html_style=header_style)
        if pagenumber == 0:
            st.markdown(body=description)
        else:
            st.markdown(f"{description}")
        if include_divider:
            st.divider()

    def get_popover_menu(self, pagenumber):
        menulist = st.popover(label="🧭 Menu", disabled=False, use_container_width=True)
        with menulist:
            st.page_link(page=self.config.get_pageconfig_item(pagenumber=0, pageconfig_element="path"), label=self.config.get_pageconfig_item(pagenumber=0, pageconfig_element="subtitle"), disabled=(pagenumber == 0))
            st.page_link(page=self.config.get_pageconfig_item(pagenumber=1, pageconfig_element="path"), label=self.config.get_pageconfig_item(pagenumber=1, pageconfig_element="subtitle"), disabled=(pagenumber == 1))
            st.page_link(page=self.config.get_pageconfig_item(pagenumber=2, pageconfig_element="path"), label=self.config.get_pageconfig_item(pagenumber=2, pageconfig_element="subtitle"), disabled=(pagenumber == 2))
            st.page_link(page=self.config.get_pageconfig_item(pagenumber=3, pageconfig_element="path"), label=self.config.get_pageconfig_item(pagenumber=3, pageconfig_element="subtitle"), disabled=(pagenumber == 3))
            # st.page_link(page=self.config.get_pageconfig_item(pagenumber=4, pageconfig_element="path"), label=self.config.get_pageconfig_item(pagenumber=4, pageconfig_element="subtitle"), disabled=(varPageNumber == 4))
            # st.page_link(page=self.config.get_pageconfig_item(pagenumber=5, pageconfig_element="path"), label=self.config.get_pageconfig_item(pagenumber=5, pageconfig_element="subtitle"), disabled=(varPageNumber == 5))
    
    def get_homepage_section_component(self, pagenumber):
        subtitle = self.config.get_pageconfig_item(pagenumber=pagenumber, pageconfig_element="subtitle")
        path = self.config.get_pageconfig_item(pagenumber=pagenumber, pageconfig_element="path")
        about = self.config.get_pageconfig_item(pagenumber=pagenumber, pageconfig_element="about")
        container = self.styles.create_stylable_container(css_style=self.styles.style_css_styled_container_5)
        with container:
            container1 = self.styles.create_stylable_container(css_style=self.styles.style_css_styled_container_6)
            with container1:
                pagelink = st.page_link(page=path, label=subtitle, icon=None, use_container_width=True)
                pop = st.popover(label="About", disabled=False, use_container_width=True)
                with pop:
                    st.markdown(about)

    def get_homepage_section(self):
        container = st.container(border=False)
        with container:
            cols = st.columns([1,20,20,1])
            with cols[1]:
                self.get_homepage_section_component(pagenumber=1)
                self.get_homepage_section_component(pagenumber=3)
            with cols[2]:
                self.get_homepage_section_component(pagenumber=2)
                self.get_homepage_section_component(pagenumber=4)

    def master_title_display(self, pagenumber, include_divider: bool=True):
        headercontainer = st.container(border=False)
        with headercontainer:
            headercols = st.columns([10,2])
            with headercols[0]:
                self.get_page_title_section(pagenumber=pagenumber, include_divider=False)
            with headercols[1]:
                self.get_popover_menu(pagenumber=pagenumber)
            if include_divider:
                st.divider()

    def master_page_display(self, pagenumber):
        self.display_background_image()
        #self.styles.master_page_style
        self.master_title_display(pagenumber=pagenumber)
        self.get_page_overview_section(pagenumber=pagenumber)
        if pagenumber == 0:
            self.get_homepage_section()

    def get_page_title_manual(self, title, subtitle, include_divider: bool=True):
        style = self.styles.style_html_title_subtitle_1.format(title=title, subtitle=subtitle)
        self.styles.create_markdown(html_style=style)

    def display_background_image(self):
        style = self.styles.style_html_background_image_2.format(background_image=self.config.app_background_image)
        self.styles.create_markdown(html_style=style)

    def switch_to_homepage(self):
        path = st.secrets.pageconfig.page_paths[0]
        #path = "pages/1_Home🏠_Home.py"
        st.switch_page(page=self.config.get_pageconfig_item(pageconfig_element="path", pagenumber=0))