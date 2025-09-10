import time
import threading
import keyboard
import numpy as np
import sounddevice as sd
import speech_recognition as sr
import os
import subprocess as sp
import webbrowser
import imdb
import requests
import urllib.parse

from kivy.uix import widget, image, label, boxlayout, textinput
from kivy import clock
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, GEMINI_API_KEY
from online import speak, youtube, search_on_google, search_on_wikipedia, send_email, get_news, weather_forecast, find_my_ip
from jarvis_button import JarvisButton
import google.generativeai as genai

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')


class Jarvis(widget.Widget):
    def __init__(self, **kwargs):
        super(Jarvis, self).__init__(**kwargs)
        self.volume = 0
        self.volume_history = [0, 0, 0, 0, 0, 0, 0]
        self.volume_history_size = 140

        self.min_size = .2 * SCREEN_WIDTH
        self.max_size = .7 * SCREEN_WIDTH

        self.add_widget(image.Image(source='static/border.eps.png', size=(1920, 1080)))
        self.circle = JarvisButton(size=(284.0, 284.0), background_normal='static/circle.png')
        self.circle.bind(on_press=self.start_recording)
        self.start_recording()
        self.add_widget(image.Image(
            source='static/jarvis.gif',
            size=(self.min_size, self.min_size),
            pos=(SCREEN_WIDTH / 2 - self.min_size / 2, SCREEN_HEIGHT / 2 - self.min_size / 2)
        ))

        time_layout = boxlayout.BoxLayout(orientation='vertical', pos=(150, 900))
        self.time_label = label.Label(text='', font_size=24, markup=True, font_name='static/mw.ttf')
        time_layout.add_widget(self.time_label)
        self.add_widget(time_layout)

        clock.Clock.schedule_interval(self.update_time, 1)

        self.title = label.Label(
            text='[b][color=3333ff]JARVIS AI[/color][/b]',
            font_size=42,
            markup=True,
            font_name='static/dusri.ttf',
            pos=(920, 900)
        )
        self.add_widget(self.title)

        self.subtitles_input = textinput.TextInput(
            text='Hey Sravanthi ! I am your personal assistant',
            font_size=24,
            readonly=False,
            background_color=(0, 0, 0, 0),
            foreground_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=80,
            pos=(720, 100),
            width=1200,
            font_name='static/teesri.otf',
        )
        self.add_widget(self.subtitles_input)

        self.vrh = label.Label(text='', font_size=30, markup=True, font_name='static/mw.ttf', pos=(1500, 500))
        self.add_widget(self.vrh)

        self.vlh = label.Label(text='', font_size=30, markup=True, font_name='static/mw.ttf', pos=(400, 500))
        self.add_widget(self.vlh)

        self.add_widget(self.circle)
        keyboard.add_hotkey('`', self.start_recording)

    # ---------------- SPEECH RECOGNITION ----------------
    def take_command(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            print("Recognizing....")
            queri = r.recognize_google(audio, language='en-in')
            return queri.lower()
        except Exception:
            speak("Sorry I couldn't understand. Can you please repeat that?")
            return "none"

    def start_recording(self, *args):
        print("recording started")
        threading.Thread(target=self.run_speech_recognition).start()
        print("recording ended")

    def run_speech_recognition(self):
        r = sr.Recognizer()
        query = ""
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)
            print("audio recorded")

        try:
            query = r.recognize_google(audio, language="en-in")
            print(f'Recognised: {query}')
            clock.Clock.schedule_once(lambda dt: setattr(self.subtitles_input, 'text', query))
            self.handle_jarvis_commands(query.lower())
        except sr.UnknownValueError:
            print("Google speech recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Speech recognition API error: {e}")

        return query.lower()

    # ---------------- GUI UPDATES ----------------
    def update_time(self, dt):
        current_time = time.strftime('TIME\n\t%H:%M:%S')
        self.time_label.text = f'[b][color=3333ff]{current_time}[/color][/b]'

    def update_circle(self, dt):
        try:
            self.size_value = int(np.mean(self.volume_history))
        except Exception as e:
            self.size_value = self.min_size
            print('Warning:', e)

        if self.size_value <= self.min_size:
            self.size_value = self.min_size
        elif self.size_value >= self.max_size:
            self.size_value = self.max_size
        self.circle.size = (self.size_value, self.size_value)
        self.circle.pos = (SCREEN_WIDTH / 2 - self.circle.width / 2, SCREEN_HEIGHT / 2 - self.circle.height / 2)

    def update_volume(self, indata, frames, time, status):
        volume_norm = np.linalg.norm(indata) * 200
        self.volume = volume_norm
        self.volume_history.append(volume_norm)

        self.vlh.text = "\n".join([f"{round(v, 7)}" for v in self.volume_history[-7:]])
        self.vrh.text = self.vlh.text

        if len(self.volume_history) > self.volume_history_size:
            self.volume_history.pop(0)

    def start_listening(self):
        self.stream = sd.InputStream(callback=self.update_volume)
        self.stream.start()

    # ---------------- GEMINI ----------------
    def get_gemini_response(self, query):
        try:
            response = model.generate_content(query)
            return response.text
        except Exception as e:
            print(f"Error getting Gemini response: {e}")
            return "I'm sorry, I couldn't process that request."

    # ---------------- WOLFRAM ----------------
    def wolfram_query(self, query):
        app_id = "6EV7A3PUP3"
        encoded = urllib.parse.quote_plus(query)
        url = f"http://api.wolframalpha.com/v1/result?appid={app_id}&i={encoded}"
        res = requests.get(url)
        if res.status_code == 200:
            return res.text
        else:
            return "Sorry, I couldn't find the answer."

    # ---------------- COMMAND HANDLER ----------------
    def handle_jarvis_commands(self, query):
        try:
            if "how are you" in query:
                speak("I am absolutely fine. What about you")

            elif "open command prompt" in query:
                speak("Opening command prompt")
                os.system('start cmd')

            elif "open camera" in query:
                speak("Opening camera")
                sp.run('start microsoft.windows.camera:', shell=True)

            elif "open notepad" in query:
                speak("Opening Notepad for you")
                notepad_path = "C:\\Program Files\WindowsApps\\Microsoft.WindowsNotepad_11.2112.32.0_x64__8wekyb3d8bbwe\\Notepad\\Notepad.exe"
                os.startfile(notepad_path)

            elif 'ip address' in query:
                ip_address = find_my_ip()
                speak(f'Your IP Address is {ip_address}')
                print(f'Your IP Address is {ip_address}')

            elif "youtube" in query:
                speak("What do you want to play on youtube?")
                video = self.take_command().lower()
                youtube(video)

            elif "google" in query:
                speak("What do you want to search on google?")
                q = self.take_command().lower()
                search_on_google(q)

            elif "wikipedia" in query:
                speak("What do you want to search on wikipedia?")
                search = self.take_command().lower()
                results = search_on_wikipedia(search)
                speak(f"According to wikipedia,{results}")

            elif "send an email" in query:
                speak("Enter receiver email in terminal")
                receiver_add = input("Email address:")
                speak("What should be the subject?")
                subject = self.take_command().capitalize()
                speak("What is the message?")
                message = self.take_command().capitalize()
                if send_email(receiver_add, subject, message):
                    speak("I have sent the email")
                else:
                    speak("Something went wrong, please check logs")

            elif "news" in query:
                speak("Reading latest headlines")
                speak(get_news())

            elif "weather" in query:
                speak("Enter your city in terminal")
                city = input("Enter city: ")
                weather, temp, feels_like = weather_forecast(city)
                speak(f"The current temperature is {temp}, feels like {feels_like}")
                speak(f"Weather report: {weather}")
                print(f"Description: {weather}\nTemperature: {temp}\nFeels like: {feels_like}")

            elif "calculate" in query:
                text = query.replace("calculate", "").strip()
                if not text:
                    speak("Please tell me what to calculate")
                else:
                    ans = self.wolfram_query(text)
                    speak("The answer is " + ans)
                    print("The answer is " + ans)

            elif any(x in query for x in ["what is", "who is", "which is"]):
                ans = self.wolfram_query(query)
                speak("The answer is " + ans)
                print("The answer is " + ans)

            else:
                gemini_response = self.get_gemini_response(query)
                gemini_response = gemini_response.replace("*", "")
                if gemini_response and gemini_response != "I'm sorry, I couldn't process that request.":
                    speak(gemini_response)
                    print(gemini_response)

        except Exception as e:
            print("Error in handle_jarvis_commands:", e)
