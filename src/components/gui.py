import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
from components.chatbot import get_chatgpt_response
from components.speech_recognition_helper import recognize_speech
from components.text_to_speech import speak_text

class AICommunicationRobot:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Communication Robot")
        self.root.geometry("400x600")  # Increased height to fit controls
        self.root.resizable(False, False)  # Disable manual resizing

        # Load face images with correct paths
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images"))
        self.happy_face = ImageTk.PhotoImage(Image.open(os.path.join(base_path, "happy.png")).resize((300, 300)))
        self.thinking_face = ImageTk.PhotoImage(Image.open(os.path.join(base_path, "thinking.png")).resize((300, 300)))
        self.speaking_face = ImageTk.PhotoImage(Image.open(os.path.join(base_path, "speaking.png")).resize((300, 300)))
        self.listening_face = ImageTk.PhotoImage(Image.open(os.path.join(base_path, "listening.png")).resize((300, 300)))

        # Create GUI elements
        self.label = tk.Label(root, text="Say 'Hey Bud' to start speaking", font=("Arial", 14))
        self.label.pack()

        self.face_label = tk.Label(root, image=self.happy_face)
        self.face_label.pack()

        # Humor Level Slider
        tk.Label(root, text="Humor Level").pack()
        self.humor_slider = ttk.Scale(root, from_=0, to=100, orient="horizontal", length=200)
        self.humor_slider.set(50)  # Default value
        self.humor_slider.pack()

        # Drama Level Slider
        tk.Label(root, text="Drama Level").pack()
        self.drama_slider = ttk.Scale(root, from_=0, to=100, orient="horizontal", length=200)
        self.drama_slider.set(50)  # Default value
        self.drama_slider.pack()

        # Child Mode Toggle
        self.child_mode_var = tk.BooleanVar()
        self.child_mode_checkbox = tk.Checkbutton(root, text="Child Mode", variable=self.child_mode_var)
        self.child_mode_checkbox.pack()

        # Conversation Loop
        self.listening = False
        self.root.after(1000, self.auto_listen)  # Start automatic listening

    def auto_listen(self):
        if not self.listening:
            self.listening = True
            self.face_label.config(image=self.listening_face)
            threading.Thread(target=self.process_conversation, daemon=True).start()
        self.root.after(1000, self.auto_listen)  # Check for input every 5 seconds

    def process_conversation(self):
        user_text = recognize_speech()
        if user_text:
            self.face_label.config(image=self.speaking_face)

            # Get slider values
            humor_level = int(self.humor_slider.get())
            drama_level = int(self.drama_slider.get())
            child_mode = self.child_mode_var.get()

            # Get AI response with personality settings
            response_text = get_chatgpt_response(user_text, humor_level, drama_level, child_mode)

            self.label.config(text=response_text)
            speak_text(response_text)

        self.face_label.config(image=self.happy_face)
        self.listening = False  # Reset listening toggle

def launch_app():
    root = tk.Tk()
    app = AICommunicationRobot(root)
    root.mainloop()

if __name__ == "__main__":
    launch_app()
