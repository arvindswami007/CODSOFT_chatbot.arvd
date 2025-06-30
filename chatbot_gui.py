
import tkinter as tk
from tkinter import scrolledtext, messagebox
import pyttsx3
from textblob import TextBlob
from datetime import datetime
import wikipedia
import json
import speech_recognition as sr

# Load or create memory
try:
    with open("memory.json", "r") as f:
        memory = json.load(f)
except:
    memory = {"name": None, "mood": None}

def save_memory():
    with open("memory.json", "w") as f:
        json.dump(memory, f)

# Initialize TTS
tts = pyttsx3.init()
tts.setProperty("rate", 150)

def speak(text):
    tts.say(text)
    tts.runAndWait()

def chatbot_response(user_input):
    user_input = user_input.lower()

    if "my name is" in user_input:
        memory["name"] = user_input.split("my name is")[-1].strip().capitalize()
        save_memory()
        return f"Nice to meet you, {memory['name']}! That's a great name!"

    if "i am feeling" in user_input:
        mood = user_input.split("i am feeling")[-1].strip()
        memory["mood"] = mood.capitalize()
        save_memory()
        return f"Got it. Hope things get even better from here!"

    if "what is my name" in user_input:
        return f"You're {memory['name']}." if memory["name"] else "Hmm, I don’t know your name yet. Tell me?"

    if "how am i feeling" in user_input:
        return f"You said you're feeling {memory['mood']}." if memory["mood"] else "You haven't told me how you feel."

    if "how are you" in user_input:
        return "I'm coded with care, so I feel fantastic 😄 How about you?"

    if "time" in user_input:
        return "⏰ The time is " + datetime.now().strftime("%I:%M %p")

    if "joke" in user_input:
        return "Why did the JavaScript developer leave the restaurant? Because they didn’t get arrays. 😂"

    if "tell me about" in user_input:
        topic = user_input.split("tell me about")[-1].strip()
        try:
            return wikipedia.summary(topic, sentences=2)
        except:
            return "Couldn't find info on that 🤔 Try something else?"

    if "bye" in user_input or "exit" in user_input:
        return "Goodbye! It was lovely chatting with you. Come back soon 🖐️"

    if any(word in user_input for word in ["hello", "hi", "hey"]):
        return "Hey! 👋 I’m here to chat, help, and maybe make you smile!"

    polarity = TextBlob(user_input).sentiment.polarity
    if polarity > 0.3:
        return "You sound cheerful today! I love that energy ✨"
    elif polarity < -0.3:
        return "That sounds tough... I'm here for you. 🧡"
    else:
        return "Got it. I'm always here to chat, no matter the mood."

def send_message():
    msg = user_input.get()
    if not msg.strip():
        return
    chat_display.insert(tk.END, "You: " + msg + "\n")
    reply = chatbot_response(msg)
    chat_display.insert(tk.END, "Bot: " + reply + "\n\n")
    speak(reply)
    user_input.delete(0, tk.END)

def listen_to_microphone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            user_input.delete(0, tk.END)
            user_input.insert(0, text)
            send_message()
        except sr.UnknownValueError:
            speak("Sorry, I didn’t catch that.")
        except sr.RequestError:
            speak("Sorry, I can't connect to Google right now.")
        except sr.WaitTimeoutError:
            speak("You were silent. Try again.")

def export_chat():
    try:
        with open("chat_history.txt", "w") as f:
            f.write(chat_display.get("1.0", tk.END))
        messagebox.showinfo("Export", "Chat exported to chat_history.txt")
    except:
        messagebox.showerror("Export Failed", "Could not save the chat.")

# GUI Setup
root = tk.Tk()
root.title("Smart Chatbot")

# Dark mode styling
root.configure(bg="#1e1e1e")

chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, font=("Consolas", 12), bg="#2e2e2e", fg="white", insertbackground="white")
chat_display.pack(padx=10, pady=10)

frame = tk.Frame(root, bg="#1e1e1e")
frame.pack(pady=(0,10))

user_input = tk.Entry(frame, width=45, font=("Consolas", 12), bg="#2e2e2e", fg="white", insertbackground="white")
user_input.pack(side=tk.LEFT, padx=(10, 0))

send_button = tk.Button(frame, text="Send", command=send_message, font=("Arial", 12), bg="#4CAF50", fg="white")
send_button.pack(side=tk.LEFT, padx=10)

voice_button = tk.Button(frame, text="🎤 Speak", command=listen_to_microphone, font=("Arial", 12), bg="#2196F3", fg="white")
voice_button.pack(side=tk.LEFT, padx=10)

export_button = tk.Button(frame, text="💾 Export", command=export_chat, font=("Arial", 12), bg="#FF9800", fg="white")
export_button.pack(side=tk.LEFT, padx=10)

root.mainloop()
