import datetime
import webbrowser
import weather
import os
import urllib.parse
import requests
import pyautogui
import psutil
import winshell
import wikipedia
import speak
import memory 
from thefuzz import process

# ==========================================
# 1. HELPER FUNCTIONS (The Assistant's Tools)
# ==========================================

def invert_pronouns(text):
    """Swaps I/My/Me to You/Your so the bot sounds natural."""
    inversions = {
        "my": "your", 
        "your": "my", 
        "i": "you", 
        "me": "you",
        "mine": "yours", 
        "yours": "mine",
        "am": "are"
    }
    words = text.split()
    inverted_words = [inversions.get(word, word) for word in words]
    return " ".join(inverted_words)

def get_time():
    time_str = datetime.datetime.now().strftime("%I:%M %p")
    return f"The current time is {time_str}."

def take_screenshot():
    import random
    name = random.randint(1, 1000)
    filepath = f"E:\\screenshot_{name}.png"
    try:
        pyautogui.screenshot(filepath)
        return f"Screenshot taken and saved to your E drive as screenshot_{name}."
    except Exception:
        return "I couldn't save the screenshot. Please check the E drive."

def check_battery():
    battery = psutil.sensors_battery()
    plug_status = "and plugged in" if battery.power_plugged else "running on battery"
    return f"Your system battery is at {battery.percent} percent {plug_status}."

def clean_system():
    try:
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
        return "Recycle bin emptied successfully."
    except Exception:
        return "The recycle bin is already empty."

def get_joke():
    try:
        url = "https://official-joke-api.appspot.com/random_joke"
        response = requests.get(url).json()
        return f"{response['setup']} ... {response['punchline']}"
    except Exception:
        return "I couldn't think of a joke right now."

def get_news():
    try:
        url = "https://saurav.tech/NewsAPI/top-headlines/category/general/in.json"
        response = requests.get(url).json()
        articles = response.get('articles', [])[:3] 
        if not articles: return "I couldn't find any news."
        
        news_text = "Here are the top headlines. "
        for i, article in enumerate(articles):
            news_text += f"Headline {i+1}: {article['title']}. "
        return news_text
    except Exception:
        return "I couldn't fetch the news right now."

# ==========================================
# 2. THE COMMAND DICTIONARY (The Brain Map)
# ==========================================

STATIC_COMMANDS = {
    "hello": lambda: "Hey there! How can I help you?",
    "what time is it": get_time,
    "take a screenshot": take_screenshot,
    "battery status": check_battery,
    "clean my system": clean_system,
    "empty recycle bin": clean_system,
    "volume up": lambda: pyautogui.press("volumeup", presses=5) or "Turning volume up.",
    "volume down": lambda: pyautogui.press("volumedown", presses=5) or "Turning volume down.",
    "mute volume": lambda: pyautogui.press("volumemute") or "Volume muted.",
    "tell me a joke": get_joke,
    "tell me the news": get_news,
    "shutdown": lambda: "ok sir",
    "quit": lambda: "ok sir"
}

# ==========================================
# 3. THE MAIN ACTION ROUTER
# ==========================================

def Action(send):   
    data_btn = send.lower().strip()
    bot_answer = ""

    # --- A. Check Dynamic Commands (Memory, Search, Open) ---
    
    # 1. MEMORY: Saving Facts
    if data_btn.startswith("remember that "):
        raw_fact = data_btn.replace("remember that ", "").strip()
        fact = invert_pronouns(raw_fact)
        
        success = memory.save_fact(fact)
        if success:
            bot_answer = f"Got it. I will remember that {fact}."
        else:
            bot_answer = "My memory banks are currently offline."

    # 2. MEMORY: Recalling Facts
    elif data_btn.startswith("where is ") or data_btn.startswith("what is my "):
        raw_query = data_btn.replace("where is ", "").replace("what is my ", "").replace("what is ", "").replace("?", "").strip()
        query = invert_pronouns(raw_query)
        
        recalled_fact = memory.search_memory(query)
        
        if recalled_fact:
            bot_answer = recalled_fact
        else:
            bot_answer = f"I don't have anything in my memory banks about {raw_query}."

    # 3. Web & App Navigation
    elif data_btn.startswith("search "):
        query = data_btn.replace("search ", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(query)}")
        bot_answer = f"Searching Google for {query}."

    elif data_btn.startswith("open "):
        app_name = data_btn.replace("open ", "").strip()
        try:
            os.system(f"start {app_name}")
            bot_answer = f"Opening {app_name}."
        except Exception:
            bot_answer = f"I couldn't figure out how to open {app_name}."

    elif data_btn.startswith("wikipedia "):
        query = data_btn.replace("wikipedia ", "").strip()
        try:
            bot_answer = f"According to Wikipedia: {wikipedia.summary(query, sentences=2)}"
        except Exception:
            bot_answer = f"I couldn't find a Wikipedia page for {query}."

    elif 'weather' in data_btn:
        city = data_btn.split("in ")[-1].strip() if "in" in data_btn else "bangalore"
        bot_answer = weather.Weather(city)

    elif data_btn.startswith("play ") and "on youtube" in data_btn:
        query = data_btn.replace("play ", "").replace("on youtube", "").strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}")
        bot_answer = f"Looking up {query} on YouTube."

    # --- B. Fuzzy Match Static Commands (Typos & General Chat) ---
    else:
        best_match, score = process.extractOne(data_btn, STATIC_COMMANDS.keys())
        
        if score >= 75:
            bot_answer = STATIC_COMMANDS[best_match]()
        else:
            bot_answer = "I'm not quite sure how to help with that yet."

    # --- C. Speak and Return ---
    speak.speak(bot_answer)
    return bot_answer