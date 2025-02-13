import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Start speaking.")
        recognizer.adjust_for_ambient_noise(source)  # Adapt to background noise

        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            text = recognizer.recognize_google(audio)
            print(f"User: {text}")
            return text
        except sr.WaitTimeoutError:
            print("Listening timed out. No speech detected.")
            return "I didn't hear anything. Please try again."
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return "I couldn't understand what you said."
        except sr.RequestError as e:
            print(f"Speech Recognition service error: {e}")
            return "I'm having trouble processing that. Please check your internet connection."
