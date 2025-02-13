import openai
import os

# Load API key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("API Key is missing! Make sure OPENAI_API_KEY is set.")

print(f"Using API Key: {api_key[:5]}**********")  # Debugging: Print first 5 characters

def get_chatgpt_response(user_text):
    client = openai.OpenAI(api_key=api_key)  # Pass API key explicitly

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": user_text}]
    )
    return response.choices[0].message.content
