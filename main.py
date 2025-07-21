import speech_recognition as sr
import webbrowser
import pyttsx3
import time
import musicLibrary
import requests

recognizer = sr.Recognizer()
# engine=pyttsx3.init()
newsapi = "7100c5b6a9ed451c822fa2dc225631fb"
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[0].id) 


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif c.lower().startswith("play"):
        song=c.lower().split(" ")[1]
        link = musicLibrary.music[song] 
        webbrowser.open(link)
    elif "news" in c.lower():
        r=requests.get(f"https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={newsapi}")
        if r.status_code==200:
            data = r.json()

            articles = data.get('articles',[])

            for article in articles:
                speak(article['title']) 




if __name__=="__main__":
    speak("Initializing Jarvis...")
    while True:
        r=sr.Recognizer()
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source,timeout=2,phrase_time_limit=3)
            word= r.recognize_google(audio)
            if(word.lower()=="jarvis"):
                time.sleep(0.5) 
                speak("Yeah")
                time.sleep(1) 
                print("Jarvis Active...")
                # engine.runAndWait()
                # time.sleep(1.5)
                # print("Jarvis Active...")
                with sr.Microphone() as source:
                    audio = recognizer.listen(source, timeout=3, phrase_time_limit=4)
                    command = recognizer.recognize_google(audio)
                    print(command)
                    processCommand(command)
                    
        except Exception as e:
            print("error; {0}".format(e))    

