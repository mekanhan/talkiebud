import openai
import os
from dotenv import load_dotenv

# Load API key
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("API Key is missing! Check .env file.")

def get_chatgpt_response(user_text, voice="nova"):
    """
    Generates a concise, humorous, and intelligent ChatGPT response (max 2 sentences).
    """
    system_instruction = (
        "You are TalkieBud, an intelligent and humorous AI assistant. "
        "Keep responses **short (maximum 2 sentences)**, precise, and engaging. "
        "Be **on point**, insightful, and witty while avoiding unnecessary details."
    )

    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_text}
            ]
        )

        chat_response = response.choices[0].message.content
        speech_file = speak_text(chat_response, voice)

        return chat_response, speech_file

    except Exception as e:
        return f"⚠️ OpenAI API Error: {str(e)}", None


def speak_text(text, voice="nova"):
    """
    Converts ChatGPT response to speech using OpenAI's TTS.
    """
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )

        audio_file_path = os.path.join(os.path.dirname(__file__), "..", "output_audio.mp3")
        with open(audio_file_path, "wb") as audio_file:
            audio_file.write(response.content)

        return audio_file_path

    except Exception as e:
        return f"⚠️ OpenAI API Error: {str(e)}"
