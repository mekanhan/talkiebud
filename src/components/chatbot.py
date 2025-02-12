import openai
import os

# Load API key from environment variable
api_key = os.getenv("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")

def get_chatgpt_response(user_text):
    client = openai.OpenAI(api_key=api_key)  # Pass API key explicitly

    response = client.chat.completions.create(
        model="gpt-4-turbo",  # Or use "gpt-4-turbo"
        messages=[{"role": "user", "content": user_text}]
    )
    return response.choices[0].message.content
