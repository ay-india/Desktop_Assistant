import pyttsx3
import pythoncom  # NEW: The Windows COM object manager

def speak(text):
    # 1. Safely initialize the Windows COM apartment for this thread
    # This completely prevents the PyEval_RestoreThread GIL crash
    pythoncom.CoInitialize()
    
    # 2. Spin up the engine
    engine = pyttsx3.init()
    
    # 3. Set the speaking rate
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 70)

    # 4. The throwaway word to prevent audio clipping
    buffered_text = "Um... " + text 
    
    # 5. Speak and wait
    engine.say(buffered_text)
    engine.runAndWait()