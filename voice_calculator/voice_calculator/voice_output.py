import pyttsx3

# Initialize the engine once globally (best practice)
engine = pyttsx3.init()

def speak(text):
    """Convert the given text to speech and play it."""
    engine.say(text)
    engine.runAndWait()

# Optional: Test if module works standalone
if __name__ == "__main__":
    speak("Hello Aman, your voice output is working perfectly!")
