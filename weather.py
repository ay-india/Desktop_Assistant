import requests

def Weather(city="bangalore"):
    try:
        # wttr.in has special formatting. %C gets the condition, %t gets the temp
        url = f"https://wttr.in/{city}?format=%C+and+the+temperature+is+%t"
        
        response = requests.get(url)
        
        if response.status_code == 200:
            # We remove the '+' sign that wttr.in adds to positive temperatures 
            # so the text-to-speech engine reads it more naturally
            weather_text = response.text.replace("+", "").strip()
            return f"Currently in {city.capitalize()}, it is {weather_text}."
        else:
            return "I couldn't find the weather for that specific location."

    except Exception as e:
        # This will only trigger if your actual internet connection drops
        return "I'm sorry, my weather connection is currently down."