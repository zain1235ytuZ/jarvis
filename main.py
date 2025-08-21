import tkinter as tk
import speech_recognition as sr
import webbrowser
import pyttsx3
import music
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
import sys
import base64
from queue import Queue
from dotenv import load_dotenv

# Initialize speech recognition
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Load environment variables
load_dotenv(dotenv_path="env/.env")

# Get API keys
newsapi = os.getenv("NEWSAPI_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

if not newsapi or not openai_api_key:
    print("Error: Required API keys not found in environment variables")
    sys.exit(1)

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# Global queue for UI updates
ui_queue = Queue()

def speak(text, queue=None, use_openai_audio=False):
    """
    Convert text to speech using either gTTS or OpenAI's audio API
    
    Args:
        text: Text to be spoken
        queue: Optional queue for UI updates
        use_openai_audio: If True, use OpenAI's audio API (requires API key)
    """
    if queue:
        queue.put(("add_message", "Jarvis", text))
    
    if use_openai_audio and openai_api_key:
        try:
            # Use OpenAI's audio API
            response = client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=text,
                response_format="wav"
            )
            
            # Save the audio file
            audio_path = "temp_audio.wav"
            response.stream_to_file(audio_path)
            
            # Initialize Pygame mixer if not already done
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            
            # Load and play the audio
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
            # Clean up
            pygame.mixer.music.unload()
            os.remove(audio_path)
            
            return
            
        except Exception as e:
            print(f"OpenAI Audio API Error: {e}")
            print("Falling back to gTTS...")
    
    # Fallback to gTTS if OpenAI audio fails or not requested
    try:
        # Use gTTS for better voice quality
        tts = gTTS(text=text, lang='en')
        tts.save('temp.mp3')

        # Initialize Pygame mixer if not already done
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        # Load and play the audio
        pygame.mixer.music.load('temp.mp3')
        pygame.mixer.music.play()
        
        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        # Clean up
        pygame.mixer.music.unload()
        os.remove("temp.mp3")
        
    except Exception as e:
        print(f"Error in speak function: {e}")
        # Fallback to pyttsx3 if gTTS fails
        engine.say(text)
        engine.runAndWait()

def aiProcess(command, queue=None):
    """
    Process command using OpenAI's API
    """
    if queue:
        queue.put(("status", "Thinking..."))
    
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """You are Jarvis, a helpful AI assistant. 
                Be concise and helpful in your responses. If asked to perform an action, 
                confirm it's done in a friendly manner."""},
                {"role": "user", "content": command}
            ],
            temperature=0.7
        )
        response = completion.choices[0].message.content
        return response
    except Exception as e:
        error_msg = f"I encountered an error: {str(e)}"
        print(f"OpenAI API Error: {e}")
        return error_msg

def processCommand(command, queue=None, use_openai_audio=False):
    """
    Process user commands and execute appropriate actions
    
    Args:
        command: The user's command
        queue: Optional queue for UI updates
        use_openai_audio: If True, use OpenAI's audio for responses
    """
    if not command:
        return
        
    command = command.lower()
    
    try:
        if command == "exit" or command == "quit" or command == "goodbye":
            speak("Goodbye! Have a great day!", queue, use_openai_audio=use_openai_audio)
            if queue:
                queue.put(("status", "Ready"))
            return "exit"
            
        elif "open google" in command:
            webbrowser.open("https://google.com")
            speak("Opening Google", queue)
            
        elif "open youtube" in command:
            webbrowser.open("https://youtube.com")
            speak("Opening YouTube", queue)
            
        elif "open linkedin" in command:
            webbrowser.open("https://linkedin.com")
            speak("Opening LinkedIn", queue)
            
        elif command.startswith("play"):
            try:
                song = command.split(" ", 1)[1]
                if hasattr(music, 'music') and song in music.music:
                    webbrowser.open(music.music[song])
                    speak(f"Playing {song}", queue)
                else:
                    speak(f"I couldn't find a song named {song}", queue)
            except Exception as e:
                speak("Please specify a song to play", queue)
                
        elif "news" in command:
            if queue:
                queue.put(("status", "Fetching news..."))
                
            try:
                r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
                if r.status_code == 200:
                    articles = r.json().get('articles', [])[:5]  # Get top 5 articles
                    if articles:
                        speak("Here are the top news headlines", queue)
                        for i, article in enumerate(articles, 1):
                            title = article.get('title', '').split(' - ')[0]
                            if title:
                                speak(f"{i}. {title}", queue)
                    else:
                        speak("I couldn't fetch the news right now", queue)
                else:
                    speak("Sorry, I'm having trouble getting the news", queue)
            except Exception as e:
                print(f"Error fetching news: {e}")
                speak("I encountered an error while fetching the news", queue)
                
        else:
            # Let OpenAI handle other requests
            output = aiProcess(command, queue)
            speak(output, queue, use_openai_audio=use_openai_audio)
            
    except Exception as e:
        error_msg = f"I encountered an error: {str(e)}"
        print(f"Command processing error: {e}")
        speak(error_msg, queue)
        
    if queue:
        queue.put(("status", "Ready")) 

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

def start_cli():
    """
    Start the command line interface for Jarvis
    """
    print("Jarvis AI Assistant - CLI Mode")
    print("Type 'exit' or 'quit' to end the session\n")
    
    while True:
        try:
            command = input("You: ").strip()
            if not command:
                continue
                
            if command.lower() in ['exit', 'quit', 'goodbye']:
                print("\nGoodbye!")
                break
                
            # Process the command
            processCommand(command)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    # Check if running in CLI mode or GUI mode
    if '--cli' in sys.argv or len(sys.argv) > 1 and sys.argv[1] == '--cli':
        start_cli()
    else:
        try:
            from jarvis_ui import JarvisUI
            root = tk.Tk()
            app = JarvisUI(root)
            root.mainloop()
        except ImportError as e:
            print(f"Error: Could not import UI components. {e}")
            print("Falling back to CLI mode...\n")
            start_cli()
