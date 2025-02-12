import openai
import os
import tempfile
import requests
from pydub import AudioSegment
from pydub.playback import play

def speak_text(text):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Ensure API key is set

    try:
        response = client.audio.speech.create(
            model="tts-1",  # OpenAI's text-to-speech model
            voice="alloy",  # Voices: alloy, echo, fable, onyx, nova, shimmer
            input=text
        )

        # Save audio file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            temp_audio.write(response.content)
            temp_audio_path = temp_audio.name

        # Play the generated speech
        audio = AudioSegment.from_file(temp_audio_path, format="mp3")
        play(audio)

        # Cleanup temp file
        os.remove(temp_audio_path)

    except Exception as e:
        print(f"Error with OpenAI TTS: {e}")
