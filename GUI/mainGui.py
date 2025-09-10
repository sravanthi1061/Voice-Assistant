from kivy import app
from kivy import clock
from jarvisGui import Jarvis

class MykivyApp(app.App):
    def build(self):
        jarvis = Jarvis()
        jarvis.start_listening()

        clock.Clock.schedule_interval(jarvis.update_circle, 1/60)
        clock.Clock.schedule_interval(jarvis.circle.rotate_button, 1/60)

        return jarvis


if __name__ == '__main__':
    MykivyApp().run()
