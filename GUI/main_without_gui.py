

import pyttsx3 #txt to speech conversion library in py

import speech_recognition as sr
#import requests

import keyboard
import os
import subprocess as sp
#import imdb
import wolframalpha
'''import pyautogui
import webbrowser'''
import time
#from online import find_my_ip, search_on_google, search_on_wikipedia, youtube,send_email,get_news  # , send_email, get_news, weather_forecast
from datetime import datetime
from decouple import config
from random import choice
from const import random_text
from online import find_my_ip, search_on_google, search_on_wikipedia, youtube, send_email, get_news, weather_forecast

import requests
USER = config('USER')
HOSTNAME = config('BOT')




def update_time(self,dt):
    current_time = time.strftime('TIME\n\t%H:%M:%S')
    self.time_label.text = f'[b][color=3333ff]{current_time}[/color][/b]'
              
def update_circle(self, dt):
    try:
        self.size_value = int(np.mean(self.volume_history))
                
    except Exception as e:
        self.size_value = self.min_size
        print('Warning:',e)
                
        if self.size_value <= self.min_size:
            self.size_value = self.min_size
        elif self.size_value >= self.max_size:
            self.size_value = self.max_size                                     
        self.circle.size = (self.size_value,self.size_value)
        self.circle.pos = (SCREEN_WIDTH / 2 - self.circle.width / 2, SCREEN_HEIGHT / 2 - self.circle.height / 2)
            
            
    


def speak(text):
    engine = pyttsx3.init()


    engine.setProperty('volume', 1.0)
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')#voice property of jarvis include ..
    engine.setProperty('voice', voices[0].id)#1 for female voice 0 for male voice

    print("Speaking:")
    engine.say(text)
    engine.runAndWait()   # ✅ let engine finish



def greet_me():
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good morning {USER}")
    elif (hour >= 12) and (hour <= 16):
        speak(f"Good afternoon {USER}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good evening {USER}")
    speak(f"I am {HOSTNAME}. How may i assist you? {USER}")


listening = False


def start_listening():
    global listening
    listening = True
    print("started listening ")


def pause_listening():
    global listening
    listening = False
    print("stopped listening")


keyboard.add_hotkey('ctrl+alt+k', start_listening)
keyboard.add_hotkey('ctrl+alt+p', pause_listening)

import urllib.parse

def wolfram_query(query):
    app_id = "6EV7A3PUP3"
    encoded = urllib.parse.quote_plus(query)
    url = f"http://api.wolframalpha.com/v1/result?appid={app_id}&i={encoded}"
    res = requests.get(url)
    if res.status_code == 200:
        return res.text
    else:
        return "Sorry, I couldn't find the answer."

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing....")
        queri = r.recognize_google(audio, language='en-in')
        print("You said:", queri)

        # exit condition
        if "stop" in queri or "exit" in queri:
            hour = datetime.now().hour
            if hour >= 21 or hour < 6:
                speak("Good night sir, take care!")
            else:
                speak("Have a good day ,Byee!")
            exit()

        return queri

    except Exception:
        speak("Sorry I couldn't understand. Can you please repeat that?")
        return "None"



if __name__ == '__main__':
    greet_me()
    while True:
        if listening:
            query = take_command().lower()
            if "how are you" in query:
                speak("I am absolutely fine . What about you")

            elif "open command promp" in query:
                speak("Opening command prompt")
                #os.system('start cmd')
                #sp.Popen('cmd')

            elif "open camera" in query:
                speak("Opening camera ")
                sp.run('start microsoft.windows.camera:', shell=True)

            
            elif "open notepad" in query:
                speak("Opening Notepad for you ")
                notepad_path = "C:\\Program Files\WindowsApps\\Microsoft.WindowsNotepad_11.2112.32.0_x64__8wekyb3d8bbwe\\Notepad\\Notepad.exe"
                os.startfile(notepad_path)

           

            elif 'ip address' in query:
                ip_address = find_my_ip()
                speak(
                    f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen .')
                print(f'Your IP Address is {ip_address}')

            elif "open youtube" in query:
                speak("What do you want to play on youtube ?")
                video = take_command().lower()
                youtube(video)

            elif "open google" in query:
                speak(f"What do you want to search on google {USER}")
                query = take_command().lower()
                search_on_google(query)

            elif "wikipedia" in query:
                speak("what do you want to search on wikipedia ?")
                search = take_command().lower()
                results = search_on_wikipedia(search)
                speak(f"According to wikipedia,{results}")
                speak("I am printing in on terminal")
                print(results)

            
            elif "send an email" in query:
                speak("On what email address do you want to send sir?. Please enter in the terminal")
                receiver_add = input("Email address:")
                speak("What should be the subject mam?")
                subject = take_command().capitalize()
                speak("What is the message ?")
                message = take_command().capitalize()
                if send_email(receiver_add, subject, message):
                    speak("I have sent the email mam")
                    print("I have sent the email mam")
                else:
                    speak("something went wrong Please check the error log")
            
            elif "give me news" in query:
                speak(f"I am reading out the latest headline of today,mam")
                speak(get_news())
                speak("I am printing it on screen mam")
                print(*get_news(), sep='\n')

            elif 'weather' in query:
                ip_address = find_my_ip()
                speak("tell me the name of your city")
                city = input("Enter name of your city")
                speak(f"Getting weather report for your city {city}")
                weather, temp, feels_like = weather_forecast(city)
                speak(f"The current temperature is {temp}, but it feels like {feels_like}")
                speak(f"Also, the weather report talks about {weather}")
                speak("For your convenience, I am printing it on the screen sir.")
                print(f"Description: {weather}\nTemperature: {temp}\nFeels like: {feels_like}")

            

            elif "calculate" in query:
                app_id = "6EV7A3PUP3"
                ind = query.lower().split().index("calculate")
                text = query.split()[ind + 1:]   # everything after "calculate"

                if not text:  # if user said only "calculate"
                    speak("Please tell me what you want me to calculate, for example, calculate 5 plus 7.")
                else:
                    question = " ".join(text)
                    url = f"http://api.wolframalpha.com/v1/result?appid={app_id}&i={question}"
                    res = requests.get(url)

                    if res.status_code == 200:
                        speak("The answer is " + res.text)
                        print("The answer is " + res.text)
                    else:
                        speak("Sorry, I couldn't fetch the answer.")
                        print("DEBUG Response:", res.text)

                      
            elif 'what is' in query.lower() or 'who is' in query.lower() or 'which is' in query.lower():
                q = query.lower()
                if 'what is' in q:
                    question = q.replace("what is", "").strip()
                elif 'who is' in q:
                    question = q.replace("who is", "").strip()
                elif 'which is' in q:
                    question = q.replace("which is", "").strip()
                else:
                    question = q

                ans = wolfram_query(question)
                speak("The answer is " + ans)
                print("The answer is " + ans)


                               
            
    

   