import os
import json
import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk
import threading
import sounddevice as sd
import numpy as np
import random
from components.chatbot import get_chatgpt_response
from components.speech_recognition_helper import recognize_speech
from components.text_to_speech import speak_text

class AICommunicationRobot:
    def __init__(self, root):
        self.root = root
        self.root.title("TalkieBud - AI Communication Robot")
        self.root.geometry("400x700")  # Increased height to fit new features
        self.root.resizable(False, False)  # Disable manual resizing

        # Load face images with correct paths
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images"))
        self.happy_face = ImageTk.PhotoImage(Image.open(os.path.join(base_path, "happy.png")).resize((300, 300)))
        self.thinking_face = ImageTk.PhotoImage(Image.open(os.path.join(base_path, "thinking.png")).resize((300, 300)))
        self.speaking_face = ImageTk.PhotoImage(Image.open(os.path.join(base_path, "speaking.png")).resize((300, 300)))
        self.listening_face = ImageTk.PhotoImage(Image.open(os.path.join(base_path, "listening.png")).resize((300, 300)))

        # Create GUI elements
        self.label = tk.Label(root, text="Say 'Hey Bud' to start talking", font=("Arial", 14))
        self.label.pack()

        self.face_label = tk.Label(root, image=self.happy_face)
        self.face_label.pack()

        # Voice Visualization Canvas
        self.voice_canvas = tk.Canvas(root, width=300, height=50, bg="black")
        self.voice_canvas.pack()
        
        # Audio Input Stream with callback to update voice visualization
        self.stream = sd.InputStream(callback=self.audio_callback, channels=1, samplerate=44100)
        self.stream.start()

        # User Input Box (optional manual input)
        tk.Label(root, text="User Input").pack()
        self.user_input_box = scrolledtext.ScrolledText(root, height=3, wrap=tk.WORD)
        self.user_input_box.pack(fill=tk.X, padx=10, pady=5)

        # Robot Output Box
        tk.Label(root, text="TalkieBud's Response").pack()
        self.robot_output_box = scrolledtext.ScrolledText(root, height=3, wrap=tk.WORD, state=tk.DISABLED)
        self.robot_output_box.pack(fill=tk.X, padx=10, pady=5)

        # Humor Level Slider
        tk.Label(root, text="Humor Level").pack()
        self.humor_slider = ttk.Scale(root, from_=0, to=100, orient="horizontal", length=200)
        self.humor_slider.set(50)
        self.humor_slider.pack()

        # Drama Level Slider
        tk.Label(root, text="Drama Level").pack()
        self.drama_slider = ttk.Scale(root, from_=0, to=100, orient="horizontal", length=200)
        self.drama_slider.set(50)
        self.drama_slider.pack()

        # Child Mode Toggle
        self.child_mode_var = tk.BooleanVar()
        self.child_mode_checkbox = tk.Checkbutton(root, text="Child Mode", variable=self.child_mode_var)
        self.child_mode_checkbox.pack()

        # Random Mode Toggle (default: OFF)
        self.random_mode_var = tk.BooleanVar(value=False)
        self.random_mode_checkbox = tk.Checkbutton(root, text="Random Mode (Idle Actions)", variable=self.random_mode_var)
        self.random_mode_checkbox.pack()

        # Idle Timer settings
        self.idle_time = 0
        self.max_idle_time = 180  # 3 minutes (180 seconds)
        self.random_action_count = 0
        self.max_random_actions = 3  # Max 3 random actions before stopping

        # Start monitoring idle time every second
        self.root.after(1000, self.monitor_idle)

        # Load Random Actions from JSON file
        self.random_actions = self.load_random_actions()

        # Conversation Loop: automatically listen for user speech every second
        self.listening = False
        self.root.after(1000, self.auto_listen)
    
    def audio_callback(self, indata, frames, time, status):
        """Updates the voice visualization based on real-time microphone input."""
        if status:
            print(status)
        volume = np.linalg.norm(indata) * 10
        bar_height = min(int(volume), 50)
        self.voice_canvas.delete("all")
        self.voice_canvas.create_rectangle(50, 50 - bar_height, 250, 50, fill="green")

    def load_random_actions(self):
        """Load random actions from JSON file; fallback to an empty list if missing."""
        actions_file = os.path.join(os.path.dirname(__file__), "random_actions.json")
        if os.path.exists(actions_file):
            with open(actions_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data.get("actions", [])
        return []

    def monitor_idle(self):
        """Checks for inactivity and, if in random mode, performs a random action."""
        self.idle_time += 1

        if (self.random_mode_var.get() and 
            self.idle_time >= self.max_idle_time and 
            self.random_action_count < self.max_random_actions):
            
            if self.random_actions:
                action = random.choice(self.random_actions)
                # Update face to thinking while performing a random action
                self.face_label.config(image=self.thinking_face)
                self.update_robot_text(action)
                speak_text(action)
                self.random_action_count += 1
                self.idle_time = 0  # Reset idle timer after performing an action

        self.root.after(1000, self.monitor_idle)

    def auto_listen(self):
        """Automatically starts the conversation process if not already listening."""
        if not self.listening:
            self.listening = True
            threading.Thread(target=self.process_conversation, daemon=True).start()
        self.root.after(1000, self.auto_listen)

    def process_conversation(self):
        """Handles the conversation process with the user."""
        self.idle_time = 0
        self.random_action_count = 0

        # Update face to indicate listening
        self.face_label.config(image=self.listening_face)
        user_text = recognize_speech()

        if user_text:
            # Update face to thinking while processing the response
            self.face_label.config(image=self.thinking_face)
            response_text = get_chatgpt_response(
                user_text,
                int(self.humor_slider.get()),
                int(self.drama_slider.get()),
                self.child_mode_var.get()
            )
            self.update_robot_text(response_text)
            # Update face to speaking while delivering the response
            self.face_label.config(image=self.speaking_face)
            speak_text(response_text)
        
        # Return face to the default happy state after conversation
        self.face_label.config(image=self.happy_face)
        self.listening = False

    def update_robot_text(self, response_text):
        """Updates the GUI text box with the robot's response."""
        self.robot_output_box.config(state=tk.NORMAL)
        self.robot_output_box.delete("1.0", tk.END)
        self.robot_output_box.insert(tk.END, response_text)
        self.robot_output_box.config(state=tk.DISABLED)


def launch_app():
    root = tk.Tk()
    app = AICommunicationRobot(root)
    root.mainloop()


if __name__ == "__main__":
    launch_app()
