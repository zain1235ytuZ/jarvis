import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
import time
from PIL import Image, ImageTk
import os
import sys

# Import main functions with error handling
try:
    from main import listen_for_command, processCommand, speak, recognizer, openai_api_key
    HAS_OPENAI = bool(openai_api_key)
except ImportError as e:
    print(f"Error importing main functions: {e}")
    # Create dummy functions to prevent errors
    def dummy_function(*args, **kwargs):
        return "Error: Could not load required functions"
    
    listen_for_command = processCommand = speak = recognizer = dummy_function
    HAS_OPENAI = False

class JarvisUI:
    def __init__(self, root):
        self.root = root
        self.queue = queue.Queue()
        self.listening = False
        self.use_openai_audio = False
        self.setup_ui()
        self.root.after(100, self.process_queue)
    
    def setup_ui(self):
        self.root.title("Jarvis AI Assistant")
        self.root.geometry("800x600")
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            main_frame, wrap=tk.WORD, font=('Arial', 11),
            bg='#f0f0f0', state='disabled')
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X)
        
        self.input_entry = ttk.Entry(input_frame, font=('Arial', 11))
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.input_entry.bind('<Return>', self.process_text_input)
        
        ttk.Button(input_frame, text="Send", command=self.process_text_input).pack(side=tk.LEFT)
        
        # Add audio settings frame
        left_panel = ttk.Frame(main_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # OpenAI Audio Toggle
        if HAS_OPENAI:
            self.audio_var = tk.BooleanVar(value=self.use_openai_audio)
            audio_toggle = ttk.Checkbutton(
                left_panel,
                text="Use OpenAI Voice",
                variable=self.audio_var,
                command=self.toggle_openai_audio,
                style='TCheckbutton'
            )
            audio_toggle.pack(anchor=tk.W, pady=5)
        
        # Listen button
        self.listen_btn = ttk.Button(
            left_panel,
            text=" Start Listening",
            command=self.toggle_listening,
            style='Accent.TButton'
        )
        self.listen_btn.pack(fill=tk.X, pady=5)
        
        # Status indicator
        self.status_var = tk.StringVar(value="Status: Ready")
        status_label = ttk.Label(
            left_panel,
            textvariable=self.status_var,
            style='Status.TLabel'
        )
        status_label.pack(fill=tk.X, pady=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(main_frame, textvariable=self.status_var,
                 relief=tk.SUNKEN, anchor=tk.W).pack(fill=tk.X, pady=(5, 0))
        
        # Add welcome message
        self.add_message("Jarvis", "Hello! How can I help you today?")
    
    def add_message(self, sender, message, style=""):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state='disabled')
    
    def toggle_listening(self):
        self.listening = not self.listening
        if self.listening:
            self.status_var.set("Listening...")
            threading.Thread(target=self.listen_loop, daemon=True).start()
        else:
            self.status_var.set("Ready")
    
    def listen_loop(self):
        while self.listening:
            try:
                audio = listen_for_command()
                if audio and self.listening:
                    command = recognizer.recognize_google(audio).lower()
                    if command == "jarvis":
                        self.queue.put(("add_message", "You", "Jarvis"))
                        audio = listen_for_command()
                        if audio and self.listening:
                            command = recognizer.recognize_google(audio).lower()
                            self.queue.put(("add_message", "You", command))
                            self.process_command(command)
            except:
                pass
    
    def process_text_input(self, event=None):
        command = self.input_entry.get().strip()
        if command:
            self.add_message("You", command)
            self.input_entry.delete(0, tk.END)
            self.process_command(command)
    
    def toggle_openai_audio(self):
        """Toggle OpenAI audio on/off"""
        self.use_openai_audio = self.audio_var.get()
        status = "enabled" if self.use_openai_audio else "disabled"
        self.queue.put(("status", f"OpenAI audio {status}"))
        self.add_message("System", f"OpenAI audio {status}", "system")
    
    def process_command(self, command):
        if not command:
            return
        
        self.queue.put(("status", "Processing..."))
        
        def process():
            try:
                processCommand(command, queue=self.queue, use_openai_audio=self.use_openai_audio)
                self.queue.put(("status", "Ready"))
            except Exception as e:
                error_msg = str(e)
                self.queue.put(("status", f"Error: {error_msg}"))
                self.queue.put(("add_message", "Jarvis", f"I encountered an error: {error_msg}"))
        
        threading.Thread(target=process, daemon=True).start()
    
    def process_queue(self):
        try:
            while True:
                task = self.queue.get_nowait()
                if task[0] == "add_message":
                    self.add_message(task[1], task[2])
                elif task[0] == "status":
                    self.status_var.set(task[1])
        except queue.Empty:
            pass
        self.root.after(100, self.process_queue)

if __name__ == "__main__":
    root = tk.Tk()
    app = JarvisUI(root)
    root.mainloop()
