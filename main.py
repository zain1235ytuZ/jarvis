import speech_recognition as sr
import webbrowser
import pyttsx3
import music
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

# pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init() 

newsapi = "a5dd4e93c9b04cec9044ef561b3188cd"  # Keep this for news API

# OpenAI API key configuration
openai_api_key = "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"
client = OpenAI(api_key=openai_api_key)

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    try:
        tts = gTTS(text)
        tts.save('temp.mp3') 

        # Initialize Pygame mixer
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init()
            except Exception as init_error:
                print(f"Pygame mixer initialization error: {init_error}")
                return

        # Load the MP3 file
        try:
            pygame.mixer.music.load('temp.mp3')
        except Exception as load_error:
            print(f"Pygame mixer load error: {load_error}")
            return

        # Play the MP3 file
        try:
            pygame.mixer.music.play()
        except Exception as play_error:
            print(f"Pygame mixer play error: {play_error}")
            return

        # Keep the program running until the music stops playing
        try:
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as busy_error:
            print(f"Pygame mixer busy wait error: {busy_error}")
            return
        
        try:
            pygame.mixer.music.unload()
        except Exception as unload_error:
            print(f"Pygame mixer unload error: {unload_error}")

        try:
            os.remove("temp.mp3") 
        except Exception as remove_error:
            print(f"Error removing temp.mp3: {remove_error}")
    except Exception as e:
        print(f"Error in speak function: {e}")

def aiProcess(command):
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
                {"role": "user", "content": command}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Exception during OpenAI call: {e}")
        return "Sorry, I am having trouble connecting to the AI service."

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = music.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])

    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output) 

def listen_for_command(timeout=5, phrase_time=5):
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Use recognizer instead of r
            try:
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time)
                return audio
            except sr.WaitTimeoutError:
                print("Listening timed out")
                return None
    except Exception as e:
        print(f"Error in listening: {e}")
        return None

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        print("recognizing...")
        try:
            audio = listen_for_command()
            if not audio:
                continue
                
            try:
                word = recognizer.recognize_google(audio)  # Use recognizer instead of r
                if word.lower() == "jarvis":
                    speak("Ya")
                    audio = listen_for_command()
                    if not audio:
                        continue
                        
                    try:
                        command = recognizer.recognize_google(audio)  # Use recognizer instead of r
                        print(f"Recognized command: {command}")
                        processCommand(command)
                    except sr.UnknownValueError:
                        speak("Sorry, I didn't catch that command")
                    except Exception as e:
                        print(f"Error processing command: {e}")
                        speak("Sorry, there was an error processing your command")
            except sr.UnknownValueError:
                pass  # Silently continue if no word is recognized
            except Exception as e:
                print(f"Recognition error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
