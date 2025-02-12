# components/gui.py
import os
import tkinter as tk
from PIL import Image, ImageTk
import threading
from components.chatbot import get_chatgpt_response
from components.speech_recognition_helper import recognize_speech
from components.text_to_speech import speak_text

class AICommunicationRobot:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Communication Robot")
        self.root.geometry("400x500")  # Lock window size to prevent resizing based on text
        self.root.resizable(False, False)  # Disable manual resizing

        # Load face images with correct paths
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images"))
        self.happy_face = ImageTk.PhotoImage(Image.open(os.path.join(base_path, "happy.png")).resize((300, 300)))
        self.thinking_face = ImageTk.PhotoImage(Image.open(os.path.join(base_path, "thinking.png")).resize((300, 300)))
        self.speaking_face = ImageTk.PhotoImage(Image.open(os.path.join(base_path, "speaking.png")).resize((300, 300)))
        self.listening_face = ImageTk.PhotoImage(Image.open(os.path.join(base_path, "listening.png")).resize((300, 300)))  # New facial expression

        # Create GUI elements
        self.label = tk.Label(root, text="Say 'Hey Robot' to start speaking", font=("Arial", 14))
        self.label.pack()

        self.face_label = tk.Label(root, image=self.happy_face)
        self.face_label.pack()

        self.listening = False  # Toggle for continuous listening
        self.root.after(1000, self.auto_listen)  # Start automatic listening

    def auto_listen(self):
        if not self.listening:
            self.listening = True
            self.face_label.config(image=self.listening_face)
            threading.Thread(target=self.process_conversation, daemon=True).start()
        self.root.after(5000, self.auto_listen)  # Check for input every 5 seconds

    def process_conversation(self):
        user_text = recognize_speech()
        if user_text:
            self.face_label.config(image=self.speaking_face)
            response_text = get_chatgpt_response(user_text)
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
