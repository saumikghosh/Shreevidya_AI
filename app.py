import os
import pandas as pd
import streamlit as st

from datetime import datetime,time
from PIL import Image
import google.generativeai as genai

gemini_api_key = os.getenv("GOOGLE_API_19jan_key1")
genai.configure(api_key = gemini_api_key)
model = genai.GenerativeModel("gemini-2.5-flash-lite")

st.title(":orange[Shreevidya AI:] :blue[Your Personal Fortune Teller]")
st.markdown("##### Ask any fortune-related questions and get instant personalised answers!")
st.write('''
Follow these steps,
* Enter your details in the sidebar and click on the submit button first before proceeding.
* Then, ask any fortune-related question in the text area and click 'Generate Report'!!!
''')

st.sidebar.header(":red[ENTER YOUR DETAILS]")
name = st.sidebar.text_input('Enter your Name')
gender = st.sidebar.selectbox('Select your Gender', ['Male', 'Female', 'Other'])
dob = st.sidebar.date_input(
    "Date of Birth",
    min_value=datetime(1920, 1, 1),
    max_value=datetime.now(),
)
tob = st.sidebar.time_input(
    "Time of Birth", 
    value=time(12, 0), # Defaults to Noon
    step=60 # Steps by seconds/minutes
)
birth_place = st.sidebar.text_input(
    "Place of Birth", 
    placeholder="City, State, Country",
    help="Enter the geographical region where you were born."
)
uploaded_image = st.sidebar.file_uploader("Choose the image of your lagna kundli...", type=["jpg", "jpeg","png","jfif"],accept_multiple_files=True)
uploaded_image = [Image.open(img) for img in uploaded_image] 
if uploaded_image:
    st.sidebar.success('Image has been loaded successfully')
    
    st.sidebar.subheader(':blue[Uploaded Image]')
    st.sidebar.image(uploaded_image)

if st.sidebar.button('Submit'):
    st.sidebar.write(f"{name}, Your Gender is: {gender} Date of Birth is: {dob} Time of Birth is: {tob} and Birth Place is: {birth_place}")
user_input = st.text_area("Enter your fortune-related queries here:")

if st.button('Submit'):
    with st.spinner('Processing...'):
         prompt = f'''<Role> You are an expert in astrology and has 25+ years experience in guiding people wishing to know about their fortune.
         <Goal> Generate the customised report addressing the problem the user has asked.
         Here, is the question that user has asked :{user_input}.
         <Context>Here are the details that the user has provided.
         name = {name}
         gender = {gender}
         date of birth = {dob}
         time of birth = {tob}
         place of birth = {birth_place}
         <format> Following should be the outline in the sequence provided,
         * Get the details of the latitude and longitude of the place of birth provided by the user. Then write according to the kundli provided by you. And specefically give your judgement only by the image provided and don't try to analyse anything based on the other details provided by the user. no need to state the planets and their houses in your generated report just give your verdict.
         * Explain what the person has faced in terms of accomplishments and struggles in the various field of life like education, health,career and other fields which the user wants to know and has provided in the prompt.
         * Suggest the possible reasons for the problem.
         * What are the possible solutions.
         * Try to answer specific queries asked by the user like an astrologer.  
         * Mention any specefic remedies which are needed depending on the planetary alignment.
         * You can also suggest gemstone if required. Giving stones for the planets which are well placed in the ascendant's birth chart as an expert astrologer does and just suggesting vedic rituals, mantras and remedies for the maligned planets as positioned in the chart. Do not suggest stones for the maligned positioned planets.
         * At last, create a final brief summary and try to instill hope in the mind of the user while not deviating from the astrological future reality.
         <Instruction> 
         * Use bullet points wherever required.
         * Create tables to represent any data wherever possible to represent the time frame when a particular work, which the user wants to know can be accomplished.
         * Strictly do not be overly pessimistic.
         * The report should be in MS-Word format and not exceeding 2 pages.
         '''

         response = model.generate_content([prompt,*uploaded_image],generation_config={'temperature':0.8})
         st.write(response.text)
    if st.download_button(label='Click to Download',data = response.text,file_name='structural defect report.txt',mime = 'text/plain'):
        st.success('Your file is downloaded')
 