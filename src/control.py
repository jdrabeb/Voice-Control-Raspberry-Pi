from led import led
from ifttt import ifttt_webhooks
import speech_recognition as sr
import pygame as pg
import sys

def main():
    r = sr.Recognizer()

    # Instantiate IFTTT Webhooks object.
    webhooks = ifttt_webhooks('402LsIog5lt0cMATLnmtb')
    webhooks_keyword = 'activate '

    # Instantiate led object.
    red_led = led()
    pg.mixer.init()
    pg.mixer.music.load("../audio/can_i_help_you.wav")
    pg.mixer.music.play()
    while pg.mixer.music.get_busy() == True:
        continue
    while True:
        with sr.Microphone() as source:
            print("Speak Anything :")
            audio = r.listen(source, None, 2)
        try:
            #TODO Use Sphynx since it's offline.
            text = r.recognize_google(audio)
            print("You said : {}".format(text))
            if text.startswith(webhooks_keyword):
                pg.mixer.init()
                pg.mixer.music.load("../audio/noted.wav")
                pg.mixer.music.play()
                while pg.mixer.music.get_busy() == True:
                    continue
                event_name = text[len(webhooks_keyword):]
                webhooks.trig(event_name)
            elif text.startswith('turn on'):
                red_led.turn_on()
                pg.mixer.init()
                pg.mixer.music.load("../audio/activated.wav")
                pg.mixer.music.play()
                while pg.mixer.music.get_busy() == True:
                    continue
            elif text.startswith('turn off'):
                red_led.turn_off()
                pg.mixer.init()
                pg.mixer.music.load("../audio/shutting_down.wav")
                pg.mixer.music.play()
                while pg.mixer.music.get_busy() == True:
                    continue
            elif text.startswith('goodbye'):
                red_led.turn_off()
                pg.mixer.init()
                pg.mixer.music.load("../audio/goodbye.wav")
                pg.mixer.music.play()
                while pg.mixer.music.get_busy() == True:
                    continue
                sys.exit(0)

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
