import speech_recognition as sr
import webbrowser
import pyttsx3
import time
import musicLibrary

# It's more efficient to initialize these once, outside the loop
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Optional: Set voice properties
try:
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
except IndexError:
    print("No voices found. Using default voice.")

def speak(text):
    """Function to speak the given text."""
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    """Processes the recognized command."""
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif c.lower().startswith("play"):
        # Basic error handling for song name
        parts = c.lower().split()
        if len(parts) > 1:
            song = parts[1]
            if song in musicLibrary.music:
                link = musicLibrary.music[song]
                webbrowser.open(link)
                speak(f"Playing {song}")
            else:
                speak(f"Sorry, I don't have the song {song} in my library.")
        else:
            speak("You need to tell me which song to play.")

if __name__ == "__mainn__":
    speak("Initializing Jarvis...")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                # Adjust recognizer for ambient noise once
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            
            # Recognize the wake word
            word = recognizer.recognize_google(audio)
            print(f"Heard: {word}") # Debug print

            if "jarvis" in word.lower():
                speak("Yeah?") # Changed to a slightly longer word to ensure it plays
                print("Jarvis Active... Listening for a command.")
                
                with sr.Microphone() as source:
                    # No need to adjust for noise again
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
                
                # Recognize the command
                command = recognizer.recognize_google(audio)
                print(f"Command Heard: {command}") # Debug print
                processCommand(command)
                    
        except sr.UnknownValueError:
            # This is common when no speech is detected, so we can ignore it
            # print("Could not understand audio")
            pass
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"An error occurred: {e}")