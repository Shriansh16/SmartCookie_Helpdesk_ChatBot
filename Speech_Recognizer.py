import speech_recognition as sr
import streamlit as st

recognizer = sr.Recognizer()
def recognize_speech():
    with sr.Microphone() as source:
        status_message = st.empty()
        status_message.write("Listening... Please speak clearly.")
        audio = recognizer.listen(source)
        status_message.write("Processing...")
        text = recognizer.recognize_google(audio)
        status_message.empty()  # Clear the status message
        return text