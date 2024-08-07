import speech_recognition as sr

r = sr.Recognizer()
def recognize_speech():
  with sr.Microphone() as source:
    print("Speak Anything :")
    audio = r.listen(source,timeout=3,phrase_time_limit=10)
    print('Done, Please wait while we are processing what you said...')
    try:
        text = r.recognize_google(audio)
        return text
    except:
        print("Sorry we could not recognize what you said. You can try again.")