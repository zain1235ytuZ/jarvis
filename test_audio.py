from main import speak, openai_api_key
from openai import OpenAI
import os

def test_openai_audio():
    if not openai_api_key:
        print("Error: OpenAI API key not found in environment variables")
        print("Please set the OPENAI_API_KEY environment variable")
        return
    
    test_text = "Hello! This is a test of the OpenAI text-to-speech system."
    print(f"Testing with text: {test_text}")
    
    try:
        # First try with OpenAI's audio API
        print("\nTesting OpenAI TTS...")
        speak(test_text, use_openai_audio=True)
        
        input("\nPress Enter to test with gTTS...")
        
        # Then try with gTTS
        print("\nTesting gTTS...")
        speak(test_text, use_openai_audio=False)
        
    except Exception as e:
        print(f"\nError during test: {e}")

if __name__ == "__main__":
    test_openai_audio()
