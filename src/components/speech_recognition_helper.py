import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=2)  # Reduce suppression time
        
        print("Knock knock... Start speaking.")
        try:
            # Capture audio
            audio = recognizer.listen(source, timeout=30, phrase_time_limit=50)  # Extended time
            
            # **Ensure the audio is long enough before processing**
            if len(audio.frame_data) < 50000:  # Adjust threshold if necessary
                print("Audio too short, retrying...")
                return recognize_speech()  # Retry listening
            
            # Convert speech to text
            text = recognizer.recognize_google(audio)
            print(f"User: {text}")
            return text

        except sr.WaitTimeoutError:
            print("⏳ Listening timed out. No speech detected.")
            return None
        except sr.UnknownValueError:
            print("🤷 Could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"🚨 Speech Recognition service error: {e}")
            return None
