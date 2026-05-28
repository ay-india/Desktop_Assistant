import schedule
import time
import threading
import action
import speak

def morning_routine():
    """The tasks the assistant will perform automatically every morning."""
    
    # 1. Fetch the data
    time_str = action.get_time()
    news = action.get_news()
    
    # 2. Build the proactive greeting
    greeting = f"Good morning, Ashish. {time_str}. Don't forget to grab your overnight oats and chia seeds for breakfast. Here is your daily update. {news}"
    
    # 3. Speak it out loud!
    speak.speak(greeting)

def start_scheduling():
    """Runs continuously in the background checking the clock."""
    # Set this to whenever you usually wake up
    schedule.every().day.at("08:00").do(morning_routine)
    
    # FOR TESTING: Uncomment the line below to make it run every 1 minute instead of daily
    # schedule.every(1).minutes.do(morning_routine)

    while True:
        schedule.run_pending()
        time.sleep(1) # Rests for 1 second so it doesn't max out your CPU

def run_in_background():
    """Spins up a separate thread so it doesn't freeze the Tkinter UI."""
    t = threading.Thread(target=start_scheduling, daemon=True)
    t.start()