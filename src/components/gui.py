import tkinter as tk
import threading
import sys
import queue
from components.chatbot import get_chatgpt_response
from components.speech_recognition_helper import recognize_speech
from components.text_to_speech import speak_text

class ConsoleOutput:
    """Redirects print statements to a Tkinter Text widget."""
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.queue = queue.Queue()  # Buffer messages

    def write(self, message):
        """Send messages to the queue for GUI display."""
        self.queue.put(message)

    def flush(self):
        """Flush method required for stdout redirection."""
        pass

    def update_console(self):
        """Fetch messages from the queue and update the Text widget."""
        while not self.queue.empty():
            message = self.queue.get()
            self.text_widget.insert(tk.END, message)
            self.text_widget.see(tk.END)  # Auto-scroll to latest log

class AICommunicationRobot:
    def __init__(self, root):
        self.root = root
        self.root.title("TalkieBud - AI Communication Robot")
        self.root.geometry("700x500")
        self.root.configure(bg="#2C3E50")  # Dark blue-grey background

        # Styling
        button_style = {"font": ("Arial", 12), "fg": "white", "bg": "#3498DB", "padx": 10, "pady": 5, "bd": 3}

        # Label - App Title
        self.label = tk.Label(root, text="🤖 TalkieBud - AI Robot", font=("Arial", 16, "bold"), fg="white", bg="#2C3E50")
        self.label.pack(pady=10)

        self.listening = True
        self.processing = False
        self.lock = threading.Lock()

        # **Control Buttons (Now in a frame)**
        button_frame = tk.Frame(root, bg="#2C3E50")
        button_frame.pack(pady=10)

        self.start_button = tk.Button(button_frame, text="Start App", command=self.start_app, **button_style)
        self.start_button.grid(row=0, column=0, padx=10)

        self.toggle_button = tk.Button(button_frame, text="Stop App", command=self.stop_app, **button_style)
        self.toggle_button.grid(row=0, column=1, padx=10)

        # **Voice Selection Dropdown**
        self.available_voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
        self.selected_voice = tk.StringVar(value="nova")  # Default voice

        voice_frame = tk.Frame(root, bg="#2C3E50")
        voice_frame.pack(pady=10)

        self.voice_label = tk.Label(voice_frame, text="🎙️ Select Voice:", font=("Arial", 12), fg="white", bg="#2C3E50")
        self.voice_label.grid(row=0, column=0, padx=5)

        self.voice_dropdown = tk.OptionMenu(voice_frame, self.selected_voice, *self.available_voices)
        self.voice_dropdown.config(font=("Arial", 12), bg="#3498DB", fg="white", width=10)
        self.voice_dropdown.grid(row=0, column=1, padx=5)

        # **Console Output Box**
        self.console_text = tk.Text(root, height=12, width=80, bg="#1C2833", fg="white", font=("Arial", 10), wrap="word")
        self.console_text.pack(pady=10, padx=10)

        # Redirect print output to console widget
        self.console_output = ConsoleOutput(self.console_text)
        sys.stdout = self.console_output

        # Start updating logs
        self.update_console_output()

        # Start listening loop
        self.root.after(1000, self.auto_listen)

    def stop_app(self):
        """Fully stops the app's processes but keeps GUI open."""
        print("⚠️ Stopping AI communication...")
        self.listening = False
        self.processing = False
        self.label.config(text="🔴 App Stopped")

    def start_app(self):
        """Restarts the process by re-enabling listening."""
        print("✅ Restarting AI communication...")
        self.listening = True
        self.label.config(text="🟢 App Running")

    def auto_listen(self):
        """Continuously listens when enabled, but only one process at a time."""
        if self.listening and not self.processing:
            thread = threading.Thread(target=self.process_conversation, daemon=True)
            thread.start()

        self.root.after(2000, self.auto_listen)

    def process_conversation(self):
        """Handles voice recognition and AI response."""
        with self.lock:
            if not self.listening or self.processing:
                return

            self.processing = True
            print("🎙 Listening for speech...")

            user_text = recognize_speech()
            if user_text:
                print(f"👤 User said: {user_text}")
                
                # Get selected voice from the dropdown
                selected_voice = self.selected_voice.get()
                print(f"🗣 Using voice: {selected_voice}")

                response_text, speech_file = get_chatgpt_response(user_text)
                print(f"🤖 AI Response: {response_text}")
                speak_text(response_text, selected_voice)

            self.processing = False  # Allow next cycle

    def update_console_output(self):
        """Continuously update console output in GUI."""
        self.console_output.update_console()  # Fetch messages
        self.root.after(100, self.update_console_output)  # Keep refreshing every 100ms

def launch_app():
    root = tk.Tk()
    AICommunicationRobot(root)
    root.mainloop()

if __name__ == "__main__":
    launch_app()
