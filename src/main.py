import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))  # Ensure `src` is in sys.path

from components.gui import launch_app

if __name__ == "__main__":
    print("🚀 AI Communication Robot is starting...")
    launch_app()
