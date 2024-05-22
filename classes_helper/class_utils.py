import streamlit as st
from classes_helper import class_clients 
from tempfile import NamedTemporaryFile


class Utils:
    def __init__(self):
        self.clients = class_clients.Clients()
        self.initialize_request_headers()

    def initialize_request_headers(self):
        self.request_headers = {'Accept': 'application/json', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36', 'Accept-Language': 'en-US,en;q=0.9','Accept-Encoding': 'gzip, deflate, br'}

    def create_openai_file(self, file_path, purpose):
        openai_file = self.clients.openai_client.files.create(file=open(file=file_path, mode="rb"), purpose=purpose)
        openai_file_id = openai_file.id
        return openai_file_id

    def create_temp_file(suffix: str=None):
        if suffix is not None:
            with NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                temp_file_path = temp_file.name
            return temp_file_path