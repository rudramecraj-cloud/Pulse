#Pulse - Daily Summary Bot
#Fetches - weather (wttr.in) + a quote (zenquotes.io)
#Runs - every day at 8:00 AM IST via Github actions

import requests
import smtplib
from email.mime.text import MIMEText
import os
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
    summary = generate_summary()
    print(summary)
    with open("daily_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)
    send_email(summary)
    print("Pulse ran successfully")

def send_email(summary_text):
    sender=os.environ.get("SENDER_EMAIL")       
    receiver=os.environ.get("RECEIVER_EMAIL") 
    password=os.environ.get("EMAIL_PASSWORD")
    msg=MIMEText(summary_text)
    msg["Subject"]="Pulse - Daily Summary"
    msg["From"]=sender
    msg["To"]=receiver

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)
    print("Email sent successfully")

if __name__ == "__main__":    
    run()

