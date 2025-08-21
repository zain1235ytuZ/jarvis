# Jarvis AI Assistant

A modern, voice-enabled AI assistant with a sleek graphical user interface. Jarvis can help you with various tasks, answer questions, play music, fetch news, and more!

## Features

- 🎙️ Voice commands with wake word ("Jarvis")
- 💬 Text-based chat interface
- 🎵 Play music from YouTube
- 📰 Get the latest news headlines
- 🌐 Web search and navigation
- 🧠 Powered by OpenAI's GPT-3.5 for natural language understanding
- 🎨 Modern, responsive UI with dark theme

## Prerequisites

- Python 3.8 or higher
- Microphone (for voice commands)
- Internet connection

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd jarvis
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   NEWSAPI_KEY=your_newsapi_key
   ```

5. (Optional) Create a logo:
   ```bash
   python create_logo.py
   ```

## Usage

### Graphical User Interface (Default)
```bash
python main.py
```

### Command Line Interface
```bash
python main.py --cli
```

## Voice Commands

- "Jarvis, what's the weather?"
- "Jarvis, play [song name]"
- "Jarvis, what's in the news?"
- "Jarvis, open Google"
- "Jarvis, tell me a joke"

## Keyboard Shortcuts (GUI)

- `Enter`: Send message
- `Ctrl+Q`: Quit application
- `Ctrl+M`: Toggle microphone

## Troubleshooting

- If you encounter audio issues, make sure your default playback device is set correctly.
- For speech recognition issues, check your microphone settings and ensure it's not muted.
- Make sure you have a stable internet connection for API calls.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
