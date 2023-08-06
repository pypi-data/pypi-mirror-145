import speech_recognition as sr,pyttsx3
import pyaudio
engine = pyttsx3.init()

def set_voice(path):
    engine.setProperty('voice', path)

def say(*text):
    text=' '.join(map(str,text))
    engine.say(text)
    engine.runAndWait()
    return text

def listen(say_text=False,text_to_say='Say',lang='ru-RU'):
    r=sr.Recognizer()
    with sr.Microphone() as fl:
        if say_text:
            print(say(text_to_say))
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(fl,duration=1)
        task = r.listen(fl)
        try:
            teext = r.recognize_google(task,language=lang)
        except sr.UnknownValueError:
            if say_text:
                print(say("Error, say again"))
            try:teext=listen(say_text,text_to_say)
            except Exception as e:print(e)
        return teext