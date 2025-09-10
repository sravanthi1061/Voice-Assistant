import requests
import wikipedia
import pywhatkit as kit #used to access online youtube search,google search,play songs on youtube
from email.message import EmailMessage
import smtplib #simple mail transfer protocol 
from decouple import config
import pyttsx3

'''from constants import (
    
    
    NEWS_FETCH_API_URL,
    
    NEWS_FETCH_API_KEY,
    
)
'''
EMAIL = "224g1a33a6@srit.ac.in"
PASSWORD ="Srit@1234"

USER = config('USER')
HOSTNAME = config('BOT')
def speak(text):
    engine = pyttsx3.init()


    engine.setProperty('volume', 1.0)
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')#voice property of jarvis include ..
    engine.setProperty('voice', voices[0].id)#1 for female voice 0 for male voice

    print("Speaking:")
    engine.say(text)
    engine.runAndWait()   
def find_my_ip():
    ip_address = requests.get('https://api.ipify.org?format=json').json()
    return ip_address["ip"]

def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results

def search_on_google(query):
    kit.search(query)

def youtube(video):
    kit.playonyt(video)

def send_email(receiver_address, subject, message):
    
    try:
        email = EmailMessage()
        email['To'] = receiver_address
        email['Subject'] = subject
        email.set_content(message)
        with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(EMAIL, PASSWORD)
            smtp.send_message(email)
            return True
    except Exception as e:
        print(e)
        return False


NEWS_FETCH_API_URL = config("NEWS_FETCH_API_URL")
NEWS_FETCH_API_KEY = config("NEWS_FETCH_API_KEY")
def get_news():
    news_headline = []
    result = requests.get(
        NEWS_FETCH_API_URL,
        params={
            "country":"in",
            "category":"general",
            "apiKey": NEWS_FETCH_API_KEY
        },
    ).json()
    articles = result["articles"]
    for article in articles:
        news_headline.append(article["title"])
    return news_headline[:6]

WEATHER_FORECAST_API_URL = config("WEATHER_FORECAST_API_URL")
WEATHER_FORECAST_API_KEY = config("WEATHER_FORECAST_API_KEY")  
'''def weather_forecast(city):
    res = requests.get(
        WEATHER_FORECAST_API_URL,
        params={
            "q":city,
            "appid":WEATHER_FORECAST_API_KEY,
            "units":"metric"
        },
        ).json()
    weather = res["weather"][0]["main"]
    temp = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return weather, f"{temp}°C", f"{feels_like}°C"'''
def weather_forecast(city):
    res = requests.get(
        WEATHER_FORECAST_API_URL,
        params={
            "q": city,
            "appid": WEATHER_FORECAST_API_KEY,
            "units": "metric"
        },
    ).json()

    print("DEBUG API Response:", res)  # 👈 See full response in terminal

    # Check if response was successful
    if res.get("cod") != 200:  # If code is not 200, it's an error
        return f"Error: {res.get('message', 'Unknown error')}", "N/A", "N/A"

    # Normal successful response
    weather = res["weather"][0]["main"]
    temp = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return weather, f"{temp}°C", f"{feels_like}°C"
