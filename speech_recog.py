import speech_recognition as sr
import streamlit as st

# Initialize recognizer
recognizer = sr.Recognizer()

# Capture audio from the microphone
def fun1():
    with sr.Microphone() as source:
        st.write("Listening... Please speak clearly.")
        audio = recognizer.listen(source)

        try:
            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError:
            return "Could not request results; check your network connection."

if st.button('Click here to record'):
    st.write("Recording...")
    ok = fun1()
    st.write("You said: ", ok)

    