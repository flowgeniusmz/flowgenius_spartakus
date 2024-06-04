import streamlit as st
from openai import OpenAI


client = OpenAI(api_key=st.secrets.openai.api_key)

assistantid = st.secrets.openai.assistant_id
toolchoice = {"type": "function", "function": {"name": "create_image"}}
additionalinstructions = "YOU BETTER USE THE TOOL CREATE_IMAGE AS REQUESTED. YOU WILL USE THAT TOOL AND YOU WILL LIKE IT. NO EXCEPTIONS. YOU BETTER CREATE A GOOD ASS PROMPT TO SO THE IMAGE ISNT HORRIBLE LIKE MOST OF YOUR WORK."

prompt = "A sleek, modern logo for an AI assistant called 'On Brand'. The logo should feature a friendly, futuristic AI character interacting with various objects like a house, car, and other items, showcasing how they would look in different settings. The design should be clean, professional, and visually appealing, with a color palette that includes shades of blue and white to convey trust and innovation."

response = client.images.generate(
  model="dall-e-3",
  prompt=prompt,
  size="1024x1024",
  quality="hd",
  n=1,
)
print(response)

image_url = response.data[0].url