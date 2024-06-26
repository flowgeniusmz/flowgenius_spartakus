import os
import toml

class ProjectSetup:
    def __init__(self):
        self.ensure_directories()
        self.create_secrets_file()
        self.secrets = toml.load(".streamlit/secrets.toml")
        self.page_paths = self.secrets["pageconfig"]["page_paths"]
        self.page_titles = self.secrets["pageconfig"]["page_titles"]
        self.setup_directories()
        self.create_files()

    def ensure_directories(self):
        directories = [
            ".streamlit",
            "config",
            "classes",
            "pages",
            "assets"
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def create_secrets_file(self):
        secrets_path = ".streamlit/secrets.toml"
        if not os.path.exists(secrets_path):
            with open(secrets_path, "w") as file:
                file.write(self.get_default_secrets_toml_content())
            print(f"Created {secrets_path} with default content.")

    def get_default_secrets_toml_content(self):
        return """[appconfig]
app_name = "Spartakus.AI"
app_icon = "assets/logo/icon.png"
app_layout = "wide"
app_initial_sidebar = "collapsed"

[pageconfig]
page_icons = ["🏠", "📝", "📂", "⚙️"]
page_titles = ["Spartakus.AI Home", "Submit Quote Request", "View Submissions", "Admin"]
page_subtitles = ["Home 🏠", "Submit a Quote Request 📝", "View Submitted Quotes 📂", "Admin Settings ⚙️"]
page_descriptions = [
    "Welcome to Spartakus.AI, the streamlined solution for commercial insurance submissions.",
    "Submit your commercial insurance quote requests with ease using our AI-assisted system.",
    "View and manage your previously submitted insurance quotes.",
    "Admin settings and configurations for Spartakus.AI."
]
page_headers = ["Welcome to Spartakus.AI", "Submit Quote Request", "View Submissions", "Admin"]
page_paths = ["pages/1_🏠_Home.py", "pages/2_📝_Submit_Quote_Request.py", "pages/3_📂_View_Submissions.py", "pages/4_⚙️_Admin.py"]
page_abouts = ["Home page and navigation.", "Submit new quote requests.", "View and manage submissions.", "Admin settings."]
page_count = 4

[statusconfig]
error_icon = "⚠️"
waiting_icon = "⏳"
success_icon = "✅"

[openai]
api_key = ""
assistant_id = ""

[supabase]
api_key = ""
api_key_admin = ""
url = ""
table_users = "users"
column_username = "username"
column_password = "password"

[salesforce]
username = 'michael.zozulia@almalasers.com'
password = 'EverlyQuinn#7665'
security_token = '8VY2ZFvXya0eyI1oGCMOZeVc'

[tavily]
api_key = "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"

[google]
google_api_key = "AIzaSyDGy9el4sZshs5guM-nlI3-v3rqd-CpowE"
maps_api_key = "AIzaSyDodiR_fX83xula4pUmtFmFt39aOQsoCDw"

[yelp]
client_id = "4mBcAx4cYawepsiZK-RwGQ"
api_key = "4h9E_DyulVOPOTbOwV-KaSdcEAz14ieJ5PWCcmXkJFMa61_hMSrl-F1-5FtLU5JOQ8sBaNNLwi02StFPmeEVVH33-ZY0erhbbJWf42BmmOpovDsyeYRGTYcG7I1LZnYx"
"""

    def setup_directories(self):
        self.create_page_files()

    def create_page_files(self):
        page_template = """import streamlit as st
from config import pagesetup as ps

page_number = {page_number}
ps.master_page_display_styled_popmenu_pop(varPageNumber=page_number)
"""
        for page_number, path in enumerate(self.page_paths):
            full_path = os.path.join("pages", path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            content = page_template.format(page_number=page_number)
            with open(full_path, "w") as file:
                file.write(content)
        print("Pages created successfully.")

    def create_files(self):
        files_content = {
            ".streamlit/config.toml": self.get_config_toml_content(),
            "config/pagesetup.py": "",
            "config/sessionstates.py": "",
            "config/style.css": self.get_sytle_css_content(),
            ".gitignore": ".streamlit/secrets.toml\n",
            "requirements.txt": self.get_requirements_txt_content(),
            "app.py": self.get_app_py_content(),
            "classes/class_pagesetup.py": self.get_class_pagesetup_py_content()
        }
        for file_path, content in files_content.items():
            with open(file_path, "w") as file:
                file.write(content)
        print("Files created successfully.")

    def get_config_toml_content(self):
        return """[server]
maxUploadSize=1028

[theme]
base = "light"
primaryColor="#1E3A8A"
secondaryBackgroundColor="#FCA311"
textColor="#000000"
backgroundColor = "#FFFFFF"

[client]
showSidebarNavigation = false
"""

    def get_requirements_txt_content(self):
        return """asyncio
bs4
extra_streamlit_components
ffmpeg
folium
google-api-python-client
ipython
moviepy
nest-asyncio
numpy
openai
opencv-python-headless
pandas
pillow
plotly
pydub
pygwalker
pytube
requests
simple_salesforce
streamlit
streamlit-folium
streamlit_elements
streamlit_extras
stripe
supabase
tavily-python
temp
urllib3
youtube-transcript-api
youtube_dl
beautifulsoup4
PyScrappy
webscraping
WebScraperAPI
Scrapy
playwright
scrapegraphai
yelpapi
googlemaps
pydantic
"""

    def get_app_py_content(self):
        return """import streamlit as st
from config import pagesetup as ps, sessionstates as ss

st.set_page_config(page_title=st.secrets.appconfig.app_name, page_icon=st.secrets.appconfig.app_icon, layout=st.secrets.appconfig.app_layout, initial_sidebar_state=st.secrets.appconfig.app_initial_sidebar)

ps.get_page_styling()
ps.display_background_image()

ss.initialize_session_states()

ps.set_title_manual(varTitle="SpartakusAI", varSubtitle="Login / Registration", varDiv=True)
"""
    def get_sytle_css_content(self):
        return """@import url('https://fonts.googleapis.com/css2?family=Kode+Mono:wght@400..700&family=Roboto+Slab:wght@100..900&display=swap'); 

html, body, div, p, [class*="css"] {
    font-family: 'Roboto', kode mono; 
    font-size: 18px;
    font-weight: 500;
    color: #717da3;
}
"""
    def get_class_pagesetup_py_content(self):
        return """class PageSetup:
    @staticmethod
    def master_page_display_styled_popmenu_pop(varPageNumber: int):
        pass

    @staticmethod
    def get_page_styling():
        pass

    @staticmethod
    def display_background_image():
        pass

    @staticmethod
    def set_title_manual(varTitle: str, varSubtitle: str, varDiv: bool):
        pass
"""

   

# Example usage
project_setup = ProjectSetup()
