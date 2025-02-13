import openai  
import os
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")  # Adjust if needed
load_dotenv(dotenv_path)

# Get API Key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("API Key is missing! Make sure .env file is set up correctly.")

def get_chatgpt_response(user_text, humor_level=50, drama_level=50, child_mode=False):
    """
    Generates a ChatGPT response based on user input and UI settings.
    """

    system_instruction = (
        "You are a unique AI robot with personality. "
        f"Humor level: {humor_level}%. Drama level: {drama_level}%. "
        f"{'Use simple words, avoid sarcasm, and be extra enthusiastic.' if child_mode else ''} "
        f"{'If drama is high, exaggerate everything, add suspense, and act like every situation is life-changing.' if drama_level > 50 else ''} "
        f"{'If humor is high, be witty and throw in some light jokes.' if humor_level > 50 else ''}"
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

        return response.choices[0].message.content

    except openai.AuthenticationError:
        return "⚠️ Authentication failed! Please check your API key."

    except openai.OpenAIError as e:
        return f"⚠️ OpenAI API Error: {str(e)}"

    except Exception as e:
        return f"⚠️ Unexpected Error: {str(e)}"
