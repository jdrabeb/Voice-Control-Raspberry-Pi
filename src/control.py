from led import led
from ifttt import ifttt_webhooks
import speech_recognition as sr
import pygame as pg

def main():
    r = sr.Recognizer()

    # Instantiate IFTTT Webhooks object.
    webhooks = ifttt_webhooks('402LsIog5lt0cMATLnmtb')
    webhooks_keyword = 'start '

    # Instantiate led object.
    red_led = led()
    pg.mixer.init()
    pg.mixer.music.load("../audio/can_i_help_you.wav")
    pg.mixer.music.play()
    while pg.mixer.music.get_busy() == True:
        continue
    audio = r.listen(source, None, 2)
    while True:
        with sr.Microphone() as source:
            print("Speak Anything :")
                    try:
            #TODO Use Sphynx since it's offline.
            text = r.recognize_google(audio)
            print("You said : {}".format(text))
            if text.startswith(webhooks_keyword):
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


        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
