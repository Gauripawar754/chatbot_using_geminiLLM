import json
import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
from PIL import Image


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
work_directory = os.path.dirname(os.path.abspath(__file__))



def get_gemini_reponse():
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    return model
  

def gemini_vision(prompt,image):
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content([prompt,image])
    result = response.text
    return result


# example
# image = Image.open("pexels-xmtnguyen-699953.jpg")
# prompt = "Write short caption for this image"
# output = gemini_vision(prompt,image)
# print(output)




def embediing_text(input_text):
    embedding_model = "models/embedding-001"
    embedding = genai.embed_content(model = embedding_model,
                                    content=input_text,
                                    task_type="retrieval_document")
    embedding_list = embedding['embedding']
    return embedding_list

# example
# output = embediing_text("who is thanos")
# print(output)


def calorie_advisor(prompt, image):
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    advisor = model.generate_content([prompt,image])
    result = advisor.text
    return result