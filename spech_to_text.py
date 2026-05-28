import speech_recognition as sr
import speak

def spech_to_text():
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        # 1. NEW: Adjust for background noise for better accuracy
        r.adjust_for_ambient_noise(source, duration=0.5)
        
        try:
            # 2. Listen for audio (we can add a timeout so it doesn't hang forever if you stay silent)
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            
            # 3. Recognize using Google
            voice_data = r.recognize_google(audio)
            return voice_data

        except sr.UnknownValueError:
            speak.speak("Sorry, I didn't catch that.")
            return "" # Return empty string instead of None

        except sr.RequestError:
            speak.speak("No internet connection. Please check your network.")
            return ""

        except sr.WaitTimeoutError:
            # Triggers if you click Ask but don't say anything for 5 seconds
            return ""