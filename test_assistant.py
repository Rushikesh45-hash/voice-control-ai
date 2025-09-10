import speech_recognition as sr
import pyttsx3
import os
import time
import shutil

engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    print("[Assistant]:", text)
    engine.say(text)
    engine.runAndWait()

r = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)  # adjust for ambient noise
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



def execute_command(command):
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    
    if "shutdown" in command:
        print("[Test] Shutdown command detected.")
    elif "restart" in command:
        print("[Test] Restart command detected.")
    elif "create folder" in command:
        folder_name = command.replace("create folder", "").strip()
        print(f"[Test] Would create folder: {folder_name}")
    elif "delete folder" in command:
        folder_name = command.replace("delete folder", "").strip()
        print(f"[Test] Would delete folder: {folder_name}")
    elif "open notepad" in command:
        print("[Test] Open Notepad command detected.")
    elif "open chrome" in command:
        print("[Test] Open Chrome command detected.")
    elif "exit" in command or "stop" in command:
        print("[Test] Exit command detected.")
        return False
    else:
        print("[Test] Command not recognized.")
    
    return True

speak("Voice assistant is running. Say 'Alita' to activate.")

while True:
    text = listen()
    if "Alita" in text:
        speak("Yes Rushikesh, how can I help you?")
        command = listen()
        if not execute_command(command):
            break
    time.sleep(1)
