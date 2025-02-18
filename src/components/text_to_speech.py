import openai
import os
import tempfile
from pydub import AudioSegment
from pydub.playback import play

def speak_text(response_text, selected_voice):
    if not isinstance(response_text, str):
        print(f"Error: Expected string, but got {type(response_text)}")
        return

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice=selected_voice,
            input=response_text
        )

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            temp_audio.write(response.content)
            temp_audio_path = temp_audio.name

        audio = AudioSegment.from_file(temp_audio_path, format="mp3")
        play(audio)

    except Exception as e:
        print(f"Error with OpenAI TTS: {e}")
