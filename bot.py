#Pulse - Daily Summary Bot
#Fetches - weather (wttr.in) + a quote (zenquotes.io)
#Runs - every day at 8:00 AM IST via Github actions

import requests
from datetime import date
def get_weather(city="Thiruvananthapuram"):
    """Fetch today's weather as a one-line text summary."""
    url = f"https://wttr.in/{city}?format=3"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.text.strip()    
    except Exception as e:
        return f"Weather data unavailable ({e})"
    
def get_quote():
    """Fetch a random inspirational quote."""
    url = "https://zenquotes.io/api/random"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()      # JSON -> Python List
        quote = data[0].get("q", "No quote found")
        author = data[0].get("a", "Unknown")
        return f'"{quote}" - {author}'
    except Exception as e:
        return f"Quote data unavailable ({e})"
    
def generate_summary():
    """Assembly the full daily summary from all data sources."""
    today = date.today().strftime(" %A, %d %B %Y")
    weather = get_weather()
    quote = get_quote()
    
    summary = f"""
    -------------------------------------------
    -------------------------------------------
    PULSE - Your Daily Summary
    -------------------------------------------
    -------------------------------------------
    WEATHER:
    {weather}
    TODAY'S QUOTE:
    {quote}
    -------------------------------------------
    -------------------------------------------
    """
    return summary

def run():
    """Main entry point. Called by Github actions"""
    summary = generate_summary()
    print(summary)  # Shows in the action log.
    #Save to a file (uploaded as a downloadable artifact in Github actions)
    with open("daily_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)
    print("Pulse ran succesfully")

if __name__ == "__main__":    
    run()

