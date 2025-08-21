import tkinter as tk
from tkinter import ttk, scrolledtext
import speech_recognition as sr
import pyttsx3
import threading
import datetime
import webbrowser
import os
import requests
import json
import subprocess
import sys
from PIL import Image, ImageTk
import random
import math

class JarvisAI:
    def __init__(self):
        # Initialize attributes first
        self.is_listening = False
        self.conversation_history = []
        
        # Then setup UI and speech
        self.root = tk.Tk()
        self.setup_ui()
        self.setup_speech()
        
    def setup_ui(self):
        """Setup the beautiful UI"""
        self.root.title("JARVIS - AI Assistant")
        self.root.geometry("1000x700")
        self.root.configure(bg='#0a0a0a')
        self.root.resizable(True, True)
        
        # Create main frame with gradient-like effect
        self.main_frame = tk.Frame(self.root, bg='#0a0a0a')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title with glowing effect
        self.title_label = tk.Label(
            self.main_frame,
            text="J.A.R.V.I.S",
            font=("Arial", 32, "bold"),
            fg="#00ffff",
            bg="#0a0a0a"
        )
        self.title_label.pack(pady=20)
        
        # Subtitle
        self.subtitle_label = tk.Label(
            self.main_frame,
            text="Just A Rather Very Intelligent System",
            font=("Arial", 12),
            fg="#888888",
            bg="#0a0a0a"
        )
        self.subtitle_label.pack(pady=(0, 30))
        
        # Status indicator
        self.status_frame = tk.Frame(self.main_frame, bg='#0a0a0a')
        self.status_frame.pack(pady=10)
        
        self.status_indicator = tk.Label(
            self.status_frame,
            text="●",
            font=("Arial", 20),
            fg="#ff0000",
            bg="#0a0a0a"
        )
        self.status_indicator.pack(side=tk.LEFT)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="Ready",
            font=("Arial", 14),
            fg="#ffffff",
            bg="#0a0a0a"
        )
        self.status_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Conversation display
        self.conversation_frame = tk.Frame(self.main_frame, bg='#1a1a1a', relief=tk.RAISED, bd=2)
        self.conversation_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        self.conversation_text = scrolledtext.ScrolledText(
            self.conversation_frame,
            font=("Consolas", 11),
            bg="#1a1a1a",
            fg="#00ff00",
            insertbackground="#00ff00",
            selectbackground="#333333",
            wrap=tk.WORD,
            height=15
        )
        self.conversation_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Control buttons
        self.button_frame = tk.Frame(self.main_frame, bg='#0a0a0a')
        self.button_frame.pack(fill=tk.X, pady=20)
        
        # Listen button
        self.listen_button = tk.Button(
            self.button_frame,
            text="🎤 Start Listening",
            font=("Arial", 12, "bold"),
            bg="#004080",
            fg="#ffffff",
            activebackground="#0066cc",
            activeforeground="#ffffff",
            command=self.toggle_listening,
            padx=20,
            pady=10,
            relief=tk.RAISED,
            bd=3
        )
        self.listen_button.pack(side=tk.LEFT, padx=10)
        
        # Clear button
        self.clear_button = tk.Button(
            self.button_frame,
            text="🗑️ Clear",
            font=("Arial", 12, "bold"),
            bg="#800040",
            fg="#ffffff",
            activebackground="#cc0066",
            activeforeground="#ffffff",
            command=self.clear_conversation,
            padx=20,
            pady=10,
            relief=tk.RAISED,
            bd=3
        )
        self.clear_button.pack(side=tk.LEFT, padx=10)
        
        # Exit button
        self.exit_button = tk.Button(
            self.button_frame,
            text="❌ Exit",
            font=("Arial", 12, "bold"),
            bg="#404040",
            fg="#ffffff",
            activebackground="#666666",
            activeforeground="#ffffff",
            command=self.exit_app,
            padx=20,
            pady=10,
            relief=tk.RAISED,
            bd=3
        )
        self.exit_button.pack(side=tk.RIGHT, padx=10)
        
        # Add welcome message
        self.add_to_conversation("JARVIS", "Hello! I'm JARVIS, your AI assistant. Click 'Start Listening' to begin our conversation.")
        
    def setup_speech(self):
        """Setup speech recognition and text-to-speech"""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 180)
        voices = self.tts_engine.getProperty('voices')
        if voices:
            # Try to use a male voice if available
            for voice in voices:
                if 'male' in voice.name.lower() or 'david' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
    
    def add_to_conversation(self, speaker, message):
        """Add message to conversation display"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {speaker}: {message}\n\n"
        
        self.conversation_text.insert(tk.END, formatted_message)
        self.conversation_text.see(tk.END)
        self.root.update()
        
        # Store in history
        self.conversation_history.append({
            'timestamp': timestamp,
            'speaker': speaker,
            'message': message
        })
    
    def speak(self, text):
        """Convert text to speech"""
        def _speak():
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        
        threading.Thread(target=_speak, daemon=True).start()
    
    def listen_for_speech(self):
        """Listen for speech input"""
        try:
            with self.microphone as source:
                self.update_status("Listening...", "#00ff00")
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
                
            self.update_status("Processing...", "#ffff00")
            text = self.recognizer.recognize_google(audio)
            return text.lower()
            
        except sr.WaitTimeoutError:
            self.update_status("Timeout - No speech detected", "#ff8800")
            return None
        except sr.UnknownValueError:
            self.update_status("Could not understand audio", "#ff8800")
            return None
        except sr.RequestError as e:
            self.update_status(f"Error: {e}", "#ff0000")
            return None
    
    def update_status(self, status, color):
        """Update status indicator"""
        self.status_label.config(text=status)
        self.status_indicator.config(fg=color)
        self.root.update()
    
    def process_command(self, command):
        """Process voice commands and generate responses"""
        response = ""
        
        try:
            if any(greeting in command for greeting in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
                responses = [
                    "Hello! How can I assist you today?",
                    "Hi there! What can I do for you?",
                    "Greetings! I'm here to help.",
                    "Hello! Ready to assist you with any task."
                ]
                response = random.choice(responses)
                
            elif any(word in command for word in ['time', 'what time']):
                current_time = datetime.datetime.now().strftime("%I:%M %p")
                response = f"The current time is {current_time}."
                
            elif any(word in command for word in ['date', 'what date', 'today']):
                current_date = datetime.datetime.now().strftime("%B %d, %Y")
                response = f"Today is {current_date}."
                
            elif 'weather' in command:
                response = "I'd be happy to help with weather information, but I need access to a weather API. You can ask me to open a weather website instead."
                
            elif 'calculate' in command or 'math' in command:
                # Extract mathematical expression
                math_expression = command.replace('calculate', '').replace('math', '').strip()
                try:
                    # Simple math evaluation (be careful with eval in real applications)
                    result = eval(math_expression.replace('x', '*').replace('plus', '+').replace('minus', '-'))
                    response = f"The result is {result}."
                except:
                    response = "I couldn't process that mathematical expression. Please try a simpler format."
            
            elif 'open' in command:
                if 'google' in command:
                    webbrowser.open('https://www.google.com')
                    response = "Opening Google in your browser."
                elif 'youtube' in command:
                    webbrowser.open('https://www.youtube.com')
                    response = "Opening YouTube in your browser."
                elif 'notepad' in command:
                    try:
                        subprocess.Popen(['notepad.exe'])
                        response = "Opening Notepad."
                    except:
                        response = "Couldn't open Notepad. This might be a system limitation."
                else:
                    response = "Please specify what you'd like me to open (Google, YouTube, Notepad, etc.)."
            
            elif 'search' in command:
                search_query = command.replace('search', '').replace('for', '').strip()
                if search_query:
                    webbrowser.open(f'https://www.google.com/search?q={search_query}')
                    response = f"Searching for '{search_query}' on Google."
                else:
                    response = "What would you like me to search for?"
            
            elif any(word in command for word in ['joke', 'funny', 'humor']):
                jokes = [
                    "Why don't scientists trust atoms? Because they make up everything!",
                    "I told my wife she was drawing her eyebrows too high. She seemed surprised.",
                    "Why don't programmers like nature? It has too many bugs.",
                    "I'm reading a book about anti-gravity. It's impossible to put down!"
                ]
                response = random.choice(jokes)
            
            elif any(word in command for word in ['who are you', 'what are you', 'introduce yourself']):
                response = "I'm JARVIS, your AI assistant. I can help you with various tasks like telling time, opening applications, searching the web, doing calculations, and much more. Just ask me anything!"
            
            elif any(word in command for word in ['thank you', 'thanks']):
                responses = [
                    "You're welcome! Happy to help.",
                    "My pleasure! Anything else you need?",
                    "Glad I could assist you!",
                    "No problem at all!"
                ]
                response = random.choice(responses)
            
            elif any(word in command for word in ['bye', 'goodbye', 'exit', 'quit']):
                response = "Goodbye! It was nice talking with you. Have a great day!"
                
            elif 'stop listening' in command:
                response = "Stopping voice recognition. Click the button to start listening again."
                self.is_listening = False
                self.listen_button.config(text="🎤 Start Listening")
                self.update_status("Ready", "#ff0000")
                
            else:
                # General responses for unrecognized commands
                responses = [
                    "I'm not sure how to handle that request. Could you please rephrase?",
                    "I didn't quite understand. Can you try asking in a different way?",
                    "That's an interesting question! I'm still learning, so I might not have the perfect answer.",
                    "I'm here to help! Could you be more specific about what you need?"
                ]
                response = random.choice(responses)
                
        except Exception as e:
            response = f"Sorry, I encountered an error while processing your request: {str(e)}"
        
        return response
    
    def toggle_listening(self):
        """Toggle voice recognition on/off"""
        if not self.is_listening:
            self.is_listening = True
            self.listen_button.config(text="🔴 Stop Listening")
            threading.Thread(target=self.listening_loop, daemon=True).start()
        else:
            self.is_listening = False
            self.listen_button.config(text="🎤 Start Listening")
            self.update_status("Ready", "#ff0000")
    
    def listening_loop(self):
        """Main listening loop"""
        while self.is_listening:
            try:
                command = self.listen_for_speech()
                if command:
                    self.add_to_conversation("You", command.title())
                    
                    # Process the command
                    response = self.process_command(command)
                    
                    # Add response to conversation and speak it
                    self.add_to_conversation("JARVIS", response)
                    self.speak(response)
                    
                    self.update_status("Listening...", "#00ff00")
                    
                    # Check for exit command
                    if any(word in command for word in ['bye', 'goodbye', 'exit', 'quit']):
                        self.is_listening = False
                        self.listen_button.config(text="🎤 Start Listening")
                        self.update_status("Ready", "#ff0000")
                        break
                        
            except Exception as e:
                self.add_to_conversation("System", f"Error: {str(e)}")
                self.update_status("Error occurred", "#ff0000")
                continue
    
    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_text.delete(1.0, tk.END)
        self.conversation_history = []
        self.add_to_conversation("JARVIS", "Conversation cleared. How can I help you?")
    
    def exit_app(self):
        """Exit the application"""
        self.speak("Goodbye! Shutting down JARVIS.")
        self.root.after(2000, self.root.destroy)  # Give time for the speech to finish
    
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.destroy()

def main():
    """Main function to run JARVIS"""
    print("Initializing JARVIS AI Assistant...")
    print("Required packages: speech_recognition, pyttsx3, requests, pillow")
    print("Make sure you have these installed: pip install SpeechRecognition pyttsx3 requests pillow pyaudio")
    
    try:
        app = JarvisAI()
        app.run()
    except Exception as e:
        print(f"Error starting JARVIS: {e}")
        print("Make sure you have all required dependencies installed.")

if __name__ == "__main__":
    main()