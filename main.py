import os
import streamlit as st
from streamlit_option_menu import option_menu
from gemini_utility  import (get_gemini_reponse, gemini_vision, embediing_text, calorie_advisor)
from PIL import Image



working_dir = os.path.dirname(os.path.abspath(__file__))


# Set the page configuration
st.set_page_config(
    page_title="Gen AI",
    page_icon="robot",
    layout="centered",
    initial_sidebar_state="expanded"
)


with st.sidebar:

    selected = option_menu(
        menu_title='Gemini AI',
        options=["Chatbot", 
                 "Nutrition Details",
                 "Describe image",
                 "Embed Text"],
        icons=["chat-dots-fill", "patch-question-fill","image-fill","textarea-t"],
        menu_icon="robot",
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"padding": "0!important", "background-color": "#f8f9fa"},
            "icon": {"color": "#495057"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px"},
            "nav-link-selected": {"background-color": "#007bff"},
        }
    )


# to map terminology present in gemini model and streamlit
def translate_role_for_streamlit(user_role):
    if user_role == 'model':
        return 'assistant'
    else:
        return 'user'


# ------------------------------ for chatbot-------------------------#
if selected =='Chatbot':
    model = get_gemini_reponse()

    # to maintain history of chat
    if 'chat_session' not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    st.title("🤖 Chatbot")
        
    # to display chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(name=translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    
    # input field for user message
    user_prompt = st.chat_input('Ask Gemini...')


    if user_prompt:
        # user message
        st.chat_message(name='user').markdown(user_prompt)

        #  sent to gemini/LLM
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # display gemini reponse
        with st.chat_message(name='assistant'):
            st.markdown(gemini_response.text)




# ------------------------ for Image Captioning----------------------#

if selected == 'Describe image':
    
    st.title ("📸Snap Narrate")

    upload_image = st.file_uploader("Upload image...", type=["jpg","png","jpeg"])

    if st.button("Describe Image"):
        image = Image.open(upload_image)
        # col1,col2 = st.columns(2)

        # with col1:
        resized_image = image.resize((500,300))
        st.image(resized_image)

        prompt = "Describe this  image"

        describe = gemini_vision(prompt,image)

        # with col2:
        st.info(describe)




# --------------------for text embedding-------------------#

if selected =="Embed Text":

    st.title("🔠 Embed Text")

    input_text = st.text_area(label="", placeholder="Enter the text to get embeddings")

    if  st.button("Get Embedding"):
        response = embediing_text(input_text)
        st.markdown(response)


#-------------------calorie advisor--------------------#

if selected =="Nutrition Details":
    st.title(" 🥗 Nutrition Details")
    
    input_prompt  = '''assume that your health instructor. describe ingredient present in given image like
    
    Key Ingredints:
    ingredint 1
    ingredient 2...
    
    display percentage of calories and time required to digest it.
    also display percentage of carbohyadrates , fats, sugar, cholesterol and  also explain any food contraindicated to eat together and '''


    upload_img = st.file_uploader(label="Upload Image...", type=["jpg","png","jpeg"])

    if st.button("Nutrition Details"):

        food_img = Image.open(upload_img)

        resize_img = food_img.resize((500,300))
        st.image(resize_img,caption="Uploaded Food Image")

        advisor = calorie_advisor(input_prompt, food_img)  # add PIL image in LLM model
        st.info(advisor)
    