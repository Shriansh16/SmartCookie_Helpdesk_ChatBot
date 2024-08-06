import speech_recognition as sr
import streamlit as st
import sounddevice as sd
import numpy as np
import wave

recognizer = sr.Recognizer()

def record_audio(filename, duration=5, fs=16000):
    print("Recording...")
    status_message = st.empty()
    status_message.write("Listening... Please speak clearly.")
    
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype=np.int16)
    sd.wait()  # Wait until the recording is finished
    
    status_message.write("Processing...")
    
    # Save the recorded data as a WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit audio
        wf.setframerate(fs)
        wf.writeframes(audio_data.tobytes())
    status_message.empty()

    return filename

def recognize_speech():
    audio_filename = "recorded_audio.wav"
    record_audio(audio_filename)
    
    with sr.AudioFile(audio_filename) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            text = "Sorry, I couldn't understand the audio."
        except sr.RequestError:
            text = "Sorry, there was an issue with the speech recognition service."
    
    #status_message.empty()  # Clear the status message
    return text