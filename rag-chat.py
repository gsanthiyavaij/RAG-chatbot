import requests
import pyttsx3
import speech_recognition as sr
import asyncio
import threading
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import time

# OpenRouter.ai API config
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = "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"
MODEL = "meta-llama/llama-3-8b-instruct"

# Initialize TTS engine
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 160)
tts_engine.setProperty('volume', 1.0)

# Initialize speech recognition
recognizer = sr.Recognizer()

# GUI setup
window = tk.Tk()
window.title("Voice Assistant UI")

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window.attributes('-fullscreen', True)
window.bind("<Escape>", lambda e: toggle_fullscreen(window))

bg_image_path = r"static/bgg.jpg"
bg_image = Image.open(bg_image_path)
bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(window, bg="black", height=screen_height, width=screen_width)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

text_y = 10
conversations = []
max_text_width = screen_width // 2

def toggle_fullscreen(root, event=None):
    root.attributes('-fullscreen', not root.attributes('-fullscreen'))
    return "break"

def wrap_text(text, max_width):
    wrapped_lines = []
    current_line = ""
    for word in text.split():
        test_line = current_line + " " + word if current_line else word
        temp_text_id = canvas.create_text(0, 0, text=test_line, font=("Arial", 14), tags="temp")
        text_width = canvas.bbox(temp_text_id)[2]
        canvas.delete(temp_text_id)
        if text_width <= max_width:
            current_line = test_line
        else:
            wrapped_lines.append(current_line)
            current_line = word
    if current_line:
        wrapped_lines.append(current_line)
    return "\n".join(wrapped_lines)

def add_text_to_canvas(text):
    conversations.append(text)
    if len(conversations) > 4:
        conversations.pop(0)
    canvas.delete("convo")
    y_position = text_y
    for convo in conversations:
        wrapped_text = wrap_text(convo, max_text_width)
        text_id = canvas.create_text(10, y_position, anchor="nw", text=wrapped_text, font=("Arial", 14), fill="white", tags="convo")
        bbox = canvas.bbox(text_id)
        text_height = bbox[3] - bbox[1] if bbox else 20
        y_position += text_height + 10

def update_display(text):
    add_text_to_canvas(text)

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen():
    mic_index = 0  # Adjust if needed
    with sr.Microphone(device_index=mic_index) as source:
        update_display("Bot: Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        recognizer.pause_threshold = 1
        try:
            audio = recognizer.listen(source)
            phrase = recognizer.recognize_google(audio)
            update_display(f"You: {phrase}")
            return phrase
        except sr.WaitTimeoutError:
            return "timeout"
        except sr.UnknownValueError:
            return "I didn't catch that"
        except sr.RequestError as e:
            return f"Speech Recognition error: {e}"

# Main OpenRouter call
def query_openrouter(user_input, chat_history):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    chat_history.append({"role": "user", "content": user_input})

    payload = {
        "model": MODEL,
        "messages": chat_history,
        "max_tokens": 256,
        "temperature": 0.7
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        reply = data['choices'][0]['message']['content'].strip()
        chat_history.append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        return f"Error: {e}"

# Chat handling loop
async def chat_with_user():
    chat_history = [
        {"role": "system", "content": "You are a helpful assistant. Please respond in about 2 to 3 lines or around 50-60 words."}
    ]
    # Start directly with greeting
    greeting = "Hi, how can I help you today?"
    update_display(f"Bot: {greeting}")
    speak(greeting)

    while True:
        user_input = listen()
        if user_input.lower() in ['bye', 'exit', 'quit']:
            speak("Goodbye! Have a great day!")
            update_display("Assistant: Goodbye!")
            break
        elif user_input == "timeout":
            speak("Sorry, I didn't hear anything. Say 'Hello' to wake me again.")
            continue
        elif "I didn't catch that" in user_input:
            speak("Sorry, I couldn't understand you. Could you repeat?")
            continue

        response = query_openrouter(user_input, chat_history)
        update_display(f"Bot: {response}")
        speak(response)

# Wake word loop
async def main():
    # Start the conversation directly without wake word
    await chat_with_user()

def run_async_loop():
    asyncio.run(main())

# Start Button
btn_start = tk.Button(
    window,
    text="Start Conversation",
    font=("Helvetica", 14, "bold"),
    bg="#0052cc",
    fg="white",
    relief="raised",
    height=2,
    width=20,
    command=lambda: update_display("Assistant: How can I assist you?")
)
btn_start.place(x=220, y=1050)

# Start thread
thread = threading.Thread(target=run_async_loop)
thread.start()

window.mainloop()
