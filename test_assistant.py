import speech_recognition as sr
import pyttsx3
import os
import time
import re
import requests
import webbrowser
import shutil
from datetime import datetime

engine = pyttsx3.init()
engine.setProperty('rate', 150)

is_muted = False
reminders = []

def speak(text):
    print("[Assistant]:", text)
    if not is_muted:
        engine.say(text)
        engine.runAndWait()

r = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio).lower()
    except sr.UnknownValueError:
        speak("I can't capture, say again.")
        return ""
    except sr.RequestError:
        speak("Network error.")
        return ""

# NLP: Extract word to define
def extract_word_for_meaning(command):
    patterns = [
        r"meaning of (.+)",
        r"what is the meaning of (.+)",
        r"define (.+)",
        r"what does (.+) mean"
    ]
    for pattern in patterns:
        match = re.search(pattern, command)
        if match:
            return match.group(1).strip()
    return None

# Call Dictionary API
def get_word_meaning(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(url)
        data = response.json()

        if isinstance(data, list):
            meaning = data[0]['meanings'][0]['definitions'][0]['definition']
            example = data[0]['meanings'][0]['definitions'][0].get('example', 'No example available.')
            speak(f"The meaning of {word} is: {meaning}. Example: {example}")
        else:
            speak(f"Sorry, I couldn't find the meaning of {word}.")
    except Exception:
        speak("Sorry, something went wrong while fetching the meaning.")

# Other commands
def tell_time():
    current_time = datetime.now().strftime("%H:%M")
    speak(f"The current time is {current_time}.")

def search_google(command):
    query = command.replace("search google for", "").strip()
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak(f"Here are the search results for {query}.")

def shutdown_pc():
    speak("Shutting down the computer.")
    os.system("shutdown /s /t 5")

def restart_pc():
    speak("Restarting the computer.")
    os.system("shutdown /r /t 5")

def create_folder(command):
    folder_name = command.replace("create folder", "").strip()
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    path = os.path.join(desktop, folder_name)
    if not os.path.exists(path):
        os.mkdir(path)
        speak(f"Folder {folder_name} created on desktop.")
    else:
        speak(f"Folder {folder_name} already exists.")

def delete_folder(command):
    folder_name = command.replace("delete folder", "").strip()
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    path = os.path.join(desktop, folder_name)
    if os.path.exists(path):
        shutil.rmtree(path)
        speak(f"Folder {folder_name} deleted from desktop.")
    else:
        speak(f"Folder {folder_name} does not exist.")

def open_notepad():
    os.system("notepad")
    speak("Opening Notepad.")

def open_chrome():
    webbrowser.open("https://www.google.com")
    speak("Opening Google in browser.")

def mute_alita():
    global is_muted
    is_muted = True
    speak("Okay, I will be silent now.")

def unmute_alita():
    global is_muted
    is_muted = False
    speak("I am back to speaking.")

def execute_command(command):
    word = extract_word_for_meaning(command)
    if word:
        get_word_meaning(word)
        return True

    if "what time is it" in command:
        tell_time()
    elif "search google for" in command:
        search_google(command)
    elif "shutdown" in command:
        shutdown_pc()
    elif "restart" in command:
        restart_pc()
    elif "create folder" in command:
        create_folder(command)
    elif "delete folder" in command:
        delete_folder(command)
    elif "open notepad" in command:
        open_notepad()
    elif "open chrome" in command:
        open_chrome()
    elif "mute alita" in command:
        mute_alita()
    elif "unmute alita" in command:
        unmute_alita()
    elif "exit" in command or "stop" in command:
        speak("Goodbye!")
        return False
    else:
        speak("Sorry, I don't know that one.")

    return True

# Start assistant
speak("Voice assistant is running. Say 'Alita' to activate.")

while True:
    text = listen()
    if "alita" in text:
        speak("Yes Rushikesh, how can I help you?")
        command = listen()
        if not execute_command(command):
            break
    time.sleep(1)
