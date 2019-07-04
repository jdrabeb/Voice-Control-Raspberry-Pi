from led import led
from ifttt import ifttt_webhooks
import speech_recognition as sr

if __name__ == '__main__':
    r = sr.Recognizer()

    # Instantiate IFTTT Webhooks object.
    webhooks = ifttt_webhooks('402LsIog5lt0cMATLnmtb')
    webhooks_keyword = 'start '

    # Instantiate led object.
    red_led = led()

    while True:
        with sr.Microphone() as source:
            print("Speak Anything :")
            audio = r.listen(source)

        try:
            #TODO Use Sphynx since it's offline.
            text = r.recognize_google(audio)
            print("You said : {}".format(text))

            if text.startswith(webhooks_keyword):
                event_name = text[len(webhooks_keyword):]
                webhooks.trig(event_name)
            elif text.startswith('turn on'):
                red_led.turn_on()
            elif text.startswith('turn off'):
                red_led.turn_off()

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
